#!/usr/bin/env python3
"""BUILD_SPEC v3 section 3.2: key magenta cut-outs, split poses into rigs, split prop sheets.

  python3 build/cutout.py poses     # images/raw/pose_*.png  -> images/cast/<cast>_<pose>/{body,head,armL,armR}.png + rig.json
  python3 build/cutout.py props     # images/raw/props_*.png -> images/props/<prop>.png
  python3 build/cutout.py check     # images/check_*.png: every cut-out on a contrasting blue, for the eye check

Keying: soft matte from distance to the sampled background plus a magenta-ness term, holes keyed too,
despill on the edge pixels. A rig is the keyed figure cut at the neck (head) and, where the pose holds its
arms clear of the torso, at the shoulders (arms); pivots are stored in the pose image's own pixels.
"""
import glob, json, os, sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
DAY = os.path.dirname(HERE)
RAW = os.path.join(DAY, "images", "raw")
sys.path.insert(0, HERE)


def key(path):
    """RGBA float image with the magenta background keyed out (soft matte, despill)."""
    im = np.asarray(Image.open(path).convert("RGB")).astype(float)
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    mag = np.minimum(r, b) - g
    # the background is the magenta that covers most of the canvas (a stray frame round it is dropped below)
    sel = im[(mag > 30) & (r > 140) & (b > 90)]
    bg = np.median(sel, 0) if len(sel) > im.shape[0] * im.shape[1] * 0.2 else np.array([0, 0, 0])
    bgmag = min(bg[0], bg[2]) - bg[1]
    if bgmag < 30:
        sys.exit(f"STOP {os.path.basename(path)}: background is not magenta ({bg.round()})")
    d = np.linalg.norm(im - bg, axis=2)
    a = np.clip((d - 36) / 40, 0, 1)
    a = np.maximum(a, np.clip((bgmag * 0.55 - mag) / (bgmag * 0.25), 0, 1))
    mask = ndi.binary_opening(a > 0.5, iterations=2)
    mask = ndi.binary_fill_holes(mask)
    holes = mask & (mag > bgmag * 0.45) & (d < 70)
    holes = ndi.binary_opening(holes, iterations=2)
    mask &= ~holes
    lab, n = ndi.label(mask)  # anything touching the canvas edge is a frame, not the subject
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    if edge:
        mask &= ~np.isin(lab, list(edge))
    a = np.where(mask, np.maximum(a, ndi.binary_erosion(mask, iterations=2)), 0)
    spill = np.clip(mag - 10, 0, None) * (a < 1)
    out = im.copy()
    out[..., 0] -= spill * 0.6
    out[..., 2] -= spill * 0.8
    alpha = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7)))
    return np.dstack([np.clip(out, 0, 255), alpha]).astype(np.uint8)


def components(rgba, min_px):
    lab, n = ndi.label(rgba[..., 3] > 128)
    sizes = ndi.sum(np.ones_like(lab), lab, range(1, n + 1))
    return lab, [i + 1 for i, s in enumerate(sizes) if s >= min_px]


def crop(rgba, keep, pad=6):
    ys, xs = np.nonzero(keep)
    y0, y1, x0, x1 = max(0, ys.min() - pad), ys.max() + pad + 1, max(0, xs.min() - pad), xs.max() + pad + 1
    part = rgba[y0:y1, x0:x1].copy()
    k = ndi.binary_dilation(keep, iterations=3)[y0:y1, x0:x1]
    part[..., 3] = np.where(k, part[..., 3], 0)
    return part, (x0, y0)


def head_box(path, shape):
    """Head bounding box (y0, x0, y1, x1 in pixels) from Gemini 2.5 Flash, cached as <pose>_head.json."""
    cache = path.replace(".png", "_head.json")
    if not os.path.exists(cache):
        import base64
        sys.path.insert(0, os.path.join(os.path.dirname(DAY), "skills", "motion-video-style", "scripts"))
        import vertex_assets as va
        vx = va.Vertex()
        if not vx.creds.valid:
            vx.creds.refresh(vx.Request())
        prompt = ("Detect the head of the main cartoon figure: hair, face and any hat or cap, down to the chin, not the "
                  "neck or collar. Return JSON {\"box_2d\": [ymin, xmin, ymax, xmax]} normalised to 0-1000.")
        url = (f"https://aiplatform.googleapis.com/v1/projects/{vx.project}/locations/global/publishers/google/"
               "models/gemini-2.5-flash:generateContent")
        body = {"contents": [{"role": "user", "parts": [
            {"inlineData": {"mimeType": "image/png", "data": base64.b64encode(open(path, "rb").read()).decode()}},
            {"text": prompt}]}], "generationConfig": {"responseMimeType": "application/json",
                                                       "thinkingConfig": {"thinkingBudget": 0}}}
        r = vx.requests.post(url, json=body, timeout=300, headers={"Authorization": f"Bearer {vx.creds.token}"})
        r.raise_for_status()
        d = json.loads(r.json()["candidates"][0]["content"]["parts"][0]["text"])
        json.dump(d[0] if isinstance(d, list) else d, open(cache, "w"))
    b = json.load(open(cache))["box_2d"]
    h, w = shape
    pad = 0.015
    return (int((b[0] / 1000 - pad) * h), int((b[1] / 1000 - pad) * w),
            int((b[2] / 1000 + pad * 0.3) * h), int((b[3] / 1000 + pad) * w))


