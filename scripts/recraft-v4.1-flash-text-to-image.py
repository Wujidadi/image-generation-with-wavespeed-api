#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 recraft-ai/recraft-v4.1-flash/text-to-image 進行文生圖。

用法範例（於專案根目錄執行）：
    python3 scripts/recraft-v4.1-flash-text-to-image.py
    python3 scripts/recraft-v4.1-flash-text-to-image.py -p prompts/xxx.txt -o output/xxx --aspect-ratio 16:9
    python3 scripts/recraft-v4.1-flash-text-to-image.py --prompt "A cinematic shot of a city at sunset"
    python3 scripts/recraft-v4.1-flash-text-to-image.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "recraft-ai/recraft-v4.1-flash/text-to-image"
ASPECT_RATIOS = ["1:1", "16:9", "9:16", "4:3", "3:4"]


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--aspect-ratio", choices=ASPECT_RATIOS, default="1:1", help="輸出長寬比")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    return {"aspect_ratio": args.aspect_ratio}


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload)
