#!/bin/bash
# Render scenes (final quality, no cache), 3 in parallel; print each scene's QA result.  Usage: ./render_all.sh [stem ...]
cd "$(dirname "$0")"
all="s01_hook:S01Hook s02_welcome:S02Welcome s03_why:S03Why s04_crowd:S04Crowd s05_rule:S05Rule s06_again:S06Again s07_dials:S07Dials s08_real:S08Real s09_mistakes:S09Mistakes s10_recipe:S10Recipe s11_subscribe:S11Subscribe s12_next:S12Next"
if [ $# -gt 0 ]; then sel=""; for a in $all; do for w in "$@"; do [ "${a%%:*}" = "$w" ] && sel="$sel $a"; done; done; else sel=$all; fi
mkdir -p build
echo $sel | tr ' ' '\n' | xargs -P 3 -I{} bash -c 'f=${1%%:*}; c=${1##*:}; manim -qh --disable_caching --media_dir build/media scenes/$f.py $c > build/final_$f.log 2>&1 && echo "$c ok $(tr -d " \n" < build/qa/$c.json)" || echo "$c FAILED"' _ {}