def split_pose(path, arms):
    """Body, head and (optionally) arms of one keyed pose. Returns {name: (rgba, (x, y))} and pivots."""
    rgba = key(path)
    lab, ids = components(rgba, 1500)
    fig = np.isin(lab, ids)
    ys, xs = np.nonzero(fig)
    top, bot = ys.min(), ys.max()
    hgt = bot - top
    parts, piv = {}, {"feet": [float(np.median(xs[ys > bot - 6])), float(bot)], "top": float(top)}
    # the head: a box from Gemini (cached next to the pose), then the figure inside it minus thin
    # things passing through (rifle barrels, straps), which stay on the body
    y0, x0, y1, x1 = head_box(path, fig.shape)
    yy, xx = np.mgrid[0:fig.shape[0], 0:fig.shape[1]]
    inbox = fig & (yy >= y0) & (yy <= y1) & (xx >= x0) & (xx <= x1)
    k = max(4, int((x1 - x0) * 0.12))
    disk = np.add.outer(np.arange(-k, k + 1) ** 2, np.arange(-k, k + 1) ** 2) <= k * k
    core = ndi.binary_opening(inbox, structure=disk)
    hl, hn = ndi.label(core)
    if not hn:
        sys.exit(f"STOP {os.path.basename(path)}: no head found")
    core = hl == np.argmax(np.bincount(hl[hl > 0]))
    head = ndi.binary_dilation(core, iterations=k + 2) & inbox
    hy, hx = np.nonzero(head)
    ny, nl, nr = hy.max(), hx[hy > hy.max() - 6].min(), hx[hy > hy.max() - 6].max()
    body = fig & ~head
    piv["neck"] = [float((nl + nr) / 2), float(ny)]
    matte = path.replace(".png", "_matte.png")
    if arms and os.path.exists(matte):
        m = np.asarray(Image.open(matte).convert("RGB")).astype(int)
        mr, mg, mb = m[..., 0], m[..., 1], m[..., 2]
        mfig = ~((mr > 150) & (mb > 100) & (mg < 120))
        iou = (fig & mfig).sum() / (fig | mfig).sum()
        if iou < 0.95:
            print(f"  {os.path.basename(path)}: matte does not line up (IoU {iou:.3f}); arms stay on the body")
            arms = False
        else:
            for side, sel in (("armL", (mg > 180) & (mr < 110) & (mb < 110)), ("armR", (mb > 180) & (mr < 110) & (mg < 110))):
                sl, sn = ndi.label(sel & fig)
                if not sn:
                    arms = False
                    break
                sleeve = sl == (np.argmax(np.bincount(sl[sl > 0])))
                sleeve = ndi.binary_closing(sleeve, iterations=3)
                py, px = np.nonzero(sleeve)
                # the hand: figure pixels just below the sleeve, within its width, connected to it
                below = fig & (yy >= py.max() - 6) & (yy < py.max() + hgt * 0.12) & \
                    (xx >= px[py > py.max() - 15].min() - 12) & (xx <= px[py > py.max() - 15].max() + 12)
                bl, bn = ndi.label(below)
                hand = np.zeros_like(fig)
                for i in range(1, bn + 1):
                    c = bl == i
                    if (c & ndi.binary_dilation(sleeve, iterations=3)).any():
                        hand |= c
                arm = (ndi.binary_dilation(sleeve, iterations=3) & fig) | hand
                arm &= ~head
                ay, ax = np.nonzero(arm)
                ytop = ay.min()
                piv[side] = [float(ax[ay < ytop + 10].mean()), float(ytop + 6)]
                parts[side] = crop(rgba, arm)
                body &= ~arm
    elif arms:
        arms = False
    parts["head"] = crop(rgba, head)
    parts["body"] = crop(rgba, body)
    return parts, piv, (rgba.shape[1], rgba.shape[0]), bool(arms)


