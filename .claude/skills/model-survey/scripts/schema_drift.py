#!/usr/bin/env python3
"""把已串接腳本的參數定義與線上 Input Schema 比對，列出可選值、預設值、欄位增減的差異。

用法：
    schema_drift.py                      全部腳本
    schema_drift.py qwen-image-3.0-text-to-image …

比對項目：
- 腳本 choices 與 Schema enum 是否相同
- 腳本 default 與 Schema default 是否相同（腳本 default 為 None 表示不送出，不比對）
- 腳本有、Schema 沒有的參數（可能已被官方移除）
- Schema 有、腳本沒有的參數（參考圖與 LoRA 欄位略過）
- IMAGE_INPUT 的欄位、型別與張數上下限是否與 Schema 相同
- 模型是否仍在目錄中
"""

import argparse

import survey_common as sc


def compare_images(spec, schema: dict, required: list[str]) -> list[str]:
    field = schema.get(spec.field)
    if field is None:
        return [f"參考圖欄位 {spec.field} 不在 Schema 中"]
    is_array = field.get("type") == "array"
    if is_array != (spec.shape != "string"):
        return [f"參考圖欄位 {spec.field} 的型別不同：腳本 {spec.shape} → Schema {field.get('type')}"]
    minimum = max(field.get("minItems", 0), 1 if spec.field in required else 0) if is_array else (1 if spec.field in required else 0)
    if is_array:
        maximum = field.get("maxItems")
    elif spec.rest_field:
        rest = schema.get(spec.rest_field)
        if rest is None:
            return [f"參考圖欄位 {spec.rest_field} 不在 Schema 中"]
        maximum = 1 + (rest.get("maxItems") or 0)
    else:
        maximum = 1
    issues = []
    if maximum != spec.max_items:
        issues.append(f"{spec.field} 的張數上限不同：腳本 {spec.max_items} → Schema {maximum}")
    if minimum != spec.min_items:
        issues.append(f"{spec.field} 的張數下限不同：腳本 {spec.min_items} → Schema {minimum}")
    return issues


def compare(module, schema: dict, required: list[str]) -> list[str]:
    parser = sc.model_parser(module)
    issues = []
    script_fields = set()
    for action in parser._actions:
        dest = action.dest
        script_fields.add(dest)
        field = schema.get(dest)
        if field is None:
            issues.append(f"腳本參數 {dest} 不在 Schema 中")
            continue
        if action.choices and field.get("enum") and list(action.choices) != list(field["enum"]):
            issues.append(f"{dest} 的可選值不同：腳本 {list(action.choices)} → Schema {field['enum']}")
        if action.default is not None and field.get("default") is not None and str(action.default) != str(field["default"]):
            issues.append(f"{dest} 的預設值不同：腳本 {action.default!r} → Schema {field['default']!r}")
    spec = getattr(module, "IMAGE_INPUT", None)
    if spec:
        issues += compare_images(spec, schema, required)
        script_fields.update({spec.field, spec.rest_field})
    for name, field in schema.items():
        if name in sc.EXCLUDED_FIELDS or name in script_fields:
            continue
        kind = field.get("enum") or field.get("type")
        issues.append(f"Schema 欄位 {name}（{kind}）腳本未支援")
    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("scripts", nargs="*", help="腳本名稱，省略時比對全部")
    args = parser.parse_args()

    catalog = sc.fetch_catalog(sc.api_key())
    total = drifted = 0
    for path in sc.model_scripts(args.scripts):
        module = sc.load_script(path)
        total += 1
        entry = catalog.get(module.MODEL_ID)
        if entry is None:
            drifted += 1
            print(f"{path.stem}：{module.MODEL_ID} 已不在目錄中")
            continue
        issues = compare(module, sc.request_schema(entry), sc.required_fields(entry))
        if issues:
            drifted += 1
            print(f"{path.stem}（{module.MODEL_ID}）")
            for issue in issues:
                print(f"  - {issue}")
    print(f"\n共 {total} 支腳本，{drifted} 支與線上 Schema 有差異")


if __name__ == "__main__":
    main()
