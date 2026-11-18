#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 kwaivgi/kling-image-v4.0/image-set 產生主體與風格一致的組圖；指定 --image 時作為整組共用的參考圖。

用法範例（於專案根目錄執行）：
    python3 scripts/kling-image-v4.0-image-set.py
    python3 scripts/kling-image-v4.0-image-set.py -p prompts/xxx.txt -o output/xxx --num-images 6 --aspect-ratio 16:9
    python3 scripts/kling-image-v4.0-image-set.py --prompt "A four-panel story of a cat exploring a city"
    python3 scripts/kling-image-v4.0-image-set.py --image refs/a.png --prompt "<<<image_1>>> from four angles"
    python3 scripts/kling-image-v4.0-image-set.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "kwaivgi/kling-image-v4.0/image-set"
IMAGE_INPUT = ws.ImageInput("images", max_items=10)
ASPECT_RATIOS = ["1:1", "3:2", "2:3", "3:4", "4:3", "9:16", "16:9", "21:9"]
RESOLUTIONS = ["2k", "4k", "8k"]
OUTPUT_FORMATS = ["png", "jpeg", "webp"]


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--aspect-ratio", choices=ASPECT_RATIOS, default=None,
        help="每張圖的長寬比，未指定時由 API 依提示詞與參考圖決定",
    )
    parser.add_argument("--resolution", choices=RESOLUTIONS, default="2k", help="輸出解析度層級，同時是計費依據")
    parser.add_argument("--num-images", type=ws.number_type(2, 10), default=4, help="組圖張數，費用與張數成正比")
    parser.add_argument("--output-format", choices=OUTPUT_FORMATS, default="png", help="輸出圖片格式")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    payload = {
        "resolution": args.resolution,
        "num_images": args.num_images,
        "output_format": args.output_format,
    }
    if args.aspect_ratio is not None:
        payload["aspect_ratio"] = args.aspect_ratio
    return payload


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload, IMAGE_INPUT)
