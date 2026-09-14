#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 openai/gpt-image-2.5-sunburst/text-to-image 進行文生圖。

用法範例（於專案根目錄執行）：
    python3 scripts/gpt-image-2.5-sunburst-text-to-image.py
    python3 scripts/gpt-image-2.5-sunburst-text-to-image.py -o output/xxx --quality low --resolution 1k
    python3 scripts/gpt-image-2.5-sunburst-text-to-image.py --prompt "A cinematic shot of a city at sunset"
    python3 scripts/gpt-image-2.5-sunburst-text-to-image.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "openai/gpt-image-2.5-sunburst/text-to-image"
ASPECT_RATIOS = [
    "1:1", "1:2", "2:1", "1:3", "3:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "9:21",
    "21:9",
]
RESOLUTIONS = ["1k", "2k", "4k"]
QUALITIES = ["low", "medium", "high", "xhigh", "max"]
OUTPUT_FORMATS = ["png", "jpeg", "webp"]


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--aspect-ratio", choices=ASPECT_RATIOS, default=None,
        help="輸出長寬比，未指定時由 API 決定",
    )
    parser.add_argument("--resolution", choices=RESOLUTIONS, default="1k", help="輸出解析度層級，同時是計費依據")
    parser.add_argument("--quality", choices=QUALITIES, default="medium", help="生成品質層級，同時是計費依據")
    parser.add_argument("--output-format", choices=OUTPUT_FORMATS, default="png", help="輸出圖片格式")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    payload = {
        "resolution": args.resolution,
        "quality": args.quality,
        "output_format": args.output_format,
    }
    if args.aspect_ratio is not None:
        payload["aspect_ratio"] = args.aspect_ratio
    return payload


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload)
