<!--
來源：https://wavespeed.ai/docs/docs-api/bytedance/bytedance-seedream-v5.0-pro
模型頁：https://wavespeed.ai/models/bytedance/seedream-v5.0-pro
下載時間：2026-09-02T21:00:41+08:00
說明：由 WaveSpeed 官方文件頁靜態 HTML 轉為 Markdown；Node.js／Python 範例為前端動態渲染，靜態頁僅含 cURL 版本
-->

# Bytedance Seedream V5.0 Pro API Documentation

## Playground

[Try it on WaveSpeedAI!](https://wavespeed.ai/models/bytedance/seedream-v5.0-pro)

Seedream V5.0 Pro Text to Image by ByteDance generates high-quality images from text prompts, with aspect ratio selection, strong prompt following, and 1K / 2K output tiers for flexible image creation. Ready-to-use REST inference API, best performance, no coldstarts, affordable pricing.

## Features

**Seedream V5.0 Pro** is a multimodal image model built for professional work: high-density infographics, precise composition, photographic realism, and native multilingual text. It supports flexible aspect ratios, multiple resolution tiers, prompt optimization, and standard image output formats for production image workflows.

---

## Why Choose This?

- **Pro image quality**
  Designed for high-quality image generation with strong prompt adherence.
- **Flexible resolution tiers**
  Choose `1k` or `1.5k` for lower-cost generation, or `2k` for higher-resolution output.
- **Flexible aspect ratios**
  Supports square, portrait, landscape, tall, wide, and cinematic aspect ratios.
- **Prompt optimization**
  Use `standard` prompt optimization for fuller prompt rewriting, or `fast` mode for quicker generation with lighter optimization.
- **Standard output formats**
  Generate images in `jpeg` or `png` format.
- **Clean text-to-image workflow**
  Provide a prompt, choose output settings, and generate the final image.

---

## Parameters

| Parameter                | Required | Description                                                                                                                                                                                                                                                                                           |
| ------------------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| prompt                   | Yes      | Positive prompt for the image generation. Describe the subject, scene, style, lighting, composition, and visual details.                                                                                                                                                                              |
| aspect_ratio             | No       | Output aspect ratio. Options: `1:1`, `1:2`, `2:1`, `1:3`, `3:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `9:21`, or `21:9`.                                                                                                                                                         |
| resolution               | No       | Output resolution tier: `1k`, `1.5k`, or `2k`.                                                                                                                                                                                                                                                        |
| output_format            | No       | Output image format: `jpeg` or `png`.                                                                                                                                                                                                                                                                 |
| prompt_optimization_mode | No       | Prompt optimization mode: `standard` (default) or `fast`. The model rewrites your prompt before generating; `fast` uses a lighter rewrite that returns several times quicker but follows long or intricate prompts less closely. Reference time: 14s (`fast`) vs 26s (`standard`) on the same prompt. |

---

## How to Use

1. **Write your prompt** — Describe the subject, scene, style, lighting, composition, and visual details.
2. **Choose aspect ratio** — Select the layout that matches your target format.
3. **Choose resolution** — Use `1k` or `1.5k` for lower-cost drafts, or `2k` for higher-resolution output.
4. **Choose output format** — Select `jpeg` or `png`.
5. **Set prompt optimization optional** — Use `standard` for fuller prompt rewriting or `fast` for quicker generation with lighter optimization.
6. **Submit** — Generate the final image.

---

## Pricing

Pricing is based on selected `resolution`.

| Resolution | Cost   |
| ---------- | ------ |
| 1k         | $0.045 |
| 1.5k       | $0.045 |
| 2k         | $0.090 |

---

## Best Use Cases

- **High-quality image generation** — Create polished images from detailed text prompts.
- **Marketing visuals** — Generate campaign assets, social media graphics, and promotional images.
- **Creative concepting** — Explore characters, environments, products, and visual styles.
- **Layout-specific assets** — Generate square, portrait, landscape, tall, wide, or cinematic images.
- **Production image workflows** — Use `2k` when higher-resolution output is needed.
- **Fast visual iteration** — Use `fast` prompt optimization when speed matters more than detailed prompt rewriting.

---

## Pro Tips

- Use `prompt_optimization_mode: fast` for quick iterations and `standard` for the final image; the difference is a few seconds versus tens of seconds on the same prompt.
- Use detailed prompts with subject, composition, lighting, style, mood, and background details.
- Choose `1k` or `1.5k` for faster and lower-cost prompt iteration.
- Choose `2k` when you need higher-resolution final images.
- Use `9:16` for vertical mobile content and `16:9` for widescreen layouts.
- Use `jpeg` for general-purpose images and `png` when PNG output is needed.
- Use `standard` prompt optimization for complex or detailed prompts.
- Use `fast` prompt optimization when you want quicker generation and lighter prompt rewriting.
- Keep prompts clear and focused for stronger prompt adherence.

---

## Related Models

- [Seedream V5.0 Pro Edit](https://wavespeed.ai/models/bytedance/seedream-v5.0-pro/edit) — Edit images with text instructions.
- [Seedream V5.0 Lite](https://wavespeed.ai/models/bytedance/seedream-v5.0-lite) — Lightweight image generation model.

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
  "aspect_ratio": "1:1",
  "resolution": "1k",
  "output_format": "jpeg",
  "prompt_optimization_mode": "standard"
}
JSON
)

# 1. Submit the prediction.
SUBMIT_RESPONSE=$(curl --silent --show-error --fail-with-body \
  -X POST "https://api.wavespeed.ai/api/v3/bytedance/seedream-v5.0-pro" \
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

| Parameter                | Type    | Required | Default  | Range                                                                         | Description                                                                                                                                                                                                                                                                                                                     |
| ------------------------ | ------- | -------- | -------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| prompt                   | string  | Yes      |          | -                                                                             | The positive prompt for the generation.                                                                                                                                                                                                                                                                                         |
| aspect_ratio             | string  | No       | 1:1      | 1:1, 1:2, 2:1, 1:3, 3:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 9:21, 21:9 | The aspect ratio of the generated image.                                                                                                                                                                                                                                                                                        |
| resolution               | string  | No       | 1k       | 1k, 1.5k, 2k                                                                  | The output resolution tier used for billing. 1k is the lower-cost tier; 2k is the higher-cost tier.                                                                                                                                                                                                                             |
| output_format            | string  | No       | jpeg     | jpeg, png                                                                     | The format of the output image.                                                                                                                                                                                                                                                                                                 |
| prompt_optimization_mode | string  | No       | standard | standard, fast                                                                | Prompt optimization mode. The model rewrites your prompt before generating. 'standard' uses the full rewrite; 'fast' uses a lighter one that generates several times quicker but follows long or intricate prompts less closely, and is served only by the upstream providers that honour it, so it has less failover depth.    |
| enable_sync_mode         | boolean | No       | false    | -                                                                             | If set to `true`, the request attempts to wait for the generated result and return outputs in the same response. If the result is not ready within the sync wait window, the API can return a timeout body while the task continues processing. This option is only available via the API and is supported only by some models. |
| enable_base64_output     | boolean | No       | false    | -                                                                             | If set to `true`, the prediction's `output` strings are returned as **naked base64** (no `data:<mime>;base64,` prefix). When `false` (default), outputs are returned as URLs pointing to our CDN.                                                                                                                               |

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
