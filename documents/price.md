---
sources:
  - "GET https://api.wavespeed.ai/api/v3/models（模型目錄，含 base_price 與 Input Schema）"
  - "POST https://api.wavespeed.ai/api/v3/model/price（逐項報價，呼叫本端點不扣費）"
retrieved: 2026-09-15T17:55:32+08:00
---

# WaveSpeed 文生圖模型價格總表

本專案已串接的 45 個文生圖模型，單次成功呼叫、產出 1 張圖的美元金額。
依預設價格由高至低排列，同價者依模型 ID 排序。

各欄位的定義：

- 預設價格：只帶 `prompt`、其餘參數全用 Input Schema 預設值時的單次定價。
- 價格區間：把影響計費的參數分別拉到最低檔與最高檔時的定價；標為「固定」者，所有檔位實測皆同價。
- 影響計費的參數：實測會改變報價的參數名稱，標「無」者不論參數如何設定都是同一價。
- 帳戶折扣：報價端點回傳的 `discount_rate`，即實付佔定價的百分比；標「無」者無折扣。

| 模型 ID                                               | 預設價格 | 價格區間         | 影響計費的參數      | 帳戶折扣 |
| ----------------------------------------------------- | -------- | ---------------- | ------------------- | -------- |
| `google/nano-banana-pro/text-to-image-ultra`          | $0.150   | $0.150 ～ $0.180 | resolution          | 無       |
| `google/nano-banana-pro/text-to-image`                | $0.140   | $0.140 ～ $0.240 | resolution          | 90％     |
| `wavespeed-ai/hunyuan-image-3-instruct/text-to-image` | $0.120   | 固定             | 無                  | 無       |
| `z-ai/glm-image/text-to-image`                        | $0.120   | 固定             | 無                  | 無       |
| `midjourney/text-to-image`                            | $0.100   | $0.100 ～ $0.150 | hd                  | 無       |
| `alibaba/wan-2.7/text-to-image-pro`                   | $0.075   | 固定             | 無                  | 無       |
| `google/nano-banana-2/text-to-image`                  | $0.070   | $0.045 ～ $0.140 | resolution          | 90％     |
| `wavespeed-ai/flux-2-max/text-to-image`               | $0.070   | 固定             | 無                  | 無       |
| `wavespeed-ai/qwen-image-2.0-pro/text-to-image`       | $0.070   | 固定             | 無                  | 無       |
| `openai/gpt-image-2/text-to-image`                    | $0.060   | $0.010 ～ $0.220 | quality、resolution | 95％     |
| `wavespeed-ai/flux-2-flex/text-to-image`              | $0.060   | 固定             | 無                  | 無       |
| `wavespeed-ai/krea-v2-large/text-to-image`            | $0.060   | 固定             | 無                  | 無       |
| `ideogram-ai/ideogram-v4`                             | $0.050   | $0.025 ～ $0.100 | quality、resolution | 無       |
| `x-ai/grok-imagine-image-v2.0/text-to-image`          | $0.050   | 固定             | 無                  | 無       |
| `bytedance/seedream-v5.0-pro`                         | $0.045   | $0.045 ～ $0.090 | resolution          | 90％     |
| `google/nano-banana-2/text-to-image-fast`             | $0.045   | $0.045 ～ $0.050 | resolution          | 無       |
| `alibaba/qwen-image-3.0-pro/text-to-image`            | $0.040   | $0.040 ～ $0.075 | resolution          | 無       |
| `bytedance/seedream-v4.5`                             | $0.040   | 固定             | 無                  | 無       |
| `google/nano-banana-2-lite/text-to-image`             | $0.040   | 固定             | 無                  | 無       |
| `nvidia/cosmos-3-super/text-to-image`                 | $0.040   | 固定             | 無                  | 無       |
| `wavespeed-ai/flux-2-turbo/text-to-image`             | $0.040   | 固定             | 無                  | 無       |
| `bytedance/seedream-v5.0-lite`                        | $0.035   | 固定             | 無                  | 無       |
| `alibaba/qwen-image-3.0/text-to-image`                | $0.030   | 固定             | 無                  | 無       |
| `alibaba/wan-2.5/text-to-image`                       | $0.030   | 固定             | 無                  | 無       |
| `alibaba/wan-2.6/text-to-image`                       | $0.030   | 固定             | 無                  | 無       |
| `alibaba/wan-2.7/text-to-image`                       | $0.030   | 固定             | 無                  | 無       |
| `wavespeed-ai/krea-v2-medium/text-to-image`           | $0.030   | 固定             | 無                  | 無       |
| `wavespeed-ai/qwen-image-2.0/text-to-image`           | $0.030   | 固定             | 無                  | 無       |
| `kwaivgi/kling-image-v3/text-to-image`                | $0.028   | $0.028 ～ $0.252 | num_images          | 無       |
| `bytedance/seedream-v4`                               | $0.027   | 固定             | 無                  | 無       |
| `wavespeed-ai/flux-2-flash/text-to-image`             | $0.025   | 固定             | 無                  | 無       |
| `openai/gpt-image-2.5-flare/text-to-image`            | $0.024   | $0.010 ～ $0.360 | quality、resolution | 無       |
| `openai/gpt-image-2.5-sunburst/text-to-image`         | $0.024   | $0.010 ～ $0.360 | quality、resolution | 無       |
| `wavespeed-ai/minimax-h3/text-to-image`               | $0.020   | $0.020 ～ $0.060 | resolution          | 無       |
| `wavespeed-ai/qwen-image/text-to-image-2512`          | $0.020   | 固定             | 無                  | 無       |
| `wavespeed-ai/qwen-image/text-to-image`               | $0.020   | 固定             | 無                  | 無       |
| `wavespeed-ai/flux-2-klein-base-9b/text-to-image`     | $0.015   | 固定             | 無                  | 無       |
| `wavespeed-ai/krea-v2-medium-turbo/text-to-image`     | $0.015   | 固定             | 無                  | 無       |
| `wavespeed-ai/flux-2-dev/text-to-image`               | $0.012   | 固定             | 無                  | 無       |
| `wavespeed-ai/flux-dev`                               | $0.012   | $0.012 ～ $0.048 | num_images          | 無       |
| `wavespeed-ai/krea-v2/turbo`                          | $0.012   | $0.012 ～ $0.024 | resolution          | 無       |
| `wavespeed-ai/flux-2-klein-9b/text-to-image`          | $0.010   | 固定             | 無                  | 無       |
| `wavespeed-ai/z-image/base`                           | $0.010   | 固定             | 無                  | 無       |
| `wavespeed-ai/flux-dev-ultra-fast`                    | $0.005   | $0.005 ～ $0.020 | num_images          | 無       |
| `wavespeed-ai/z-image/turbo`                          | $0.005   | 固定             | 無                  | 無       |

計費參數的逐項說明、帳戶折扣明細與測試成本估算見 [模型價格調查與測試成本](../.claude/plans/model-pricing-and-test-cost.md)。
