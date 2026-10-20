"""Render a time range of the film in parallel chunks and mux the narration.

  python3 render.py out.mp4 START END [JOBS]
"""
import os, subprocess, sys

out, t0, t1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
jobs = int(sys.argv[4]) if len(sys.argv) > 4 else os.cpu_count()
os.makedirs("build/chunks", exist_ok=True)
step = (t1 - t0) / jobs
bounds = [round((t0 + i * step) * 30) / 30 for i in range(jobs)] + [t1]
procs, parts = [], []
for i in range(jobs):
    part = f"build/chunks/part{i:02d}.mp4"
    parts.append(part)
    procs.append(subprocess.Popen([sys.executable, "film.py", "render", part, str(bounds[i]), str(bounds[i + 1])]))
for p in procs:
    assert p.wait() == 0
with open("build/chunks/list.txt", "w") as f:
    f.writelines(f"file '{os.path.basename(p)}'\n" for p in parts)
subprocess.check_call(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", "build/chunks/list.txt",
                       "-ss", str(t0), "-t", str(t1 - t0), "-i", "narration.mp3",
                       "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                       "-af", f"afade=t=out:st={t1 - t0 - 0.6}:d=0.6", "-shortest", out])
print("->", out)
