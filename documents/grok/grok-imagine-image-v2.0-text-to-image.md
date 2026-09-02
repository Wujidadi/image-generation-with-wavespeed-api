<!--
來源：https://wavespeed.ai/docs/docs-api/x-ai/x-ai-grok-imagine-image-v2.0-text-to-image
模型頁：https://wavespeed.ai/models/x-ai/grok-imagine-image-v2.0/text-to-image
下載時間：2026-09-02T20:18:29+08:00
說明：由 WaveSpeed 官方文件頁靜態 HTML 轉為 Markdown；Node.js／Python 範例為前端動態渲染，靜態頁僅含 cURL 版本
-->

# X AI Grok Imagine Image V2.0 Text To Image API Documentation

## Playground

[Try it on WaveSpeedAI!](https://wavespeed.ai/models/x-ai/grok-imagine-image-v2.0/text-to-image)

xAI Grok Imagine Image V2.0 Text-to-Image generates high-quality images from text prompts, with configurable aspect ratio, resolution, and quality for creative visuals, social content, marketing assets, and production workflows. Ready-to-use REST inference API, best performance, no coldstarts, affordable pricing.

## Features

**Grok Imagine Image V2.0 Text-to-Image** generates high-quality images from natural-language prompts with configurable aspect ratio, resolution, and quality settings. It is well suited for creative generation, visual ideation, and production-ready image workflows.

---

## Parameters

| Parameter    | Required | Description                                               |
| ------------ | -------- | --------------------------------------------------------- |
| prompt       | Yes      | Text description of the image to generate.                |
| aspect_ratio | No       | Output aspect ratio. Default: `1:1`.                      |
| resolution   | No       | Output resolution: `1k` or `2k`. Default: `2k`.           |
| quality      | No       | Generation quality: `low` or `medium`. Default: `medium`. |

---

## How to Use

1. Write a clear prompt describing the subject, composition, lighting, style, and any important visual details.
2. Choose an aspect ratio that fits your target layout.
3. Select the output `resolution` and `quality` tier.
4. Submit the request and retrieve the generated image URL.

---

## Pricing

**$0.05 per generated image**, regardless of the selected `resolution` and `quality`. One image is generated per request.

---

## Best Use Cases

- Creative image generation
- Marketing and social media visuals
- Concept art and visual ideation
- Portrait, product, and scene generation
- Fast iteration across quality and resolution tiers

---

## Pro Tips

- Use detailed prompts for stronger composition and subject control.
- Choose `1k` for faster iteration.
- Choose `2k` when you need higher-resolution final output.
- Use `medium` quality for more polished results.
- Be specific about lighting, background, camera angle, and style when consistency matters.

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
  "prompt": "A cinematic ocean wave at sunrise, highly detailed",
  "aspect_ratio": "1:1",
  "resolution": "2k",
  "quality": "medium"
}
JSON
)

# 1. Submit the prediction.
SUBMIT_RESPONSE=$(curl --silent --show-error --fail-with-body \
  -X POST "https://api.wavespeed.ai/api/v3/x-ai/grok-imagine-image-v2.0/text-to-image" \
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

| Parameter    | Type   | Required | Default | Range                                                                     | Description                                |
| ------------ | ------ | -------- | ------- | ------------------------------------------------------------------------- | ------------------------------------------ |
| prompt       | string | Yes      |         | -                                                                         | Text description of the image to generate. |
| aspect_ratio | string | No       | 1:1     | 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 2:1, 1:2, 19.5:9, 9:19.5, 20:9, 9:20 | Aspect ratio of the generated image.       |
| resolution   | string | No       | 2k      | 1k, 2k                                                                    | Output image resolution tier.              |
| quality      | string | No       | medium  | low, medium                                                               | Generation quality tier.                   |

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
