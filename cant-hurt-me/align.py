"""Align script sentences to narration.mp3 using pauses (silencedetect) + speaking rate.

Writes build/timing.json: [{"i", "sec", "text", "start", "end", "parts": [[start, end, text], ...]}]
"""
import json, re

def load_sentences():
    out, sec = [], 0
    for line in open("script.md", encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("#"):
            sec += 1
            out.append({"sec": sec, "text": line.lstrip("# ").strip(), "head": True})
            continue
        for s in re.split(r"(?<=[।.?!])\s+", line):
            if s.strip():
                out.append({"sec": sec, "text": s.strip(), "head": False})
    return out

def load_silences():
    vals = [float(l.split()[1]) for l in open("build/sil.txt")]
    return [(vals[i], vals[i + 1]) for i in range(0, len(vals) - 1, 2)]

def weight(t):  # rough spoken length in characters (ignore marks)
    return len(re.sub(r"[\s,।.?!]", "", t)) + 0.6 * len(re.findall(r"[,]", t))

sents, sils = load_sentences(), load_silences()
total = sils[-1][0] if sils[-1][1] >= 960 else 961.0
speech = total - sum(b - a for a, b in sils)
W = [weight(s["text"]) for s in sents]
rate = speech / sum(W)
N, M = len(sents), len(sils)
# candidate boundaries = midpoint of each silence; DP picks N-1 of them in order
mid = [(a + b) / 2 for a, b in sils]
dur = [b - a for a, b in sils]
INF = 1e18
# dp[i][j]: sentence i ends at silence j
import math
start0 = sils[0][1] if sils[0][0] < 0.5 else 0.0
dp = [[INF] * M for _ in range(N)]
bk = [[-1] * M for _ in range(N)]
def cost(i, t0, t1, j):
    exp = rate * W[i]
    got = t1 - t0
    c = (got - exp) ** 2 / max(exp, 0.6)
    return c - 2.5 * min(dur[j], 1.2)  # prefer long pauses as sentence ends
for j in range(M):
    t1 = sils[j][0]
    if t1 > start0:
        dp[0][j] = cost(0, start0, t1, j)
for i in range(1, N):
    exp = rate * W[i]
    for j in range(M):
        best, arg = INF, -1
        t1 = sils[j][0]
        for k in range(j - 1, -1, -1):
            t0 = sils[k][1]
            if t1 - t0 > exp * 3 + 4:
                break
            v = dp[i - 1][k]
            if v < INF:
                v += cost(i, t0, t1, j)
                if v < best:
                    best, arg = v, k
        dp[i][j], bk[i][j] = best, arg
# last sentence should end at final silence (or audio end)
j = min(range(M), key=lambda j: dp[N - 1][j] + (0 if j >= M - 2 else 50))
ends = [0] * N
for i in range(N - 1, -1, -1):
    ends[i] = j
    j = bk[i][j]
res = []
for i, s in enumerate(sents):
    t0 = start0 if i == 0 else sils[ends[i - 1]][1]
    t1 = sils[ends[i]][0]
    # split long sentences into subtitle parts at commas, snapping to inner pauses
    chunks = [c.strip() for c in re.split(r"(?<=,)\s+", s["text"]) if c.strip()]
    merged = []
    for c in chunks:
        if merged and (weight(merged[-1]) < 22 or weight(c) < 10):
            merged[-1] += " " + c
        else:
            merged.append(c)
    parts, acc, tw = [], t0, sum(weight(c) for c in merged)
    inner = [x for x in sils if t0 < x[0] and x[1] < t1]
    cum = 0
    for k, c in enumerate(merged):
        cum += weight(c)
        if k == len(merged) - 1:
            e = t1
        else:
            guess = t0 + (t1 - t0) * cum / tw
            near = min(inner, key=lambda x: abs((x[0] + x[1]) / 2 - guess), default=None)
            e = near[0] if near and abs((near[0] + near[1]) / 2 - guess) < 1.5 else guess
        parts.append([round(acc, 2), round(e, 2), c])
        acc = near[1] if k < len(merged) - 1 and near and e == near[0] else e
    res.append({"i": i, "sec": s["sec"], "head": s["head"], "text": s["text"],
                "start": round(t0, 2), "end": round(t1, 2), "parts": parts})
json.dump(res, open("build/timing.json", "w"), ensure_ascii=False, indent=1)
print(f"{N} sentences, {M} pauses, rate {rate:.3f}s/char, total {total:.1f}s")
for r in res[:22]:
    print(f"{r['start']:7.2f} {r['end']:7.2f}  {r['text'][:50]}")
print("...")
for r in res[-4:]:
    print(f"{r['start']:7.2f} {r['end']:7.2f}  {r['text'][:50]}")
