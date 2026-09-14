#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 wavespeed-ai/flux-dev-ultra-fast 進行文生圖。

用法範例（於專案根目錄執行）：
    python3 scripts/flux-dev-ultra-fast.py
    python3 scripts/flux-dev-ultra-fast.py -p prompts/xxx.txt -o output/xxx --size 1280x720 --num-images 2
    python3 scripts/flux-dev-ultra-fast.py --prompt "A cinematic shot of a city at sunset"
    python3 scripts/flux-dev-ultra-fast.py --task-id <任務 ID> -o output/xxx

本腳本只做文生圖，未開放 API 的 image、mask_image、strength 等圖生圖參數。
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "wavespeed-ai/flux-dev-ultra-fast"
OUTPUT_FORMATS = ["jpeg", "png", "webp"]


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--size", type=ws.size_type(), default="1024*1024",
        help="輸出尺寸，格式 寬x高（在 shell 中比 寬*高 安全，後者需加引號）",
    )
    parser.add_argument("--num-inference-steps", type=ws.number_type(1, 50), default=28, help="去噪步數")
    parser.add_argument("--seed", type=int, default=None, help="隨機種子，未指定時由 API 隨機決定")
    parser.add_argument(
        "--guidance-scale", type=ws.number_type(0, 20, integer=False), default=3.5,
        help="提示詞遵循強度",
    )
    parser.add_argument("--num-images", type=ws.number_type(1, 4), default=1, help="產圖張數，費用與張數成正比")
    parser.add_argument("--output-format", choices=OUTPUT_FORMATS, default="jpeg", help="輸出圖片格式")


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    payload = {
        "size": args.size,
        "num_inference_steps": args.num_inference_steps,
        "guidance_scale": args.guidance_scale,
        "num_images": args.num_images,
        "output_format": args.output_format,
    }
    if args.seed is not None:
        payload["seed"] = args.seed
    return payload


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload)
