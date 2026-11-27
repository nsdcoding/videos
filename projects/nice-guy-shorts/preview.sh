#!/bin/bash
# usage: preview.sh <sid> t1,t2,...   -> contact sheet in scratchpad
set -e
SP=/tmp/claude-0/-home-user-videos/a9e25f70-53d5-50d9-9f4a-0e0f150679fc/scratchpad
O="$SP/prev_$1_$(date +%s)"; mkdir -p "$O"
cd "$(dirname "$0")/render" && SID=$1 node render.js stills "$2" "$O"
python3 - "$O" <<'P'
import sys,glob
from PIL import Image
o=sys.argv[1]; fs=sorted(glob.glob(o+'/f_*.jpg'),key=lambda f:float(f.split('_')[-1][:-4]))
sh=Image.new('RGB',(len(fs)*300,534))
for i,f in enumerate(fs): sh.paste(Image.open(f).resize((300,534)),(i*300,0))
sh.save(o+'/sheet.jpg'); print(o+'/sheet.jpg')
P
