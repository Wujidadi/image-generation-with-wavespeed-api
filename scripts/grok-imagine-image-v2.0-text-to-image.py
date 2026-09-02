#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 x-ai/grok-imagine-image-v2.0/text-to-image 進行文生圖。

用法範例（於專案根目錄執行）：
    python3 scripts/grok-imagine-image-v2.0-text-to-image.py
    python3 scripts/grok-imagine-image-v2.0-text-to-image.py -p prompts/xxx.txt -o output/xxx --aspect-ratio 9:16
    python3 scripts/grok-imagine-image-v2.0-text-to-image.py --prompt "A cinematic shot of a city at sunset"
    python3 scripts/grok-imagine-image-v2.0-text-to-image.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "x-ai/grok-imagine-image-v2.0/text-to-image"
ASPECT_RATIOS = [
    "1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3",
    "2:1", "1:2", "19.5:9", "9:19.5", "20:9", "9:20",
]
RESOLUTIONS = ["1k", "2k"]
QUALITIES = ["low", "medium"]


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--aspect-ratio", choices=ASPECT_RATIOS, default="1:1", help="輸出長寬比")
    parser.add_argument("--resolution", choices=RESOLUTIONS, default="2k", help="輸出解析度層級")
    parser.add_argument("--quality", choices=QUALITIES, default="medium", help="生成品質層級")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    return {
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
        "quality": args.quality,
    }


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload)
