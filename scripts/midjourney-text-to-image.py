#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 midjourney/text-to-image 進行文生圖。

用法範例（於專案根目錄執行）：
    python3 scripts/midjourney-text-to-image.py
    python3 scripts/midjourney-text-to-image.py -p prompts/xxx.txt -o output/xxx --aspect-ratio 16:9 --stylize 250
    python3 scripts/midjourney-text-to-image.py --prompt "A cinematic shot of a city at sunset"
    python3 scripts/midjourney-text-to-image.py --task-id <任務 ID> -o output/xxx

本腳本只做文生圖，未開放 API 的 sref 等圖生圖參數。
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "midjourney/text-to-image"
ASPECT_RATIOS = ["1:1", "9:16", "16:9", "4:3", "3:4", "2:3", "3:2", "9:21", "21:9"]
QUALITIES = [1, 4]


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--aspect-ratio", choices=ASPECT_RATIOS, default="1:1", help="輸出長寬比")
    parser.add_argument(
        "--hd", action=argparse.BooleanOptionalAction, default=False,
        help="是否啟用 HD 模式，費用由 $0.100 升為 $0.150",
    )
    parser.add_argument(
        "--quality", type=int, choices=QUALITIES, default=1,
        help="Midjourney v8.1 的品質設定，不影響計費",
    )
    parser.add_argument("--stylize", type=ws.number_type(0, 1000), default=0, help="美學風格的影響強度")
    parser.add_argument("--chaos", type=ws.number_type(0, 100), default=0, help="變化與不可預測性")
    parser.add_argument("--weird", type=ws.number_type(0, 3000), default=0, help="非常規與超現實的程度")
    parser.add_argument("--seed", type=int, default=None, help="隨機種子，未指定時由 API 隨機決定")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    payload = {
        "aspect_ratio": args.aspect_ratio,
        "hd": args.hd,
        "quality": args.quality,
        "stylize": args.stylize,
        "chaos": args.chaos,
        "weird": args.weird,
    }
    if args.seed is not None:
        payload["seed"] = args.seed
    return payload


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload)
