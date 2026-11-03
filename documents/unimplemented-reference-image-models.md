---
sources:
  - "GET https://api.wavespeed.ai/api/v3/models（模型目錄，含 base_price 與 Input Schema）"
  - "POST https://api.wavespeed.ai/api/v3/model/price（逐項報價，呼叫本端點不扣費）"
retrieved: 2026-11-03T16:37:41+08:00
---

# WaveSpeed 未實作參考圖模型

WaveSpeed 目錄中可用參考圖、帶提示詞且本專案尚無腳本的 57 個模型。
列入本表不代表建議實作：其中 55 個在最早的 2026-09-20 快照就已存在，多數已有同家族的新世代腳本，實作前應先比較出圖效果。

未列入本表的端點：

- `sequential`、`edit-multi`、`multiple-angles` 與 LoRA 變體，依 `AGENTS.md` 的慣例不實作。
- `wavespeed-ai/z-image-turbo/image-to-image`，因為 `z-image-turbo` 腳本已可透過 `image` 欄位帶參考圖。
- `ideogram-ai/ideogram-vector/text-to-vector` 與 `wavespeed-ai/z-image-turbo/controlnet`，分別輸出向量圖與依控制圖生成，用途與一般參考圖不同。
- 無提示詞端點與 `image-to-image`、`text-to-image` 以外的類型，例如去背、放大與圖層分解工具。

依 1 張報價由低至高排列，同價者依模型 ID 排序。

各欄位的定義：

- 底價：目錄的 `base_price`。
- 1 張報價、上限張數報價：以佔位網址與預設參數取得的定價，只反映參考圖張數；全部模型皆無帳戶折扣。
- 參考圖欄位與張數上限：來源圖與參考圖分屬兩個欄位時以 `＋` 連接，上限張數報價只把 `reference` 或 `reference_images` 拉到上限。
- 參考圖：`必填` 表示請求必須帶參考圖，`選填` 表示不帶也能當文生圖使用。

