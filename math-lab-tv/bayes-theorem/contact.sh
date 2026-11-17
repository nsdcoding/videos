#!/bin/bash
# contact.sh video.mp4 out_prefix — one frame every 2.5 s, 5x8 tiles per page, numbered (frame n = n*2.5 s into the scene)
v=$1; out=$2
FONT=/usr/share/fonts/opentype/inter/Inter-Bold.otf
ffmpeg -v error -y -i "$v" -vf "fps=0.4,scale=576:-1,drawtext=fontfile=$FONT:text='%{n}':x=8:y=8:fontsize=26:fontcolor=white:box=1:boxcolor=black@0.6,tile=5x8:padding=4:color=gray" "${out}_%02d.png"
