#!/bin/bash
# Render scenes (final quality, no cache), 3 in parallel; print each scene's QA result.
# Usage: ./render_all.sh [stem ...]   e.g. ./render_all.sh s01_hook s04_lesson   (no args = every scene)
cd "$(dirname "$0")"
all=""
for f in scenes/s*.py; do
  c=$(grep -oP 'class \K\w+(?=\(Base\))' "$f" | head -1); [ -n "$c" ] && all="$all $(basename "$f" .py):$c"
done
if [ $# -gt 0 ]; then sel=""; for a in $all; do for w in "$@"; do [ "${a%%:*}" = "$w" ] && sel="$sel $a"; done; done; else sel=$all; fi
mkdir -p build
echo $sel | tr ' ' '\n' | xargs -P 3 -I{} bash -c 'f=${1%%:*}; c=${1##*:}; manim -qh --disable_caching --media_dir build/media scenes/$f.py $c > build/final_$f.log 2>&1 && echo "$c ok $(tr -d " \n" < build/qa/$c.json)" || echo "$c FAILED (see build/final_$f.log)"' _ {}
