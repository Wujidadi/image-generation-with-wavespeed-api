#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 bytedance/seedream-v5.0-lite/edit 依參考圖生成。

用法範例（於專案根目錄執行）：
    python3 scripts/seedream-v5.0-lite-edit.py --image refs/a.png --prompt "Move the subject to a bamboo forest"
    python3 scripts/seedream-v5.0-lite-edit.py --image refs/a.png refs/b.png -p prompts/xxx.txt -o output/xxx
    python3 scripts/seedream-v5.0-lite-edit.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "bytedance/seedream-v5.0-lite/edit"
OUTPUT_FORMATS = ["jpeg", "png"]
SIDE_MIN, SIDE_MAX = 1440, 8192
PIXELS_MIN, PIXELS_MAX = 2560 * 1440, 4096 * 4096
IMAGE_INPUT = ws.ImageInput("images", min_items=1, max_items=10)


def parse_size(value: str) -> str:
    """接受 寬x高 或 寬*高，單邊需在 1440 到 8192 之間，總像素需在 2560*1440 到 4096*4096 之間，回傳 API 要求的 寬*高

    尺寸過小時 API 不會拒絕，而是靜默放大到總像素下限（1:1 即 1920*1920）並照常扣費，因此在本機先擋下
    """
    width, separator, height = value.lower().replace("*", "x").partition("x")
    if not separator or not width.isdigit() or not height.isdigit():
        raise argparse.ArgumentTypeError(f"格式須為 寬x高，例如 2048x2048，收到：{value}")
    width, height = int(width), int(height)
    for side in (width, height):
        if not SIDE_MIN <= side <= SIDE_MAX:
            raise argparse.ArgumentTypeError(f"寬與高須介於 {SIDE_MIN} 到 {SIDE_MAX}，收到：{value}")
    if not PIXELS_MIN <= width * height <= PIXELS_MAX:
        raise argparse.ArgumentTypeError(
            f"總像素須介於 2560*1440（{PIXELS_MIN}）到 4096*4096（{PIXELS_MAX}），收到：{value}（{width * height}）"
        )
    return f"{width}*{height}"


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--size", type=parse_size, default=None,
        help="輸出尺寸，格式 寬x高（在 shell 中比 寬*高 安全，後者需加引號），未指定時由 API 決定",
    )
    parser.add_argument("--output-format", choices=OUTPUT_FORMATS, default=None, help="輸出圖片格式，未指定時由 API 決定")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    payload = {}
    if args.size is not None:
        payload["size"] = args.size
    if args.output_format is not None:
        payload["output_format"] = args.output_format
    return payload


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload, IMAGE_INPUT)
