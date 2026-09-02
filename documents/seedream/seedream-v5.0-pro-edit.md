<!--
來源：https://wavespeed.ai/docs/docs-api/bytedance/bytedance-seedream-v5.0-pro-edit
模型頁：https://wavespeed.ai/models/bytedance/seedream-v5.0-pro/edit
下載時間：2026-09-02T21:05:05+08:00
說明：由 WaveSpeed 官方文件頁靜態 HTML 轉為 Markdown；Node.js／Python 範例為前端動態渲染，靜態頁僅含 cURL 版本
-->

# Bytedance Seedream V5.0 Pro Edit API Documentation

## Playground

[Try it on WaveSpeedAI!](https://wavespeed.ai/models/bytedance/seedream-v5.0-pro/edit)

Seedream V5.0 Pro Edit by ByteDance edits and generates images from single-image or multi-reference inputs, supporting up to 10 reference images, aspect ratio selection, and 1K / 2K output tiers. Ready-to-use REST inference API, best performance, no coldstarts, affordable pricing.

## Features

**Seedream V5.0 Pro Edit** is a multimodal image editing model built for professional work: interactive precision editing, multi-reference control, photographic realism, and native multilingual text.

---

## Why Choose This?

- **Multi-image reference editing**
  Use up to 10 reference images for complex edits, compositions, and visual guidance.
- **Natural language editing**
  Describe the desired edit in plain text and let the model transform the input images accordingly.
- **Pro image quality**
  Designed for high-quality image editing with strong prompt adherence and polished visual output.
- **Flexible resolution tiers**
  Choose `1k` or `1.5k` for lower-cost edits, or `2k` for higher-resolution output.
- **Flexible aspect ratios**
  Supports square, portrait, landscape, tall, and wide aspect ratios.
- **Standard output formats**
  Generate edited images in `jpeg` or `png` format.

---

## Parameters

| Parameter                | Required | Description                                                                                                                                                                                                                                                                                           |
| ------------------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| prompt                   | Yes      | Text description of the desired edit.                                                                                                                                                                                                                                                                 |
| images                   | Yes      | Reference image URLs or Base64 strings. Supports up to 10 images.                                                                                                                                                                                                                                     |
| aspect_ratio             | No       | Output aspect ratio.                                                                                                                                                                                                                                                                                  |
| resolution               | No       | Output resolution tier: `1k`, `1.5k`, or `2k`.                                                                                                                                                                                                                                                        |
| output_format            | No       | Output format: `jpeg` or `png`.                                                                                                                                                                                                                                                                       |
| prompt_optimization_mode | No       | Prompt optimization mode: `standard` (default) or `fast`. The model rewrites your prompt before generating; `fast` uses a lighter rewrite that returns several times quicker but follows long or intricate prompts less closely. Reference time: 14s (`fast`) vs 26s (`standard`) on the same prompt. |

---

## How to Use

1. **Upload reference images** — Provide one or more images to guide the edit.
2. **Write your prompt** — Describe what should change and what should stay the same.
3. **Choose aspect ratio** — Select a supported aspect ratio, or leave it empty to follow the closest supported ratio from the first input image.
4. **Choose resolution** — Use `1k` or `1.5k` for lower-cost edits, or `2k` for higher-resolution output.
5. **Choose output format** — Select `jpeg` or `png`.
6. **Submit** — Generate the final edited image.

---

## Pricing

Pricing includes the selected output resolution plus reference image input cost. The first input image is included; each additional input image costs **$0.003**.

| Resolution | Base Price |
| ---------- | ---------- |
| 1k         | $0.045     |
| 1.5k       | $0.045     |
| 2k         | $0.090     |

### Example Costs

| Resolution | Input Images | Cost   |
| ---------- | ------------ | ------ |
| 1k         | 1            | $0.045 |
| 1k         | 2            | $0.048 |
| 1k         | 10           | $0.072 |
| 1.5k       | 1            | $0.045 |
| 1.5k       | 2            | $0.048 |
| 1.5k       | 10           | $0.072 |
| 2k         | 1            | $0.090 |
| 2k         | 2            | $0.093 |
| 2k         | 10           | $0.117 |

---

## Best Use Cases

- **Single-image editing** — Edit one source image with natural-language instructions.
- **Multi-reference composition** — Use multiple images to guide complex edits and visual combinations.
- **Product image editing** — Refine product visuals, backgrounds, styles, and presentation.
- **Character and style guidance** — Use reference images to preserve identity, outfit, mood, or visual style.
- **Marketing image workflows** — Generate polished edited assets for campaigns, social media, and product content.
- **Creative iteration** — Test different edit directions using the same reference images.

---

## Pro Tips

- Use `prompt_optimization_mode: fast` while iterating on an edit, and `standard` for the final render — the fast rewrite is several times quicker but follows long instructions less closely.
- Use clear prompts that describe both what should change and what should remain unchanged.
- Use multiple reference images when identity, product details, or style consistency matters.
- Leave `aspect_ratio` empty when you want the output to follow the closest supported ratio from the first input image.
- Choose `1k` or `1.5k` for lower-cost editing and fast iteration.
- Choose `2k` when you need higher-resolution final output.
- Use `jpeg` for general-purpose edited images and `png` when PNG output is needed.
- Keep reference images clear, relevant, and visually consistent with the desired edit.

---

## Related Models

- [Seedream V5.0 Pro](https://wavespeed.ai/models/bytedance/seedream-v5.0-pro) — Generate images from text prompts.
- [Seedream V5.0 Lite Edit](https://wavespeed.ai/models/bytedance/seedream-v5.0-lite/edit) — Lightweight image editing model.

## Authentication

For authentication details, please refer to the [Authentication Guide](https://wavespeed.ai/docs/api-authentication).

## API Endpoints

### Submit Task & Query Result

cURL / HTTP

```bash
set -euo pipefail

export WAVESPEED_API_KEY="your-api-key"

REQUEST_BODY=$(cat <<'JSON'
{
  "prompt": "A cinematic ocean wave at sunrise, highly detailed",
  "images": [
    "https://interactive-examples.mdn.mozilla.net/media/cc0-images/painted-hand-298-332.jpg"
  ],
  "aspect_ratio": "1:1",
  "resolution": "1k",
  "output_format": "jpeg",
  "prompt_optimization_mode": "standard"
}
JSON
)

# 1. Submit the prediction.
SUBMIT_RESPONSE=$(curl --silent --show-error --fail-with-body \
  -X POST "https://api.wavespeed.ai/api/v3/bytedance/seedream-v5.0-pro/edit" \
  -H "Authorization: Bearer ${WAVESPEED_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "${REQUEST_BODY}")

TASK=$(printf '%s' "${SUBMIT_RESPONSE}" | jq 'if type == "object" and has("data") then .data else . end')
PREDICTION_ID=$(printf '%s' "${TASK}" | jq -r '.id // empty')
if [ -z "${PREDICTION_ID}" ]; then
  printf 'Submission response did not contain a prediction id
' >&2
  exit 1
fi
RESULT_URL="https://api.wavespeed.ai/api/v3/predictions/${PREDICTION_ID}/result"

# 2. Poll until the prediction finishes.
while true; do
  RESPONSE=$(curl --silent --show-error --fail-with-body \
    "${RESULT_URL}" \
    -H "Authorization: Bearer ${WAVESPEED_API_KEY}")
  RESULT=$(printf '%s' "${RESPONSE}" | jq 'if type == "object" and has("data") then .data else . end')
  STATUS=$(printf '%s' "${RESULT}" | jq -r '.status // empty')

  case "${STATUS}" in
    completed) printf '%s\n' "${RESULT}" | jq '.outputs'; break ;;
    failed|cancelled|timeout|deleted) printf '%s\n' "${RESULT}" | jq . >&2; exit 1 ;;
    *) sleep 2 ;;
  esac
done
```

## Parameters

### Task Submission Parameters

#### Request Parameters

| Parameter                | Type          | Required | Default  | Range                                                                         | Description                                                                                                                                                                                                                                                                                                                     |
| ------------------------ | ------------- | -------- | -------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| prompt                   | string        | Yes      |          | -                                                                             | The positive prompt for the generation.                                                                                                                                                                                                                                                                                         |
| images                   | array<string> | Yes      | -        | 0 ~ 10 items                                                                  | The images to edit. A maximum of 10 reference images can be uploaded.                                                                                                                                                                                                                                                           |
| aspect_ratio             | string        | No       | -        | 1:1, 1:2, 2:1, 1:3, 3:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 9:21, 21:9 | The aspect ratio of the generated image. Leave empty to automatically use the closest supported aspect ratio based on the first input image.                                                                                                                                                                                    |
| resolution               | string        | No       | 1k       | 1k, 1.5k, 2k                                                                  | The output resolution tier used for billing. 1k is the lower-cost tier; 2k is the higher-cost tier.                                                                                                                                                                                                                             |
| output_format            | string        | No       | jpeg     | jpeg, png                                                                     | The format of the output image.                                                                                                                                                                                                                                                                                                 |
| prompt_optimization_mode | string        | No       | standard | standard, fast                                                                | Prompt optimization mode. The model rewrites your prompt before generating. 'standard' uses the full rewrite; 'fast' uses a lighter one that generates several times quicker but follows long or intricate prompts less closely, and is served only by the upstream providers that honour it, so it has less failover depth.    |
| enable_sync_mode         | boolean       | No       | false    | -                                                                             | If set to `true`, the request attempts to wait for the generated result and return outputs in the same response. If the result is not ready within the sync wait window, the API can return a timeout body while the task continues processing. This option is only available via the API and is supported only by some models. |
| enable_base64_output     | boolean       | No       | false    | -                                                                             | If set to `true`, the prediction's `output` strings are returned as **naked base64** (no `data:<mime>;base64,` prefix). When `false` (default), outputs are returned as URLs pointing to our CDN.                                                                                                                               |

#### Response Parameters

| Parameter              | Type    | Description                                                                                                                             |
| ---------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| code                   | integer | HTTP status code (e.g., 200 for success)                                                                                                |
| message                | string  | Status message (e.g., “success”)                                                                                                        |
| data.id                | string  | Unique identifier for the prediction, Task Id                                                                                           |
| data.model             | string  | Model ID used for the prediction                                                                                                        |
| data.outputs           | array   | Output values, usually URL strings; some models return text strings or structured result objects (empty when status is not `completed`) |
| data.urls              | object  | Object containing related API endpoints                                                                                                 |
| data.status            | string  | Task status. `completed` is successful; `failed`, `cancelled`, `timeout`, and `deleted` are failure terminal statuses.                  |
| data.created_at        | string  | ISO timestamp of when the request was created (e.g., “2023-04-01T12:34:56.789Z”)                                                        |
| data.error             | string  | Error message (empty if no error occurred)                                                                                              |
| data.timings           | object  | Object containing timing details                                                                                                        |
| data.timings.inference | integer | Inference time in milliseconds                                                                                                          |

#### Result Request Parameters

| Parameter | Type   | Required | Default | Description |
| --------- | ------ | -------- | ------- | ----------- |
| id        | string | Yes      | -       | Task ID     |

#### Result Response Parameters

| Parameter              | Type                    | Description                                                                                                                                                                   |
| ---------------------- | ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| code                   | integer                 | HTTP status code (e.g., 200 for success)                                                                                                                                      |
| message                | string                  | Status message (e.g., “success”)                                                                                                                                              |
| data                   | object                  | The prediction data object containing all details                                                                                                                             |
| data.id                | string                  | Unique identifier for the prediction                                                                                                                                          |
| data.model             | string                  | Model ID used for the prediction                                                                                                                                              |
| data.outputs           | array<string \| object> | Array of generated outputs (empty when status is not completed). Items are usually URL strings, but may be text strings or structured result objects, depending on the model. |
| data.urls              | object                  | Object containing related API endpoints                                                                                                                                       |
| data.status            | string                  | Status: `completed` is successful; `failed`, `cancelled`, `timeout`, and `deleted` are failure terminal statuses                                                              |
| data.created_at        | string                  | ISO timestamp of when the request was created                                                                                                                                 |
| data.error             | string                  | Error message (empty if no error occurred)                                                                                                                                    |
| data.timings           | object                  | Object containing timing details                                                                                                                                              |
| data.timings.inference | integer                 | Inference time in milliseconds                                                                                                                                                |
