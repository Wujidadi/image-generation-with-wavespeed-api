#!/usr/bin/env zsh
# 對指定模型跑普通級（G）、輔導級（PG13）、限制級（R18）的生圖測試，原始輸出存成 log。
#
# 用法：
#   run-rating-test.zsh [--config 檔案] [--ratings G,PG13,R18] [--dry-run] <模型腳本名稱>...
#   run-rating-test.zsh --ratings PG13 --models-missing-from-review   # 只測實測表尚未收錄的模型
#
# 每個等級各自循序執行，三個等級彼此平行；結束後印出 RESULTS_DIR，交給 append-results.py 產表。

emulate -L zsh
setopt err_return pipe_fail

SKILL_DIR="${${(%):-%x}:A:h:h}"
PROJECT_ROOT="${SKILL_DIR:h:h:h}"
export PROJECT_ROOT

typeset -a ratings=(G PG13 R18) models
typeset config_file="${RATING_TEST_CONFIG:-$SKILL_DIR/config.zsh}"
typeset dry_run=false missing_only=false

while (( $# )); do
  case "$1" in
    --config) config_file="$2"; shift 2 ;;
    --ratings) ratings=(${(s:,:)2}); shift 2 ;;
    --dry-run) dry_run=true; shift ;;
    --models-missing-from-review) missing_only=true; shift ;;
    -h|--help) sed -n '2,8p' "${(%):-%x}" | sed 's/^# \{0,1\}//'; return 0 ;;
    -*) print -u2 -r -- "未知參數：$1"; return 2 ;;
    *) models+=("$1"); shift ;;
  esac
done

[[ -f $config_file ]] || { print -u2 -r -- "找不到設定檔：$config_file"; return 1 }
source "$config_file"
[[ -f $WS_ENV ]] || { print -u2 -r -- "找不到共享 env：$WS_ENV"; return 1 }
source "$WS_ENV"
(( $+functions[ws_outdir] )) || { print -u2 -r -- "共享 env 未定義 ws_outdir：$WS_ENV"; return 1 }
command -v wsgen >/dev/null || { print -u2 -r -- "找不到 wsgen，請先把 $PROJECT_ROOT/wsgen 加入 PATH"; return 1 }

for r in $ratings; do
  [[ $r == (G|PG13|R18) ]] || { print -u2 -r -- "等級只能是 G、PG13、R18：$r"; return 2 }
done

if $missing_only; then
  # 以第一個等級的實測表為準，列出 scripts/ 內尚未出現在表中的腳本
  typeset review_var="REVIEW_${ratings[1]}" review_file
  review_file="${(P)review_var}"
  for script in "$PROJECT_ROOT"/scripts/*.py(N); do
    name="${script:t:r}"
    [[ $name == wavespeed_common ]] && continue
    grep -q -- "| $name " "$review_file" || models+=("$name")
  done
fi
(( ${#models} )) || { print -u2 -r -- "沒有要測的模型"; return 2 }

# 事前檢查：腳本存在、輸出目錄已登記、提示詞檔存在，任何一項失敗都不送出會扣費的請求
typeset -A prompt_of=(G "$PROMPT_G" PG13 "$PROMPT_PG13" R18 "$PROMPT_R18")
for m in $models; do
  [[ -f "$PROJECT_ROOT/scripts/$m.py" ]] || { print -u2 -r -- "找不到腳本：scripts/$m.py"; return 1 }
  ws_outdir "$m" >/dev/null || { print -u2 -r -- "請先在 $WS_ENV 的 WS_OUTDIRS 登記 $m 的輸出目錄"; return 1 }
done
for r in $ratings; do
  [[ -f "$PROMPT_DIR/${prompt_of[$r]}" ]] || { print -u2 -r -- "找不到提示詞檔：$PROMPT_DIR/${prompt_of[$r]}"; return 1 }
done

typeset stamp="$(date +%Y%m%dT%H%M%S)"
typeset run_dir="$RESULTS_DIR/$stamp"
mkdir -p "$run_dir"
python3 - "$run_dir/meta.json" "$PRICE_MD" "$REVIEW_G" "$REVIEW_PG13" "$REVIEW_R18" "$PROMPT_G" "$PROMPT_PG13" "$PROMPT_R18" <<'EOF'
import json, sys
out, price, rg, rp, rr, pg, pp, pr = sys.argv[1:]
json.dump({"price_md": price,
           "reviews": {"G": rg, "PG13": rp, "R18": rr},
           "prompts": {"G": pg, "PG13": pp, "R18": pr}}, open(out, "w"), ensure_ascii=False, indent=1)
EOF

print -r -- "結果目錄：$run_dir"
print -r -- "等級：${(j:, :)ratings}"
print -r -- "模型：${(j:, :)models}"
if $dry_run; then
  print -r -- "（--dry-run：未送出任何請求）"
  return 0
fi

run_rating() {
  local rating="$1" prompt="$PROMPT_DIR/${prompt_of[$1]}" m outdir
  mkdir -p "$run_dir/$rating"
  for m in $models; do
    outdir="$(ws_outdir "$m")"
    wsgen -m "$m" -p "$prompt" -o "$outdir" > "$run_dir/$rating/$m.log" 2>&1
    print -r -- "exit=$?" >> "$run_dir/$rating/$m.log"
    print -r -- "[$rating] $m 完成"
  done
}

for r in $ratings; do
  run_rating "$r" &
done
wait
print -r -- "全部完成，接著執行："
print -r -- "  python3 \"$SKILL_DIR/scripts/append-results.py\" \"$run_dir\""
