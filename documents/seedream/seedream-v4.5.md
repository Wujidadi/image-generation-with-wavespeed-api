<!--
來源：https://wavespeed.ai/docs/docs-api/bytedance/bytedance-seedream-v4.5
模型頁：https://wavespeed.ai/models/bytedance/seedream-v4.5
下載時間：2026-09-02T21:00:41+08:00
說明：由 WaveSpeed 官方文件頁靜態 HTML 轉為 Markdown；Node.js／Python 範例為前端動態渲染，靜態頁僅含 cURL 版本
-->

# Bytedance Seedream V4.5 API Documentation

## Playground

[Try it on WaveSpeedAI!](https://wavespeed.ai/models/bytedance/seedream-v4.5)

Seedream 4.5 is a next-gen text-to-image model optimized for typography—crisper text rendering, stronger prompt adherence, and up to 4K output for posters and brand visuals. Ready-to-use REST inference API, best performance, no cold starts, affordable pricing.

## Features

**Seedream 4.5** is ’s latest high-resolution image generation model, upgraded through large-scale training and architecture refinement. It is especially strong at **typography, poster composition, and branded visuals**, with clear text rendering and strong prompt adherence.

---

## Model highlights

- **Enhanced typography** – Renders sharp, legible text for posters, logos, UI, and marketing layouts.
- **Designer-level composition** – Handles complex poster-style layouts with clear hierarchy (title, subtitle, body text, logos).
- **Strong prompt adherence** – Closely follows detailed descriptions for subjects, layout, and style.
- **High-resolution output** – Supports custom width/height with total pixel count from **2560×1440 up to 8192×8192**.
- **Aesthetic quality** – Benchmarked with strong performance on MagicBench and other visual quality suites.

---

## Recommended use cases

- Poster, banner, and KV design with embedded text
- Brand visual, logo, and campaign asset creation
- E-commerce product imagery and hero shots
- Social media graphics where typography is part of the design
- Presentation, landing-page, and in-app visuals

---

## Pricing

- **$0.04 per generated image**

---

## How to use

1. **Enter your prompt**
   Describe the subject, composition, text elements (e.g., title / subtitle / tagline), and overall style.
2. **Set `size` (width & height)**
   Choose pixel dimensions for your image. The model supports custom sizes as long as
   the total pixel count is within **2560×1440 ≤ width × height ≤ 8192×8192**.
3. **Run the job**
   Click **Run** to generate the image, then refine your prompt or size for the next iteration.

---

## Suggested resolutions

Below are example resolutions that work well in practice and stay within the supported pixel range:

| Aspect Ratio | Suggested Resolution (W × H) |
| ------------ | ---------------------------- |
| 1:1          | 2048 × 2048                  |
| 4:3          | 2688 × 2016                  |
| 3:2          | 2688 × 1792                  |
| 16:9         | 2560 × 1440                  |
| Square 4K    | 8192 × 8192                  |

You can freely adjust width and height as long as they respect the total pixel range.

---

## Notes

- For **text-heavy posters**, slightly higher resolutions (e.g. 2048×2048 or above) give noticeably cleaner typography.
- Keep logos and key text **explicitly described** (e.g. “white all-caps title at the top, small gray subtitle below”).
- If you are using an **image URL**, make sure it is publicly accessible so the system can retrieve it.

---

## Model Comparison on WaveSpeedAI

Use Seedream 4.5 together with other models, depending on your priorities:

- [google/nano-banana-pro/text-to-image](https://wavespeed.ai/models/google/nano-banana-pro/text-to-image) – Google’s **Nano Banana Pro** (Gemini 3.0 Pro Image family) is ideal for **ultra-low cost, multi-image generation**, great for large batches and exploratory runs.
- [Tongyi-MAI/Z-Image-Turbo](https://wavespeed.ai/models/wavespeed-ai/z-image/turbo) (available as Z-Image on WaveSpeedAI) – Tongyi-MAI’s **6B, 8-step turbo model** focuses on **maximum speed and throughput** while keeping photorealism and bilingual (EN/ZH) support.
- [wavespeed-ai/flux-2-pro/text-to-image](https://wavespeed.ai/models/wavespeed-ai/flux-2-pro/text-to-image) – FLUX.2 [pro] is a **flagship, general-purpose** model for cinematic quality and complex scenes, great when you need broad stylistic range beyond typography-heavy posters.
- [/seedream-v4](https://wavespeed.ai/models/bytedance/seedream-v4) – The previous Seedream generation, strong at **high-resolution illustration and diverse styles**; Seedream 4.5 builds on it with noticeably better **text rendering and layout control** for branding work.

**Rule of thumb:**

- Choose **Seedream 4.5** for **posters, brand layouts, and any text-heavy creative**.
- Choose **Nano Banana Pro** or **Z-Image-Turbo** for **fast, cheap, large-scale image batches**.
- Choose **FLUX.2 [pro]** for **cinematic, style-flexible hero shots**.
- Choose **Seedream V4** when you want its familiar look or need variety across illustration styles.

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
  "size": "2048*2048"
}
JSON
)

# 1. Submit the prediction.
SUBMIT_RESPONSE=$(curl --silent --show-error --fail-with-body \
  -X POST "https://api.wavespeed.ai/api/v3/bytedance/seedream-v4.5" \
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
