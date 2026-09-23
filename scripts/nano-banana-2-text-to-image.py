#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 google/nano-banana-2/text-to-image 進行文生圖。

用法範例（於專案根目錄執行）：
    python3 scripts/nano-banana-2-text-to-image.py
    python3 scripts/nano-banana-2-text-to-image.py -o output/xxx --resolution 0.5k --enable-web-search
    python3 scripts/nano-banana-2-text-to-image.py --prompt "A cinematic shot of a city at sunset"
    python3 scripts/nano-banana-2-text-to-image.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "google/nano-banana-2/text-to-image"
ASPECT_RATIOS = [
    "1:1", "3:2", "2:3", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9", "1:4", "4:1", "1:8", "8:1",
]
RESOLUTIONS = ["0.5k", "1k", "2k", "4k"]
OUTPUT_FORMATS = ["png", "jpeg"]


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--aspect-ratio", choices=ASPECT_RATIOS, default=None,
        help="輸出長寬比，未指定時由 API 決定",
    )
    parser.add_argument("--resolution", choices=RESOLUTIONS, default="1k", help="輸出解析度層級，同時是計費依據")
    parser.add_argument(
        "--enable-web-search", action=argparse.BooleanOptionalAction, default=False,
        help="是否以網頁搜尋補充即時資訊，開啟後每張加收 $0.014",
    )
    parser.add_argument(
        "--enable-image-search", action=argparse.BooleanOptionalAction, default=False,
        help="是否以圖片搜尋補充即時資訊，開啟後每張加收 $0.014",
    )
    parser.add_argument("--output-format", choices=OUTPUT_FORMATS, default="png", help="輸出圖片格式")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    payload = {
        "resolution": args.resolution,
        "enable_web_search": args.enable_web_search,
        "enable_image_search": args.enable_image_search,
        "output_format": args.output_format,
    }
    if args.aspect_ratio is not None:
        payload["aspect_ratio"] = args.aspect_ratio
    return payload


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload)
