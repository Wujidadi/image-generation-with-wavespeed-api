#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 ideogram-ai/ideogram-v4 進行文生圖。

用法範例（於專案根目錄執行）：
    python3 scripts/ideogram-v4.py
    python3 scripts/ideogram-v4.py -p prompts/xxx.txt -o output/xxx --quality low --resolution 1k
    python3 scripts/ideogram-v4.py --prompt "A cinematic shot of a city at sunset"
    python3 scripts/ideogram-v4.py --task-id <任務 ID> -o output/xxx

本腳本只做文生圖，未開放 API 的 image、strength 等圖生圖參數。
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "ideogram-ai/ideogram-v4"
RESOLUTIONS = ["1k", "2k"]
ASPECT_RATIOS = ["1:1", "3:2", "2:3", "4:3", "3:4", "16:9", "9:16", "21:9", "9:21"]
QUALITIES = ["low", "medium", "high"]
OUTPUT_FORMATS = ["jpeg", "png", "webp"]


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--resolution", choices=RESOLUTIONS, default="1k", help="輸出解析度層級，同時是計費依據")
    parser.add_argument("--aspect-ratio", choices=ASPECT_RATIOS, default="1:1", help="輸出長寬比")
    parser.add_argument("--quality", choices=QUALITIES, default="medium", help="生成品質層級，同時是計費依據")
    parser.add_argument("--output-format", choices=OUTPUT_FORMATS, default="jpeg", help="輸出圖片格式")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    return {
        "resolution": args.resolution,
        "aspect_ratio": args.aspect_ratio,
        "quality": args.quality,
        "output_format": args.output_format,
    }


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload)
