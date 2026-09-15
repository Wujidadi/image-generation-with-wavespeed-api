---
updated: 2026-09-15T17:55:32+08:00
---

# WaveSpeed 模型價格調查與測試成本

45 個文生圖模型的價格明細見 [價格總表](../../documents/price.md)，本文件記錄調查方法、計費參數的行為，以及串接 40 個新模型時的測試成本。

## 資料來源

價格不取自網頁，而是查 WaveSpeed 官方的兩個端點：

- `GET /api/v3/models` 取回完整模型目錄，含 `base_price` 與每個模型的 Input Schema。
- `POST /api/v3/model/price` 逐一報價，呼叫本端點不扣費，因此可對每個參數的每個檔位反覆試算。

`base_price` 只是價格下限，不能直接當單價用。
例如 `bytedance/seedream-v5.0-pro` 的 `base_price` 是 0.045，但 `resolution=2k` 實際收 0.090。

## 計費參數

四個參數會改變價格，其餘參數不論怎麼設都不影響計費：

- `resolution`：解析度檔位，是最普遍的計費變數，共 12 個模型採用。
  漲幅差異很大，`google/nano-banana-2/text-to-image-fast` 由 2K 升到 4K 只多 11％，`wavespeed-ai/minimax-h3/text-to-image` 由 1K 升到 2K 則漲為 3 倍。
  另有 `kwaivgi/kling-image-v3/text-to-image` 與 `alibaba/qwen-image-3.0/text-to-image` 雖有 `resolution` 參數，但 1K 與 2K 實測同價。
- `quality`：品質檔位，見於 `ideogram-ai/ideogram-v4` 與三個 OpenAI GPT Image 模型。
  兩個 GPT Image 2.5 模型的跨度最大，`low` 為 $0.010、`max` 為 $0.360，相差 36 倍。
- `num_images`：單次產圖張數，價格與張數成正比，見於 `kwaivgi/kling-image-v3/text-to-image`（上限 9 張）與兩個 FLUX dev 模型（上限 4 張）。
- `hd`：僅 `midjourney/text-to-image` 有，開啟後由 $0.100 升為 $0.150。

實測確認不影響計費的參數：

- 自由字串形式的 `size`：`wavespeed-ai/flux-2-max/text-to-image`、`z-ai/glm-image/text-to-image`、`alibaba/wan-2.7/text-to-image-pro` 等模型從 `512*512` 到 `8192*8192` 皆同價。
- `aspect_ratio`、`num_inference_steps`、`guidance_scale`、`strength`、`creativity`、`prompt_optimization_mode`、`thinking_mode`、`enable_prompt_expansion`、`enable_web_search`、`enable_image_search`、`output_format`。
- Midjourney 的 `quality`、`stylize`、`chaos`、`weird`：與其他模型的 `quality` 不同，Midjourney 的檔位切換不改價，只有 `hd` 改價。

注意 `bytedance/seedream-v5.0-pro` 的計費參數名為 `resolution` 而非 `size`；帶 `size` 送出報價不會反映 2K 加倍，實跑時檔位仍以 `resolution` 為準。

## 帳戶折扣

四個模型目前有折扣，其餘 41 個以定價計費。折扣為平台給定、隨時可能調整，不宜作為長期預算依據。

| 模型 ID                                | 折扣率 | 預設定價 | 預設實付 |
| -------------------------------------- | ------ | -------- | -------- |
| `bytedance/seedream-v5.0-pro`          | 90％   | $0.045   | $0.0405  |
| `google/nano-banana-2/text-to-image`   | 90％   | $0.070   | $0.0630  |
| `google/nano-banana-pro/text-to-image` | 90％   | $0.140   | $0.1260  |
| `openai/gpt-image-2/text-to-image`     | 95％   | $0.060   | $0.0570  |

## 測試成本估算

### 不花錢就能完成的部分

40 個新模型的腳本骨架完全一致，只有 `MODEL_ID`、`add_model_args` 與 `build_payload` 三處不同，因此大部分驗證不必實際產圖：

- 參數解析與 payload 組裝：以 `WAVESPEED_API_KEY=invalid` 執行，檢查參數檢核與送出的 JSON 是否正確。
- 參數的可選值與預設值：以 `GET /api/v3/models` 回傳的 Input Schema 核對，不必試誤。
- 價格與計費檔位：以 `POST /api/v3/model/price` 報價，呼叫本端點不扣費。
- 輪詢、下載與輸出目錄邏輯：以 `--task-id` 取回既有任務驗證，不重新產圖。

真正會扣費的只剩「每個模型至少成功產出 1 張圖」這一項。

### 實跑成本

| 情境       | 內容                                                             | 產圖次數 | 定價合計 | 折後實付 |
| ---------- | ---------------------------------------------------------------- | -------- | -------- | -------- |
| 最低限度   | 每個新模型 1 張，全用預設參數                                    | 40       | $1.787   | $1.763   |
| 最省設定   | 每個新模型 1 張，計費參數壓到最低檔                              | 40       | $1.659   | $1.640   |
| 含檔位驗證 | 預設參數各 1 張，另對 15 個有計費檔位的模型各加測 1 張非預設檔位 | 55       | $2.439   | $2.396   |
| 全高檔位   | 每個新模型 1 張，計費參數拉到最高檔                              | 40       | $3.286   | $3.237   |

單一模型最貴的一次呼叫是兩個 GPT Image 2.5 模型的 `quality=max`，各 $0.360；測試時務必維持預設的 `medium` 或降為 `low`。

### 實測結果

2026-09-14 以「最省設定」實際執行一輪：40 個新模型各產 1 張圖，多數用預設參數，五個模型改用非預設的最省檔位
（`google/nano-banana-2/text-to-image` 降為 `resolution=0.5k`，`ideogram-ai/ideogram-v4` 與三個 GPT Image 模型降為 `quality=low`）。
該輪 `wavespeed-ai/flux-2-flash/text-to-image` 與 `wavespeed-ai/flux-2-turbo/text-to-image` 仍以 2026-09-15 調價前的 $0.008 與 $0.010 計費，因此實付低於上表「最省設定」的估算。

- 40 個模型全部成功，無一失敗或需重試。
- 報價端點預估實付 $1.5930，帳戶餘額由 33.000158 降至 31.4，實扣約 $1.60，與預估相符。
- `midjourney/text-to-image` 一次請求回傳 4 張圖，仍只收 $0.100。

後續若要比較各模型的輸出品質，每個模型多跑 1 輪預設參數約再花 $1.76。
