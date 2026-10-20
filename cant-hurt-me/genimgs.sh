#!/bin/bash
# usage: genimgs.sh prompts.json  -> assets/<key>.png (skips existing), 4 in parallel
STYLE="Screen-printed poster illustration matching the style of the reference image: warm light-grey textured paper with speckles, flat solid black ink silhouettes, deep crimson red as the only colour accent, rough grainy print edges, bold minimal shapes, generous empty space. Absolutely no text, no letters, no words, no title, no border."
python3 -c "import json,sys; [print(k+'\t'+v) for k,v in json.load(open(sys.argv[1])).items()]" "$1" | \
while IFS=$'\t' read -r k p; do
  [ -f "assets/$k.png" ] && continue
  echo "$k"; echo "$p"
done | paste - - | xargs -P 4 -d '\n' -I{} bash -c 'k=$(cut -f1 <<<"$1"); p=$(cut -f2 <<<"$1"); python3 ../gen.py image "$p $0" "assets/$k.png" --ref assets/cover.png' "$STYLE" {}
