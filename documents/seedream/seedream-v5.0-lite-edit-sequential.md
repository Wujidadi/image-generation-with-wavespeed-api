<!--
來源：https://wavespeed.ai/docs/docs-api/bytedance/bytedance-seedream-v5.0-lite-edit-sequential
模型頁：https://wavespeed.ai/models/bytedance/seedream-v5.0-lite/edit-sequential
下載時間：2026-09-02T21:05:05+08:00
說明：由 WaveSpeed 官方文件頁靜態 HTML 轉為 Markdown；Node.js／Python 範例為前端動態渲染，靜態頁僅含 cURL 版本
-->

# Bytedance Seedream V5.0 Lite Edit Sequential API Documentation

## Playground

[Try it on WaveSpeedAI!](https://wavespeed.ai/models/bytedance/seedream-v5.0-lite/edit-sequential)

Seedream 5.0 Lite Edit Sequential performs multi-image editing while locking character and object identity across shots. It detects main subjects, preserves continuity, and applies controlled edits with up to 4K output. Ready-to-use REST inference API, best performance, no coldstarts, affordable pricing.

## Features

**Seedream V5.0 Lite Edit Sequential** is multi-image editing model designed to apply **the same edit across a whole set of images** or generate **multiple style variations from a single image**. It automatically tracks the main subject, keeps identity stable, and generates clean, high-resolution results — ideal for campaigns, product sets, and character line-ups.

---

## Why Choose This?

- **Multi-image subject tracking**
  Detects the main subject across all input images and treats them as the same person or object.
- **Character consistency lock**
  Preserves facial structure, proportions, and overall identity across every edited output.
- **High reference fidelity**
  Maintains lighting, color balance, and key visual details while applying the requested changes.
- **Controlled, repeatable edits**
  One prompt drives a consistent transformation across the entire batch.
- **Multiple variations**
  Generate multiple style variations from a single source image.
- **Prompt Enhancer**
  Built-in tool to automatically improve your edit descriptions.

---

## Parameters

| Parameter            | Required | Description                                               |
| -------------------- | -------- | --------------------------------------------------------- |
| prompt               | Yes      | Describe the edit and specify how many images to generate |
| images               | Yes      | Source images to edit (max: 10 images)                    |
| size                 | No       | Output size (click + to expand options)                   |
| max_images           | No       | Number of images to generate (max: 15, default: 2)        |
| enable_base64_output | No       | Return base64 instead of URL (API only)                   |
| enable_sync_mode     | No       | Wait for result in response (API only)                    |

---

## How to Use

1. **Upload source images** — add up to 10 images containing the same main subject or product.
2. **Set max_images first** — specify how many edited outputs you want to generate.
3. **Write the edit prompt** — describe the shared change and include the number of images in your prompt.
4. **Choose size (optional)** — select the target resolution.
5. **Run** — submit the job and review the edited series.

**Important:** Set max_images first, then specify the same number in your prompt!

Example prompt format:

- max_images = 4
- Prompt: “I want to generate 4 images. First, transform into Japanese manga style… Second, transform into cyberpunk neon style…”

---

## Pricing

| max_images | Total Price |
| ---------- | ----------- |
| 1          | $0.035      |
| 2          | $0.07       |
| 4          | $0.14       |
| 8          | $0.28       |
| 15         | $0.525      |

### Billing Rules

- **Base price:** $0.035 per output image
- **Total cost** = $0.035 × max_images

---

## Best Use Cases

- **Batch Portrait Editing** — Apply a fixed style or look across multiple portraits.
- **Product Series** — Create coherent product images that feel like one set.
- **Brand Campaigns** — Iterate on the same model or hero product with different styles.
- **Character Design** — Generate variations in outfits, moods, or lighting.
- **E-commerce Catalogs** — Refresh seasonal updates with consistent styling.
- **Social Media Series** — Create visual series where continuity matters.

---

## Pro Tips

- Use **clear, global instructions** in the prompt (“add winter outfit and snow ambience”) rather than per-image directions.
- Keep input images **reasonably consistent** in framing and lighting so the model can lock onto the same subject.
- Put your **cleanest, clearest reference image first** — the model relies on it most strongly for identity.
- **Don’t generate too many images at once** — larger batches may cause instability. Start with 2–4 images.
- For campaign work, generate at the highest resolution you need once, then downscale for web or social formats.

---

## Notes

- Both prompt and images are required fields.
- Maximum reference images: 10
- Maximum output images per run: 15 (recommended: 2–4 for stability)
- Always match max_images setting with the number specified in your prompt.
- Ensure uploaded image URLs are publicly accessible.

---

## Related Models

- [Seedream V5.0 Lite Edit](https://wavespeed.ai/models/bytedance/seedream-v5.0-lite/edit) — Single-image editing with style transfer.
- [Seedream V5.0 Lite Text-to-Image](https://wavespeed.ai/models/bytedance/seedream-v5.0-lite) — Generate images from text prompts.
- [Qwen Image Edit Plus](https://wavespeed.ai/models/wavespeed-ai/qwen-image/edit-plus) — Single-image editing with strong semantic understanding.

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
  "max_images": 1,
  "output_format": "jpeg"
}
JSON
)

# 1. Submit the prediction.
SUBMIT_RESPONSE=$(curl --silent --show-error --fail-with-body \
  -X POST "https://api.wavespeed.ai/api/v3/bytedance/seedream-v5.0-lite/edit-sequential" \
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
| max_images           | integer       | No       | 1       | 1 ~ 15       | The maximum number of images that can be generated (up to 15). This value must align with the number of images specified in the prompt above.                                                                                                                                                                                   |
| output_format        | string        | No       | -       | jpeg, png    | The format of the output image.                                                                                                                                                                                                                                                                                                 |
| enable_base64_output | boolean       | No       | false   | -            | If set to `true`, the prediction's `output` strings are returned as **naked base64** (no `data:<mime>;base64,` prefix). When `false` (default), outputs are returned as URLs pointing to our CDN.                                                                                                                               |
| enable_sync_mode     | boolean       | No       | false   | -            | If set to `true`, the request attempts to wait for the generated result and return outputs in the same response. If the result is not ready within the sync wait window, the API can return a timeout body while the task continues processing. This option is only available via the API and is supported only by some models. |

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
