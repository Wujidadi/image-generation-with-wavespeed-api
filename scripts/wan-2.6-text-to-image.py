#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 alibaba/wan-2.6/text-to-image 進行文生圖。

用法範例（於專案根目錄執行）：
    python3 scripts/wan-2.6-text-to-image.py
    python3 scripts/wan-2.6-text-to-image.py -p prompts/xxx.txt -o output/xxx --size 1440x1440 --enable-prompt-expansion
    python3 scripts/wan-2.6-text-to-image.py --prompt "A cinematic shot of a city at sunset"
    python3 scripts/wan-2.6-text-to-image.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "alibaba/wan-2.6/text-to-image"


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--size", type=ws.size_type(side_min=768, side_max=1440), default="1024*1024",
        help="輸出尺寸，格式 寬x高（在 shell 中比 寬*高 安全，後者需加引號）",
    )
    parser.add_argument(
        "--enable-prompt-expansion", action=argparse.BooleanOptionalAction, default=False,
        help="是否啟用提示詞智慧擴寫",
    )
    parser.add_argument("--seed", type=int, default=None, help="隨機種子，未指定時由 API 隨機決定")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    payload = {
        "size": args.size,
        "enable_prompt_expansion": args.enable_prompt_expansion,
    }
    if args.seed is not None:
        payload["seed"] = args.seed
    return payload


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload)
