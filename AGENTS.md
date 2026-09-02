# Image Generation with WaveSpeed API

## 架構

- `scripts/wavespeed_common.py` 是唯一的共用邏輯：金鑰載入、提示詞讀取與註解過濾、輸出目錄檢查、任務提交、輪詢重試、`--task-id` 取回、下載。
  流程性的修改一律改這裡，不在各模型腳本重複實作。
- 各模型腳本 `scripts/<模型名稱>.py` 只做三件事：定義 `MODEL_ID`、以 `add_model_args(parser)` 加入模型專屬參數、以 `build_payload(args, prompt)` 回傳 `prompt` 以外的請求欄位，最後呼叫 `ws.run(MODEL_ID, add_model_args, build_payload)`。
- 檔名即模型名稱，規則是模型 ID 去掉供應商前綴、斜線改連字號，例如 `x-ai/grok-imagine-image-v2.0/text-to-image` 對應 `grok-imagine-image-v2.0-text-to-image.py`。
  `wsgen --list` 與預設輸出目錄都依此規則自動推算，新增腳本不需改 `wsgen`。

## 慣例

- 只用 Python 標準函式庫，不引入第三方套件。
- 參數的可選值、預設值與範圍以 `documents/` 下的官方文件為準（`llms/` 內的 Input Schema 最精確），不憑記憶填寫。
- 命令列參數值若含 `*` 之類的 shell 特殊字元，提供不需引號的替代寫法，例如 `--size` 接受 `寬x高`。
- 錯誤一律以 `sys.exit("中文訊息")` 結束，不讓例外堆疊外洩；所有會扣費的請求之前，先完成本機端的檢查。
- 測試時以無效金鑰（`WAVESPEED_API_KEY=invalid`）驗證參數解析與 payload 組裝，或以 `--task-id` 取回既有任務，避免實際扣費。
- 圖片輸出不進版控；`.env` 不進版控，範本放 `.env.example`。
