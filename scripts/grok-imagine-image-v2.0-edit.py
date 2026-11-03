#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 x-ai/grok-imagine-image-v2.0/edit 依參考圖生成。

用法範例（於專案根目錄執行）：
    python3 scripts/grok-imagine-image-v2.0-edit.py --image refs/a.png --prompt "Move the subject to a bamboo forest"
    python3 scripts/grok-imagine-image-v2.0-edit.py --image refs/a.png refs/b.png -p prompts/xxx.txt -o output/xxx
    python3 scripts/grok-imagine-image-v2.0-edit.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "x-ai/grok-imagine-image-v2.0/edit"
RESOLUTIONS = ["1k", "2k"]
QUALITIES = ["low", "medium"]
IMAGE_INPUT = ws.ImageInput("images", min_items=1, max_items=3)


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--resolution", choices=RESOLUTIONS, default="2k", help="輸出解析度層級")
    parser.add_argument("--quality", choices=QUALITIES, default="medium", help="生成品質層級")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    payload = {
        "resolution": args.resolution,
        "quality": args.quality,
    }
    return payload


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload, IMAGE_INPUT)
