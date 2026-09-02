<!--
來源：https://wavespeed.ai/docs/docs-api/bytedance/bytedance-seedream-v5.0-lite-edit
模型頁：https://wavespeed.ai/models/bytedance/seedream-v5.0-lite/edit
下載時間：2026-09-02T21:05:05+08:00
說明：由 WaveSpeed 官方文件頁靜態 HTML 轉為 Markdown；Node.js／Python 範例為前端動態渲染，靜態頁僅含 cURL 版本
-->

# Bytedance Seedream V5.0 Lite Edit API Documentation

## Playground

[Try it on WaveSpeedAI!](https://wavespeed.ai/models/bytedance/seedream-v5.0-lite/edit)

Seedream 5.0 Lite Edit by is a state-of-the-art image editing model preserving facial features, lighting, and color tones from reference images. Features high-fidelity editing with professional quality, superior prompt adherence, and up to 4K resolution. Ready-to-use REST inference API, best performance, no coldstarts, affordable pricing.

## Features

**Seedream V5.0 Lite Edit** is lightweight image editing model, enabling creative transformations and style transfers using reference images and text prompts. Upload reference images and describe the desired edit — the model generates stunning results while preserving identity and key features.

---

## Why Choose This?

- **Multi-image reference**
  Use multiple reference images for complex edits and compositions.
- **Natural language editing**
  Describe your edit in plain text — reference images by Figure number for precise control.
- **Style transfer**
  Transform subjects into different aesthetics like cyberpunk, anime, fantasy, and more.
- **Lightweight & fast**
  Lite version optimized for speed while maintaining quality.
- **Prompt Enhancer**
  Built-in tool to automatically improve your edit descriptions.
- **Flexible sizing**
  Specify custom output size, or leave blank to match the reference image.

---

## Parameters

| Parameter | Required | Description                                                                           |
| --------- | -------- | ------------------------------------------------------------------------------------- |
| prompt    | Yes      | Text description of the desired edit (use “Figure 1”, “Figure 2” to reference images) |
| images    | Yes      | Reference images for the edit (click ”+ Add Item” to add more)                        |
| size      | No       | Output size; if empty, matches the reference image’s aspect ratio                     |

---

## How to Use

1. **Upload reference images** — add images containing subjects or elements for your edit.
2. **Write your prompt** — describe the transformation, using “Figure 1”, “Figure 2” to reference specific images.
3. **Set size (optional)** — specify output dimensions, or leave blank for default.
4. **Use Prompt Enhancer (optional)** — click to automatically refine your description.
5. **Run** — submit and download your edited image.

---

## Pricing

| Output    | Cost   |
| --------- | ------ |
| Per image | $0.035 |

---

## Best Use Cases

- **Style Transfer** — Transform portraits into cyberpunk, anime, fantasy, or artistic styles.
- **Character Reimagining** — Place subjects in new environments or scenarios.
- **Creative Compositing** — Combine elements from multiple references.
- **Concept Art** — Generate stylized versions of existing images.
- **Social Media Content** — Create eye-catching edits for posts and profiles.

---

## Pro Tips

- Use “Figure 1”, “Figure 2”, etc. in your prompt to reference images in upload order.
- Be specific about the style you want — include lighting, aesthetic, and mood details.
- Clear, front-facing portraits produce the best identity preservation.
- Try the Prompt Enhancer for more detailed and effective descriptions.
- Lite version is great for quick iterations before using the full model.

---

## Notes

- Both prompt and images are required fields.
- Ensure uploaded image URLs are publicly accessible.
- Output size defaults to reference image’s aspect ratio if not specified.

---

## Related Models

- [Seedream V5.0 Lite Text-to-Image](https://wavespeed.ai/models/bytedance/seedream-v5.0-lite) — Generate images from text prompts.
- [Seedream V4 Text-to-Image](https://wavespeed.ai/models/bytedance/seedream-v4) — Previous generation text-to-image.

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
  "output_format": "jpeg"
}
JSON
)

# 1. Submit the prediction.
SUBMIT_RESPONSE=$(curl --silent --show-error --fail-with-body \
  -X POST "https://api.wavespeed.ai/api/v3/bytedance/seedream-v5.0-lite/edit" \
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

| Parameter            | Type          | Required | Default | Range        | Description                                                                                                                                                                                                                                                                                                                     |
| -------------------- | ------------- | -------- | ------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| prompt               | string        | Yes      |         | -            | The positive prompt for the generation.                                                                                                                                                                                                                                                                                         |
| images               | array<string> | Yes      | -       | 0 ~ 10 items | The images to edit. A maximum of 10 reference images can be uploaded.                                                                                                                                                                                                                                                           |
| output_format        | string        | No       | -       | jpeg, png    | The format of the output image.                                                                                                                                                                                                                                                                                                 |
| enable_sync_mode     | boolean       | No       | false   | -            | If set to `true`, the request attempts to wait for the generated result and return outputs in the same response. If the result is not ready within the sync wait window, the API can return a timeout body while the task continues processing. This option is only available via the API and is supported only by some models. |
| enable_base64_output | boolean       | No       | false   | -            | If set to `true`, the prediction's `output` strings are returned as **naked base64** (no `data:<mime>;base64,` prefix). When `false` (default), outputs are returned as URLs pointing to our CDN.                                                                                                                               |

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
