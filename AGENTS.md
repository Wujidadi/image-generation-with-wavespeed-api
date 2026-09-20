# Image Generation with WaveSpeed API

## 架構

- `scripts/wavespeed_common.py` 是唯一的共用邏輯：金鑰載入、提示詞讀取與註解過濾、輸出目錄檢查、任務提交、輪詢重試、`--task-id` 取回、下載。
  流程性的修改一律改這裡，不在各模型腳本重複實作。
  參數檢核也放這裡：`ws.size_type()` 產生 `--size` 的型別函式（收 `寬x高`，可指定單邊、總像素與長寬比上下限），`ws.number_type()` 產生數值範圍檢核。
- 各模型腳本 `scripts/<模型名稱>.py` 只做三件事：定義 `MODEL_ID`、以 `add_model_args(parser)` 加入模型專屬參數、以 `build_payload(args, prompt)` 回傳 `prompt` 以外的請求欄位，最後呼叫 `ws.run(MODEL_ID, add_model_args, build_payload)`。
- 檔名即模型名稱，規則是模型 ID 去掉供應商前綴、斜線改連字號，例如 `x-ai/grok-imagine-image-v2.0/text-to-image` 對應 `grok-imagine-image-v2.0-text-to-image.py`。
  `wsgen --list` 與預設輸出目錄都依此規則自動推算，新增腳本不需改 `wsgen`。
  例外是去掉前綴後只剩任務類別的模型 ID：`midjourney/text-to-image` 會保留供應商，對應 `midjourney-text-to-image.py`，判斷依據是 `wavespeed_common.TASK_SLUGS`。

## 慣例

- 只用 Python 標準函式庫，不引入第三方套件。
- 參數的可選值、預設值與範圍以 `documents/` 下的官方文件為準（`llms/` 內的 Input Schema 最精確），不憑記憶填寫。
  `documents/` 尚未收錄的模型，改以 `GET /api/v3/models` 回傳的 `api_schema.api_schemas[].request_schema` 為準，那是同一份 Input Schema 的線上版本。
- 圖生圖參數（`image`、`mask_image`、`reference`、`sref`、`strength`）不在本專案範圍，各腳本一律不開放。
- 命令列參數值若含 `*` 之類的 shell 特殊字元，提供不需引號的替代寫法，例如 `--size` 接受 `寬x高`。
- 錯誤一律以 `sys.exit("中文訊息")` 結束，不讓例外堆疊外洩；所有會扣費的請求之前，先完成本機端的檢查。
- 測試時以無效金鑰（`WAVESPEED_API_KEY=invalid`）驗證參數解析與 payload 組裝，或以 `--task-id` 取回既有任務，避免實際扣費。
  需要確認費用時以 `POST /api/v3/model/price` 報價，該端點不扣費；各模型的價格與計費參數整理在 `documents/price.md`。
- 圖片輸出不進版控；`.env` 不進版控，範本放 `.env.example`。

## 官方 CLI（輔助工具）

官方 CLI `@wavespeed/cli`（指令 `wavespeed`，以 0.4.8 實測）只作為輔助工具，`wsgen` 與 `scripts/` 不得呼叫官方 CLI，理由見 `README.md` 的「與官方 CLI 的關係」。
遇到下列場景時，官方 CLI 是可用的途徑之一。

- 前置條件：
  - 安裝指令為 `npm install -g @wavespeed/cli`，需要 Node 18 以上。
  - 官方 CLI 讀取環境變數 `WAVESPEED_API_KEY`，在專案根目錄以 `set -a && source ./.env && set +a` 帶入即可，不需執行 `wavespeed login`。
  - 沒有金鑰時所有子命令都無法使用，包含 `wavespeed schema` 與 `wavespeed models`。
- 找出尚未撰寫腳本的模型：`wavespeed models -t text-to-image --json`，再與 `scripts/*.py` 的檔名比對。
- 查 Input Schema：`wavespeed schema <模型 ID>`，或欄位表相同的 `wavespeed run <模型 ID> -h`。
  - `--json` 輸出原始 Schema；模型目錄快取 1 小時，`--refresh` 強制更新。
  - `size` 欄位只有 `type: string` 與預設值，沒有單邊、總像素與長寬比的上下限，`ws.size_type()` 需要的數值仍以 `documents/` 的官方文件為準。
  - 欄位表會列出圖生圖參數，撰寫腳本時照「慣例」排除。
- 不扣費報價：`wavespeed price <模型 ID> -p test -i key=value --json`，資料來源與 `POST /api/v3/model/price` 相同。
- 臨時試用尚未撰寫腳本的模型：`wavespeed run <模型 ID> -p "提示詞" -i key=value --download`，此指令會扣費。
  - `run` 的送出前檢核不涵蓋可選值：`output_format=bmp` 之類的錯誤值仍會送到伺服器，由伺服器回覆 `Invalid request body` 拒絕。
  - `-i` 的值含 `*` 時必須加引號，例如 `-i 'size=1024*1024'`，否則 zsh 會因 glob 無匹配而中止指令。
- 以任務 ID 取回既有任務：`wavespeed show <任務 ID> --download`，功能等同 `--task-id`，不扣費。
- 查帳：`wavespeed balance`、`wavespeed history --since <日期>`、`wavespeed billings`、`wavespeed usage`，這四項在本專案沒有對應功能。
  - `GET /api/v3/balance` 回傳的餘額只到小數第 2 位，且為無條件捨去（網頁顯示 $27.249658 時回傳 27.24），`wavespeed balance` 原樣輸出該數值；完整精度只能在官方網頁查到。
  - `wavespeed billings --json` 的單筆金額（`order.price`）保有完整精度，例如 0.024。
