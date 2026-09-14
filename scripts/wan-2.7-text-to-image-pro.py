#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 alibaba/wan-2.7/text-to-image-pro 進行文生圖。

用法範例（於專案根目錄執行）：
    python3 scripts/wan-2.7-text-to-image-pro.py
    python3 scripts/wan-2.7-text-to-image-pro.py -p prompts/xxx.txt -o output/xxx --size 2048x2048 --no-thinking-mode
    python3 scripts/wan-2.7-text-to-image-pro.py --prompt "A cinematic shot of a city at sunset"
    python3 scripts/wan-2.7-text-to-image-pro.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "alibaba/wan-2.7/text-to-image-pro"


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--size",
        type=ws.size_type(side_min=512, side_max=8192, pixels_min=768 * 768, pixels_max=4096 * 4096, ratio_max=8),
        default="1024*1024",
        help="輸出尺寸，格式 寬x高（在 shell 中比 寬*高 安全，後者需加引號）",
    )
    parser.add_argument(
        "--thinking-mode", action=argparse.BooleanOptionalAction, default=True,
        help="是否啟用思考模式，品質較佳但耗時較長",
    )
    parser.add_argument("--seed", type=int, default=None, help="隨機種子，未指定時由 API 隨機決定")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    payload = {
        "size": args.size,
        "thinking_mode": args.thinking_mode,
    }
    if args.seed is not None:
        payload["seed"] = args.seed
    return payload


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload)
