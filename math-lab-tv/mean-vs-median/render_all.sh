#!/bin/bash
# Render every scene (final quality, no cache), 3 in parallel; print each scene's QA result.
cd "$(dirname "$0")"
scenes="s01_two_towns:S01TwoTowns s01b_welcome:S01bWelcome s02_why:S02Why s03_mean:S03Mean s04_median:S04Median s05_stress:S05Stress s06_trust:S06Trust s07_real:S07Real s08_mistakes:S08Mistakes s09_recipe:S09Recipe s09b_subscribe:S09bSubscribe s10_next:S10Next"
echo $scenes | tr ' ' '\n' | xargs -P 4 -I{} bash -c 'f=${1%%:*}; c=${1##*:}; manim -qh --disable_caching --media_dir build/media scenes/$f.py $c > build/final_$f.log 2>&1 && echo "$c ok $(tr -d " \n" < build/qa/$c.json)" || echo "$c FAILED"' _ {}
