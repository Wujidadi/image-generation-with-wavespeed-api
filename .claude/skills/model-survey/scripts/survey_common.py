"""model-survey 兩支工具共用的部分：載入模型腳本、取得線上目錄、呼叫報價端點。"""

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import wavespeed_common as ws  # noqa: E402

# 圖生圖與 LoRA 相關欄位不在本專案範圍，比對 Schema 時略過
EXCLUDED_FIELDS = {
    "image", "images", "mask_image", "reference", "sref", "cref", "oref", "strength", "image_url",
    "lora", "loras", "enable_sync_mode", "enable_base64_output", "prompt",
}


def api_key() -> str:
    ws.load_dotenv(ws.DOTENV_FILE)
    key = os.environ.get("WAVESPEED_API_KEY")
    if not key:
        sys.exit("找不到 WAVESPEED_API_KEY，請設定環境變數或寫入 .env")
    return key


def headers(key: str) -> dict:
    return {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}


def load_script(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def model_scripts(names: list[str] | None = None) -> list[Path]:
    paths = sorted(p for p in SCRIPTS_DIR.glob("*.py") if p.stem != "wavespeed_common")
    if names:
        wanted = {n.removesuffix(".py") for n in names}
        missing = wanted - {p.stem for p in paths}
        if missing:
            sys.exit(f"找不到腳本：{', '.join(sorted(missing))}")
        paths = [p for p in paths if p.stem in wanted]
    return paths


def model_parser(module) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    module.add_model_args(parser)
    return parser


def fetch_catalog(key: str) -> dict[str, dict]:
    response = ws.request_json(f"{ws.API_BASE}/models", headers(key))
    models = response.get("data")
    if not isinstance(models, list) or not models:
        sys.exit("模型目錄回傳格式不符：找不到 data 陣列")
    return {m["model_id"]: m for m in models}


def request_schema(entry: dict) -> dict:
    try:
        return entry["api_schema"]["api_schemas"][0]["request_schema"]["properties"]
    except (KeyError, IndexError, TypeError):
        return {}


def quote(key: str, model_id: str, payload: dict) -> tuple[float, int]:
    """回傳（定價，折扣率百分比）。參數必須放在 inputs 欄位，放錯欄位不會報錯但所有檔位都只回底價。"""
    body = {"model_id": model_id, "inputs": {"prompt": "test", **payload}}
    data = ws.request_json(f"{ws.API_BASE}/model/price", headers(key), body)["data"]
    return float(data["price"]), int(data["discount_rate"])


def dump_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
