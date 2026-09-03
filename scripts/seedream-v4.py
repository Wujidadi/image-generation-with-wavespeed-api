#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 bytedance/seedream-v4 進行文生圖。

用法範例（於專案根目錄執行）：
    python3 scripts/seedream-v4.py
    python3 scripts/seedream-v4.py -p prompts/xxx.txt -o output/xxx --size 1440x2560
    python3 scripts/seedream-v4.py --prompt "A cinematic shot of a city at sunset"
    python3 scripts/seedream-v4.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "bytedance/seedream-v4"
SIZE_MIN, SIZE_MAX = 512, 8192


def parse_size(value: str) -> str:
    """接受 寬x高 或 寬*高，單邊需在 512 到 8192 之間，回傳 API 要求的 寬*高"""
    width, separator, height = value.lower().replace("*", "x").partition("x")
    if not separator or not width.isdigit() or not height.isdigit():
        raise argparse.ArgumentTypeError(f"格式須為 寬x高，例如 2048x2048，收到：{value}")
    for side in (int(width), int(height)):
        if not SIZE_MIN <= side <= SIZE_MAX:
            raise argparse.ArgumentTypeError(f"寬與高須介於 {SIZE_MIN} 到 {SIZE_MAX}，收到：{value}")
    return f"{int(width)}*{int(height)}"


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--size", type=parse_size, default="2048*2048",
        help="輸出尺寸，格式 寬x高（在 shell 中比 寬*高 安全，後者需加引號）",
    )


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    return {"size": args.size}


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload)
