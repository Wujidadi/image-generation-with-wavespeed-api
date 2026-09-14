"""WaveSpeed 文生圖腳本的共用邏輯：參數解析、金鑰載入、任務提交、輪詢與下載。

各模型腳本只需提供模型 ID、模型專屬參數與 payload 組裝方式，其餘交由 run() 處理。
API 金鑰讀取順序：既有環境變數 WAVESPEED_API_KEY，其次為專案根目錄 .env 檔。
"""

import argparse
import json
import mimetypes
import os
import sys
import time
from collections.abc import Callable
from datetime import datetime
from http.client import RemoteDisconnected
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

API_BASE = "https://api.wavespeed.ai/api/v3"
RESULT_URL = API_BASE + "/predictions/{id}/result"
TERMINAL_FAILURES = {"failed", "cancelled", "timeout", "deleted"}
REQUEST_TIMEOUT = 30.0
COMMENT_PREFIXES = ("#", "//")
TASK_SLUGS = {"text-to-image", "image-to-image", "text-to-video", "image-to-video", "edit"}

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PROMPT_FILE = PROJECT_ROOT / "prompts" / "default.txt"
DOTENV_FILE = PROJECT_ROOT / ".env"

AddModelArgs = Callable[[argparse.ArgumentParser], None]
BuildPayload = Callable[[argparse.Namespace, str], dict]


def output_slug(model_id: str) -> str:
    """去掉供應商前綴後，以連字號串接模型路徑，作為預設輸出子目錄名稱

    少數模型 ID 去掉前綴後只剩任務類別（例如 midjourney/text-to-image），此時保留供應商才能辨識模型。
    """
    provider, _, rest = model_id.partition("/")
    slug = rest.replace("/", "-")
    return f"{provider}-{slug}" if slug in TASK_SLUGS else slug


def load_dotenv(path: Path) -> None:
    """將 .env 中尚未存在於環境的變數載入；既有環境變數優先"""
    if not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip().removeprefix("export ").strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if key and key not in os.environ:
            os.environ[key] = value


def size_type(
    side_min: int = 1,
    side_max: int | None = None,
    pixels_min: int | None = None,
    pixels_max: int | None = None,
    ratio_max: float | None = None,
) -> Callable[[str], str]:
    """產生 --size 的 argparse 型別函式：接受 寬x高 或 寬*高，回傳 API 要求的 寬*高

    收 寬x高 是為了在 shell 中不必為 * 加引號；各項上下限由呼叫端依該模型的 Input Schema 指定。
    尺寸不合規時部分模型不會拒絕，而是靜默改用其他尺寸並照常扣費，因此一律在本機先擋下。
    """

    def parse(value: str) -> str:
        width, separator, height = value.lower().replace("*", "x").partition("x")
        if not separator or not width.isdigit() or not height.isdigit():
            raise argparse.ArgumentTypeError(f"格式須為 寬x高，例如 1024x1024，收到：{value}")
        width, height = int(width), int(height)
        for side in (width, height):
            if side < side_min or (side_max is not None and side > side_max):
                limit = f"介於 {side_min} 到 {side_max}" if side_max is not None else f"至少 {side_min}"
                raise argparse.ArgumentTypeError(f"寬與高須{limit}，收到：{value}")
        pixels = width * height
        if (pixels_min is not None and pixels < pixels_min) or (pixels_max is not None and pixels > pixels_max):
            raise argparse.ArgumentTypeError(
                f"總像素須介於 {pixels_min} 到 {pixels_max}，收到：{value}（{pixels}）"
            )
        if ratio_max is not None and not 1 / ratio_max <= width / height <= ratio_max:
            raise argparse.ArgumentTypeError(f"長寬比須介於 1:{ratio_max:g} 到 {ratio_max:g}:1，收到：{value}")
        return f"{width}*{height}"

    return parse


