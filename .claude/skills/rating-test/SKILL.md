---
name: rating-test
description: 對 WaveSpeed 文生圖模型做普通級（G）、輔導級（PG-13）、限制級（R18）三級生圖實測，把推論時長、價格、檔名與被擋狀態整理成表格，附加到三份實測紀錄 Markdown 的最下方待人工評圖後併入。當使用者說「三級測試」「G／PG13／R18 實測」「測新模型的分級效果」「跑一輪 rating test」「把新腳本加進實測表」，或新增模型腳本後要補實測紀錄時叫用。路徑與提示詞都有預設值（共享雲端目錄），可在對話中或以設定檔覆蓋。
---

# rating-test：三級生圖實測

對指定的模型腳本，以三個固定提示詞各生一張圖，記錄推論時長、是否被內容審查擋下與輸出檔名，產成與既有實測表同欄位的表格。
評圖（效果欄的表情符號與備註）由人工完成，本技能只負責跑圖與產表。

## 預設值與覆蓋

預設值集中在 `config.zsh`，每個變數都以 `: ${VAR:=預設}` 宣告，所以**環境變數優先於設定檔**。覆蓋方式有三種，依需要擇一：

1. 對話中指定：使用者說「提示詞改用 xxx」「結果寫到另一份 md」時，以環境變數帶入單次執行，例如 `PROMPT_PG13='nsfw/xxx.txt' zsh scripts/run-rating-test.zsh …`。
2. 另一套環境：複製 `config.zsh` 改好路徑，以 `--config <檔案>` 或 `RATING_TEST_CONFIG=<檔案>` 指定。
3. 直接改 `config.zsh`：只在使用者明確要改預設值時這麼做。

| 變數                                    | 預設值                                            | 用途                                                         |
| --------------------------------------- | ------------------------------------------------- | ------------------------------------------------------------ |
| `SHARED_DIR`                            | `$DRIVE/CCK Shared/ai/image-generation/wavespeed` | 共享目錄根                                                   |
| `WS_ENV`                                | `$SHARED_DIR/scripts/env`                         | 提供 `PROMPT_DIR`、`WS_OUTDIRS`、`ws_outdir`（輸出目錄對照） |
| `PROMPT_G`／`PROMPT_PG13`／`PROMPT_R18` | 見 `config.zsh`                                   | 三個等級統一使用的提示詞檔，相對於 `PROMPT_DIR`              |
| `REVIEW_G`／`REVIEW_PG13`／`REVIEW_R18` | `$SHARED_DIR/reviews/…`                          | 三份實測紀錄 Markdown                                        |
| `PRICE_MD`                              | 本倉庫 `documents/price.md`                       | 價格與帳戶折扣來源                                           |
| `RESULTS_DIR`                           | `$TMPDIR/rating-test`                             | 原始 log 與 `meta.json` 存放處                               |

## 流程

1. **確認模型清單**。使用者通常點名模型；沒點名時用 `--models-missing-from-review` 列出 `scripts/` 內尚未出現在第一個等級實測表中的腳本，先把清單給使用者確認再跑，因為每張圖都會扣費。
2. **確認輸出目錄已登記**。`ws_outdir` 只認 `WS_ENV` 裡 `WS_OUTDIRS` 登記過的腳本名；新模型要先在 `$SHARED_DIR/scripts/env` 與同目錄的 `model-list.txt` 加一列（兩檔內容相同，短名慣例如 `nano-banana-2.1`、`flux-3-klein-base`），runner 會在送出任何請求前擋下未登記的模型。
3. **乾跑**：加 `--dry-run` 看結果目錄、等級與模型清單，確認無誤再正式跑。
4. **正式跑**：
   ```sh
   zsh .claude/skills/rating-test/scripts/run-rating-test.zsh [--ratings G,PG13,R18] <腳本名稱>...
   ```
   三個等級平行、等級內循序；單一模型最長 300 秒（`wsgen` 的 `--timeout`），五個模型約 5 到 10 分鐘，適合放背景執行。每個模型的完整輸出在 `<結果目錄>/<等級>/<腳本名稱>.log`。
5. **產表並附加**：
   ```sh
   python3 .claude/skills/rating-test/scripts/append-results.py <結果目錄>
   ```
   先加 `--print-only` 檢視，再正式附加。表格以「## <日期> 新增模型實測（待併入上表）」為標題接在各 Markdown 最下方，不動既有表格；有 `md-fmt` 時會自動對齊表格。
6. **回報**：列出每個模型在三個等級的時長與是否被擋，提醒使用者評圖後自行併入主表，並說明 `.html` 未重新產生（合併後以 `md2html <檔案>` 不帶參數轉出）。

## 表格規則

- 欄位與既有表一致：G 表為「模型、腳本、價格、時長、檔名、備註」，PG-13 與 R18 表多一欄「效果」。
- 效果欄只對被擋（error code 1200，`Content flagged as potentially sensitive`）的列填 😡，其餘留空給人工評圖；被擋不扣款。
- 價格為 `price.md` 的預設價格乘以帳戶折扣率，例如 90％ 折扣的 $0.040 記為 0.0360，與既有表一致。
- 時長取官方回報的 `timings.inference` 毫秒數換算為秒，保留三位小數。
- 成功的列依時長升序，被擋的列排在最後再依時長升序，與主表「擋住和逾時一律依時長升序」的慣例相同。
- 非 1200 的失敗（逾時、5xx）在備註欄寫「失敗：<訊息>」，效果欄留空，讓人判斷要不要重跑。

## 注意

- `wsgen` 必須在 PATH（本倉庫的 `wsgen` 通常以符號連結放在 `~/.local/bin`）。
- 共享 `env` 會 `source` 本倉庫的 `.env` 取得 `WAVESPEED_API_KEY` 與 `WAVESPEED_OUTPUT_PATH`，缺任一項 `wsgen` 會自行報錯。
- 同一模型要重測時直接再跑一次，產表時以最新結果目錄為準；不要手動合併兩次的 log。
