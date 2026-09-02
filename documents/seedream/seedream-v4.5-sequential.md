<!--
來源：https://wavespeed.ai/docs/docs-api/bytedance/bytedance-seedream-v4.5-sequential
模型頁：https://wavespeed.ai/models/bytedance/seedream-v4.5/sequential
下載時間：2026-09-02T21:05:05+08:00
說明：由 WaveSpeed 官方文件頁靜態 HTML 轉為 Markdown；Node.js／Python 範例為前端動態渲染，靜態頁僅含 cURL 版本
-->

# Bytedance Seedream V4.5 Sequential API Documentation

## Playground

[Try it on WaveSpeedAI!](https://wavespeed.ai/models/bytedance/seedream-v4.5/sequential)

Seedream 4.5 Sequential generates multi-image sets with consistent characters and objects, unifying palette, lighting, and style across all outputs. Supports up to 4K results for campaigns, storyboards, and product lines. Ready-to-use REST inference API, best performance, no cold starts, affordable pricing.

## Features

**Seedream 4.5 Sequential** is ’s multi-image generation model for creating **whole series of images in one go**. It keeps characters, props, and style consistent across all outputs, making it ideal for KVs, comic panels, and any visual set that should “look like one universe”.

---

## Model highlights

- **Character consistency** – Locks onto the same character identity (face, hairstyle, body shape) across all generated frames.
- **Object & prop stability** – Reuses key objects (products, logos, props) so they don’t randomly change between images.
- **Unified visual style** – Maintains palette, lighting, camera feel, and rendering style across the whole set.
- **Multi-image output** – Generate several images in a single request, all driven by the same prompt.
- **4K-ready detail** – Supports resolutions up to **8192 × 8192** per image for hero KVs and print-adjacent work.
- **Typography aware** – Strong on-image text rendering for branded content, titles, and UI-like elements.

---

## Best suited for

- Comic strips and story panels with recurring characters
- Brand KV series and campaign sets built around the same hero figure
- Product lineup / colourway visualisation
- Storyboard or animatic keyframes
- Social media content series that must feel coherent in the grid
- Multi-step marketing journeys (awareness → consideration → conversion visuals)

---

## Pricing

Billing is **per generated image**, controlled by **max_images**.

- **$0.04 per image**
- **Formula:** `total_price = $0.04 × max_images`

Example costs:

| max_images | Total price |
| ---------- | ----------- |
| 1          | **$0.04**   |
| 4          | **$0.16**   |
| 8          | **$0.32**   |

The exact price for your chosen settings is always shown in the WaveSpeedAI interface before you run the job.

---

## How to use

1. **Enter your prompt**
   Describe the scene, characters, and what must stay consistent, e.g.
   “Same girl with red hoodie and headphones, different city locations, cinematic lighting.”
2. **Set **max_images\*\*\*\*
   Choose how many images you want in the series. Each one will follow the same prompt and consistency logic.
3. **Set **size\***\*
   Choose width and height, up to **8192 × 8192\*\* for maximum detail.
4. **Run and review**
   Generate the series, check continuity across faces, outfits, and props, then refine the prompt for another pass if needed.

---

## Notes

- Please set the **max_image** first, and then input **how many images** you want to generate in prompt! Such as:
- max_image = 4.

_Prompt: I want to generate 4 images… + (your prompt)_

---

## Model comparison & related tools

- **[Nano Banana Pro](https://wavespeed.ai/models/google/nano-banana-pro/text-to-image)**
  Google’s ultra-low-cost, high-throughput T2I model. Great for **lots of individual images or quick ideation**, but it doesn’t provide built-in cross-image character locking.
- **[Seedream V4 – sequential](https://wavespeed.ai/models/bytedance/seedream-v4/sequential)**
  ’s single-image Seedream generator with rich detail and stylish output. Ideal when you want **one-off hero shots** or standalone illustrations rather than a strictly consistent series.
- **[Qwen Image Edit Plus](https://wavespeed.ai/models/wavespeed-ai/qwen-image/text-to-image)**
  Qwen-Image is a 20B MMDiT-based text-to-image generation model, especially strong at native text rendering in both **English and Chinese**. It is a powerful creative tool for posters, comics, and visual storytelling, while also excelling at general image generation from photorealism to anime.

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
  "size": "2048*2048",
  "max_images": 1
}
JSON
)

# 1. Submit the prediction.
SUBMIT_RESPONSE=$(curl --silent --show-error --fail-with-body \
  -X POST "https://api.wavespeed.ai/api/v3/bytedance/seedream-v4.5/sequential" \
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

| Parameter            | Type    | Required | Default    | Range      | Description                                                                                                                                                                                                                                                                                                                     |
| -------------------- | ------- | -------- | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| prompt               | string  | Yes      |            | -          | The positive prompt for the generation.                                                                                                                                                                                                                                                                                         |
| size                 | string  | No       | 2048\*2048 | 512 ~ 8192 | Specify the width and height pixel values of the generated image.                                                                                                                                                                                                                                                               |
| max_images           | integer | No       | 1          | 1 ~ 15     | The maximum number of images that can be generated (up to 15). This value must align with the number of images specified in the prompt above.                                                                                                                                                                                   |
| enable_base64_output | boolean | No       | false      | -          | If set to `true`, the prediction's `output` strings are returned as **naked base64** (no `data:<mime>;base64,` prefix). When `false` (default), outputs are returned as URLs pointing to our CDN.                                                                                                                               |
| enable_sync_mode     | boolean | No       | false      | -          | If set to `true`, the request attempts to wait for the generated result and return outputs in the same response. If the result is not ready within the sync wait window, the API can return a timeout body while the task continues processing. This option is only available via the API and is supported only by some models. |

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
