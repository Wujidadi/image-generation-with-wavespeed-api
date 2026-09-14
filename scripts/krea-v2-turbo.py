#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 wavespeed-ai/krea-v2/turbo 進行文生圖。

用法範例（於專案根目錄執行）：
    python3 scripts/krea-v2-turbo.py
    python3 scripts/krea-v2-turbo.py -p prompts/xxx.txt -o output/xxx --aspect-ratio 16:9 --resolution 2k
    python3 scripts/krea-v2-turbo.py --prompt "A cinematic shot of a city at sunset"
    python3 scripts/krea-v2-turbo.py --task-id <任務 ID> -o output/xxx

本腳本只做文生圖，未開放 API 的 image、strength 等圖生圖參數。
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "wavespeed-ai/krea-v2/turbo"
ASPECT_RATIOS = [
    "1:1", "1:2", "2:1", "1:3", "3:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "9:21",
    "21:9",
]
RESOLUTIONS = ["1k", "2k"]


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--aspect-ratio", choices=ASPECT_RATIOS, default="1:1", help="輸出長寬比")
    parser.add_argument("--resolution", choices=RESOLUTIONS, default="1k", help="輸出解析度層級，同時是計費依據")
    parser.add_argument("--seed", type=int, default=None, help="隨機種子，未指定時由 API 隨機決定")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    payload = {
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
    }
    if args.seed is not None:
        payload["seed"] = args.seed
    return payload


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload)