| 模型 ID                                          | 類型             | 底價    | 1 張報價 | 上限張數報價 | 參考圖欄位與張數上限              | 參考圖 |
| ------------------------------------------------ | ---------------- | ------- | -------- | ------------ | --------------------------------- | ------ |
| `wavespeed-ai/flux-schnell`                      | `text-to-image`  | $0.003  | $0.003   | $0.003       | `image(1)`                        | 選填   |
| `minimax/image-01/image-to-image`                | `image-to-image` | $0.0035 | $0.0035  | $0.0035      | `image(1)`                        | 選填   |
| `luma/photon-flash-modify`                       | `image-to-image` | $0.010  | $0.010   | $0.010       | `image(1)`                        | 選填   |
| `pruna-ai/p-image/edit`                          | `image-to-image` | $0.010  | $0.010   | $0.010       | `images(5)`                       | 必填   |
| `wavespeed-ai/anima/text-to-image`               | `text-to-image`  | $0.010  | $0.010   | $0.010       | `image(1)`                        | 選填   |
| `meta/muse-image/edit`                           | `image-to-image` | $0.011  | $0.011   | $0.011       | `images(10)`                      | 必填   |
| `wavespeed-ai/flux-2-klein-4b/edit`              | `image-to-image` | $0.012  | $0.012   | $0.012       | `images(3)`                       | 必填   |
| `luma/photon-modify`                             | `image-to-image` | $0.015  | $0.015   | $0.015       | `image(1)`                        | 選填   |
| `wavespeed-ai/flux-2-klein-base-4b/edit`         | `image-to-image` | $0.015  | $0.015   | $0.015       | `images(3)`                       | 必填   |
| `wavespeed-ai/flux-kontext-dev-ultra-fast`       | `image-to-image` | $0.020  | $0.020   | $0.020       | `image(1)`                        | 選填   |
| `wavespeed-ai/flux-pulid`                        | `image-to-image` | $0.020  | $0.020   | $0.020       | `image(1)`                        | 必填   |
| `wavespeed-ai/hidream-o1-image-dev/edit`         | `image-to-image` | $0.020  | $0.020   | $0.020       | `images(3)`                       | 必填   |
| `wavespeed-ai/wan-2.1/text-to-image`             | `text-to-image`  | $0.020  | $0.020   | $0.020       | `image(1)`                        | 選填   |
| `wavespeed-ai/wan-2.2/image-to-image`            | `image-to-image` | $0.020  | $0.020   | $0.020       | `image(1)`                        | 必填   |
| `wavespeed-ai/hidream-e1-full`                   | `image-to-image` | $0.024  | $0.024   | $0.024       | `image(1)`                        | 必填   |
| `wavespeed-ai/flux-kontext-dev`                  | `image-to-image` | $0.025  | $0.025   | $0.025       | `image(1)`                        | 選填   |
| `wavespeed-ai/flux-kontext-dev/multi-ultra-fast` | `image-to-image` | $0.025  | $0.025   | $0.025       | `images(4)`                       | 選填   |
| `x-ai/grok-imagine-image/edit`                   | `image-to-image` | $0.025  | $0.025   | $0.025       | `image(1)`                        | 必填   |
| `kwaivgi/kling-image-o1`                         | `image-to-image` | $0.028  | $0.028   | $0.028       | `images(10)`                      | 選填   |
| `kwaivgi/kling-image-o3/edit`                    | `image-to-image` | $0.028  | $0.028   | $0.028       | `images(10)`                      | 必填   |
| `ideogram-ai/ideogram-v3-turbo`                  | `text-to-image`  | $0.030  | $0.030   | $0.030       | `image(1)`＋`reference_images(3)` | 選填   |
| `wavespeed-ai/flux-kontext-dev/multi`            | `image-to-image` | $0.030  | $0.030   | $0.030       | `images(4)`                       | 選填   |
| `wavespeed-ai/step1x-edit`                       | `text-to-image`  | $0.030  | $0.030   | $0.030       | `image(1)`                        | 必填   |
| `runwayml/gen4-image-turbo`                      | `text-to-image`  | $0.035  | $0.035   | $0.035       | `reference_images(3)`             | 選填   |
| `google/gemini-2.5-flash-image-preview/edit`     | `image-to-image` | $0.038  | $0.038   | $0.038       | `images(10)`                      | 必填   |
| `google/gemini-2.5-flash-image/edit`             | `image-to-image` | $0.038  | $0.038   | $0.038       | `images(10)`                      | 必填   |
| `google/nano-banana/edit`                        | `image-to-image` | $0.038  | $0.038   | $0.038       | `images(10)`                      | 必填   |
| `bria/fibo-2.0/edit`                             | `image-to-image` | $0.040  | $0.040   | $0.040       | `images(4)`                       | 必填   |
| `bria/fibo-2.0/text-to-image`                    | `text-to-image`  | $0.040  | $0.040   | $0.040       | `images(1)`                       | 選填   |
| `bria/fibo-edit-1.5/edit`                        | `image-to-image` | $0.040  | $0.040   | $0.040       | `images(4)`                       | 必填   |
| `bria/fibo-edit/genfill`                         | `image-to-image` | $0.040  | $0.040   | $0.040       | `image(1)`                        | 必填   |
| `bria/fibo-generate-1.5/text-to-image`           | `text-to-image`  | $0.040  | $0.040   | $0.040       | `images(1)`                       | 選填   |
| `bria/fibo/edit`                                 | `image-to-image` | $0.040  | $0.040   | $0.040       | `images(1)`                       | 必填   |
| `ideogram-ai/ideogram-v2a`                       | `text-to-image`  | $0.040  | $0.040   | $0.040       | `image(1)`                        | 選填   |
| `ideogram-ai/ideogram-v2a-turbo`                 | `text-to-image`  | $0.040  | $0.040   | $0.040       | `image(1)`                        | 選填   |
| `vidu/reference-to-image-q2`                     | `image-to-image` | $0.040  | $0.040   | $0.050       | `images(7)`                       | 必填   |
| `wavespeed-ai/flux-kontext-pro`                  | `image-to-image` | $0.040  | $0.040   | $0.040       | `image(1)`                        | 必填   |
| `wavespeed-ai/flux-kontext-pro/multi`            | `image-to-image` | $0.040  | $0.040   | $0.040       | `images(3)`                       | 必填   |
| `wavespeed-ai/hidream-o1-image/edit`             | `image-to-image` | $0.040  | $0.040   | $0.040       | `images(3)`                       | 必填   |
| `luma/uni-v1/text-to-image`                      | `text-to-image`  | $0.042  | $0.045   | $0.069       | `reference(9)`                    | 選填   |
| `luma/uni-v1/edit`                               | `image-to-image` | $0.042  | $0.048   | $0.069       | `image(1)`＋`reference(8)`        | 必填   |
| `ideogram-ai/ideogram-v2-turbo`                  | `text-to-image`  | $0.050  | $0.050   | $0.050       | `image(1)`                        | 選填   |
| `ideogram-ai/ideogram-v3-balanced`               | `text-to-image`  | $0.060  | $0.060   | $0.060       | `image(1)`＋`reference_images(3)` | 選填   |
| `wavespeed-ai/flux-2-pro/edit`                   | `image-to-image` | $0.060  | $0.060   | $0.060       | `images(3)`                       | 必填   |
| `wavespeed-ai/qwen-image-max/edit`               | `image-to-image` | $0.070  | $0.070   | $0.070       | `images(3)`                       | 必填   |
| `x-ai/grok-imagine-image-quality/edit`           | `image-to-image` | $0.070  | $0.070   | $0.090       | `images(3)`                       | 必填   |
| `ideogram-ai/ideogram-v2`                        | `text-to-image`  | $0.080  | $0.080   | $0.080       | `image(1)`                        | 選填   |
| `wavespeed-ai/flux-kontext-max`                  | `image-to-image` | $0.080  | $0.080   | $0.080       | `image(1)`                        | 必填   |
| `wavespeed-ai/flux-kontext-max/multi`            | `image-to-image` | $0.080  | $0.080   | $0.080       | `images(3)`                       | 必填   |
| `ideogram-ai/ideogram-v3-quality`                | `text-to-image`  | $0.090  | $0.090   | $0.090       | `image(1)`＋`reference_images(3)` | 選填   |
| `runwayml/gen4-image`                            | `text-to-image`  | $0.055  | $0.090   | $0.090       | `reference_images(3)`             | 選填   |
| `openai/gpt-image-1.5/edit`                      | `image-to-image` | $0.100  | $0.120   | $0.660       | `images(10)`                      | 選填   |
| `google/gemini-3-pro-image/edit`                 | `image-to-image` | $0.140  | $0.140   | $0.140       | `images(10)`                      | 必填   |
| `ideogram-ai/ideogram-character`                 | `image-to-image` | $0.150  | $0.150   | $0.150       | `image(1)`                        | 必填   |
| `sourceful/riverflow-2.0-pro/edit`               | `image-to-image` | $0.150  | $0.150   | $0.150       | `images(10)`                      | 必填   |
| `wavespeed-ai/firered-image-v1.1/edit`           | `image-to-image` | $0.150  | $0.150   | $0.150       | `images(3)`                       | 必填   |
| `wavespeed-ai/instant-character`                 | `image-to-image` | $0.300  | $0.300   | $0.300       | `image(1)`                        | 必填   |
