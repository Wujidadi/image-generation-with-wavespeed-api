#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 wavespeed-ai/qwen-image-2.1/text-to-image 進行文生圖。

用法範例（於專案根目錄執行）：
    python3 scripts/qwen-image-2.1-text-to-image.py
    python3 scripts/qwen-image-2.1-text-to-image.py -p prompts/xxx.txt -o output/xxx --aspect-ratio 16:9 --resolution 2k
    python3 scripts/qwen-image-2.1-text-to-image.py --prompt "A cinematic shot of a city at sunset"
    python3 scripts/qwen-image-2.1-text-to-image.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "wavespeed-ai/qwen-image-2.1/text-to-image"
ASPECT_RATIOS = [
    "1:1", "1:2", "2:1", "1:3", "3:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "9:21",
    "21:9",
]
RESOLUTIONS = ["1k", "1.5k", "2k"]
OUTPUT_FORMATS = ["jpeg", "png", "webp"]


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--aspect-ratio", choices=ASPECT_RATIOS, default="1:1", help="輸出長寬比")
    parser.add_argument(
        "--resolution", choices=RESOLUTIONS, default="1k",
        help="輸出解析度層級：1k 約 1 百萬像素、1.5k 約 2.25 百萬像素、2k 約 4 百萬像素",
    )
    parser.add_argument("--output-format", choices=OUTPUT_FORMATS, default="jpeg", help="輸出圖片格式")
    parser.add_argument("--seed", type=int, default=None, help="隨機種子，未指定時由 API 隨機決定")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    payload = {
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
        "output_format": args.output_format,
    }
    if args.seed is not None:
        payload["seed"] = args.seed
    return payload


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload)
