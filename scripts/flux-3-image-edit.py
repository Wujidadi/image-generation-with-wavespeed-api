#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 black-forest-labs/flux-3/image-edit 依參考圖生成。

用法範例（於專案根目錄執行）：
    python3 scripts/flux-3-image-edit.py --image refs/a.png --prompt "Move the subject to a bamboo forest"
    python3 scripts/flux-3-image-edit.py --image refs/a.png refs/b.png -p prompts/xxx.txt -o output/xxx
    python3 scripts/flux-3-image-edit.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "black-forest-labs/flux-3/image-edit"
ASPECT_RATIOS = ["21:9", "2:1", "16:9", "3:2", "7:5", "4:3", "5:4", "1:1", "4:5", "3:4", "5:7", "2:3", "9:16", "1:2"]
RESOLUTIONS = ["1k", "2k", "4k"]
OUTPUT_FORMATS = ["jpeg", "png"]
IMAGE_INPUT = ws.ImageInput("images", min_items=1, max_items=10)


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--aspect-ratio", choices=ASPECT_RATIOS, default=None, help="輸出長寬比，未指定時由 API 依參考圖決定")
    parser.add_argument("--resolution", choices=RESOLUTIONS, default="1k", help="輸出解析度層級，同時是計費依據；4k 可能需要數分鐘")
    parser.add_argument("--output-format", choices=OUTPUT_FORMATS, default="jpeg", help="輸出圖片格式")


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
