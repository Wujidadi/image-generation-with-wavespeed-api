#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 ideogram-ai/ideogram-v4 進行文生圖；指定 --image 時以參考圖引導生成。

用法範例（於專案根目錄執行）：
    python3 scripts/ideogram-v4.py
    python3 scripts/ideogram-v4.py -p prompts/xxx.txt -o output/xxx --quality low --resolution 1k
    python3 scripts/ideogram-v4.py --prompt "A cinematic shot of a city at sunset"
    python3 scripts/ideogram-v4.py --image refs/a.png --strength 0.5 --prompt "The same warrior in a bamboo forest"
    python3 scripts/ideogram-v4.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "ideogram-ai/ideogram-v4"
IMAGE_INPUT = ws.ImageInput("image", max_items=1, shape="string", dependents=("strength",))
RESOLUTIONS = ["1k", "2k"]
ASPECT_RATIOS = ["1:1", "3:2", "2:3", "4:3", "3:4", "16:9", "9:16", "21:9", "9:21"]
QUALITIES = ["low", "medium", "high"]
OUTPUT_FORMATS = ["jpeg", "png", "webp"]


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--resolution", choices=RESOLUTIONS, default="1k", help="輸出解析度層級，同時是計費依據")
    parser.add_argument("--aspect-ratio", choices=ASPECT_RATIOS, default="1:1", help="輸出長寬比")
    parser.add_argument("--quality", choices=QUALITIES, default="medium", help="生成品質層級，同時是計費依據")
    parser.add_argument("--output-format", choices=OUTPUT_FORMATS, default="jpeg", help="輸出圖片格式")
    parser.add_argument(
        "--strength", type=ws.number_type(0, 1, integer=False), default=None,
        help="偏離參考圖的程度，須搭配 --image，未指定時由 API 預設（0.8）",
    )


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    payload = {
        "resolution": args.resolution,
        "aspect_ratio": args.aspect_ratio,
        "quality": args.quality,
        "output_format": args.output_format,
    }
    if args.strength is not None:
        payload["strength"] = args.strength
    return payload


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload, IMAGE_INPUT)
