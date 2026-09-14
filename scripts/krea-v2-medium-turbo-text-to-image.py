#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 wavespeed-ai/krea-v2-medium-turbo/text-to-image 進行文生圖。

用法範例（於專案根目錄執行）：
    python3 scripts/krea-v2-medium-turbo-text-to-image.py
    python3 scripts/krea-v2-medium-turbo-text-to-image.py -o output/xxx --aspect-ratio 16:9 --creativity raw
    python3 scripts/krea-v2-medium-turbo-text-to-image.py --prompt "A cinematic shot of a city at sunset"
    python3 scripts/krea-v2-medium-turbo-text-to-image.py --task-id <任務 ID> -o output/xxx

本腳本只做文生圖，未開放 API 的 reference 等圖生圖參數。
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "wavespeed-ai/krea-v2-medium-turbo/text-to-image"
ASPECT_RATIOS = ["1:1", "4:3", "3:2", "16:9", "2.35:1", "4:5", "2:3", "9:16"]
CREATIVITY_LEVELS = ["raw", "low", "medium", "high"]


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--aspect-ratio", choices=ASPECT_RATIOS, default="1:1", help="輸出長寬比")
    parser.add_argument("--creativity", choices=CREATIVITY_LEVELS, default="medium", help="提示詞詮釋的寬鬆程度")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    return {
        "aspect_ratio": args.aspect_ratio,
        "creativity": args.creativity,
    }


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload)
