#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 krea/v3/text-to-image 進行文生圖。

用法範例（於專案根目錄執行）：
    python3 scripts/krea-v3-text-to-image.py
    python3 scripts/krea-v3-text-to-image.py -p prompts/xxx.txt -o output/xxx --size 2048x1152 --model jam
    python3 scripts/krea-v3-text-to-image.py --prompt "A cinematic shot of a city at sunset" --reasoning-level medium
    python3 scripts/krea-v3-text-to-image.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "krea/v3/text-to-image"
MODELS = ["berry", "jam"]
REASONING_LEVELS = ["low", "medium"]
OUTPUT_FORMATS = ["png", "jpeg"]


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--negative-prompt", default=None, help="負向提示詞，僅 berry 模型生效，未指定時不送出")
    parser.add_argument(
        "--size", type=ws.size_type(side_min=256, side_max=4096, pixels_min=65_536, pixels_max=4_194_304), default="1024*1024",
        help="輸出尺寸，格式 寬x高（在 shell 中比 寬*高 安全，後者需加引號），總像素上限 4 百萬；價格與總像素成正比",
    )
    parser.add_argument("--model", choices=MODELS, default="berry", help="berry 偏重品質，jam 偏重速度")
    parser.add_argument("--reasoning-level", choices=REASONING_LEVELS, default="low", help="推理強度，較高可能更貼合提示詞但耗時較久")
    parser.add_argument("--output-format", choices=OUTPUT_FORMATS, default="png", help="輸出圖片格式")
    parser.add_argument("--seed", type=int, default=None, help="隨機種子，未指定時由 API 隨機決定")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    payload = {
        "size": args.size,
        "model": args.model,
        "reasoning_level": args.reasoning_level,
        "output_format": args.output_format,
    }
    if args.negative_prompt is not None:
        payload["negative_prompt"] = args.negative_prompt
    if args.seed is not None:
        payload["seed"] = args.seed
    return payload


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload)
