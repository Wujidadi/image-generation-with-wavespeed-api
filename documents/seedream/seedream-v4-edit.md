<!--
來源：https://wavespeed.ai/docs/docs-api/bytedance/bytedance-seedream-v4-edit
模型頁：https://wavespeed.ai/models/bytedance/seedream-v4/edit
下載時間：2026-09-02T21:05:05+08:00
說明：由 WaveSpeed 官方文件頁靜態 HTML 轉為 Markdown；Node.js／Python 範例為前端動態渲染，靜態頁僅含 cURL 版本
-->

# Bytedance Seedream V4 Edit API Documentation

## Playground

[Try it on WaveSpeedAI!](https://wavespeed.ai/models/bytedance/seedream-v4/edit)

Seedream V4 Edit is state-of-the-art image editing model that outperforms Nano Banana in fidelity and edit quality. Ready-to-use REST inference API, best performance, no coldstarts, affordable pricing.

## Features

**Seedream 4.0/Edit** is a specialized image-to-image model for accurate edits to existing images - swap outfits and accessories, adjust hair or makeup, recolor or re-materialize products, and replace interior finishes like floors, walls, or furniture while maintaining subject identity, lighting, and overall composition.

## Highlights

- **High fidelity on people & products:** Reliable skin tones, fabric/material details, logos, and fine edges.
- **Production-friendly consistency:** Generate multiple variants quickly with locked camera/look and brand color grading.
- **Structured prompts that scale:** Works best when the goal is clear up front (action + object + target feature + constraints).

## Use cases

- **Portrait & influencer workflows:** Outfit/makeup/hair changes, branded KV series, quick campaign variants.
- **E-commerce & product teams:** Colorways, material/texture swaps, packaging updates.
- **Interior/archviz:** Wall/floor finish replacements, upholstery changes, lighting-aware set dressing.
- **Marketing & growth:** Fast A/B testing with consistent brand color and camera setup.

## Price

Only **$0.027** per image!!!

## How to use

1. **Prepare source:** Upload the base images (**Up to 10 images**).
2. **Set size:** The maximum size of the image is **8192 \* 8192**.
3. **Write a clear prompt:** Write clearly in the prompt about object, feature, and constraints.

## Prompt patterns (copy-ready)

Use: change action + change object + target feature + constraints (keep/avoid)

### Portrait (KV series)

_portrait KV series, {STYLE} style, consistent color grading {BRAND_COLOR},
fixed camera look (85mm shallow depth),
interchangeable persona: {PERSONA},
reserved lower-third text “{NAME} — {ROLE}”_

### Change Clothes / Jewellery / Makeup

_Outfit swap for portrait, replace clothing with {OUTFIT_DESC};
keep pose and composition; accessories {JEWELRY_DESC};
makeup/hair {MAKEUP_HAIR}; preserve skin tone and lighting;
clean edges, no artifacts_

### Background Replacement

_Background replacement for subject, keep subject edges;
new environment: {SCENE_DESC};
match light direction and color temperature;
soft contact shadows; no haloing_

### Interior / Outdoor Replacement

_Interior finish swap, update wall {WALL_MATERIAL},
floor {FLOOR_MATERIAL}, furniture upholstery {FABRIC};
layout and lighting unchanged; realistic PBR textures_

---

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
  "images": [
    "https://interactive-examples.mdn.mozilla.net/media/cc0-images/painted-hand-298-332.jpg"
  ]
}
JSON
)

# 1. Submit the prediction.
SUBMIT_RESPONSE=$(curl --silent --show-error --fail-with-body \
  -X POST "https://api.wavespeed.ai/api/v3/bytedance/seedream-v4/edit" \
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
