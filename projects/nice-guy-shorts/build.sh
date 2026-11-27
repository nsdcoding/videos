#!/bin/bash
# usage: build.sh s2 s3 ...  -> <sid>/out/<sid>_with_promo.mp4 (+ _share)
set -e
cd "$(dirname "$0")"; ROOT=$PWD
for S in "$@"; do
  END=$(python3 -c "import json;t=json.load(open('$S/timing.json'));e=t[-1]['end']+0.6;print(round(round(e*30)/30,4))")
  mkdir -p $S/out/seg
  Q=$(python3 -c "e=$END;f=round(e*30);q=[round(round(f*k/4)/30,4) for k in range(5)];print(' '.join(map(str,q)))")
  set -- $Q; A=($Q)
  (cd render; for k in 0 1 2 3; do SID=$S node render.js video ${A[$k]} ${A[$((k+1))]} ../$S/out/seg/s$k.mp4 2>/dev/null & done; wait)
  printf "file 's%d.mp4'\n" 0 1 2 3 > $S/out/seg/list.txt
  ffmpeg -y -loglevel error -f concat -safe 0 -i $S/out/seg/list.txt -i $S/narration.wav -filter_complex "[1:a]apad=whole_dur=$END,aresample=48000[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -t $END $S/out/main.mp4
  ffmpeg -y -loglevel error -i $S/out/main.mp4 -i promo/promo.mp4 -filter_complex "[0:v]fps=30,format=yuv420p,setsar=1[v0];[1:v]scale=1080:1920,fps=30,format=yuv420p,setsar=1[v1];[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[1:a]aresample=48000,aformat=channel_layouts=stereo[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 20 -c:a aac -b:a 192k -movflags +faststart $S/out/${S}_with_promo.mp4
  ffmpeg -y -loglevel error -i $S/out/${S}_with_promo.mp4 -vf scale=720:1280 -c:v libx264 -crf 28 -c:a aac -b:a 128k -movflags +faststart $S/out/${S}_share.mp4
  echo "DONE $S $(ffprobe -v error -show_entries format=duration -of csv=p=0 $S/out/${S}_with_promo.mp4) $(du -h $S/out/${S}_with_promo.mp4|cut -f1) $(date +%T)"
done
