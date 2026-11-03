#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 bytedance/seedream-v4/edit 依參考圖生成。

用法範例（於專案根目錄執行）：
    python3 scripts/seedream-v4-edit.py --image refs/a.png --prompt "Move the subject to a bamboo forest"
    python3 scripts/seedream-v4-edit.py --image refs/a.png refs/b.png -p prompts/xxx.txt -o output/xxx
    python3 scripts/seedream-v4-edit.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "bytedance/seedream-v4/edit"
SIZE_MIN, SIZE_MAX = 512, 8192
IMAGE_INPUT = ws.ImageInput("images", min_items=1, max_items=10)


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
        "--size", type=parse_size, default=None,
        help="輸出尺寸，格式 寬x高（在 shell 中比 寬*高 安全，後者需加引號），未指定時由 API 決定",
    )


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    payload = {}
    if args.size is not None:
        payload["size"] = args.size
    return payload


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload, IMAGE_INPUT)
