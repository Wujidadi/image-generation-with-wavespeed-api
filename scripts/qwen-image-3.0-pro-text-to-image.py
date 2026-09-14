#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 alibaba/qwen-image-3.0-pro/text-to-image 進行文生圖。

用法範例（於專案根目錄執行）：
    python3 scripts/qwen-image-3.0-pro-text-to-image.py
    python3 scripts/qwen-image-3.0-pro-text-to-image.py -o output/xxx --aspect-ratio 9:16 --resolution 2k
    python3 scripts/qwen-image-3.0-pro-text-to-image.py --prompt "A cinematic shot of a city at sunset"
    python3 scripts/qwen-image-3.0-pro-text-to-image.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "alibaba/qwen-image-3.0-pro/text-to-image"
ASPECT_RATIOS = [
    "1:1", "1:2", "2:1", "1:3", "3:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "9:21",
    "21:9",
]
RESOLUTIONS = ["1k", "2k"]


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--aspect-ratio", choices=ASPECT_RATIOS, default="1:1", help="輸出長寬比")
    parser.add_argument("--resolution", choices=RESOLUTIONS, default="1k", help="輸出解析度層級，同時是計費依據")
    parser.add_argument(
        "--enable-prompt-expansion", action=argparse.BooleanOptionalAction, default=True,
        help="是否啟用提示詞智慧擴寫",
    )
    parser.add_argument("--seed", type=int, default=None, help="隨機種子，未指定時由 API 隨機決定")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    payload = {
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
        "enable_prompt_expansion": args.enable_prompt_expansion,
    }
    if args.seed is not None:
        payload["seed"] = args.seed
    return payload


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload)
