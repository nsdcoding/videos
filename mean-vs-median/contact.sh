#!/bin/bash
# contact.sh video.mp4 out.png [offset_seconds] — one frame every 2.5 s, 5 columns, timestamped (global time)
v=$1; out=$2; off=${3:-0}
FONT=/usr/share/fonts/opentype/inter/Inter-Bold.otf
ffmpeg -v error -y -i "$v" -vf "fps=0.4,scale=576:-1,drawtext=fontfile=$FONT:text='%{eif\:t*2.5+$off\:d}s':x=8:y=8:fontsize=26:fontcolor=white:box=1:boxcolor=black@0.6,tile=5x0:padding=4:color=gray" -frames:v 1 "$out" 2>/dev/null || \
ffmpeg -v error -y -i "$v" -vf "fps=0.4,scale=576:-1,drawtext=fontfile=$FONT:text='%{n}':x=8:y=8:fontsize=26:fontcolor=white:box=1:boxcolor=black@0.6,tile=5x8:padding=4:color=gray" -frames:v 1 "$out"