def number_type(minimum: float, maximum: float, integer: bool = True) -> Callable[[str], int | float]:
    """產生數值範圍檢查的 argparse 型別函式，範圍取自該模型的 Input Schema"""

    def parse(value: str) -> int | float:
        try:
            number = int(value) if integer else float(value)
        except ValueError:
            raise argparse.ArgumentTypeError(f"須為{'整數' if integer else '數值'}，收到：{value}") from None
        if not minimum <= number <= maximum:
            raise argparse.ArgumentTypeError(f"須介於 {minimum:g} 到 {maximum:g}，收到：{value}")
        return number

    return parse


def build_parser(model_id: str, add_model_args: AddModelArgs) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=f"以 {model_id} 進行文生圖，並將輸出圖像下載到本機",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    prompt_group = parser.add_mutually_exclusive_group()
    prompt_group.add_argument(
        "-p", "--prompt-file", type=Path, default=DEFAULT_PROMPT_FILE,
        help="提示詞檔案路徑，行首為 # 或 // 的整行視為註解",
    )
    prompt_group.add_argument(
        "--prompt", help="直接指定提示詞文字，優先於 --prompt-file",
    )
    parser.add_argument(
        "-o", "--output-dir", type=Path, default=PROJECT_ROOT / "output" / output_slug(model_id),
        help="輸出圖像存放目錄，不存在時自動建立",
    )
    add_model_args(parser)
    parser.add_argument("--task-id", help="不重新提交，直接取回既有任務的輸出")
    parser.add_argument("--poll-interval", type=float, default=2.0, help="輪詢間隔秒數")
    parser.add_argument("--timeout", type=float, default=300.0, help="等待結果的上限秒數")
    return parser


def strip_comments(text: str) -> str:
    """去掉提示詞檔案中以 # 或 // 起始的整行註解"""
    return "\n".join(
        line for line in text.splitlines()
        if not line.lstrip().startswith(COMMENT_PREFIXES)
    )


def load_prompt(args: argparse.Namespace) -> str:
    if args.prompt is not None:
        prompt = args.prompt
    else:
        if not args.prompt_file.is_file():
            sys.exit(f"找不到提示詞檔案：{args.prompt_file}")
        prompt = strip_comments(args.prompt_file.read_text(encoding="utf-8"))
    prompt = prompt.strip()
    if not prompt:
        sys.exit("提示詞為空")
    return prompt


class TransientError(Exception):
    """可重試的暫時性網路或伺服器錯誤"""


def request_json(url: str, headers: dict, payload: dict | None = None, retry: bool = False) -> dict:
    data = json.dumps(payload).encode() if payload is not None else None
    request = Request(url, data=data, headers=headers, method="POST" if data else "GET")
    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            return json.load(response)
    except HTTPError as error:
        body = error.read().decode(errors="replace")
        if retry and error.code >= 500:
            raise TransientError(f"HTTP {error.code}") from error
        sys.exit(f"HTTP {error.code} {url}\n{body}")
    except (URLError, RemoteDisconnected, TimeoutError, ConnectionError) as error:
        if retry:
            raise TransientError(str(error)) from error
        sys.exit(f"連線失敗 {url}：{error}")


def wait_for_result(prediction_id: str, headers: dict, interval: float, timeout: float) -> dict:
    result_url = RESULT_URL.format(id=prediction_id)
    deadline = time.monotonic() + timeout
    attempt = 0
    while True:
        attempt += 1
        try:
            body = request_json(result_url, headers, retry=True)
        except TransientError as error:
            print(f"  {attempt}: 查詢失敗（{error}），{interval:g} 秒後重試…", file=sys.stderr)
            if time.monotonic() >= deadline:
                sys.exit(f"等待逾時（{timeout:g} 秒），可稍後以 --task-id {prediction_id} 重新取回結果")
            time.sleep(interval)
            continue
        result = body.get("data", body)
        status = result.get("status")
        if status == "completed":
            return result
        if status in TERMINAL_FAILURES:
            sys.exit(f"任務結束於狀態 {status}：\n{json.dumps(result, ensure_ascii=False, indent=4)}")
        if time.monotonic() >= deadline:
            sys.exit(f"等待逾時（{timeout:g} 秒），任務仍處於 {status}，可稍後以 --task-id {prediction_id} 重新取回結果")
        print(f"  {attempt}: 狀態 {status}，{interval:g} 秒後重試…", file=sys.stderr)
        time.sleep(interval)


