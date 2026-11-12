import json, math
d = json.load(open('timing.json')); L = d['lines']; FPS = 30
idx = {l['id']: i for i, l in enumerate(L)}
def cut_before(lid):
    i = idx[lid]; a = L[i-1]['start'] + L[i-1]['dur']; b = L[i]['start']; return (a + b) / 2
cuts = [0, cut_before('d01'), cut_before('e01'), cut_before('f32'), cut_before('h01'), cut_before('j01'), d['total']]
parts = []; jobs = []
for p in range(6):
    f0, f1 = round(cuts[p] * FPS), round(cuts[p+1] * FPS)
    parts.append(dict(name=f'part{p+1}', f0=f0, f1=f1, t0=f0/FPS, t1=f1/FPS))
    n = math.ceil((f1 - f0) / 600)
    for k in range(n):
        a = f0 + k * (f1 - f0) // n; b = f0 + (k + 1) * (f1 - f0) // n
        jobs.append(dict(name=f'p{p+1}_{k:02d}', f0=a, f1=b))
json.dump(parts, open('parts.json', 'w'), indent=1); json.dump(jobs, open('jobs.json', 'w'), indent=1)
for p in parts: print(p['name'], round(p['t0'],1), round(p['t1'],1), round((p['t1']-p['t0'])/60,2),'min')
print(len(jobs), 'jobs')
