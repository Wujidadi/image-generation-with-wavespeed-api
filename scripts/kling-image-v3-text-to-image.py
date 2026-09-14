#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 kwaivgi/kling-image-v3/text-to-image 進行文生圖。

用法範例（於專案根目錄執行）：
    python3 scripts/kling-image-v3-text-to-image.py
    python3 scripts/kling-image-v3-text-to-image.py -p prompts/xxx.txt -o output/xxx --aspect-ratio 1:1 --num-images 4
    python3 scripts/kling-image-v3-text-to-image.py --prompt "A cinematic shot of a city at sunset"
    python3 scripts/kling-image-v3-text-to-image.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "kwaivgi/kling-image-v3/text-to-image"
ASPECT_RATIOS = ["16:9", "9:16", "1:1", "4:3", "3:4", "3:2", "2:3", "21:9"]
RESOLUTIONS = ["1k", "2k"]
OUTPUT_FORMATS = ["png", "jpeg", "webp"]


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--aspect-ratio", choices=ASPECT_RATIOS, default="16:9", help="輸出長寬比")
    parser.add_argument("--resolution", choices=RESOLUTIONS, default="1k", help="輸出解析度層級")
    parser.add_argument("--num-images", type=ws.number_type(1, 9), default=1, help="產圖張數，費用與張數成正比")
    parser.add_argument("--output-format", choices=OUTPUT_FORMATS, default="png", help="輸出圖片格式")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    return {
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
        "num_images": args.num_images,
        "output_format": args.output_format,
    }


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload)
