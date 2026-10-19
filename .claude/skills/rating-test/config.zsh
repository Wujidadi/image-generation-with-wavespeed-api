# rating-test 的預設設定；每個變數都可在載入前由環境變數覆蓋（已有值就不改）。
# 另一套環境可複製本檔、改掉路徑後，以 --config <檔案> 或 RATING_TEST_CONFIG=<檔案> 指定。

# 共享目錄：含 scripts/env（PROMPT_DIR、WS_OUTDIRS、ws_outdir）與 reviews/
: ${SHARED_DIR:="$DRIVE/CCK Shared/ai/image-generation/wavespeed"}
: ${WS_ENV:="$SHARED_DIR/scripts/env"}

# 三個等級統一使用的提示詞檔，相對於 scripts/env 內的 PROMPT_DIR
: ${PROMPT_G:='sfw/one-woman/ancient-ch-woman-standing-gloomy-indoor.txt'}
: ${PROMPT_PG13:='nsfw/panties-exposed/asian-squat/white-shirt-gray-sweater-black-skirt-black-socks-with-garter-belt.txt'}
: ${PROMPT_R18:='nsfw/sex/kpop-idol-reverse-cowgirl.txt'}

# 三份實測紀錄 Markdown
: ${REVIEW_G:="$SHARED_DIR/reviews/sfw/g-actual-measurement.md"}
: ${REVIEW_PG13:="$SHARED_DIR/reviews/nsfw/pg13-actual-measurement.md"}
: ${REVIEW_R18:="$SHARED_DIR/reviews/nsfw/r18-actual-measurement.md"}

# 價格總表（預設價格與帳戶折扣的來源）
: ${PRICE_MD:="${PROJECT_ROOT:-${${(%):-%x}:A:h:h:h:h}}/documents/price.md"}

# 原始執行紀錄與 meta.json 的存放處
: ${RESULTS_DIR:="${TMPDIR:-/tmp}/rating-test"}
