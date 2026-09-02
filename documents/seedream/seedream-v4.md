<!--
來源：https://wavespeed.ai/docs/docs-api/bytedance/bytedance-seedream-v4
模型頁：https://wavespeed.ai/models/bytedance/seedream-v4
下載時間：2026-09-02T21:05:05+08:00
說明：由 WaveSpeed 官方文件頁靜態 HTML 轉為 Markdown；Node.js／Python 範例為前端動態渲染，靜態頁僅含 cURL 版本
-->

# Bytedance Seedream V4 API Documentation

## Playground

[Try it on WaveSpeedAI!](https://wavespeed.ai/models/bytedance/seedream-v4)

Seedream 4.0 by is a state-of-the-art image generation model delivering high-fidelity outputs and outperforming Nano Banana. Ready-to-use REST inference API, best performance, no coldstarts, affordable pricing.

## Features

A text-to-image model optimized for **multi-panel/tiled posters**, **concept designs with copy**, **series KV**, and **social media assets**. It excels at **grid-based layouts**, **whitespace planning**, and **type readability**.

## Model Highlights

- **Layout-aware:** Grids (2×2, triptych, comics), keeps whitespace/safe areas for title/subtitle/CTA.
- **Consistent series:** Unified palette, lighting, and camera across panels/KV.
- **High fidelity:** Strong identity/detail retention; clean edges, fewer artifacts.
- **High-res:** 2K default; custom ratios; up to **8192×8192**.

## Price

Only **$0.027** for one run!!!

## Copy-ready Templates

### 2×2 Grid Poster

_2×2 grid poster, clean margins for typography; title top-center: “{TITLE}”; subtitle: “{SUBTITLE}”.
Panel 1: {SCENE_A}; Panel 2: {SCENE_B}; Panel 3: {SCENE_C}; Panel 4: {SCENE_D}.
Consistent color grading, cinematic lighting, brand color {BRAND_COLOR}, high-legibility background, minimal clutter._

### Triptych (Horizontal)

_Horizontal triptych, left-to-right narrative: {SCENE_A} → {SCENE_B} → {SCENE_C}.
Unified palette {BRAND_COLOR}, soft vignette, clear gutters, strong typographic hierarchy,
reserved space for CTA: “{CTA}”._

### Comic (4-Panel Strip)

_4-panel comic layout with speech-bubble placeholders.
Panel 1: {SCENE_A}; Panel 2: {SCENE_B}; Panel 3: {SCENE_C}; Panel 4: {SCENE_D}.
Bold line art, flat shading, clear gutters, high readability._

### Minimalist Poster

_Minimalist poster; large centered title: “{TITLE}”; small subtitle below: “{SUBTITLE}”.
Single focal object: {OBJECT}. Monochrome + accent {BRAND_COLOR}.
High-legibility background; strict grid; generous whitespace._

## How to Use

1. **Enter your prompt:**
   Describe the subject, layout, text placement (title/subtitle/CTA), and style.
2. **Set size:**
   Choose width/height.
   **Maximum:** **8192×8192**.
3. **Run:**
   Click **Run** to generate. If needed, tweak the prompt or size and run again.

## Recommended Resolutions

| Aspect Ratio | Exact (W×H) | Exact Pixels | Rounded (W×H, ÷64) | Rounded Pixels |
| ------------ | ----------- | ------------ | ------------------ | -------------- |
| 1:1          | 1448 × 1448 | 2,096,704    | 1408 × 1408        | 1,982,464      |
| 3:2          | 1773 × 1182 | 2,095,686    | 1728 × 1152        | 1,990,656      |
| 4:3          | 1672 × 1254 | 2,096,688    | 1664 × 1216        | 2,023,424      |
| 16:9         | 1936 × 1089 | 2,108,304    | 1920 × 1088        | 2,088,960      |
| 21:9         | 2212 × 948  | 2,096,976    | 2176 × 960         | 2,088,960      |
| 1:1          | 1024 × 1024 | 1,048,576    | 1024 × 1024        | 1,048,576      |
| 3:2          | 1254 × 836  | 1,048,344    | 1216 × 832         | 1,011,712      |
| 4:3          | 1182 × 887  | 1,048,434    | 1152 × 896         | 1,032,192      |
| 16:9         | 1365 × 768  | 1,048,320    | 1344 × 768         | 1,032,192      |
| 21:9         | 1564 × 670  | 1,047,880    | 1536 × 640         | 983,040        |
| 1:1          | 323 × 323   | 104,329      | 320 × 320          | 102,400        |
| 3:2          | 397 × 264   | 104,808      | 384 × 256          | 98,304         |
| 4:3          | 374 × 280   | 104,720      | 448 × 320          | 143,360        |
| 16:9         | 432 × 243   | 104,976      | 448 × 256          | 114,688        |
| 21:9         | 495 × 212   | 104,940      | 576 × 256          | 147,456        |

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
  -X POST "https://api.wavespeed.ai/api/v3/bytedance/seedream-v4" \
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
| size                 | string  | No       | 2048\*2048 | 512 ~ 8192 | The size of the generated media, supporting up to 4K resolution for images. If you need to match the size of an existing image, you must explicitly specify the dimensions, as automatic resizing to match the image is not supported.                                                                                          |
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
