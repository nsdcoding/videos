"""Split a keyed RGBA image into pieces at vertical gaps; keep the chosen piece(s)."""
import sys, numpy as np
from PIL import Image
im = Image.open(sys.argv[1]); a = np.asarray(im)
col = (a[..., 3] > 40).sum(0)
occ = col > 3
segs = []; s = None
for x, o in enumerate(list(occ) + [False]):
    if o and s is None: s = x
    if not o and s is not None:
        if x - s > 30: segs.append((s, x))
        s = None
out = []
for (x0, x1) in segs:
    sub = a[:, x0:x1]; rows = np.where((sub[..., 3] > 40).sum(1) > 0)[0]
    out.append((x0, x1, rows[0], rows[-1]))
print([(x1 - x0, y1 - y0) for x0, x1, y0, y1 in out])
mode = sys.argv[3] if len(sys.argv) > 3 else "slim"
if mode == "slim":   # keep the narrowest-for-its-height piece (the full-body figure)
    x0, x1, y0, y1 = min(out, key=lambda r: (r[1] - r[0]) / (r[3] - r[2] + 1))
    Image.fromarray(a[max(0, y0 - 4):y1 + 4, max(0, x0 - 4):x1 + 4]).save(sys.argv[2])
else:                # save all pieces with numbered suffix
    for k, (x0, x1, y0, y1) in enumerate(out):
        Image.fromarray(a[max(0, y0 - 4):y1 + 4, max(0, x0 - 4):x1 + 4]).save(f"{sys.argv[2]}_{k}.png")
