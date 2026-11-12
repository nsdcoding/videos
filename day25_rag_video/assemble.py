"""Concat rendered segments into parts, mux the matching slice of mix.wav. Output: out/Day25_RAG_PartN.mp4"""
import json, subprocess, os, sys
SEG = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
parts = json.load(open('parts.json')); jobs = json.load(open('jobs.json'))
for i, p in enumerate(parts, 1):
    lst = os.path.join(SEG, f"list{i}.txt")
    with open(lst, 'w') as f:
        for j in jobs:
            if j['name'].startswith(f"p{i}_"): f.write(f"file '{os.path.abspath(os.path.join(SEG, j['name'] + '.mp4'))}'\n")
    out = os.path.join(OUT, f"Day25_RAG_Part{i}.mp4")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst,
                    '-ss', f"{p['t0']:.4f}", '-t', f"{p['t1'] - p['t0']:.4f}", '-i', 'mix.wav',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2',
                    '-movflags', '+faststart', '-shortest', out], check=True)
    print(out, round(os.path.getsize(out) / 1e6, 1), 'MB')
