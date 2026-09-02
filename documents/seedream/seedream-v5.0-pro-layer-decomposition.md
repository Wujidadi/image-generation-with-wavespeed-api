<!--
來源：https://wavespeed.ai/docs/docs-api/bytedance/bytedance-seedream-v5.0-pro-layer-decomposition
模型頁：https://wavespeed.ai/models/bytedance/seedream-v5.0-pro/layer-decomposition
下載時間：2026-09-02T21:05:05+08:00
說明：由 WaveSpeed 官方文件頁靜態 HTML 轉為 Markdown；Node.js／Python 範例為前端動態渲染，靜態頁僅含 cURL 版本
注意：官方頁面的「Request Parameters」與「Response Parameters」段落是未渲染的 MDX 元件，原始頁面即缺少內容；完整的請求參數定義請見 llms/seedream-v5.0-pro-layer-decomposition.md 的 Input Schema
-->

# Bytedance Seedream V5.0 Pro Layer Decomposition API Documentation

## Playground

[Try it on WaveSpeedAI!](https://wavespeed.ai/models/bytedance/seedream-v5.0-pro/layer-decomposition)

Seedream V5.0 Pro Layer Decomposition separates a single image into a base image and transparent layers, enabling flexible compositing, image editing, asset extraction, and layered design workflows. Ready-to-use REST inference API, best performance, no coldstarts, affordable pricing.

## Features

**Seedream V5.0 Pro Layer Decomposition** separates a single input image into a base image and transparent image layers for compositing, design, and editing workflows. It is useful for breaking a flat image into editable visual components that can be reused, rearranged, or refined in downstream creative tools.

---

## Why Choose This?

- **Layered image decomposition**
  Separate one image into a base image and multiple transparent layers.
- **Editing-ready outputs**
  Use decomposed layers for compositing, retouching, layout design, and creative editing.
- **Prompt-guided layer control**
  Optionally describe the desired layers, targets, objects, or grouping behavior.
- **Automatic element detection**
  When no prompt is provided, the model can identify key visual elements automatically.
- **Flexible resolution tiers**
  Choose `1k`, `1.5k`, or `2k` depending on your workflow needs.
- **Prompt optimization**
  Use `standard` prompt optimization for fuller prompt rewriting, or `fast` mode for quicker generation with lighter optimization.

---

## Parameters

| Parameter                | Required | Description                                                                                                                                                                  |
| ------------------------ | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| image                    | Yes      | The image to decompose into layers. Supports PNG and JPEG images.                                                                                                            |
| prompt                   | No       | Optional positive prompt describing the desired layers, targets, objects, or grouping behavior.                                                                              |
| resolution               | No       | Output resolution tier: `1k`, `1.5k`, or `2k`.                                                                                                                               |
| output_format            | No       | Output image format: `jpeg` or `png`.                                                                                                                                        |
| prompt_optimization_mode | No       | Prompt optimization mode: `standard` or `fast`. Default: `standard`. `standard` uses a fuller prompt rewrite, while `fast` uses lighter optimization for quicker generation. |

---

## How to Use

1. **Upload an image** — Provide a single PNG or JPEG image for decomposition.
2. **Add a prompt optional** — Describe the objects, groups, targets, or layer structure you want.
3. **Choose resolution** — Select `1k`, `1.5k`, or `2k`.
4. **Choose output format** — Select `jpeg` or `png`.
5. **Set prompt optimization optional** — Use `standard` for fuller prompt rewriting or `fast` for quicker generation with lighter optimization.
6. **Submit** — Generate the decomposed image result.

---

## Pricing

Pricing is based on selected `resolution`.

| Resolution | Price  |
| ---------- | ------ |
| 1k         | $0.765 |
| 1.5k       | $0.765 |
| 2k         | $1.53  |

---

## Best Use Cases

- **Compositing workflows** — Separate foreground objects and background elements for layered editing.
- **Design production** — Convert flat images into editable visual components.
- **Marketing asset preparation** — Extract reusable objects, people, products, or scene elements from campaign images.
- **Creative editing** — Rearrange, restyle, replace, or refine isolated image layers.
- **Layout workflows** — Prepare clean visual parts for presentations, ads, thumbnails, and design systems.
- **Post-production** — Use decomposed layers for downstream image editing, animation, or visual effects workflows.

---

## Pro Tips

- Use a clear image with distinct foreground, subject, and background regions.
- Add a prompt when you need specific objects, groupings, or layer behavior.
- Keep the prompt focused on what should become separate layers.
- Choose `1k` or `1.5k` for lower-cost iteration.
- Choose `2k` when higher-resolution layer outputs are needed.
- Use `standard` prompt optimization for more detailed decomposition instructions.
- Use `fast` prompt optimization when speed matters more than detailed prompt rewriting.
- Avoid cluttered scenes when you need precise layer separation.

---

## Related Models

- [Seedream V5.0 Pro](https://wavespeed.ai/models/bytedance/seedream-v5.0-pro) — Generate high-quality images from text prompts.
- [Seedream V5.0 Pro Edit](https://wavespeed.ai/models/bytedance/seedream-v5.0-pro/edit) — Edit images with text instructions and reference images.
- [Seedream V5.0 Lite](https://wavespeed.ai/models/bytedance/seedream-v5.0-lite) — Lightweight image generation model.

```
## Authentication

For authentication details, please refer to the [Authentication Guide](/api-authentication).

## API Endpoints

### Submit Task & Query Result

<ApiTabs submitUrl={model.submitUrl} resultUrl={model.resultUrl} payload={model.defaultValues} />

## Parameters

### Task Submission Parameters

#### Request Parameters

<RequestParams params={model.params} />

#### Response Parameters

<SubmitResponse />

#### Result Request Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| id | string | Yes | - | Task ID |

#### Result Response Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| code | integer | HTTP status code (e.g., 200 for success) |
| message | string | Status message (e.g., "success") |
| data | object | The prediction data object containing all details |
| data.id | string | Unique identifier for the prediction |
| data.model | string | Model ID used for the prediction |
| data.outputs | array&lt;string \| object&gt; | Array of generated outputs (empty when status is not completed). Items are usually URL strings, but may be text strings or structured result objects, depending on the model. |
| data.urls | object | Object containing related API endpoints |
| data.status | string | Status: `completed` is successful; `failed`, `cancelled`, `timeout`, and `deleted` are failure terminal statuses |
| data.created_at | string | ISO timestamp of when the request was created |
| data.error | string | Error message (empty if no error occurred) |
| data.timings | object | Object containing timing details |
| data.timings.inference | integer | Inference time in milliseconds |
```
