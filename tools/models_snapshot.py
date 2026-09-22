#!/usr/bin/env python3
"""擷取 WaveSpeed 模型目錄快照，並與前一份快照比對，找出新增、下架與改價的模型。

快照存於 documents/snapshots/models-<日期>.json，只保留 model_id、type、base_price、sort_order 與 description，
不含 Input Schema（Schema 隨時可由 GET /api/v3/models 取回，存進版控只會讓快照膨脹）。
呼叫 GET /api/v3/models 不扣費。

用法範例（於專案根目錄執行）：
    python3 tools/models_snapshot.py                     擷取今日快照並與最新一份既有快照比對
    python3 tools/models_snapshot.py --type text-to-image   比對結果只列文生圖模型
    python3 tools/models_snapshot.py --diff-only         不擷取，只比對最新兩份既有快照
    python3 tools/models_snapshot.py --since 2026-09-20  以指定日期的快照為比對基準
"""

import argparse
import json
import os
import sys
from datetime import date, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import wavespeed_common as ws  # noqa: E402

SNAPSHOT_DIR = PROJECT_ROOT / "documents" / "snapshots"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
KEEP_FIELDS = ("model_id", "type", "base_price", "sort_order", "description")


def snapshot_path(day: date) -> Path:
    return SNAPSHOT_DIR / f"models-{day.isoformat()}.json"


def list_snapshots() -> list[Path]:
    return sorted(SNAPSHOT_DIR.glob("models-????-??-??.json"))


def load_snapshot(path: Path) -> dict[str, dict]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        sys.exit(f"讀取快照失敗 {path}：{error}")
    return {m["model_id"]: m for m in data["models"]}


def fetch_models(api_key: str) -> list[dict]:
    response = ws.request_json(f"{ws.API_BASE}/models", {"Authorization": f"Bearer {api_key}"})
    models = response.get("data")
    if not isinstance(models, list) or not models:
        sys.exit("模型目錄回傳格式不符：找不到 data 陣列")
    return [{key: m.get(key) for key in KEEP_FIELDS} for m in models]


def write_snapshot(path: Path, models: list[dict]) -> None:
    payload = {
        "fetched_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "source": f"GET {ws.API_BASE}/models",
        "count": len(models),
        "models": sorted(models, key=lambda m: m["model_id"]),
    }
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def has_script(model_id: str) -> bool:
    return (SCRIPTS_DIR / f"{ws.output_slug(model_id)}.py").is_file()


def print_diff(old: dict[str, dict], new: dict[str, dict], model_type: str | None) -> None:
    def wanted(model: dict) -> bool:
        return model_type is None or model["type"] == model_type

    added = [new[i] for i in sorted(set(new) - set(old)) if wanted(new[i])]
    removed = [old[i] for i in sorted(set(old) - set(new)) if wanted(old[i])]
    repriced = [
        (old[i], new[i]) for i in sorted(set(old) & set(new))
        if wanted(new[i]) and old[i]["base_price"] != new[i]["base_price"]
    ]

    print(f"新增 {len(added)} 個")
    for m in added:
        mark = "" if model_type != "text-to-image" else ("　已有腳本" if has_script(m["model_id"]) else "　尚無腳本")
        print(f"  {m['type']:<16} {m['model_id']:<60} ${m['base_price']}{mark}")
    print(f"下架 {len(removed)} 個")
    for m in removed:
        print(f"  {m['type']:<16} {m['model_id']:<60} ${m['base_price']}")
    print(f"改價 {len(repriced)} 個")
    for before, after in repriced:
        print(f"  {after['type']:<16} {after['model_id']:<60} ${before['base_price']} → ${after['base_price']}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--type", help="只列出指定類型的差異，例如 text-to-image")
    parser.add_argument("--since", type=date.fromisoformat, help="比對基準快照的日期（YYYY-MM-DD），預設為最新一份既有快照")
    parser.add_argument("--diff-only", action="store_true", help="不呼叫 API，只比對既有快照")
    args = parser.parse_args()

    today = date.today()
    if args.diff_only:
        snapshots = list_snapshots()
        if len(snapshots) < 2 and args.since is None:
            sys.exit("既有快照不足兩份，無法比對")
        current_path = snapshots[-1]
    else:
        ws.load_dotenv(ws.DOTENV_FILE)
        api_key = os.environ.get("WAVESPEED_API_KEY")
        if not api_key:
            sys.exit("找不到 WAVESPEED_API_KEY，請設定環境變數或寫入 .env")
        current_path = snapshot_path(today)
        write_snapshot(current_path, fetch_models(api_key))
        print(f"已寫入快照 {current_path.relative_to(PROJECT_ROOT)}")

    if args.since is not None:
        base_path = snapshot_path(args.since)
        if not base_path.is_file():
            sys.exit(f"找不到快照 {base_path.relative_to(PROJECT_ROOT)}")
    else:
        earlier = [p for p in list_snapshots() if p != current_path]
        if not earlier:
            print("沒有更早的快照可比對，下次執行即可看到差異")
            return
        base_path = earlier[-1]

    old, new = load_snapshot(base_path), load_snapshot(current_path)
    print(f"比對基準 {base_path.name}（{len(old)} 個）→ {current_path.name}（{len(new)} 個）")
    print_diff(old, new, args.type)


if __name__ == "__main__":
    main()
