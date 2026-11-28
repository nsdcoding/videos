#!/bin/bash
# Generate the Short's 9:16 images (skips finished ones). Run from cant-hurt-me/.
STYLE="Screen-printed poster illustration matching the style of the reference image: warm light-grey textured paper with speckles, flat solid black ink silhouettes, deep crimson red as the only colour accent, rough grainy print edges, bold minimal shapes, generous empty space. Absolutely no text, no letters, no words, no title, no border."
python3 -c "import json,sys; [print(k+'\t'+v) for k,v in json.load(open(sys.argv[1])).items()]" short/prompts.json |
while IFS=$'\t' read -r k p; do
  [ -f "short/assets/$k.png" ] && continue
  echo "$k"; echo "$p"
done | paste - - | xargs -P 3 -d '\n' -I{} bash -c 'k=$(cut -f1 <<<"$1"); p=$(cut -f2 <<<"$1"); python3 ../gen.py image "$p $0" "short/assets/$k.png" --aspect 9:16 --ref assets/cover.png' "$STYLE" {}
