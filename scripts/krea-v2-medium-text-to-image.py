#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 wavespeed-ai/krea-v2-medium/text-to-image 進行文生圖。

用法範例（於專案根目錄執行）：
    python3 scripts/krea-v2-medium-text-to-image.py
    python3 scripts/krea-v2-medium-text-to-image.py -o output/xxx --aspect-ratio 16:9 --output-format jpeg
    python3 scripts/krea-v2-medium-text-to-image.py --prompt "A cinematic shot of a city at sunset"
    python3 scripts/krea-v2-medium-text-to-image.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "wavespeed-ai/krea-v2-medium/text-to-image"
ASPECT_RATIOS = ["1:1", "4:3", "3:4", "16:9", "9:16"]
OUTPUT_FORMATS = ["png", "jpeg"]


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--aspect-ratio", choices=ASPECT_RATIOS, default="1:1", help="輸出長寬比")
    parser.add_argument("--output-format", choices=OUTPUT_FORMATS, default="png", help="輸出圖片格式")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    return {
        "aspect_ratio": args.aspect_ratio,
        "output_format": args.output_format,
    }


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload)
