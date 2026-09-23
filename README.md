# Image Generation with WaveSpeed API

以 [WaveSpeed](https://wavespeed.ai/) 的 REST API 進行文生圖的腳本集，只依賴 Python 3 標準函式庫。

## 環境需求

- Python 3.10 以上。
- WaveSpeed API 金鑰，二擇一設定：
  - 環境變數 `WAVESPEED_API_KEY`。
  - 專案根目錄的 `.env` 檔，格式見 `.env.example`。
    既有環境變數優先，`.env` 只補上未設定的變數。

## 使用方式

`wsgen` 是共用入口，以 `-m/--model` 指定模型，其餘參數原樣轉交給對應的 `scripts/<模型名稱>.py`。
可從任意目錄執行，也可建立符號連結放進 `PATH`。

```bash
./wsgen --list
./wsgen -m seedream-v4.5 --size 1440x2560
./wsgen -m grok-imagine-image-v2.0-text-to-image -p prompts/xxx.txt -o output/xxx --resolution 1k
./wsgen -m seedream-v4.5 --help
```

模型名稱可寫腳本名、含 `.py` 的檔名，或 `bytedance/seedream-v4.5` 形式的模型 ID。
直接執行 `python3 scripts/<模型名稱>.py ...` 效果相同。

### 共用參數

| 參數                  | 預設值                | 說明                                             |
| --------------------- | --------------------- | ------------------------------------------------ |
| `-p`, `--prompt-file` | `prompts/default.txt` | 提示詞檔案，行首為 `#` 或 `//` 的整行視為註解    |
| `--prompt`            | 無                    | 直接指定提示詞文字，與 `--prompt-file` 互斥      |
| `-o`, `--output-dir`  | `output/<模型名稱>/`  | 輸出目錄，不存在時遞迴建立，提交任務前先檢查可寫 |
| `--task-id`           | 無                    | 不重新提交，直接取回既有任務的輸出               |
| `--poll-interval`     | `2`                   | 輪詢間隔秒數                                     |
| `--timeout`           | `300`                 | 等待結果的上限秒數                               |

### 模型專屬參數

共 48 個模型。各參數的可選值與預設值以 `./wsgen -m <模型名稱> --help` 為準。
「每張價格」為全用預設參數時的單張定價，括號內是把計費參數拉到最低與最高檔位的範圍；
完整的價格區間、影響計費的參數與帳戶折扣見 [模型價格總表](documents/price.md)，
調查方法與測試成本見 [模型價格調查與測試成本](.claude/plans/model-pricing-and-test-cost.md)。

| 腳本名稱                                 | 模型 ID                                               | 每張價格                   | 專屬參數                                                                                        |
| ---------------------------------------- | ----------------------------------------------------- | -------------------------- | ----------------------------------------------------------------------------------------------- |
| `cosmos-3-super-text-to-image`           | `nvidia/cosmos-3-super/text-to-image`                 | $0.040                     | `--negative-prompt` `--size` `--num-inference-steps` `--guidance-scale` `--output-format`       |
| `flux-2-dev-text-to-image`               | `wavespeed-ai/flux-2-dev/text-to-image`               | $0.012                     | `--size` `--seed`                                                                               |
| `flux-2-flash-text-to-image`             | `wavespeed-ai/flux-2-flash/text-to-image`             | $0.025                     | `--size` `--seed`                                                                               |
| `flux-2-flex-text-to-image`              | `wavespeed-ai/flux-2-flex/text-to-image`              | $0.060                     | `--size` `--seed`                                                                               |
| `flux-2-klein-9b-text-to-image`          | `wavespeed-ai/flux-2-klein-9b/text-to-image`          | $0.010                     | `--size` `--seed`                                                                               |
| `flux-2-klein-base-9b-text-to-image`     | `wavespeed-ai/flux-2-klein-base-9b/text-to-image`     | $0.015                     | `--size` `--seed`                                                                               |
| `flux-2-max-text-to-image`               | `wavespeed-ai/flux-2-max/text-to-image`               | $0.070                     | `--size` `--seed`                                                                               |
| `flux-2-turbo-text-to-image`             | `wavespeed-ai/flux-2-turbo/text-to-image`             | $0.040                     | `--size` `--seed`                                                                               |
| `flux-dev-ultra-fast`                    | `wavespeed-ai/flux-dev-ultra-fast`                    | $0.005（$0.005 ～ $0.020） | `--size` `--num-inference-steps` `--seed` `--guidance-scale` `--num-images` `--output-format`   |
| `flux-dev`                               | `wavespeed-ai/flux-dev`                               | $0.012（$0.012 ～ $0.048） | `--size` `--num-inference-steps` `--seed` `--guidance-scale` `--num-images` `--output-format`   |
| `glm-image-text-to-image`                | `z-ai/glm-image/text-to-image`                        | $0.120                     | `--size` `--seed` `--output-format`                                                             |
| `gpt-image-2-text-to-image`              | `openai/gpt-image-2/text-to-image`                    | $0.060（$0.010 ～ $0.220） | `--aspect-ratio` `--resolution` `--quality` `--output-format`                                   |
| `gpt-image-2.5-flare-text-to-image`      | `openai/gpt-image-2.5-flare/text-to-image`            | $0.024（$0.010 ～ $0.360） | `--aspect-ratio` `--resolution` `--quality` `--output-format`                                   |
| `gpt-image-2.5-sunburst-text-to-image`   | `openai/gpt-image-2.5-sunburst/text-to-image`         | $0.024（$0.010 ～ $0.360） | `--aspect-ratio` `--resolution` `--quality` `--output-format`                                   |
| `grok-imagine-image-v2.0-text-to-image`  | `x-ai/grok-imagine-image-v2.0/text-to-image`          | $0.050                     | `--aspect-ratio` `--resolution` `--quality`                                                     |
| `hunyuan-image-2.1`                      | `wavespeed-ai/hunyuan-image-2.1`                      | $0.025                     | `--size` `--seed` `--output-format`                                                             |
| `hunyuan-image-3`                        | `wavespeed-ai/hunyuan-image-3`                        | $0.100                     | `--size` `--seed`                                                                               |
| `hunyuan-image-3-instruct-text-to-image` | `wavespeed-ai/hunyuan-image-3-instruct/text-to-image` | $0.450                     | `--size` `--seed`                                                                               |
| `ideogram-v4`                            | `ideogram-ai/ideogram-v4`                             | $0.050（$0.025 ～ $0.100） | `--resolution` `--aspect-ratio` `--quality` `--output-format`                                   |
| `kling-image-v3-text-to-image`           | `kwaivgi/kling-image-v3/text-to-image`                | $0.028（$0.028 ～ $0.252） | `--aspect-ratio` `--resolution` `--num-images` `--output-format`                                |
| `krea-v2-large-text-to-image`            | `wavespeed-ai/krea-v2-large/text-to-image`            | $0.060                     | `--aspect-ratio` `--creativity`                                                                 |
| `krea-v2-medium-text-to-image`           | `wavespeed-ai/krea-v2-medium/text-to-image`           | $0.030                     | `--aspect-ratio` `--output-format`                                                              |
| `krea-v2-medium-turbo-text-to-image`     | `wavespeed-ai/krea-v2-medium-turbo/text-to-image`     | $0.015                     | `--aspect-ratio` `--creativity`                                                                 |
| `krea-v2-turbo`                          | `wavespeed-ai/krea-v2/turbo`                          | $0.012（$0.012 ～ $0.024） | `--aspect-ratio` `--resolution` `--seed`                                                        |
| `midjourney-text-to-image`               | `midjourney/text-to-image`                            | $0.100（$0.100 ～ $0.150） | `--aspect-ratio` `--hd` `--quality` `--stylize` `--chaos` `--weird` `--seed`                    |
| `minimax-h3-text-to-image`               | `wavespeed-ai/minimax-h3/text-to-image`               | $0.020（$0.020 ～ $0.060） | `--aspect-ratio` `--resolution` `--output-format` `--seed`                                      |
| `nano-banana-2-lite-text-to-image`       | `google/nano-banana-2-lite/text-to-image`             | $0.040                     | `--aspect-ratio` `--output-format`                                                              |
| `nano-banana-2-text-to-image-fast`       | `google/nano-banana-2/text-to-image-fast`             | $0.045（$0.045 ～ $0.064） | `--aspect-ratio` `--resolution` `--enable-web-search` `--output-format`                         |
| `nano-banana-2-text-to-image`            | `google/nano-banana-2/text-to-image`                  | $0.070（$0.045 ～ $0.168） | `--aspect-ratio` `--resolution` `--enable-web-search` `--enable-image-search` `--output-format` |
| `nano-banana-pro-text-to-image-ultra`    | `google/nano-banana-pro/text-to-image-ultra`          | $0.150（$0.150 ～ $0.180） | `--aspect-ratio` `--resolution` `--output-format`                                               |
| `nano-banana-pro-text-to-image`          | `google/nano-banana-pro/text-to-image`                | $0.140（$0.140 ～ $0.240） | `--aspect-ratio` `--resolution` `--output-format`                                               |
| `qwen-image-2.0-pro-text-to-image`       | `wavespeed-ai/qwen-image-2.0-pro/text-to-image`       | $0.070                     | `--size` `--seed`                                                                               |
| `qwen-image-2.0-text-to-image`           | `wavespeed-ai/qwen-image-2.0/text-to-image`           | $0.030                     | `--size` `--seed`                                                                               |
| `qwen-image-2.1-text-to-image`           | `wavespeed-ai/qwen-image-2.1/text-to-image`           | $0.020（$0.020 ～ $0.080） | `--aspect-ratio` `--resolution` `--output-format` `--seed`                                      |
| `qwen-image-3.0-pro-text-to-image`       | `alibaba/qwen-image-3.0-pro/text-to-image`            | $0.040（$0.040 ～ $0.075） | `--aspect-ratio` `--resolution` `--enable-prompt-expansion` `--seed`                            |
| `qwen-image-3.0-text-to-image`           | `alibaba/qwen-image-3.0/text-to-image`                | $0.030                     | `--aspect-ratio` `--resolution` `--enable-prompt-expansion` `--seed`                            |
| `qwen-image-text-to-image-2512`          | `wavespeed-ai/qwen-image/text-to-image-2512`          | $0.020                     | `--size` `--seed` `--output-format`                                                             |
| `qwen-image-text-to-image`               | `wavespeed-ai/qwen-image/text-to-image`               | $0.020                     | `--size` `--seed` `--output-format`                                                             |
| `seedream-v4.5`                          | `bytedance/seedream-v4.5`                             | $0.040                     | `--size`                                                                                        |
| `seedream-v4`                            | `bytedance/seedream-v4`                               | $0.027                     | `--size`                                                                                        |
| `seedream-v5.0-lite`                     | `bytedance/seedream-v5.0-lite`                        | $0.035                     | `--size` `--output-format`                                                                      |
| `seedream-v5.0-pro`                      | `bytedance/seedream-v5.0-pro`                         | $0.045（$0.045 ～ $0.090） | `--aspect-ratio` `--resolution` `--output-format` `--prompt-optimization-mode`                  |
| `wan-2.5-text-to-image`                  | `alibaba/wan-2.5/text-to-image`                       | $0.030                     | `--negative-prompt` `--size` `--enable-prompt-expansion` `--seed`                               |
| `wan-2.6-text-to-image`                  | `alibaba/wan-2.6/text-to-image`                       | $0.030                     | `--size` `--enable-prompt-expansion` `--seed`                                                   |
| `wan-2.7-text-to-image-pro`              | `alibaba/wan-2.7/text-to-image-pro`                   | $0.075                     | `--size` `--thinking-mode` `--seed`                                                             |
| `wan-2.7-text-to-image`                  | `alibaba/wan-2.7/text-to-image`                       | $0.030                     | `--size` `--thinking-mode` `--seed`                                                             |
| `z-image-base`                           | `wavespeed-ai/z-image/base`                           | $0.010                     | `--size` `--seed` `--output-format`                                                             |
| `z-image-turbo`                          | `wavespeed-ai/z-image/turbo`                          | $0.005                     | `--size` `--seed` `--output-format`                                                             |

`--size` 一律接受 `寬x高` 與 `寬*高` 兩種寫法，前者在 shell 中不需加引號。
各模型的單邊、總像素與長寬比上限不同，超出範圍時在送出請求前就會被擋下，不會扣費。
這道本機檢核是必要的：部分模型（例如 `seedream-v5.0-lite`）收到過小的尺寸不會回報錯誤，而是靜默改用其他尺寸並照常扣費。

### 輸出與補救

- 輸出檔名為 `<任務建立時間>-<任務 ID>.<副檔名>`，時間為本地時區；多張輸出時再加序號。
- 任務提交後以任務 ID 輪詢結果。輪詢階段遇到連線中斷或伺服器 5xx 會自動重試，直到 `--timeout`。
- 若仍失敗，任務通常已在雲端完成，改用 `--task-id <任務 ID>` 即可重新取回，不會再次扣費。

## 與官方 CLI 的關係

WaveSpeed 官方提供 Node.js 撰寫的 CLI（`npm install -g @wavespeed/cli`，指令為 `wavespeed`），生成圖片的主要流程不使用官方 CLI：

- 官方 CLI 需要 Node 18 以上與 99 個 npm 套件，本專案只用 Python 標準函式庫。
- 官方 CLI 與 `scripts/wavespeed_common.py` 呼叫的是同一組 REST 端點，包一層子行程只會多一個故障點。
- 官方 CLI 的參數錯誤要送到伺服器才被擋下；本專案在送出請求之前，就在本機完成尺寸、數值範圍與可選值的檢核。
- 官方 CLI 的 Input Schema 不含 `size` 的單邊、總像素與長寬比上下限，也會開放本專案刻意排除的圖生圖參數。
- 提示詞檔的註解過濾、依模型名稱推算的輸出目錄、中文錯誤訊息，官方 CLI 都沒有對應功能。

官方 CLI 仍用於主要流程以外的輔助工作：

- 瀏覽模型目錄，找出尚未撰寫腳本的模型：`wavespeed models -t text-to-image`；要知道自上次調查以來上架了哪些模型，改用 `tools/models_snapshot.py`（見「模型目錄快照」）
- 臨時試用尚未撰寫腳本的模型：`wavespeed run <模型 ID> -p "提示詞" --download`
- 查詢模型的 Input Schema：`wavespeed schema <模型 ID>`
- 不扣費報價：`wavespeed price <模型 ID> -p test`
- 查帳：`wavespeed balance`、`wavespeed history`、`wavespeed billings`、`wavespeed usage`

官方 CLI 會讀取環境變數 `WAVESPEED_API_KEY`，與本專案的 `.env` 共用同一把金鑰，不需另外執行 `wavespeed login`。

## 模型目錄快照

`GET /api/v3/models` 沒有上架日期欄位，要知道一段時間內新增了哪些模型，只能靠前後兩份目錄快照比對。
`tools/models_snapshot.py` 把目錄存成 `documents/snapshots/models-<日期>.json`（不含 Input Schema），並與最新一份既有快照比對；呼叫該端點不扣費。

```sh
python3 tools/models_snapshot.py                        # 擷取今日快照並與最新一份既有快照比對
python3 tools/models_snapshot.py --type text-to-image   # 只列文生圖模型，並標示是否已有腳本
python3 tools/models_snapshot.py --since 2026-09-20     # 指定比對基準
python3 tools/models_snapshot.py --diff-only            # 不呼叫 API，只比對既有快照
```

每次調查模型（新增腳本、更新價格）時先執行一次，快照隨調查結果一起提交。

## 目錄結構

| 路徑                          | 內容                                                                    |
| ----------------------------- | ----------------------------------------------------------------------- |
| `wsgen`                       | 共用入口腳本                                                            |
| `scripts/wavespeed_common.py` | 共用邏輯：金鑰載入、提示詞讀取、提交、輪詢、下載                        |
| `scripts/<模型名稱>.py`       | 各模型腳本，只定義模型 ID、專屬參數與 payload                           |
| `prompts/`                    | 提示詞檔                                                                |
| `output/`                     | 預設輸出目錄，圖片副檔名已在 `.gitignore` 排除                          |
| `documents/`                  | 官方 API 文件、原始 HTML 與 llms.txt；`price.md` 為 48 個模型的價格總表 |
| `documents/snapshots/`        | 模型目錄快照，由 `tools/models_snapshot.py` 產生                        |
| `tools/models_snapshot.py`    | 擷取模型目錄快照並與前一份比對，列出新增、下架與改價的模型              |
| `.claude/plans/`              | 調查與規劃文件，含價格調查方法與測試成本估算                            |
| `sdk/sample/`                 | 官方模型頁 Quick start 的 cURL、Node.js、Python 範例                    |
