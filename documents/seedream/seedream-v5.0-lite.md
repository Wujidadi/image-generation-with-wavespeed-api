<!--
來源：https://wavespeed.ai/docs/docs-api/bytedance/bytedance-seedream-v5.0-lite
模型頁：https://wavespeed.ai/models/bytedance/seedream-v5.0-lite
下載時間：2026-09-02T21:00:41+08:00
說明：由 WaveSpeed 官方文件頁靜態 HTML 轉為 Markdown；Node.js／Python 範例為前端動態渲染，靜態頁僅含 cURL 版本
-->

# Bytedance Seedream V5.0 Lite API Documentation

## Playground

[Try it on WaveSpeedAI!](https://wavespeed.ai/models/bytedance/seedream-v5.0-lite)

Seedream 5.0 Lite by is a state-of-the-art text-to-image model with enhanced typography, clear text rendering for posters and brand visuals, superior prompt adherence, and up to 4K resolution. Ready-to-use REST inference API, best performance, no coldstarts, affordable pricing.

## Features

**Seedream V5.0 Lite** is lightweight text-to-image model, generating high-quality images from text descriptions with fast inference speed. With flexible aspect ratios and custom resolution support up to 4K, it delivers stunning visuals at an affordable price.

---

## Why Choose This?

- **Lightweight & fast**
  Optimized for speed while maintaining high visual quality.
- **Flexible aspect ratios**
  Multiple presets including 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, and 2:3.
- **High resolution support**
  Custom width and height from 1440 to 8192 pixels.
- **Prompt Enhancer**
  Built-in tool to automatically improve your descriptions for better results.
- **Affordable pricing**
  Just $0.035 per image for professional-quality output.

---

## Parameters

| Parameter | Required | Description                                              |
| --------- | -------- | -------------------------------------------------------- |
| prompt    | Yes      | Text description of the desired image                    |
| size      | No       | Aspect ratio preset: 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3 |
| width     | No       | Custom width in pixels (range: 1440–8192)                |
| height    | No       | Custom height in pixels (range: 1440–8192)               |

---

## How to Use

1. **Write your prompt** — describe the image in detail, including style, lighting, and composition.
2. **Choose aspect ratio** — select a preset or customize width/height.
3. **Use Prompt Enhancer (optional)** — click to automatically refine your description.
4. **Run** — submit and download your generated image.

---

## Pricing

| Output    | Cost   |
| --------- | ------ |
| Per image | $0.035 |

---

## Best Use Cases

- **Social Media Content** — Create eye-catching visuals for Instagram, TikTok, and more.
- **Photography Style** — Generate photorealistic images with camera and lighting references.
- **Marketing & Ads** — Produce professional images for campaigns and promotions.
- **Concept Art** — Visualize ideas and creative concepts quickly.
- **Personal Projects** — Bring your creative visions to life affordably.

---

## Pro Tips

- Be specific in your prompts — include camera settings, lighting, and style references for best results.
- Use cinematic language like “shot on Leica, golden hour, urban backdrop” for photorealistic output.
- Try the Prompt Enhancer to automatically improve your descriptions.
- Match aspect ratio to your target platform: 9:16 for Stories/Reels, 16:9 for banners, 1:1 for feeds.
- Lite version is great for quick iterations and high-volume generation.

---

## Notes

- Prompt is the only required field.
- Resolution range: 1440–8192 pixels for both width and height.
- Ensure your prompts comply with content guidelines.

---

## Related Models

- [Seedream V5.0 Lite Edit](https://wavespeed.ai/models/bytedance/seedream-v5.0-lite/edit) — Edit images with text instructions.
- [Seedream V4 Text-to-Image](https://wavespeed.ai/models/bytedance/seedream-v4) — Previous generation model.

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
  "output_format": "jpeg"
}
JSON
)

# 1. Submit the prediction.
SUBMIT_RESPONSE=$(curl --silent --show-error --fail-with-body \
  -X POST "https://api.wavespeed.ai/api/v3/bytedance/seedream-v5.0-lite" \
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

| Parameter            | Type    | Required | Default    | Range       | Description                                                                                                                                                                                                                                                                                                                     |
| -------------------- | ------- | -------- | ---------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| prompt               | string  | Yes      |            | -           | The positive prompt for the generation.                                                                                                                                                                                                                                                                                         |
| size                 | string  | No       | 2048\*2048 | 1440 ~ 8192 | Specify the width and height pixel values of the generated image.Total pixel value range: [2560\*1440, 4096\*4096]                                                                                                                                                                                                              |
| output_format        | string  | No       | -          | jpeg, png   | The format of the output image.                                                                                                                                                                                                                                                                                                 |
| enable_base64_output | boolean | No       | false      | -           | If set to `true`, the prediction's `output` strings are returned as **naked base64** (no `data:<mime>;base64,` prefix). When `false` (default), outputs are returned as URLs pointing to our CDN.                                                                                                                               |
| enable_sync_mode     | boolean | No       | false      | -           | If set to `true`, the request attempts to wait for the generated result and return outputs in the same response. If the result is not ready within the sync wait window, the API can return a timeout body while the task continues processing. This option is only available via the API and is supported only by some models. |

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
