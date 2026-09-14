#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 wavespeed-ai/qwen-image/text-to-image 進行文生圖。

用法範例（於專案根目錄執行）：
    python3 scripts/qwen-image-text-to-image.py
    python3 scripts/qwen-image-text-to-image.py -p prompts/xxx.txt -o output/xxx --size 1280x720 --output-format png
    python3 scripts/qwen-image-text-to-image.py --prompt "A cinematic shot of a city at sunset"
    python3 scripts/qwen-image-text-to-image.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "wavespeed-ai/qwen-image/text-to-image"
OUTPUT_FORMATS = ["jpeg", "png", "webp"]


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--size", type=ws.size_type(), default="1024*1024",
        help="輸出尺寸，格式 寬x高（在 shell 中比 寬*高 安全，後者需加引號）",
    )
    parser.add_argument("--seed", type=int, default=None, help="隨機種子，未指定時由 API 隨機決定")
    parser.add_argument("--output-format", choices=OUTPUT_FORMATS, default="jpeg", help="輸出圖片格式")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    payload = {
        "size": args.size,
        "output_format": args.output_format,
    }
    if args.seed is not None:
        payload["seed"] = args.seed
    return payload


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload)
