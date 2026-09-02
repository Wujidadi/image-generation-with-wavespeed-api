<!--
來源：https://wavespeed.ai/docs/docs-api/x-ai/x-ai-grok-imagine-image-v2.0-edit
模型頁：https://wavespeed.ai/models/x-ai/grok-imagine-image-v2.0/edit
下載時間：2026-09-02T20:18:29+08:00
說明：由 WaveSpeed 官方文件頁靜態 HTML 轉為 Markdown；Node.js／Python 範例為前端動態渲染，靜態頁僅含 cURL 版本
-->

# X AI Grok Imagine Image V2.0 Edit API Documentation

## Playground

[Try it on WaveSpeedAI!](https://wavespeed.ai/models/x-ai/grok-imagine-image-v2.0/edit)

xAI Grok Imagine Image V2.0 Edit transforms input images with text prompts, with configurable resolution and quality for precise image editing, visual refinements, creative variations, social content, marketing assets, and production workflows. Ready-to-use REST inference API, best performance, no coldstarts, affordable pricing.

## Features

**Grok Imagine Image V2.0 Edit** transforms a source image with natural-language instructions. It is designed for prompt-guided image editing with configurable resolution and quality, making it suitable for creative iteration, visual refinement, and marketing asset updates.

---

## Parameters

| Parameter  | Required | Description                                               |
| ---------- | -------- | --------------------------------------------------------- |
| images     | Yes      | Input image to edit, as an array. At most one image.      |
| prompt     | Yes      | Text instruction describing the desired edit.             |
| resolution | No       | Output resolution: `1k` or `2k`. Default: `2k`.           |
| quality    | No       | Generation quality: `low` or `medium`. Default: `medium`. |

---

## How to Use

1. Upload one source image in the `images` array (at most one).
2. Write a clear edit prompt describing what should change.
3. Choose the output `resolution` and `quality` tier.
4. Submit the request and retrieve the edited image URL.

---

## Pricing

**$0.06 per edit**, regardless of the selected `resolution` and `quality`.

---

### Billing Rules

- Each request accepts exactly **one input image**.
- The listed price already includes the **input-image fee**.

---

## Best Use Cases

- **Prompt-guided image editing** — Transform an existing image with simple natural-language instructions.
- **Style and visual changes** — Adjust mood, color, composition, or overall style.
- **Product and marketing updates** — Refine product shots, campaign assets, and promotional visuals.
- **Creative iteration** — Explore multiple edit directions from the same source image.

---

## Related Models

- [Grok Imagine Image V2.0 Text-to-Image](https://wavespeed.ai/models/x-ai/grok-imagine-image-v2.0/text-to-image) — Generate images from natural-language prompts.
- [Grok Imagine Image V2.0 Edit](https://wavespeed.ai/models/x-ai/grok-imagine-image-v2.0/edit) — Edit images with text instructions.

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
  "images": [
    "https://interactive-examples.mdn.mozilla.net/media/cc0-images/painted-hand-298-332.jpg"
  ],
  "prompt": "A cinematic ocean wave at sunrise, highly detailed",
  "resolution": "2k",
  "quality": "medium"
}
JSON
)

# 1. Submit the prediction.
SUBMIT_RESPONSE=$(curl --silent --show-error --fail-with-body \
  -X POST "https://api.wavespeed.ai/api/v3/x-ai/grok-imagine-image-v2.0/edit" \
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

| Parameter  | Type          | Required | Default | Range       | Description                                                                        |
| ---------- | ------------- | -------- | ------- | ----------- | ---------------------------------------------------------------------------------- |
| images     | array<string> | Yes      | -       | 0 ~ 1 items | Input image to edit. Accepts at most one image. Supports jpg, jpeg, png, and webp. |
| prompt     | string        | Yes      |         | -           | Text instruction describing how to edit the image.                                 |
| resolution | string        | No       | 2k      | 1k, 2k      | Output image resolution tier.                                                      |
| quality    | string        | No       | medium  | low, medium | Generation quality tier.                                                           |

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
