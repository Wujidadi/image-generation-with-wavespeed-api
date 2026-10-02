#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 ideogram-ai/ideogram-v4.5 進行文生圖。

用法範例（於專案根目錄執行）：
    python3 scripts/ideogram-v4.5.py
    python3 scripts/ideogram-v4.5.py -p prompts/xxx.txt -o output/xxx --quality low --resolution 2k
    python3 scripts/ideogram-v4.5.py --prompt "A cinematic shot of a city at sunset" --no-enable-prompt-expansion
    python3 scripts/ideogram-v4.5.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "ideogram-ai/ideogram-v4.5"
RESOLUTIONS = ["1k", "2k"]
ASPECT_RATIOS = ["1:1", "4:3", "3:4", "3:2", "2:3", "16:9", "9:16"]
QUALITIES = ["low", "medium", "high"]


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--resolution", choices=RESOLUTIONS, default="1k", help="輸出解析度層級，各層級同價")
    parser.add_argument("--aspect-ratio", choices=ASPECT_RATIOS, default="1:1", help="輸出長寬比")
    parser.add_argument(
        "--quality", choices=QUALITIES, default="medium",
        help="生成品質層級，亦為計費依據（low $0.03、medium $0.06、high $0.22）",
    )
    parser.add_argument(
        "--enable-prompt-expansion", action=argparse.BooleanOptionalAction, default=True,
        help="生成前先由模型擴寫提示詞",
    )


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    return {
        "resolution": args.resolution,
        "aspect_ratio": args.aspect_ratio,
        "quality": args.quality,
        "enable_prompt_expansion": args.enable_prompt_expansion,
    }


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload)
