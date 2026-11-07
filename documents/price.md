---
sources:
  - "GET https://api.wavespeed.ai/api/v3/models（模型目錄，含 base_price 與 Input Schema）"
  - "POST https://api.wavespeed.ai/api/v3/model/price（逐項報價，呼叫本端點不扣費）"
retrieved: 2026-11-07T22:59:03+08:00
---

# WaveSpeed 模型價格總表

本專案已串接的 108 個模型，單次成功呼叫、產出 1 張圖的美元金額。
依預設價格由高至低排列，同價者依模型 ID 排序。

各欄位的定義：

- 預設價格：只帶 `prompt`、其餘參數全用 Input Schema 預設值時的單次定價。必須帶參考圖的模型以張數下限報價，選填參考圖的模型不帶參考圖。
- 價格區間：把影響計費的參數全部同時拉到最低檔與最高檔時的定價，多個計費參數的加價會疊加；標為「固定」者，所有檔位實測皆同價。參考圖張數也算計費參數，最高檔取張數上限。
- 影響計費的參數：實測會改變報價的參數名稱，標「無」者不論參數如何設定都是同一價。
- 帳戶折扣：報價端點回傳的 `discount_rate`，即實付佔定價的百分比；標「無」者無折扣。

| 模型 ID                                                   | 預設價格 | 價格區間         | 影響計費的參數                                             | 帳戶折扣 |
| --------------------------------------------------------- | -------- | ---------------- | ---------------------------------------------------------- | -------- |
| `wavespeed-ai/hunyuan-image-3-instruct/edit`              | $0.450   | 固定             | 無                                                         | 無       |
| `wavespeed-ai/hunyuan-image-3-instruct/text-to-image`     | $0.450   | 固定             | 無                                                         | 無       |
| `krea/v3/edit`                                            | $0.240   | $0.004 ～ $1.080 | images、size                                               | 無       |
| `google/nano-banana-pro/edit-ultra`                       | $0.150   | $0.150 ～ $0.180 | resolution                                                 | 無       |
| `google/nano-banana-pro/text-to-image-ultra`              | $0.150   | $0.150 ～ $0.180 | resolution                                                 | 無       |
| `google/nano-banana-pro/edit`                             | $0.140   | $0.140 ～ $0.240 | resolution                                                 | 90％     |
| `google/nano-banana-pro/text-to-image`                    | $0.140   | $0.140 ～ $0.240 | resolution                                                 | 90％     |
| `wavespeed-ai/flux-2-flex/edit`                           | $0.120   | 固定             | 無                                                         | 無       |
| `z-ai/glm-image/edit`                                     | $0.120   | 固定             | 無                                                         | 無       |
| `z-ai/glm-image/text-to-image`                            | $0.120   | 固定             | 無                                                         | 無       |
| `midjourney/text-to-image`                                | $0.100   | $0.100 ～ $0.150 | hd                                                         | 無       |
| `wavespeed-ai/hunyuan-image-3`                            | $0.100   | 固定             | 無                                                         | 無       |
| `x-ai/grok-imagine-image-v2.0/edit`                       | $0.090   | $0.050 ～ $0.110 | images、quality、resolution                                | 無       |
| `x-ai/grok-imagine-image-v2.0/text-to-image`              | $0.080   | $0.040 ～ $0.080 | quality、resolution                                        | 無       |
| `alibaba/wan-2.7/image-edit-pro`                          | $0.075   | 固定             | 無                                                         | 無       |
| `alibaba/wan-2.7/text-to-image-pro`                       | $0.075   | 固定             | 無                                                         | 無       |
| `google/nano-banana-2/edit`                               | $0.070   | $0.045 ～ $0.168 | enable_image_search、enable_web_search、resolution         | 90％     |
| `google/nano-banana-2/text-to-image`                      | $0.070   | $0.045 ～ $0.168 | enable_image_search、enable_web_search、resolution         | 90％     |
| `openai/gpt-image-2/edit`                                 | $0.070   | $0.020 ～ $0.910 | images、quality、resolution                                | 95％     |
| `wavespeed-ai/flux-2-max/edit`                            | $0.070   | 固定             | 無                                                         | 無       |
| `wavespeed-ai/flux-2-max/text-to-image`                   | $0.070   | 固定             | 無                                                         | 無       |
| `wavespeed-ai/qwen-image-2.0-pro/edit`                    | $0.070   | 固定             | 無                                                         | 無       |
| `wavespeed-ai/qwen-image-2.0-pro/text-to-image`           | $0.070   | 固定             | 無                                                         | 無       |
| `openai/gpt-image-2.6-flare/edit`                         | $0.065   | $0.045 ～ $1.090 | images、quality、resolution                                | 90％     |
| `openai/gpt-image-2.6-sunburst/edit`                      | $0.065   | $0.045 ～ $1.090 | images、quality、resolution                                | 90％     |
| `ideogram-ai/ideogram-v4.5`                               | $0.060   | $0.030 ～ $0.220 | quality                                                    | 無       |
| `ideogram-ai/ideogram-v4.5/edit`                          | $0.060   | $0.008 ～ $0.220 | quality                                                    | 無       |
| `openai/gpt-image-2/text-to-image`                        | $0.060   | $0.010 ～ $0.720 | quality、resolution                                        | 95％     |
| `wavespeed-ai/flux-2-flex/text-to-image`                  | $0.060   | 固定             | 無                                                         | 無       |
| `wavespeed-ai/krea-v2-large/text-to-image`                | $0.060   | $0.060 ～ $0.065 | reference                                                  | 無       |
| `ideogram-ai/ideogram-v4`                                 | $0.050   | $0.025 ～ $0.200 | quality、resolution                                        | 無       |
| `openai/gpt-image-2.6-flare/text-to-image`                | $0.050   | $0.030 ～ $0.870 | output_format、quality、resolution                         | 90％     |
| `openai/gpt-image-2.6-sunburst/text-to-image`             | $0.050   | $0.030 ～ $0.870 | output_format、quality、resolution                         | 90％     |
| `black-forest-labs/flux-3/image-edit`                     | $0.048   | $0.048 ～ $0.607 | resolution                                                 | 無       |
| `black-forest-labs/flux-3/text-to-image`                  | $0.048   | $0.048 ～ $0.607 | resolution                                                 | 無       |
| `wavespeed-ai/flux-2-turbo/edit`                          | $0.048   | $0.048 ～ $0.064 | images                                                     | 無       |
| `bytedance/seedream-v5.0-pro`                             | $0.045   | $0.045 ～ $0.090 | resolution                                                 | 90％     |
| `bytedance/seedream-v5.0-pro/edit`                        | $0.045   | $0.045 ～ $0.117 | images、resolution                                         | 90％     |
| `google/nano-banana-2/edit-fast`                          | $0.045   | $0.045 ～ $0.064 | enable_web_search、resolution                              | 無       |
| `google/nano-banana-2/text-to-image-fast`                 | $0.045   | $0.045 ～ $0.064 | enable_web_search、resolution                              | 無       |
| `wavespeed-ai/flux-3-klein-image-base/edit`               | $0.045   | $0.045 ～ $0.280 | images、resolution                                         | 無       |
| `alibaba/qwen-image-3.0-pro/edit`                         | $0.043   | $0.043 ～ $0.084 | images、resolution                                         | 無       |
| `google/nano-banana-2.1/edit`                             | $0.042   | $0.042 ～ $0.191 | enable_image_search、enable_web_search、images、resolution | 90％     |
| `alibaba/qwen-image-3.0-pro/text-to-image`                | $0.040   | $0.040 ～ $0.075 | resolution                                                 | 無       |
| `bytedance/seedream-v4.5`                                 | $0.040   | 固定             | 無                                                         | 無       |
| `bytedance/seedream-v4.5/edit`                            | $0.040   | 固定             | 無                                                         | 無       |
| `google/nano-banana-2-lite/edit`                          | $0.040   | 固定             | 無                                                         | 無       |
| `google/nano-banana-2-lite/text-to-image`                 | $0.040   | 固定             | 無                                                         | 無       |
| `google/nano-banana-2.1/text-to-image`                    | $0.040   | $0.040 ～ $0.163 | enable_image_search、enable_web_search、resolution         | 90％     |
| `nvidia/cosmos-3-super/text-to-image`                     | $0.040   | 固定             | 無                                                         | 無       |
| `wavespeed-ai/flux-2-turbo/text-to-image`                 | $0.040   | 固定             | 無                                                         | 無       |
| `openai/gpt-image-2.5-flare/edit`                         | $0.039   | $0.025 ～ $1.240 | images、quality、resolution                                | 無       |
| `openai/gpt-image-2.5-sunburst/edit`                      | $0.039   | $0.025 ～ $1.240 | images、quality、resolution                                | 無       |
| `alibaba/wan-2.5/image-edit`                              | $0.035   | 固定             | 無                                                         | 無       |
| `alibaba/wan-2.6/image-edit`                              | $0.035   | 固定             | 無                                                         | 無       |
| `bytedance/seedream-v5.0-lite`                            | $0.035   | 固定             | 無                                                         | 無       |
| `bytedance/seedream-v5.0-lite/edit`                       | $0.035   | 固定             | 無                                                         | 無       |
| `alibaba/qwen-image-3.0/edit`                             | $0.033   | $0.033 ～ $0.039 | images                                                     | 無       |
| `alibaba/qwen-image-3.0/text-to-image`                    | $0.030   | 固定             | 無                                                         | 無       |
| `alibaba/wan-2.5/text-to-image`                           | $0.030   | 固定             | 無                                                         | 無       |
| `alibaba/wan-2.6/text-to-image`                           | $0.030   | 固定             | 無                                                         | 無       |
| `alibaba/wan-2.7/image-edit`                              | $0.030   | 固定             | 無                                                         | 無       |
| `alibaba/wan-2.7/text-to-image`                           | $0.030   | 固定             | 無                                                         | 無       |
| `krea/v3/text-to-image`                                   | $0.030   | $0.002 ～ $0.120 | size                                                       | 無       |
| `wavespeed-ai/flux-2-flash/edit`                          | $0.030   | $0.030 ～ $0.040 | images                                                     | 無       |
| `wavespeed-ai/flux-3-klein-image-base/text-to-image`      | $0.030   | $0.030 ～ $0.120 | resolution                                                 | 無       |
| `wavespeed-ai/krea-v2-medium/text-to-image`               | $0.030   | 固定             | 無                                                         | 無       |
| `wavespeed-ai/minimax-h3/image-edit`                      | $0.030   | $0.030 ～ $0.130 | images、resolution                                         | 無       |
| `wavespeed-ai/p-h3-image/edit`                            | $0.030   | $0.030 ～ $0.220 | images、resolution                                         | 無       |
| `wavespeed-ai/qwen-image-2.0/edit`                        | $0.030   | 固定             | 無                                                         | 無       |
| `wavespeed-ai/qwen-image-2.0/text-to-image`               | $0.030   | 固定             | 無                                                         | 無       |
| `wavespeed-ai/qwen-image-2.1/edit`                        | $0.030   | $0.030 ～ $0.300 | images、resolution                                         | 無       |
| `bytedance/seedream-v5.5/edit`                            | $0.028   | $0.028 ～ $0.134 | images、resolution                                         | 無       |
| `kwaivgi/kling-image-v3/edit`                             | $0.028   | $0.028 ～ $0.252 | num_images                                                 | 無       |
| `kwaivgi/kling-image-v3/text-to-image`                    | $0.028   | $0.028 ～ $0.252 | num_images                                                 | 無       |
| `bytedance/seedream-v4`                                   | $0.027   | 固定             | 無                                                         | 無       |
| `bytedance/seedream-v4/edit`                              | $0.027   | 固定             | 無                                                         | 無       |
| `bytedance/seedream-v5.0-flash`                           | $0.027   | 固定             | 無                                                         | 90％     |
| `bytedance/seedream-v5.0-flash/edit`                      | $0.027   | 固定             | 無                                                         | 90％     |
| `wavespeed-ai/flux-2-flash/text-to-image`                 | $0.025   | 固定             | 無                                                         | 無       |
| `wavespeed-ai/hunyuan-image-2.1`                          | $0.025   | 固定             | 無                                                         | 無       |
| `openai/gpt-image-2.5-flare/text-to-image`                | $0.024   | $0.010 ～ $1.000 | quality、resolution                                        | 無       |
| `openai/gpt-image-2.5-sunburst/text-to-image`             | $0.024   | $0.010 ～ $1.000 | quality、resolution                                        | 無       |
| `wavespeed-ai/flux-2-dev/edit`                            | $0.024   | 固定             | 無                                                         | 無       |
| `wavespeed-ai/flux-2-klein-base-9b/edit`                  | $0.021   | 固定             | 無                                                         | 無       |
| `bytedance/seedream-v5.5`                                 | $0.020   | $0.020 ～ $0.054 | resolution                                                 | 無       |
| `wavespeed-ai/minimax-h3/text-to-image`                   | $0.020   | $0.020 ～ $0.060 | resolution                                                 | 無       |
| `wavespeed-ai/moss-image/text-to-image`                   | $0.020   | $0.020 ～ $0.080 | resolution                                                 | 無       |
| `wavespeed-ai/p-h3-image/text-to-image`                   | $0.020   | $0.020 ～ $0.120 | resolution                                                 | 無       |
| `wavespeed-ai/qwen-image-2.1/text-to-image`               | $0.020   | $0.020 ～ $0.080 | resolution                                                 | 無       |
| `wavespeed-ai/qwen-image/edit`                            | $0.020   | 固定             | 無                                                         | 無       |
| `wavespeed-ai/qwen-image/edit-2511`                       | $0.020   | 固定             | 無                                                         | 無       |
| `wavespeed-ai/qwen-image/edit-plus`                       | $0.020   | 固定             | 無                                                         | 無       |
| `wavespeed-ai/qwen-image/text-to-image`                   | $0.020   | 固定             | 無                                                         | 無       |
| `wavespeed-ai/qwen-image/text-to-image-2512`              | $0.020   | 固定             | 無                                                         | 無       |
| `wavespeed-ai/flux-2-klein-9b/edit`                       | $0.016   | 固定             | 無                                                         | 無       |
| `wavespeed-ai/flux-3-klein-image-distilled/edit`          | $0.016   | $0.016 ～ $0.084 | images、resolution                                         | 無       |
| `wavespeed-ai/flux-2-klein-base-9b/text-to-image`         | $0.015   | 固定             | 無                                                         | 無       |
| `wavespeed-ai/krea-v2-medium-turbo/text-to-image`         | $0.015   | $0.015 ～ $0.018 | reference                                                  | 無       |
| `wavespeed-ai/flux-2-dev/text-to-image`                   | $0.012   | 固定             | 無                                                         | 無       |
| `wavespeed-ai/flux-dev`                                   | $0.012   | $0.012 ～ $0.048 | num_images                                                 | 無       |
| `wavespeed-ai/krea-v2/turbo`                              | $0.012   | $0.012 ～ $0.024 | resolution                                                 | 無       |
| `wavespeed-ai/flux-2-klein-9b/text-to-image`              | $0.010   | 固定             | 無                                                         | 無       |
| `wavespeed-ai/flux-3-klein-image-distilled/text-to-image` | $0.010   | $0.010 ～ $0.040 | resolution                                                 | 無       |
| `wavespeed-ai/z-image/base`                               | $0.010   | 固定             | 無                                                         | 無       |
| `recraft-ai/recraft-v4.1-flash/text-to-image`             | $0.008   | 固定             | 無                                                         | 無       |
| `wavespeed-ai/flux-dev-ultra-fast`                        | $0.005   | $0.005 ～ $0.020 | num_images                                                 | 無       |
| `wavespeed-ai/z-image/turbo`                              | $0.005   | 固定             | 無                                                         | 無       |

計費參數的逐項說明、帳戶折扣明細與測試成本估算見 [模型價格調查與測試成本](../.claude/plans/model-pricing-and-test-cost.md)。
