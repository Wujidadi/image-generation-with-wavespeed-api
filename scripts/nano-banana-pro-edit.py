#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 google/nano-banana-pro/edit 依參考圖生成。

用法範例（於專案根目錄執行）：
    python3 scripts/nano-banana-pro-edit.py --image refs/a.png --prompt "Move the subject to a bamboo forest"
    python3 scripts/nano-banana-pro-edit.py --image refs/a.png refs/b.png -p prompts/xxx.txt -o output/xxx
    python3 scripts/nano-banana-pro-edit.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "google/nano-banana-pro/edit"
ASPECT_RATIOS = ["1:1", "3:2", "2:3", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"]
RESOLUTIONS = ["1k", "2k", "4k"]
OUTPUT_FORMATS = ["png", "jpeg"]
IMAGE_INPUT = ws.ImageInput("images", min_items=1, max_items=14)


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--aspect-ratio", choices=ASPECT_RATIOS, default=None, help="輸出長寬比，未指定時由 API 依參考圖決定")
    parser.add_argument("--resolution", choices=RESOLUTIONS, default="1k", help="輸出解析度層級，同時是計費依據")
    parser.add_argument("--output-format", choices=OUTPUT_FORMATS, default="png", help="輸出圖片格式")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    payload = {
        "resolution": args.resolution,
        "output_format": args.output_format,
    }
    if args.aspect_ratio is not None:
        payload["aspect_ratio"] = args.aspect_ratio
    return payload


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload, IMAGE_INPUT)
