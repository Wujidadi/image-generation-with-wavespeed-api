#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 alibaba/qwen-image-3.0/edit 依參考圖生成。

用法範例（於專案根目錄執行）：
    python3 scripts/qwen-image-3.0-edit.py --image refs/a.png --prompt "Move the subject to a bamboo forest"
    python3 scripts/qwen-image-3.0-edit.py --image refs/a.png refs/b.png -p prompts/xxx.txt -o output/xxx
    python3 scripts/qwen-image-3.0-edit.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "alibaba/qwen-image-3.0/edit"
ASPECT_RATIOS = [
    "1:1", "1:2", "2:1", "1:3", "3:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "9:21", "21:9",
]
RESOLUTIONS = ["1k", "2k"]
IMAGE_INPUT = ws.ImageInput("images", min_items=1, max_items=3)


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--aspect-ratio", choices=ASPECT_RATIOS, default=None, help="輸出長寬比，未指定時由 API 依參考圖決定")
    parser.add_argument("--resolution", choices=RESOLUTIONS, default="1k", help="輸出解析度層級")
    parser.add_argument(
        "--enable-prompt-expansion", action=argparse.BooleanOptionalAction, default=False,
        help="是否啟用提示詞智慧擴寫",
    )
    parser.add_argument("--seed", type=int, default=None, help="隨機種子，未指定時由 API 隨機決定")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    payload = {
        "resolution": args.resolution,
        "enable_prompt_expansion": args.enable_prompt_expansion,
    }
    if args.aspect_ratio is not None:
        payload["aspect_ratio"] = args.aspect_ratio
    if args.seed is not None:
        payload["seed"] = args.seed
    return payload


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload, IMAGE_INPUT)
