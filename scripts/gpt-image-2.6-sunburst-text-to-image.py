#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 openai/gpt-image-2.6-sunburst/text-to-image 進行文生圖。

用法範例（於專案根目錄執行）：
    python3 scripts/gpt-image-2.6-sunburst-text-to-image.py
    python3 scripts/gpt-image-2.6-sunburst-text-to-image.py -p prompts/xxx.txt -o output/xxx --quality low --resolution 1k
    python3 scripts/gpt-image-2.6-sunburst-text-to-image.py --prompt "A cinematic shot of a city at sunset"
    python3 scripts/gpt-image-2.6-sunburst-text-to-image.py --output-format gif --frame-count 12 --frame-duration-ms 150
    python3 scripts/gpt-image-2.6-sunburst-text-to-image.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "openai/gpt-image-2.6-sunburst/text-to-image"
ASPECT_RATIOS = [
    "1:1", "1:2", "2:1", "1:3", "3:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "9:21",
    "21:9",
]
RESOLUTIONS = ["1k", "2k", "4k"]
QUALITIES = ["low", "medium", "high", "xhigh", "max"]
COMPLEXITIES = ["low", "medium", "high"]
OUTPUT_FORMATS = ["png", "jpeg", "webp", "gif", "svg"]


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--aspect-ratio", choices=ASPECT_RATIOS, default="1:1", help="輸出長寬比")
    parser.add_argument("--resolution", choices=RESOLUTIONS, default="1k", help="輸出解析度層級，同時是計費依據")
    parser.add_argument("--quality", choices=QUALITIES, default="medium", help="生成品質層級，同時是計費依據")
    parser.add_argument("--complexity", choices=COMPLEXITIES, default="high", help="生成前的構圖規劃程度，越高越能處理細節繁多的提示詞，不影響價格")
    parser.add_argument("--output-format", choices=OUTPUT_FORMATS, default="png", help="輸出圖片格式")
    parser.add_argument(
        "--frame-count", type=ws.number_type(2, 16), default=9,
        help="動畫影格數，只在 --output-format gif 時送出",
    )
    parser.add_argument(
        "--frame-duration-ms", type=ws.number_type(20, 2000), default=200,
        help="每格停留毫秒數，只在 --output-format gif 時送出",
    )


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    payload = {
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
        "quality": args.quality,
        "complexity": args.complexity,
        "output_format": args.output_format,
    }
    if args.output_format == "gif":
        payload["frame_count"] = args.frame_count
        payload["frame_duration_ms"] = args.frame_duration_ms
    return payload


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload)
