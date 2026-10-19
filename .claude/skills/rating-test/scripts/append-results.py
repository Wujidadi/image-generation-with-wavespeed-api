#!/usr/bin/env python3
"""把 run-rating-test.zsh 的執行紀錄整理成表格，附加到各等級實測紀錄 Markdown 的最下方。

用法：
    append-results.py <結果目錄> [--print-only]

表格與既有實測表同欄位，但獨立成「待併入上表」區段，效果欄只對被擋的列填 😡，其餘留給人工評圖後填寫。
價格取 price.md 的預設價格，有帳戶折扣者乘上折扣率；時長取官方回報的推論毫秒數。
"""

import argparse
import json
import re
import shutil
import subprocess
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]

PRICE_ROW = re.compile(r"\| `([^`]+)`\s*\| \$([\d.]+)\s*\|[^|]*\|[^|]*\| ([^|]+?)\s*\|")
HEADING = "## {day} 新增模型實測（待併入上表）"


def load_prices(price_md: Path) -> dict[str, str]:
    prices = {}
    for line in price_md.read_text(encoding="utf-8").splitlines():
        m = PRICE_ROW.match(line)
        if not m:
            continue
        model_id, price, discount = m.group(1), float(m.group(2)), m.group(3)
        rate = int(discount.rstrip("％")) / 100 if discount.endswith("％") else 1.0
        prices[model_id] = f"{price * rate:.4f}"
    return prices


def parse_log(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    result = {"script": path.stem, "model_id": None, "ms": None, "file": None, "blocked": False, "error": None}
    if m := re.search(r"^模型：(.+)$", text, re.M):
        result["model_id"] = m.group(1).strip()
    if m := re.search(r"^推論耗時：(\d+) 毫秒", text, re.M):
        result["ms"] = int(m.group(1))
    if m := re.search(r"^已儲存：(.+)$", text, re.M):
        result["file"] = Path(m.group(1).strip()).name
    if '"code": 1200' in text:
        result["blocked"] = True
    elif m := re.search(r'"error": "(.+?)"', text):
        result["error"] = m.group(1)
    elif not result["file"]:
        result["error"] = text.strip().splitlines()[-2] if text.strip() else "無輸出"
    return result


def model_id_of(script: str) -> str:
    source = (PROJECT_ROOT / "scripts" / f"{script}.py").read_text(encoding="utf-8")
    m = re.search(r'^MODEL_ID = "([^"]+)"', source, re.M)
    return m.group(1) if m else script


def seconds(ms: int | None) -> str:
    return f"{ms / 1000:.3f}s" if ms is not None else "-"


def build_rows(rating: str, logs: list[dict], prices: dict[str, str]) -> list[list[str]]:
    ok, bad = [], []
    for r in logs:
        model_id = r["model_id"] or model_id_of(r["script"])
        price = prices.get(model_id, "?")
        if rating == "G":
            note = "" if r["file"] else ("擋住" if r["blocked"] else f"失敗：{r['error']}")
            row = [model_id, r["script"], price, seconds(r["ms"]), r["file"] or "", note]
        else:
            effect = "" if r["file"] else "😡"
            note = "" if r["file"] or r["blocked"] else f"失敗：{r['error']}"
            row = [model_id, r["script"], price, seconds(r["ms"]), effect, note]
        (ok if r["file"] else bad).append(row)
    key = lambda row: float(row[3][:-1]) if row[3] != "-" else 1e9
    return sorted(ok, key=key) + sorted(bad, key=key)


def render(cols: list[tuple[str, str]], rows: list[list[str]]) -> str:
    """cols 為（欄名，對齊）；對齊取 left、right、center，與主表的分隔列一致"""
    marks = {"left": "---", "right": "--:", "center": ":-:"}
    lines = ["| " + " | ".join(name for name, _ in cols) + " |", "| " + " | ".join(marks[align] for _, align in cols) + " |"]
    lines += ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--print-only", action="store_true", help="只印出表格，不改動 Markdown")
    args = parser.parse_args()

    meta = json.loads((args.run_dir / "meta.json").read_text(encoding="utf-8"))
    prices = load_prices(Path(meta["price_md"]))
    heading = HEADING.format(day=date.today().isoformat())
    for rating in ("G", "PG13", "R18"):
        rating_dir = args.run_dir / rating
        if not rating_dir.is_dir():
            continue
        logs = [parse_log(p) for p in sorted(rating_dir.glob("*.log"))]
        cols = [("模型", "left"), ("腳本", "left"), ("價格", "right"), ("時長", "right")]
        cols += [("檔名", "left"), ("備註", "left")] if rating == "G" else [("效果", "center"), ("備註", "left")]
        table = render(cols, build_rows(rating, logs, prices))
        print(f"=== {rating}\n{table}\n")
        if args.print_only:
            continue
        review = Path(meta["reviews"][rating])
        text = review.read_text(encoding="utf-8").rstrip("\n")
        review.write_text(f"{text}\n\n{heading}\n\n{table}\n", encoding="utf-8")
        if shutil.which("md-fmt"):
            subprocess.run(["md-fmt", "--tables-only", str(review)], check=False, capture_output=True)
        print(f"已附加到 {review}")


if __name__ == "__main__":
    main()
