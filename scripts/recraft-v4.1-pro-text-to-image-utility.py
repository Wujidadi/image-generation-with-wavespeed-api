#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 recraft-ai/recraft-v4.1-pro/text-to-image-utility 進行文生圖。

用法範例（於專案根目錄執行）：
    python3 scripts/recraft-v4.1-pro-text-to-image-utility.py
    python3 scripts/recraft-v4.1-pro-text-to-image-utility.py -p prompts/xxx.txt -o output/xxx --image-size 16:9
    python3 scripts/recraft-v4.1-pro-text-to-image-utility.py --prompt "A cinematic shot of a city at sunset"
    python3 scripts/recraft-v4.1-pro-text-to-image-utility.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "recraft-ai/recraft-v4.1-pro/text-to-image-utility"
IMAGE_SIZES = ["1:1", "16:9", "9:16", "4:3", "3:4"]


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--image-size", choices=IMAGE_SIZES, default="1:1", help="輸出長寬比")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    return {"image_size": args.image_size}


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload)
