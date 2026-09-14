#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 google/nano-banana-pro/text-to-image-ultra 進行文生圖。

用法範例（於專案根目錄執行）：
    python3 scripts/nano-banana-pro-text-to-image-ultra.py
    python3 scripts/nano-banana-pro-text-to-image-ultra.py -o output/xxx --aspect-ratio 16:9 --resolution 8k
    python3 scripts/nano-banana-pro-text-to-image-ultra.py --prompt "A cinematic shot of a city at sunset"
    python3 scripts/nano-banana-pro-text-to-image-ultra.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "google/nano-banana-pro/text-to-image-ultra"
ASPECT_RATIOS = ["1:1", "3:2", "2:3", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"]
RESOLUTIONS = ["4k", "8k"]
OUTPUT_FORMATS = ["png", "jpeg"]


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--aspect-ratio", choices=ASPECT_RATIOS, default=None,
        help="輸出長寬比，未指定時由 API 決定",
    )
    parser.add_argument("--resolution", choices=RESOLUTIONS, default="4k", help="輸出解析度層級，同時是計費依據")
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
    ws.run(MODEL_ID, add_model_args, build_payload)
