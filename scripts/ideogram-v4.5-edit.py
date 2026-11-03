#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 ideogram-ai/ideogram-v4.5/edit 依參考圖生成。

用法範例（於專案根目錄執行）：
    python3 scripts/ideogram-v4.5-edit.py --image refs/a.png --prompt "Move the subject to a bamboo forest"
    python3 scripts/ideogram-v4.5-edit.py --image refs/a.png refs/b.png -p prompts/xxx.txt -o output/xxx
    python3 scripts/ideogram-v4.5-edit.py --task-id <任務 ID> -o output/xxx

本腳本未開放 API 的 mask_url 參數。
"""

import argparse
import sys

import wavespeed_common as ws

MODEL_ID = "ideogram-ai/ideogram-v4.5/edit"
QUALITIES = ["very_low", "low", "medium", "high"]
EDIT_PRECISIONS = ["regular", "high"]
IMAGE_INPUT = ws.ImageInput("image", min_items=1, max_items=5, shape="string", rest_field="reference_images")


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--quality", choices=QUALITIES, default="medium", help="生成品質層級，亦為計費依據")
    parser.add_argument(
        "--edit-precision", choices=EDIT_PRECISIONS, default="regular",
        help="編輯精度，regular 依提示詞編輯，high 會還原未變更的像素且不可指定 --size",
    )
    parser.add_argument(
        "--size", type=ws.size_type(side_min=256, side_max=4992), default=None,
        help="輸出尺寸，格式 寬x高（在 shell 中比 寬*高 安全，後者需加引號），未指定時由 API 決定",
    )


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    payload = {
        "quality": args.quality,
        "edit_precision": args.edit_precision,
    }
    if args.size is not None:
        if args.edit_precision == "high":
            sys.exit("--edit-precision high 不可同時指定 --size")
        payload["size"] = args.size
    return payload


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload, IMAGE_INPUT)
