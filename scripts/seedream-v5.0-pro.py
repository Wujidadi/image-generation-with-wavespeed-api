#!/usr/bin/env python3
"""以 WaveSpeed API 呼叫 bytedance/seedream-v5.0-pro 進行文生圖。

用法範例（於專案根目錄執行）：
    python3 scripts/seedream-v5.0-pro.py
    python3 scripts/seedream-v5.0-pro.py -p prompts/xxx.txt -o output/xxx --aspect-ratio 9:16 --resolution 2k
    python3 scripts/seedream-v5.0-pro.py --prompt "A cinematic shot of a city at sunset" --prompt-optimization-mode fast
    python3 scripts/seedream-v5.0-pro.py --task-id <任務 ID> -o output/xxx
"""

import argparse

import wavespeed_common as ws

MODEL_ID = "bytedance/seedream-v5.0-pro"
ASPECT_RATIOS = [
    "1:1", "1:2", "2:1", "1:3", "3:1", "2:3", "3:2", "3:4", "4:3",
    "4:5", "5:4", "9:16", "16:9", "9:21", "21:9",
]
RESOLUTIONS = ["1k", "1.5k", "2k"]
OUTPUT_FORMATS = ["jpeg", "png"]
PROMPT_OPTIMIZATION_MODES = ["standard", "fast"]


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--aspect-ratio", choices=ASPECT_RATIOS, default="1:1", help="輸出長寬比")
    parser.add_argument(
        "--resolution", choices=RESOLUTIONS, default="1k",
        help="輸出解析度層級，亦為計費依據（1k 與 1.5k 同價，2k 為兩倍）",
    )
    parser.add_argument("--output-format", choices=OUTPUT_FORMATS, default="jpeg", help="輸出圖片格式")
    parser.add_argument(
        "--prompt-optimization-mode", choices=PROMPT_OPTIMIZATION_MODES, default="standard",
        help="提示詞改寫模式，fast 較快但對長提示詞的遵循度較低",
    )


def build_payload(args: argparse.Namespace, prompt: str) -> dict:
    return {
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
        "output_format": args.output_format,
        "prompt_optimization_mode": args.prompt_optimization_mode,
    }


if __name__ == "__main__":
    ws.run(MODEL_ID, add_model_args, build_payload)
