<!--
來源：https://wavespeed.ai/docs/docs-api/bytedance/bytedance-seedream-v4.5-edit-sequential
模型頁：https://wavespeed.ai/models/bytedance/seedream-v4.5/edit-sequential
下載時間：2026-09-02T21:05:05+08:00
說明：由 WaveSpeed 官方文件頁靜態 HTML 轉為 Markdown；Node.js／Python 範例為前端動態渲染，靜態頁僅含 cURL 版本
-->

# Bytedance Seedream V4.5 Edit Sequential API Documentation

## Playground

[Try it on WaveSpeedAI!](https://wavespeed.ai/models/bytedance/seedream-v4.5/edit-sequential)

Seedream 4.5 Edit Sequential performs multi-image editing while locking character and object identity across shots. It detects main subjects, preserves continuity, and applies controlled edits with up to 4K output. Ready-to-use REST inference API, best performance, no cold starts, affordable pricing.

## Features

**Seedream 4.5 Edit Sequential** is ’s multi-image editing model designed to apply **the same edit across a whole set of images**. It automatically tracks the main subject through the series, keeps identity stable, and generates clean, high-resolution results—ideal for campaigns, product sets, and character line-ups.

---

## Model highlights

- **Multi-image subject tracking** – Detects the main subject across all input images and treats them as the same person or object.
- **Character consistency lock** – Preserves facial structure, proportions, and overall identity across every edited output.
- **High reference fidelity** – Maintains lighting, colour balance, and key visual details while applying the requested changes.
- **Controlled, repeatable edits** – One prompt drives a consistent transformation across the entire batch.
- **4K-ready resolution** – Supports sizes up to **8192 × 8192** for print-adjacent and hero visual use.
- **Production quality** – Sharp edges, low artifacts, and stable composition suitable for professional workflows.

---

## Best suited for

- Batch portrait editing with a fixed style or look
- Product series images that must feel like one coherent set
- Brand or ad campaign iterations with the same model or hero product
- Character design variations (outfits, moods, lighting)
- E-commerce catalog refreshes and seasonal updates
- Social / marketing visual series where continuity matters

---

## Pricing

Billing is **per output image**, scaled by the **max_images** you request.

- **Base price:** **$0.04 per image**
- **Formula:** total_price = $0.04 × max_images

Example costs:

| max_images | Total price |
| ---------- | ----------- |
| 1          | **$0.04**   |
| 4          | **$0.16**   |
| 8          | **$0.32**   |

---

## How to use

1. **Upload source images**
   Add the images you want to edit sequentially (all should contain the same main subject or product).
2. **Write the edit prompt**
   Describe the shared change you want across the whole set, e.g.
   “Change outfit to a black suit, add soft studio lighting, keep poses and background the same.”
3. **Set max_images**
   Specify how many edited outputs you want the model to generate from your input set.
4. **Choose size**
   Select the target resolution, up to **8192 × 8192** for maximum detail.
5. **Run and review**
   Submit the job, inspect the edited series, and optionally refine the prompt for another pass.

---

## Tips for best results

- Use **clear, global instructions** in the prompt (“add winter outfit and snow ambience”) rather than per-image directions.
- Keep input images **reasonably consistent** in framing and lighting so the model can lock onto the same subject.
- Put your **cleanest, clearest reference image first**; the model tends to rely on it most strongly for identity.
- For campaign work, generate at the **highest resolution you need once**, then downscale for web or social formats.

---

## Note

- Please set the **max_image** first, and then input how many images you want to generate in prompt! Such as:
- max_image = 4.
  _Prompt: I want to generate 4 images… + (your prompt)_

---

## More Models to Try!

- [Nano Banana Pro](https://wavespeed.ai/models/google/nano-banana-pro/edit)

Google’s ultra, fast text-to-image model for generating many ideas from scratch; great for large batches of new images, not for editing existing photo series.

- [Seedream V4](https://wavespeed.ai/models/bytedance/seedream-v4)

’s high-resolution text-to-image generator with rich detail and diverse styles; ideal when you want new scenes in the Seedream aesthetic rather than editing your own photos.

- [Qwen Image Edit Plus](https://wavespeed.ai/models/wavespeed-ai/qwen-image/edit-plus)

Single-image, prompt-based editing with strong semantic understanding; perfect for one-off or small-batch edits where you don’t need strict identity matching across many images.

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
  "max_images": 1
}
JSON
)

# 1. Submit the prediction.
SUBMIT_RESPONSE=$(curl --silent --show-error --fail-with-body \
  -X POST "https://api.wavespeed.ai/api/v3/bytedance/seedream-v4.5/edit-sequential" \
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
