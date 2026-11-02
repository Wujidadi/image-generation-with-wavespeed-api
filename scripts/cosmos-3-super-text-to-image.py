#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 nvidia/cosmos-3-super/text-to-image 進行文生圖。

用法範例（於專案根目錄執行）：
    python3 scripts/cosmos-3-super-text-to-image.py
    python3 scripts/cosmos-3-super-text-to-image.py -o output/xxx --size 16:9
    python3 scripts/cosmos-3-super-text-to-image.py --prompt "A cinematic shot of a city at sunset"
    python3 scripts/cosmos-3-super-text-to-image.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "nvidia/cosmos-3-super/text-to-image"
SIZES = ["1:1", "3:4", "9:16", "4:3", "16:9"]
OUTPUT_FORMATS = ["jpeg", "png"]


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--size", choices=SIZES, default="1:1", help="輸出尺寸預設組合，以長寬比表示")
    parser.add_argument("--output-format", choices=OUTPUT_FORMATS, default="jpeg", help="輸出圖片格式")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    return {
        "size": args.size,
        "output_format": args.output_format,
    }


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload)
