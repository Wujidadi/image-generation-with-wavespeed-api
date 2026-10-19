#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 black-forest-labs/flux-3/text-to-image 進行文生圖。

用法範例（於專案根目錄執行）：
    python3 scripts/flux-3-text-to-image.py
    python3 scripts/flux-3-text-to-image.py -p prompts/xxx.txt -o output/xxx --aspect-ratio 16:9 --resolution 2k
    python3 scripts/flux-3-text-to-image.py --prompt "A cinematic shot of a city at sunset" --enable-prompt-expansion
    python3 scripts/flux-3-text-to-image.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "black-forest-labs/flux-3/text-to-image"
ASPECT_RATIOS = ["21:9", "2:1", "16:9", "3:2", "7:5", "4:3", "5:4", "1:1", "4:5", "3:4", "5:7", "2:3", "9:16", "1:2"]
RESOLUTIONS = ["1k", "2k", "4k"]
OUTPUT_FORMATS = ["jpeg", "png"]


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--aspect-ratio", choices=ASPECT_RATIOS, default="1:1", help="輸出長寬比")
    parser.add_argument(
        "--resolution", choices=RESOLUTIONS, default="1k",
        help="輸出解析度層級，同時是計費依據；4k 可能需要數分鐘",
    )
    parser.add_argument("--output-format", choices=OUTPUT_FORMATS, default="jpeg", help="輸出圖片格式")
    parser.add_argument(
        "--enable-prompt-expansion", action=argparse.BooleanOptionalAction, default=False,
        help="是否在保留原意的前提下擴寫提示詞",
    )


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    return {
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
        "output_format": args.output_format,
        "enable_prompt_expansion": args.enable_prompt_expansion,
    }


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload)