def task_stamp(created_at: str | None) -> str:
    """把任務建立時間（UTC）轉成本地時間戳；解析失敗時退回目前時間"""
    if created_at:
        try:
            utc = datetime.fromisoformat(created_at[:19] + "+00:00")
            return utc.astimezone().strftime("%Y%m%dT%H%M%S")
        except ValueError:
            pass
    return datetime.now().strftime("%Y%m%dT%H%M%S")


def download(url: str, destination_stem: Path) -> Path:
    request = Request(url, headers={"User-Agent": "wavespeed-api-script"})
    with urlopen(request, timeout=REQUEST_TIMEOUT) as response:
        content = response.read()
        content_type = response.headers.get_content_type()
    extension = Path(urlparse(url).path).suffix or mimetypes.guess_extension(content_type) or ".bin"
    destination = destination_stem.with_suffix(extension)
    destination.write_bytes(content)
    return destination


def ensure_output_dir(path: Path) -> None:
    """在提交任務前遞迴建立輸出目錄，避免扣費後才發現路徑不可用"""
    try:
        path.mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        sys.exit(f"輸出路徑已存在但不是目錄：{path}")
    except NotADirectoryError:
        sys.exit(f"輸出路徑的上層有同名檔案，無法建立目錄：{path}")
    except PermissionError:
        sys.exit(f"沒有權限建立輸出目錄：{path}")
    except OSError as error:
        sys.exit(f"無法建立輸出目錄 {path}：{error.strerror or error}")
    if not os.access(path, os.W_OK):
        sys.exit(f"輸出目錄不可寫入：{path}")


def run(model_id: str, add_model_args: AddModelArgs, build_payload: BuildPayload) -> None:
    args = build_parser(model_id, add_model_args).parse_args()
    load_dotenv(DOTENV_FILE)
    api_key = os.environ.get("WAVESPEED_API_KEY")
    if not api_key:
        sys.exit(f"請設定環境變數 WAVESPEED_API_KEY，或寫入 {DOTENV_FILE}")

    ensure_output_dir(args.output_dir)
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    if args.task_id:
        prediction_id = args.task_id
        print(f"取回既有任務：{prediction_id}")
    else:
        prompt = load_prompt(args)
        payload = {"prompt": prompt, **build_payload(args, prompt)}
        print(f"模型：{model_id}")
        print(f"提示詞來源：{'命令列 --prompt' if args.prompt is not None else args.prompt_file}")
        print("參數：" + " ".join(f"{key}={value}" for key, value in payload.items() if key != "prompt"))

        submit_body = request_json(f"{API_BASE}/{model_id}", headers, payload)
        task = submit_body.get("data", submit_body)
        prediction_id = task.get("id")
        if not prediction_id:
            sys.exit(f"提交回應中沒有任務 ID：\n{json.dumps(submit_body, ensure_ascii=False, indent=4)}")
        print(f"任務 ID：{prediction_id}")

    result = wait_for_result(prediction_id, headers, args.poll_interval, args.timeout)
    outputs = result.get("outputs") or []
    if not outputs:
        sys.exit("任務完成但沒有任何輸出")
    inference_ms = (result.get("timings") or {}).get("inference")
    if inference_ms is not None:
        print(f"推論耗時：{inference_ms / 1000:.1f} 秒")

    stamp = task_stamp(result.get("created_at"))
    for index, output in enumerate(outputs, start=1):
        if not isinstance(output, str) or not output.startswith("http"):
            print(f"略過非網址輸出：{output!r}", file=sys.stderr)
            continue
        stem = args.output_dir / (f"{stamp}-{prediction_id}" + (f"-{index}" if len(outputs) > 1 else ""))
        saved = download(output, stem)
        print(f"已儲存：{saved}")
