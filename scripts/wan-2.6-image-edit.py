#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 alibaba/wan-2.6/image-edit 依參考圖生成。

用法範例（於專案根目錄執行）：
    python3 scripts/wan-2.6-image-edit.py --image refs/a.png --prompt "Move the subject to a bamboo forest"
    python3 scripts/wan-2.6-image-edit.py --image refs/a.png refs/b.png -p prompts/xxx.txt -o output/xxx
    python3 scripts/wan-2.6-image-edit.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "alibaba/wan-2.6/image-edit"
IMAGE_INPUT = ws.ImageInput("images", min_items=1, max_items=3)


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--size", type=ws.size_type(side_min=384, side_max=4096), default=None,
        help="輸出尺寸，格式 寬x高（在 shell 中比 寬*高 安全，後者需加引號），未指定時由 API 決定",
    )
    parser.add_argument(
        "--enable-prompt-expansion", action=argparse.BooleanOptionalAction, default=False,
        help="是否啟用提示詞智慧擴寫",
    )
    parser.add_argument("--seed", type=int, default=None, help="隨機種子，未指定時由 API 隨機決定")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    payload = {
        "enable_prompt_expansion": args.enable_prompt_expansion,
    }
    if args.size is not None:
        payload["size"] = args.size
    if args.seed is not None:
        payload["seed"] = args.seed
    return payload


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload, IMAGE_INPUT)
