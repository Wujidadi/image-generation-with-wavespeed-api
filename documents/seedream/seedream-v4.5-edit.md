<!--
來源：https://wavespeed.ai/docs/docs-api/bytedance/bytedance-seedream-v4.5-edit
模型頁：https://wavespeed.ai/models/bytedance/seedream-v4.5/edit
下載時間：2026-09-02T21:05:05+08:00
說明：由 WaveSpeed 官方文件頁靜態 HTML 轉為 Markdown；Node.js／Python 範例為前端動態渲染，靜態頁僅含 cURL 版本
-->

# Bytedance Seedream V4.5 Edit API Documentation

## Playground

[Try it on WaveSpeedAI!](https://wavespeed.ai/models/bytedance/seedream-v4.5/edit)

Seedream 4.5 Edit preserves facial features, lighting, and color tone from reference images, delivering professional, high-fidelity edits up to 4K with strong prompt adherence. Ready-to-use REST inference API, best performance, no cold starts, affordable pricing.

## Features

**Seedream 4.5 Edit** is ’s high-end image editing model. It preserves facial structure, lighting, and colour tone from your input while applying precise, prompt-driven changes that look like they were done by a professional retoucher—not an over-filtered AI.

---

## Model highlights

- **Reference-faithful editing** – Keeps identity, pose, lighting, and palette close to the original image.
- **Multi-image support** – Upload **1–10 images** and apply the same edit prompt across the whole batch.
- **High-fidelity details** – Crisp textures, clean edges, and minimal artifacts even on complex edits.
- **Strong prompt adherence** – Understands nuanced edit instructions for clothing, background, mood, and style.
- **4K-ready output** – Supports resolutions up to **8192 × 8192** when you need extra detail.

---

## Recommended use cases

- Portrait retouching and beauty / fashion edits
- Outfit, hairstyle, and accessory changes
- Background replacement or scene upgrades
- Product visual updates and colourway exploration
- Interior / architecture visual tweaks
- Brand KV and campaign asset iterations

---

## Pricing

Flat, simple pricing:

- **$0.04 per generated image**

Each successfully edited output counts as one image.

---

## How to use

1. **Upload images**
   Add **1–10 images** under **images**. These are the photos that will be edited.
2. **Write your edit prompt**
   Clearly describe what should change and what must stay the same, e.g.
   _“Change jacket to red leather, keep pose and background, cinematic lighting.”_
3. **(Optional) Set **size\*\*\*\*

- Choose **width** and **height** (e.g. 1024×1024, 2048×2048, up to **8192×8192**).
- If you **leave size empty**, the model uses its default resolution.

4. **Run**
   Submit the job. All uploaded images will be edited using the same instructions.

---

## Prompt patterns (copy & adapt)

**Outfit / accessory change**

> Change outfit to {DESCRIPTION}, keep pose and lighting, preserve skin tone, clean edges, no distortions.

**Background replacement**

> Replace background with {SCENE}, match original light direction, natural shadows, no haloing around subject.

**Style / mood change**

> Apply {STYLE} colour grading, keep subject identity and composition, subtle filmic contrast, rich details.

**Product recolour**

> Change product colour to {HEX / COLOUR NAME}, keep material and reflections, no change to logo.

---

## Notes

- Higher input resolution generally yields better detail; for heavy crops, consider upscaling first.
- For best results, keep edit prompts **specific but focused**—avoid mixing too many unrelated changes at once.
- All image URLs must be publicly accessible for the model to load them.

---

## Model comparison on WaveSpeedAI

Use **Seedream 4.5 Edit** together with other editing models depending on what you’re optimising for:

- **[/seedream-v4.5/edit-sequential](https://wavespeed.ai/models/bytedance/seedream-v4.5/edit-sequential)** – multi-image editing that keeps **the same character and style** across a whole batch; best when you need a series of consistent portraits, product shots or KV variations.
- **[wavespeed-ai/flux-2-dev/edit](https://wavespeed.ai/models/wavespeed-ai/flux-2-dev/edit)** – lightweight FLUX.2 edit model for **fast, low-cost batch updates**; great for everyday asset tweaks where ultimate fidelity is less critical.
- **[flux-2-flex/edit](https://wavespeed.ai/models/wavespeed-ai/flux-2-flex/edit)** – more **style-rich and adventurous** editing; good for creative restyling, mood shifts and art-direction heavy work rather than strict realism.
- **[flux-2-pro/edit](https://wavespeed.ai/models/wavespeed-ai/flux-2-pro/edit)** – production-grade FLUX.2 editing with **multi-reference and context-aware control**, suited to complex commercial composites and e-commerce pipelines.
- **[qwen-image/edit-plus](https://wavespeed.ai/models/wavespeed-ai/qwen-image/edit-plus)** – strong **semantic understanding and local control**, ideal for masking-style edits, UI mockups, and precise object-level changes.

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
  ]
}
JSON
)

# 1. Submit the prediction.
SUBMIT_RESPONSE=$(curl --silent --show-error --fail-with-body \
  -X POST "https://api.wavespeed.ai/api/v3/bytedance/seedream-v4.5/edit" \
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
