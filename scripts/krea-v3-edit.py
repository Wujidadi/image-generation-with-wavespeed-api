#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 krea/v3/edit 依參考圖生成。

用法範例（於專案根目錄執行）：
    python3 scripts/krea-v3-edit.py --image refs/a.png --prompt "Move the subject to a bamboo forest"
    python3 scripts/krea-v3-edit.py --image refs/a.png refs/b.png -p prompts/xxx.txt -o output/xxx
    python3 scripts/krea-v3-edit.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "krea/v3/edit"
MODELS = ["berry", "jam"]
REASONING_LEVELS = ["low", "medium"]
OUTPUT_FORMATS = ["png", "jpeg"]
IMAGE_INPUT = ws.ImageInput("images", min_items=1, max_items=8)


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--negative-prompt", default=None, help="負向提示詞，僅 berry 模型生效，未指定時不送出")
    parser.add_argument(
        "--size", type=ws.size_type(side_min=256, side_max=4096, pixels_min=65_536, pixels_max=4_194_304), default=None,
        help="輸出尺寸，格式 寬x高（在 shell 中比 寬*高 安全，後者需加引號），總像素上限 4 百萬，同時是計費依據，未指定時由 API 決定",
    )
    parser.add_argument("--model", choices=MODELS, default="berry", help="berry 偏重品質，jam 偏重速度")
    parser.add_argument("--reasoning-level", choices=REASONING_LEVELS, default="low", help="推理強度，較高可能更貼合提示詞但耗時較久")
    parser.add_argument("--output-format", choices=OUTPUT_FORMATS, default="png", help="輸出圖片格式")
    parser.add_argument("--seed", type=int, default=None, help="隨機種子，未指定時由 API 隨機決定")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    payload = {
        "model": args.model,
        "reasoning_level": args.reasoning_level,
        "output_format": args.output_format,
    }
    if args.negative_prompt is not None:
        payload["negative_prompt"] = args.negative_prompt
    if args.size is not None:
        payload["size"] = args.size
    if args.seed is not None:
        payload["seed"] = args.seed
    return payload


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload, IMAGE_INPUT)
