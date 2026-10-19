#!/usr/bin/env python3
"""對已串接的模型逐檔位重新報價，列出與 documents/price.md 的差異。

用法：
    requote.py                       全部腳本
    requote.py seedream-v5.0-pro …   只測指定腳本
    requote.py --json 結果.json      另存逐模型結果

每個模型先以全預設參數報價，再把每個參數單獨拉到其他檔位（choices 逐一、布林旗標翻轉、整數取 Schema 的 maximum），
記錄價格區間、會改價的參數與折扣率；呼叫 POST /api/v3/model/price 不扣費。
價格區間取所有計費參數同時拉到最低檔與最高檔的疊加極端，與 price.md 的定義一致。
"""

import argparse
import re
from pathlib import Path

import survey_common as sc

PRICE_MD = sc.PROJECT_ROOT / "documents" / "price.md"
PRICE_ROW = re.compile(r"\| `([^`]+)`\s*\| \$([\d.]+)\s*\| ([^|]+?)\s*\| ([^|]+?)\s*\| ([^|]+?)\s*\|")


def documented_prices() -> dict[str, tuple[str, str, str, str]]:
    rows = {}
    for line in PRICE_MD.read_text(encoding="utf-8").splitlines():
        if m := PRICE_ROW.match(line):
            rows[m.group(1)] = m.groups()[1:]
    return rows


SIZE_CANDIDATES = ["256*256", "512*512", "1024*1024", "2048*2048", "4096*4096", "8192*8192"]


def variants(action: argparse.Action, schema_field: dict) -> list:
    """列出要個別試算的其他檔位：choices 逐一、布林翻轉、整數取 Schema 上限、自由字串 size 取驗證器放行的各級尺寸"""
    if action.choices:
        return [c for c in action.choices if c != action.default]
    if isinstance(action, (argparse._StoreTrueAction, argparse._StoreFalseAction, argparse.BooleanOptionalAction)):
        return [not action.default]
    if action.dest == "size" and callable(action.type):
        values = []
        for candidate in SIZE_CANDIDATES:
            try:
                value = action.type(candidate)
            except argparse.ArgumentTypeError:
                continue
            if value != action.default:
                values.append(value)
        return values
    if schema_field.get("type") == "integer" and schema_field.get("maximum") is not None:
        maximum = int(schema_field["maximum"])
        return [maximum] if maximum != action.default else []
    return []


def survey(key: str, module, schema: dict) -> dict:
    parser = sc.model_parser(module)
    defaults = parser.parse_args([])
    base_payload = module.build_payload(defaults, "test")
    base, discount = sc.quote(key, module.MODEL_ID, base_payload)
    low, high, billing = base, base, set()
    cheapest, dearest = {}, {}
    for action in parser._actions:
        for value in variants(action, schema.get(action.dest, {})):
            namespace = parser.parse_args([])
            setattr(namespace, action.dest, value)
            try:
                payload = module.build_payload(namespace, "test")
            except SystemExit:
                continue
            price, _ = sc.quote(key, module.MODEL_ID, payload)
            if price == base:
                continue
            billing.add(action.dest)
            if price < cheapest.get(action.dest, (base, None))[0]:
                cheapest[action.dest] = (price, value)
            if price > dearest.get(action.dest, (base, None))[0]:
                dearest[action.dest] = (price, value)
            low, high = min(low, price), max(high, price)
    # 計費參數會疊加（例如品質與解析度、解析度與搜尋旗標），再以全部最低檔與全部最高檔各報一次，區間取疊加後的極端
    for combo in (cheapest, dearest):
        if len(combo) < 2:
            continue
        namespace = parser.parse_args([])
        for dest, (_, value) in combo.items():
            setattr(namespace, dest, value)
        price, _ = sc.quote(key, module.MODEL_ID, module.build_payload(namespace, "test"))
        low, high = min(low, price), max(high, price)
    return {"base": base, "low": low, "high": high, "params": sorted(billing), "discount": discount}


def as_row(result: dict) -> tuple[str, str, str, str]:
    base = f"{result['base']:.3f}"
    span = "固定" if result["low"] == result["high"] else f"${result['low']:.3f} ～ ${result['high']:.3f}"
    params = "、".join(result["params"]) or "無"
    discount = "無" if result["discount"] == 100 else f"{result['discount']}％"
    return base, span, params, discount


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("scripts", nargs="*", help="腳本名稱，省略時測全部")
    parser.add_argument("--json", type=Path, help="把逐模型結果另存為 JSON")
    args = parser.parse_args()

    key = sc.api_key()
    catalog = sc.fetch_catalog(key)
    documented = documented_prices()
    results, diffs = {}, []
    for path in sc.model_scripts(args.scripts):
        module = sc.load_script(path)
        entry = catalog.get(module.MODEL_ID)
        if entry is None:
            print(f"{module.MODEL_ID}：目錄中已不存在，略過")
            continue
        result = survey(key, module, sc.request_schema(entry))
        results[module.MODEL_ID] = result
        row = as_row(result)
        old = documented.get(module.MODEL_ID)
        status = "缺列" if old is None else ("變動" if tuple(old) != row else "相同")
        print(f"{status}  {module.MODEL_ID}  ${row[0]}  {row[1]}  {row[2]}  折扣 {row[3]}", flush=True)
        if status != "相同":
            diffs.append((module.MODEL_ID, old, row))

    print(f"\n共 {len(results)} 個模型，{len(diffs)} 個與 price.md 不同")
    for model_id, old, new in diffs:
        print(f"- {model_id}\n    price.md：{old}\n    現在    ：{new}")
    if args.json:
        sc.dump_json(args.json, results)


if __name__ == "__main__":
    main()
