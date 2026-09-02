<!--
來源：https://wavespeed.ai/docs/docs-api/bytedance/bytedance-seedream-v5.0-lite-sequential
模型頁：https://wavespeed.ai/models/bytedance/seedream-v5.0-lite/sequential
下載時間：2026-09-02T21:05:05+08:00
說明：由 WaveSpeed 官方文件頁靜態 HTML 轉為 Markdown；Node.js／Python 範例為前端動態渲染，靜態頁僅含 cURL 版本
-->

# Bytedance Seedream V5.0 Lite Sequential API Documentation

## Playground

[Try it on WaveSpeedAI!](https://wavespeed.ai/models/bytedance/seedream-v5.0-lite/sequential)

Seedream 5.0 Lite Sequential generates multi-image sets with consistent characters and objects, unifying palette, lighting, and style across all outputs. Supports up to 4K results for campaigns, storyboards, and product lines. Ready-to-use REST inference API, best performance, no coldstarts, affordable pricing.

## Features

**Seedream V5.0 Lite Sequential** is multi-image text-to-image model designed to generate **a series of coherent images from a single prompt**. Describe multiple scenes in one prompt — the model generates a consistent visual sequence with stable character identity and style continuity, perfect for storytelling, storyboards, and visual narratives.

---

## Why Choose This?

- **Multi-image generation**
  Generate multiple related images in a single run with consistent style and characters.
- **Character consistency**
  Maintains character identity, proportions, and visual style across the entire sequence.
- **Narrative storytelling**
  Create visual stories by describing multiple scenes in one prompt.
- **High resolution support**
  Custom width and height from 1440 to 8192 pixels.
- **Flexible aspect ratios**
  Multiple presets including 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, and 2:3.
- **Prompt Enhancer**
  Built-in tool to automatically improve your descriptions.

---

## Parameters

| Parameter  | Required | Description                                               |
| ---------- | -------- | --------------------------------------------------------- |
| prompt     | Yes      | Describe the images to generate (include count in prompt) |
| size       | No       | Aspect ratio preset: 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3  |
| width      | No       | Custom width in pixels (range: 1440–8192)                 |
| height     | No       | Custom height in pixels (range: 1440–8192)                |
| max_images | No       | Number of images to generate (default: 2)                 |

---

## How to Use

1. **Set max_images first** — specify how many images you want to generate.
2. **Write your prompt** — describe each image in sequence, starting with the count.
3. **Choose size** — select a preset or customize width/height.
4. **Use Prompt Enhancer (optional)** — click to automatically refine your description.
5. **Run** — submit and download your image sequence.

**Important:** Specify the number of images in your prompt to match max_images!

Example prompt format:

- max_images = 2
- Prompt: “2 images. First, a young princess in a torn royal dress sneaking through a dark castle corridor… Second, the princess and the cloaked figure riding together on horseback at dawn…”

---

## Pricing

| max_images | Total Price |
| ---------- | ----------- |
| 1          | $0.035      |
| 2          | $0.07       |
| 4          | $0.14       |
| 8          | $0.28       |

### Billing Rules

- **Base price:** $0.035 per output image
- **Total cost** = $0.035 × max_images

---

## Best Use Cases

- **Visual Storytelling** — Create sequential narratives with consistent characters.
- **Storyboards** — Generate scene-by-scene illustrations for projects.
- **Comic & Manga** — Produce multi-panel visual sequences.
- **Character Series** — Generate variations of the same character in different scenarios.
- **Marketing Campaigns** — Create cohesive visual series for brand storytelling.
- **Social Media Content** — Produce carousel posts with narrative continuity.

---

## Pro Tips

- Always specify the number of images at the start of your prompt (e.g., “2 images. First… Second…”).
- Use “First,” “Second,” “Third,” etc. to clearly separate each image description.
- Include consistent character descriptions across scenes for better identity preservation.
- Keep style references consistent throughout the prompt (e.g., “fantasy art, cinematic” for all scenes).
- Start with fewer images (2–4) to test consistency before generating larger sequences.

---

## Notes

- Prompt is the only required field.
- Always match max_images setting with the number specified in your prompt.
- Resolution range: 1440–8192 pixels for both width and height.
- Ensure your prompts comply with content guidelines.

---

## Related Models

- [Seedream V5.0 Lite Edit Sequential](https://wavespeed.ai/models/bytedance/seedream-v5.0-lite/edit-sequential) — Multi-image editing with consistent identity.
- [Seedream V5.0 Lite Text-to-Image](https://wavespeed.ai/models/bytedance/seedream-v5.0-lite) — Single image generation.
- [Seedream V5.0 Lite Edit](https://wavespeed.ai/models/bytedance/seedream-v5.0-lite/edit) — Single-image editing with style transfer.

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
  "max_images": 1,
  "output_format": "jpeg"
}
JSON
)

# 1. Submit the prediction.
SUBMIT_RESPONSE=$(curl --silent --show-error --fail-with-body \
  -X POST "https://api.wavespeed.ai/api/v3/bytedance/seedream-v5.0-lite/sequential" \
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
| max_images           | integer | No       | 1          | 1 ~ 15      | The maximum number of images that can be generated (up to 15). This value must align with the number of images specified in the prompt above.                                                                                                                                                                                   |
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
