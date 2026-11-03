#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 wavespeed-ai/krea-v2/turbo 進行文生圖；指定 --image 時以參考圖引導生成。

用法範例（於專案根目錄執行）：
    python3 scripts/krea-v2-turbo.py
    python3 scripts/krea-v2-turbo.py -p prompts/xxx.txt -o output/xxx --aspect-ratio 16:9 --resolution 2k
    python3 scripts/krea-v2-turbo.py --prompt "A cinematic shot of a city at sunset"
    python3 scripts/krea-v2-turbo.py --image refs/a.png --strength 0.5 --prompt "The same warrior in a bamboo forest"
    python3 scripts/krea-v2-turbo.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "wavespeed-ai/krea-v2/turbo"
IMAGE_INPUT = ws.ImageInput("image", max_items=1, shape="string", dependents=("strength",))
ASPECT_RATIOS = [
    "1:1", "1:2", "2:1", "1:3", "3:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "9:21",
    "21:9",
]
RESOLUTIONS = ["1k", "2k"]


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--aspect-ratio", choices=ASPECT_RATIOS, default="1:1", help="輸出長寬比")
    parser.add_argument("--resolution", choices=RESOLUTIONS, default="1k", help="輸出解析度層級，同時是計費依據")
    parser.add_argument("--seed", type=int, default=None, help="隨機種子，未指定時由 API 隨機決定")
    parser.add_argument(
        "--strength", type=ws.number_type(0, 1, integer=False), default=None,
        help="偏離參考圖的程度，須搭配 --image，未指定時由 API 預設（0.8）",
    )


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    payload = {
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
    }
    if args.strength is not None:
        payload["strength"] = args.strength
    if args.seed is not None:
        payload["seed"] = args.seed
    return payload


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload, IMAGE_INPUT)