def do_poses(only=()):
    import assets
    for path in sorted(glob.glob(os.path.join(RAW, "pose_*.png"))):
        cid_pose = None
        for pid in assets.POSES:
            if os.path.basename(path) == "pose_" + pid.replace("/", "_") + ".png":
                cid_pose = pid
        if not cid_pose or (only and cid_pose not in only):
            continue
        parts, piv, size, has_arms = split_pose(path, assets.POSES[cid_pose][1])
        out = os.path.join(DAY, "images", "cast", cid_pose.replace("/", "_"))
        os.makedirs(out, exist_ok=True)
        rig = {"size": size, "pivots": piv, "parts": {}, "arms": has_arms}
        for name, (img, off) in parts.items():
            Image.fromarray(img).save(os.path.join(out, f"{name}.png"))
            rig["parts"][name] = {"offset": [int(off[0]), int(off[1])]}
        json.dump(rig, open(os.path.join(out, "rig.json"), "w"), indent=1)
        print(f"{cid_pose}: parts {sorted(parts)}{'' if has_arms or not assets.POSES[cid_pose][1] else ' (arms not separable)'}")


def do_props(only=()):
    import assets
    out = os.path.join(DAY, "images", "props")
    os.makedirs(out, exist_ok=True)
    for sheet in assets.PROP_SHEETS:
        path = os.path.join(RAW, "props_" + "+".join(sheet) + ".png")
        if not os.path.exists(path) or (only and not set(only) & set(sheet)):
            continue
        rgba = key(path)
        lab, ids = components(rgba, 120)
        # group components into objects by their horizontal extent (a scatter of leaflets is one object)
        spans = []
        for i in ids:
            xs = np.nonzero((lab == i).any(0))[0]
            spans.append([xs.min(), xs.max(), [i]])
        spans.sort()
        groups = []
        for s in spans:
            if groups and s[0] <= groups[-1][1] + 30:
                groups[-1][1] = max(groups[-1][1], s[1])
                groups[-1][2] += s[2]
            else:
                groups.append(s)
        groups = [g for g in groups if np.isin(lab, g[2]).sum() > 2500]
        if len(groups) != len(sheet):
            sys.exit(f"STOP {os.path.basename(path)}: found {len(groups)} objects, expected {len(sheet)}")
        for name, g in zip(sheet, groups):
            img, _ = crop(rgba, np.isin(lab, g[2]))
            Image.fromarray(img).save(os.path.join(out, f"{name}.png"))
            print(f"prop {name}: {img.shape[1]}x{img.shape[0]}")


def check():
    """Every cut-out on a contrasting blue: rigs assembled and exploded, props side by side."""
    for kind in ("cast", "props"):
        tiles = []
        if kind == "cast":
            for d in sorted(glob.glob(os.path.join(DAY, "images", "cast", "*"))):
                rig = json.load(open(os.path.join(d, "rig.json")))
                W_, H_ = rig["size"]
                asm = Image.new("RGBA", (W_ * 2, H_), (40, 90, 200, 255))
                for name in ("body", "armL", "armR", "head"):
                    if name in rig["parts"]:
                        p = Image.open(os.path.join(d, f"{name}.png"))
                        ox, oy = rig["parts"][name]["offset"]
                        asm.alpha_composite(p, (ox, oy))
                        dx = {"head": 0, "body": 0, "armL": -60, "armR": 60}[name]
                        dy = {"head": -40, "body": 0, "armL": 0, "armR": 0}[name]
                        asm.alpha_composite(p, (W_ + ox + dx - W_ // 4, oy + dy + 30 if name != "head" else oy + dy + 30))
                tiles.append(asm.resize((W_ // 2, H_ // 4)).convert("RGB"))
        else:
            for f in sorted(glob.glob(os.path.join(DAY, "images", "props", "*.png"))):
                p = Image.open(f)
                k = 220 / max(p.size)
                t = Image.new("RGBA", (240, 240), (40, 90, 200, 255))
                q = p.resize((max(1, int(p.width * k)), max(1, int(p.height * k))))
                t.alpha_composite(q, ((240 - q.width) // 2, (240 - q.height) // 2))
                tiles.append(t.convert("RGB"))
        if not tiles:
            continue
        cols = 3 if kind == "cast" else 6
        tw, th = tiles[0].size
        sheet = Image.new("RGB", (cols * tw, -(-len(tiles) // cols) * th), (20, 40, 90))
        for i, t in enumerate(tiles):
            sheet.paste(t, ((i % cols) * tw, (i // cols) * th))
        sheet.save(os.path.join(DAY, "images", f"check_{kind}.png"))
        print("check", kind, len(tiles))


if __name__ == "__main__":
    cmd, rest = sys.argv[1], sys.argv[2:]
    {"poses": lambda: do_poses(rest), "props": lambda: do_props(rest), "check": check}[cmd]()
