<!--
來源：https://wavespeed.ai/docs/docs-api/x-ai/x-ai-grok-2-image
模型頁：https://wavespeed.ai/models/x-ai/grok-2-image
下載時間：2026-09-02T20:18:29+08:00
說明：由 WaveSpeed 官方文件頁靜態 HTML 轉為 Markdown；Node.js／Python 範例為前端動態渲染，靜態頁僅含 cURL 版本
-->

# X AI Grok 2 Image API Documentation

## Playground

[Try it on WaveSpeedAI!](https://wavespeed.ai/models/x-ai/grok-2-image)

Grok 2 Image is xAI’s latest image generation model that turns simple text prompts into sharp, photorealistic visuals in seconds. From product shots to social posts and concept art, it follows your instructions closely so you can go from idea to production-ready image with just one prompt. Ready-to-use REST inference API, best performance, no coldstarts, affordable pricing.

## Features

## What is Grok 2 Image?

Grok 2 Image turns a **natural-language text prompt** into vivid, realistic images.
It’s xAI’s flagship image generation model, tuned for marketing creatives, social posts, product visuals, concept art, and more.

In the API, you use the **grok-2-image**. A single request can generate multiple images, making it easy to explore variations on a single idea.

---

## Why it looks great

- **Photorealistic, high-fidelity imagery**
  Trained to produce detailed textures, convincing lighting, and sharp compositions that work well for ads, hero images, and product renders.
- **Strong prompt following**
  Optimized for following descriptive prompts closely, capturing objects, layouts, and styles specified in your text while minimizing “prompt drift.”
- **Flexible visual styles**
  Handles realistic photography, digital illustration, stylized artwork, and concept sketches, making it useful for storyboards, thumbnails, and creative exploration.
- **Multi-image generation in one shot**
  A single request can generate **up to 10 JPG images**, so you can explore multiple creative directions from one prompt.
- **Competitive per-image pricing**
  Images are billed **per output image**, keeping costs predictable for batch runs and A/B creative testing.
- **Prompt refinement under the hood**
  Before reaching the image model, your text prompt can be lightly revised by a chat model to improve clarity, often leading to more accurate results without extra work on your side.

---

## Pricing

- Billing is based on the **number of images generated**.
- Each image will cost **$0.07**.

---

## How to Use

1. **Write your prompt**

- Describe the subject, scene, style, and mood, for example:
- “ultra-wide shot of a neon city at night, rainy streets, cinematic”
- “product photo of wireless earbuds on a marble surface, soft studio lighting”

2. **Send the generation job**

- Call the image API with **model: “grok-2-image”** (or **grok-2-image-1212**) and your prompt.
- Optionally specify how many variations to generate (up to 10 images per request).

3. **Download or display the results**

- The API returns **JPG images** via URLs or encoded data, which you can save, display in an app, or feed into downstream editing/compositing tools.

---

## Note

- **Output format:**
  Images are returned in **JPG** format.
- **Per-job limits:**
- Up to **4 images per request**
- Additional throughput limits depend on your account/plan.
- **Prompt tips:**
- Be concrete about objects, layout, and style (e.g., “centered product on plain background”).
- Avoid contradictory instructions in a single prompt.
- Iterate: start simple, then gradually add details once you like the base composition.

---

## More Image Generation Model Choices

- [Nano Banana Pro](https://wavespeed.ai/models/google/nano-banana-pro/text-to-image)
  High-quality text-to-image generation from Google, suitable for product shots, concept art, and creative visuals.
- [Seedream v4.5](https://wavespeed.ai/models/bytedance/seedream-v4.5)
  A versatile image generation model from, tuned for detailed scenes, characters, and stylized compositions.
- [Kling Image O1](https://wavespeed.ai/models/kwaivgi/kling-image-o1)
  A flagship image model from Kwaivgi/Kuaishou’s Kling series, focused on sharp, high-fidelity visuals and strong prompt adherence.
- [Qwen Image](https://wavespeed.ai/models/wavespeed-ai/qwen-image/text-to-image)
  An Qwen-based generator hosted by WaveSpeedAI, delivering robust semantic understanding and reliable text-to-image rendering across diverse styles.

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
  "num_images": 1
}
JSON
)

# 1. Submit the prediction.
SUBMIT_RESPONSE=$(curl --silent --show-error --fail-with-body \
  -X POST "https://api.wavespeed.ai/api/v3/x-ai/grok-2-image" \
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

| Parameter            | Type    | Required | Default | Range | Description                                                                                                                                                                                                                                                                                                                     |
| -------------------- | ------- | -------- | ------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| prompt               | string  | Yes      |         | -     | The positive prompt for the generation.                                                                                                                                                                                                                                                                                         |
| num_images           | integer | No       | 1       | 1 ~ 4 | Number of images to be generated.                                                                                                                                                                                                                                                                                               |
| enable_sync_mode     | boolean | No       | false   | -     | If set to `true`, the request attempts to wait for the generated result and return outputs in the same response. If the result is not ready within the sync wait window, the API can return a timeout body while the task continues processing. This option is only available via the API and is supported only by some models. |
| enable_base64_output | boolean | No       | false   | -     | If set to `true`, the prediction's `output` strings are returned as **naked base64** (no `data:<mime>;base64,` prefix). When `false` (default), outputs are returned as URLs pointing to our CDN.                                                                                                                               |

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
