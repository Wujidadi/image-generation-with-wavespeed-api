---
name: model-survey
description: 定期盤點 WaveSpeed 模型目錄的完整流程：比對快照找出新增、下架與改價的模型，逐檔位重新報價並與 documents/price.md 比對，檢查既有腳本的參數定義是否與線上 Input Schema 漂移，再同步 price.md、README 與調查文件，必要時為新模型撰寫腳本。當使用者說「探測／盤點新模型」「WaveSpeed 又上架了什麼」「更新價格總表」「重新調查價格」「檢查腳本參數是否過期」，或距離上次調查已有一段時間要更新現狀時叫用；只查單一模型的價格也可用本技能的 requote.py。
---

# model-survey：盤點模型目錄與價格

一次盤點分五段，前三段各有工具腳本，後兩段靠本文的檢查清單。全部呼叫的端點（`GET /api/v3/models`、`POST /api/v3/model/price`）都不扣費。

## 0. 先同步遠端

跑任何東西之前先 `git fetch` 並確認本機 main 沒有落後 origin/main。使用者可能在另一台機器做過調查並推上去，直接在舊基底上工作會製造衝突與重工。

## 1. 目錄差異

```sh
python3 tools/models_snapshot.py --type text-to-image
```

寫入當日快照並與最新一份既有快照比對，列出新增（標示是否已有腳本）、下架、改價的文生圖模型。要指定基準用 `--since <日期>`；`--diff-only` 只比對不呼叫 API。
`base_price` 只是底價，改價判斷以第 2 段的逐檔報價為準。

## 2. 重新報價

```sh
python3 .claude/skills/model-survey/scripts/requote.py            # 全部腳本，約數分鐘
python3 .claude/skills/model-survey/scripts/requote.py <腳本名稱>… # 只測指定模型
```

對每個腳本以全預設參數報價，再把每個參數單獨拉到其他檔位（choices 逐一、布林旗標翻轉、整數取 Schema 上限、自由字串 `size` 取驗證器放行的各級尺寸），最後把所有會改價的參數同時拉到最低與最高再報一次，因為解析度與搜尋旗標之類的加價會疊加。輸出每個模型的「預設價格、價格區間、影響計費的參數、折扣」四欄，並列出與 `price.md` 不同的列。
工具已處理兩個容易出錯的細節，改動時不要退回去：報價請求的參數要放在 `inputs` 欄位（放錯欄位不報錯、所有檔位都回底價）；`BooleanOptionalAction` 旗標要翻轉試算，`num_images` 要取上限。

## 3. Schema 漂移

```sh
python3 .claude/skills/model-survey/scripts/schema_drift.py
```

比對每支腳本的 choices／default 與線上 Schema 的 enum／default，列出腳本有 Schema 沒有、Schema 有腳本沒有（圖生圖與 LoRA 欄位略過）的參數，以及已從目錄消失的模型。慣例是預設值跟官方走，所以 default 不同時改腳本；新欄位是否開放依 AGENTS.md「慣例」判斷。

## 4. 同步文件

三份文件的數字互相牽連，改任何一處都要一起看：

- `documents/price.md`：改列、插列（依預設價格降序、同價依模型 ID 排序）、更新檔頭 `retrieved` 與「已串接的 N 個文生圖模型」。
- `README.md`：模型專屬參數表（依腳本名稱排序）、「共 N 個模型」、目錄結構表的 `price.md` 說明。
- `.claude/plans/model-pricing-and-test-cost.md`：檔頭 `updated`、模型總數、`resolution` 採用數、`quality` 等計費參數的模型清單、折扣模型數與折扣表。

時間戳以指令取得（`python3 -c "from datetime import datetime; print(datetime.now().astimezone().isoformat(timespec='seconds'))"`），表格改完跑 `md-fmt --tables-only`；新列若加寬欄位，整張表會重排，commit 說明要註明內容只有新增列。

## 5. 新模型腳本（視需要）

先把候選清單（模型 ID、預設價、折扣）給使用者挑，確認後再寫；LoRA 變體與圖生圖端點依慣例不寫。每支腳本：

- 參數以第 1 段快照同日的線上 Schema 為準，用 `wavespeed schema <模型 ID>` 或目錄回傳的 `request_schema` 查，`enum`、`default` 原樣照抄，自由字串 `size` 的上下限用 `ws.size_type()` 在本機擋。
- 檔名依 `wavespeed_common.output_slug` 推算，寫完以 `./wsgen --list` 確認看得到；以 `WAVESPEED_API_KEY=invalid` 執行確認 payload，不實際扣費。
- 用 `requote.py <腳本名稱>` 取得價格四欄再填進三份文件。
- 若共享的執行環境（`$DRIVE/CCK Shared/ai/image-generation/wavespeed/scripts/env` 與 `model-list.txt`）需要登記輸出目錄，一併加列；之後的分級實測交給 `rating-test` 技能。

## 回報格式

- 開頭一句：目錄總數變化、文生圖新增／下架／改價各幾個。
- 已更新的現狀：改價模型與新舊價格、預設值跟進的腳本、文件計數。
- 新上架且尚無腳本的候選表（模型 ID、預設價格、折扣），讓使用者點名要寫哪些。
- 提交分成「價格與快照（docs）」「共用規則變更」「新腳本（feat）」等獨立意圖，依 `my-commit` 技能撰寫訊息。
