"""Day 02 motion engine (BUILD_SPEC v3): one paper world of set plates, rigged cut-out cast, props,
photo cards and ink graphics, under a log-zoom camera.

Built on the Day 01 engine (same timeline, camera swoop and subtitle rules) with what v3 adds:
- sets are full-bleed plates, each a 1920x1080 station placed somewhere in one continuous world
- cast are rigs (body, head, arms) keyed from magenta poses; idle breathing, head tilt, arm swing
- photo cards: never cropped or altered, matte from the photo's own dark tones, caption on the matte,
  low_res photos never larger than native size, contents move at most 6% in scale
- energy: `still` beats and structural silences (pause_after >= 2000) stop every animation clock
"""
import json, math, os
import numpy as np
import skia

W, H, FPS = 1920, 1080, 30
HERE = os.path.dirname(os.path.abspath(__file__))
DAY = os.path.dirname(HERE)
SAMPLING = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear)
CUBIC = skia.SamplingOptions(skia.CubicResampler.Mitchell())

# palette (BUILD_SPEC 3.1)
INK = (0x26 / 255, 0x39 / 255, 0x2b / 255)
MUSTARD = (0xd4 / 255, 0xa6 / 255, 0x40 / 255)
CREAM = (0xf3 / 255, 0xe7 / 255, 0xcf / 255)
OLIVE = (0x6d / 255, 0x6a / 255, 0x3a / 255)
RUST = (0xb5 / 255, 0x52 / 255, 0x2f / 255)
OFFWHITE = (0.96, 0.94, 0.90)

FONTS = os.path.join(HERE, "fonts")
_tf = {}


def font(name, size):
    path = name if name.startswith("/") else os.path.join(FONTS, name)
    if path not in _tf:
        _tf[path] = skia.Typeface.MakeFromFile(path)
    f = skia.Font(_tf[path], size)
    f.setSubpixel(True)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    return f


def head_font(size):   # tags, labels, numbers
    return font("Baloo2-800.ttf", size)


def semi_font(size):
    return font("Baloo2-600.ttf", size)


def title_font(size):  # display serif
    return font("RozhaOneRegular.ttf", size)


def body_font(size, bold=False):  # subtitles, captions (sans-serif)
    return font("MuktaBold.ttf" if bold else "MuktaMedium.ttf", size)


def col(rgb, a=1.0):
    return skia.Color4f(rgb[0], rgb[1], rgb[2], max(0.0, min(1.0, a)))


def stroke(rgb, w, a=1.0):
    return skia.Paint(Color=col(rgb, a), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w,
                      StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)


def fill(rgb, a=1.0):
    return skia.Paint(Color=col(rgb, a), AntiAlias=True)


def shadow_paint(a=0.3, blur=12):
    p = fill((0, 0, 0), a)
    p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    return p


# ---------------------------------------------------------------- easing

def clamp01(x):
    return 0.0 if x < 0 else 1.0 if x > 1 else x


def smooth(x):
    x = clamp01(x)
    return x * x * x * (x * (6 * x - 15) + 10)


def in_out(x):
    x = clamp01(x)
    return x * x * (3 - 2 * x)


def out_cubic(x):
    x = clamp01(x)
    return 1 - (1 - x) ** 3


def in_cubic(x):
    x = clamp01(x)
    return x ** 3


def out_back(x, k=1.7):
    x = clamp01(x)
    return 1 + (k + 1) * (x - 1) ** 3 + k * (x - 1) ** 2


def lerp(a, b, t):
    return a + (b - a) * t


# ---------------------------------------------------------------- timing

class Timeline:
    """Segment timings, word-time estimates, and the clock freezes: structural silences
    (pause_after >= 2000) and `energy: still` beats."""

    def __init__(self, build=None):
        d = json.load(open(os.path.join(DAY, "audio", "timings.json")))
        self.total = d["total"]
        self.segs = {s["id"]: s for s in d["segments"]}
        self.order = [s["id"] for s in d["segments"]]
        self.silences = [(s["end"], s["end"] + s["pause_after"] / 1000)
                         for s in d["segments"] if s["pause_after"] >= 2000]
        self.freezes = list(self.silences)
        build = build or json.load(open(os.path.join(DAY, "build.json")))
        for b in build["beats"]:
            if b["energy"] == "still":
                self.freezes.append((self.start(b["segments"][0]), self.next_start(b["segments"][-1])))
        self.freezes.sort()

    def start(self, sid):
        return self.segs[sid]["start"]

    def end(self, sid):
        return self.segs[sid]["end"]

    def next_start(self, sid):
        s = self.segs[sid]
        return s["end"] + s["pause_after"] / 1000

    def _units(self, text):
        u = []
        for ch in text:
            w = 1.0
            if ch in ".!?":
                w += 9
            elif ch in ",;:":
                w += 4
            elif ch in "—-":
                w += 2
            u.append(w)
        return np.cumsum([0] + u)

    def at(self, sid, phrase, nth=0):
        """Estimated time at which `phrase` begins in segment `sid` (character position, punctuation-weighted)."""
        s = self.segs[sid]
        text = s["text"]
        idx = -1
        for _ in range(nth + 1):
            idx = text.find(phrase, idx + 1)
        if idx < 0:
            raise KeyError(f"{phrase!r} not in {sid}")
        cu = self._units(text)
        return s["start"] + (s["end"] - s["start"]) * cu[idx] / cu[-1]

    def anim_time(self, t):
        """Animation clock: stopped inside every freeze."""
        for a, b in self.freezes:
            if a <= t < b:
                return a
        return t

    def frozen(self, t):
        return any(a <= t < b for a, b in self.freezes)


# ---------------------------------------------------------------- images

def load_rgba(path, size=None):
    from PIL import Image
    im = Image.open(path).convert("RGBA")
    if size:
        im = im.resize(size, Image.LANCZOS)
    return np.asarray(im)


def to_skia(arr):
    return skia.Image.fromarray(np.ascontiguousarray(arr), colorType=skia.kRGBA_8888_ColorType).withDefaultMipmaps()


def dark_tone(arr):
    """Matte colour sampled from a photograph's own dark tones (spec 4.4), never pure black."""
    rgb = arr[..., :3].reshape(-1, 3).astype(float)
    lum = rgb @ [0.299, 0.587, 0.114]
    sel = rgb[lum <= np.percentile(lum, 10)]
    c = sel.mean(0) / 255
    return tuple(max(v, 0.08) for v in c)


def make_paper(size=1024, seed=3, base=CREAM):
    """Tileable cream paper with mottling and fine grain."""
    from scipy.ndimage import gaussian_filter
    rng = np.random.default_rng(seed)
    f = np.zeros((size, size))
    for k, amp in ((4, 0.012), (16, 0.008), (64, 0.006), (size, 0.016)):
        n = rng.normal(0, 1, (k, k))
        n = np.kron(n, np.ones((size // k, size // k)))
        if k < size:
            n = gaussian_filter(n, size / k / 2, mode="wrap")
            n /= n.std() + 1e-9
        f += n * amp
    rgb = np.stack([base[0] + f, base[1] + f * 0.97, base[2] + f * 0.92], -1)
    a = np.clip(rgb * 255, 0, 255).astype(np.uint8)
    return np.dstack([a, np.full((size, size), 255, np.uint8)])


# ---------------------------------------------------------------- drawing primitives

def text(c, s, x, y, f, rgb, a=1.0, align="left", tracking=0.0):
    p = fill(rgb, a)
    w = text_width(s, f, tracking)
    x0 = x - (w if align == "right" else w / 2 if align == "center" else 0)
    if tracking == 0:
        c.drawString(s, x0, y, f, p)
    else:
        for ch in s:
            c.drawString(ch, x0, y, f, p)
            x0 += f.measureText(ch) + tracking
    return w


def text_width(s, f, tracking=0.0):
    return sum(f.measureText(ch) + tracking for ch in s) - tracking if tracking else f.measureText(s)


def partial(path, p):
    if p >= 1:
        return path
    out = skia.Path()
    if p <= 0:
        return out
    pm = skia.PathMeasure(path, False)
    while True:
        L = pm.getLength()
        pm.getSegment(0, L * p, out, True)
        if not pm.nextContour():
            break
    return out


def poly(points, closed=False):
    p = skia.Path()
    p.moveTo(*points[0])
    for q in points[1:]:
        p.lineTo(*q)
    if closed:
        p.close()
    return p


def arc_path(cx, cy, r, a0=-90, sweep=360):
    p = skia.Path()
    p.addArc(skia.Rect.MakeLTRB(cx - r, cy - r, cx + r, cy + r), a0, sweep)
    return p


def curve(p0, p1, bend=0.25):
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    p = skia.Path()
    p.moveTo(*p0)
    p.quadTo(mx - dy * bend, my + dx * bend, *p1)
    return p


def point_on(path, p):
    pm = skia.PathMeasure(path, False)
    pos, tan = pm.getPosTan(pm.getLength() * clamp01(p))
    return (pos.x(), pos.y()), math.degrees(math.atan2(tan.y(), tan.x()))


def dashed(paint, on=14, off=12):
    paint.setPathEffect(skia.DashPathEffect.Make([on, off], 0))
    return paint


# ---------------------------------------------------------------- stations and elements

class El:
    def __init__(self, t0, draw, until=None, fade=0.25, z=0, realtime=False):
        self.t0, self.draw, self.until, self.fade, self.z, self.realtime = t0, draw, until, fade, z, realtime


class Station:
    """A 1920x1080 card in the world at centre (x, y), scale s. Elements draw in card-local pixels."""

    def __init__(self, name, x, y, s=1.0, reveal=None):
        """reveal=(z0, z1): a place nested inside another plate fades in as the on-screen scale
        (camera zoom x s) grows from z0 to z1, so diving into it reads as one move."""
        self.name, self.x, self.y, self.s, self.reveal = name, x, y, s, reveal
        self.els = []

    def add(self, t0, draw, until=None, fade=0.25, z=0, realtime=False):
        self.els.append(El(t0, draw, until, fade, z, realtime))
        return draw

    def matrix(self):
        m = skia.Matrix()
        m.setTranslate(self.x - W * self.s / 2, self.y - H * self.s / 2)
        m.preScale(self.s, self.s)
        return m

    def world(self, lx, ly):
        return (self.x + (lx - W / 2) * self.s, self.y + (ly - H / 2) * self.s)

    def alpha(self, zoom):
        if not self.reveal:
            return 1.0
        z0, z1 = self.reveal
        return smooth((zoom * self.s - z0) / (z1 - z0))

    def render(self, c, ta, t=None, zoom=1.0):
        al = self.alpha(zoom)
        if al <= 0:
            return
        c.save()
        c.concat(self.matrix())
        if al < 1:
            c.saveLayerAlpha(None, int(255 * al))
        for e in sorted(self.els, key=lambda e: e.z):
            ta_e = t if (e.realtime and t is not None) else ta
            if ta_e < e.t0:
                continue
            if e.until is not None and ta_e >= e.until + e.fade:
                continue
            if e.until is not None and ta_e >= e.until:
                k = 1 - (ta_e - e.until) / e.fade if e.fade else 0
                c.saveLayerAlpha(None, int(255 * clamp01(k)))
                e.draw(c, ta_e - e.t0)
                c.restore()
            else:
                e.draw(c, ta_e - e.t0)
        if al < 1:
            c.restore()
        c.restore()


# ---------------------------------------------------------------- element builders (card-local)

def plate(img):
    """A set plate, full bleed on its station (a hair oversized so drift never shows an edge)."""
    r = skia.Rect.MakeXYWH(-24, -14, W + 48, H + 28)

    def draw(c, age):
        c.drawImageRect(img, r, CUBIC, skia.Paint(AntiAlias=True))
    return draw


def sprite(img, x, y, w, anchor=(0.5, 0.5), entry="pop", dur=0.5, rot=0.0, wobble=0.0, seed=0.0,
           path=None, flip=False, exit_at=None, exit="shrink"):
    """A cut-out image at (x, y) with width w. entry: pop | rise | drop | slide_l | slide_r | fade | none.
    `path` (skia.Path) flies it along an arc over `dur`. `wobble` adds a gentle float (degrees)."""
    iw, ih = img.width(), img.height()
    h = w * ih / iw

    def draw(c, age):
        p = clamp01(age / dur)
        sx = sy = 1.0
        dx = dy = 0.0
        a = 1.0
        r = rot
        if path is not None:
            (px, py), _ = point_on(path, in_out(p))
            dx, dy = px - x, py - y
            r = rot + (1 - in_out(p)) * 20
        elif entry == "pop":
            sx = sy = out_back(p)
            r = rot - 8 * (1 - out_cubic(p))
            a = min(1, p * 3)
        elif entry == "rise":
            dy = 70 * (1 - out_cubic(p))
            a = out_cubic(p)
        elif entry == "drop":
            dy = -260 * (1 - out_back(p, 1.2))
            a = min(1, p * 4)
        elif entry == "slide_l":
            dx = -W * 0.7 * (1 - out_cubic(p))
        elif entry == "slide_r":
            dx = W * 0.7 * (1 - out_cubic(p))
        elif entry == "fade":
            a = smooth(p)
        if wobble:
            r += math.sin(age * 1.3 + seed) * wobble
            dy += math.sin(age * 1.7 + seed * 2) * wobble * 2.5
        if exit_at is not None and age > exit_at:
            q = clamp01((age - exit_at) / 0.35)
            if exit == "shrink":
                sx = sy = sx * (1 - in_cubic(q))
            else:
                dy += 80 * in_cubic(q)
                a *= 1 - q
        if a <= 0 or sx <= 0:
            return
        c.save()
        c.translate(x + dx, y + dy)
        c.rotate(r)
        c.scale(sx * (-1 if flip else 1), sy)
        rect = skia.Rect.MakeXYWH(-w * anchor[0], -h * anchor[1], w, h)
        if a < 1:
            c.saveLayerAlpha(None, int(255 * a))
            c.drawImageRect(img, rect, SAMPLING, skia.Paint(AntiAlias=True))
            c.restore()
        else:
            c.drawImageRect(img, rect, SAMPLING, skia.Paint(AntiAlias=True))
        c.restore()
    return draw


def tag(s, x, y, size=40, rgb=INK, bg=CREAM, rot=0.0, dur=0.45, pin=False, border=True):
    """A pill label with a hard offset shadow, popping in with overshoot; optionally pinned at an angle."""
    f = head_font(size)
    tw = text_width(s, f)
    pw, ph = tw + size * 0.9, size * 1.35

    def draw(c, age):
        p = out_back(age / dur)
        if p <= 0:
            return
        c.save()
        c.translate(x, y)
        c.rotate(rot - 10 * (1 - out_cubic(age / dur)))
        c.scale(p, p)
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-pw / 2, -ph / 2, pw, ph), ph * 0.32, ph * 0.32)
        if border:
            c.drawRRect(rr.makeOffset(6, 6) if hasattr(rr, "makeOffset") else rr, fill(INK))
        c.drawRRect(rr, fill(bg))
        if border:
            c.drawRRect(rr, stroke(INK, 4))
        text(c, s, 0, size * 0.36, f, rgb, 1, "center")
        if pin:
            c.drawCircle(0, -ph / 2 - 2, 9, fill(RUST))
            c.drawCircle(0, -ph / 2 - 2, 9, stroke(INK, 3))
        c.restore()
    draw.size = (pw, ph)
    return draw


def headline(s, x, y, size=72, rgb=INK, align="center", dur=0.5, rise=30, f=None):
    f = f or head_font(size)

    def draw(c, age):
        p = out_cubic(age / dur)
        if p <= 0:
            return
        text(c, s, x, y + rise * (1 - p), f, rgb, p, align)
    return draw


def typewriter(s, x, y, size=34, rgb=INK, cps=26, align="left", f=None, caret=True):
    f = f or semi_font(size)
    full = text_width(s, f)

    def draw(c, age):
        n = int(age * cps)
        if n <= 0:
            return
        sub = s[:n]
        x0 = x - (full if align == "right" else full / 2 if align == "center" else 0)
        text(c, sub, x0, y, f, rgb, 1)
        if caret and n < len(s) + 6 and int(age * 3) % 2 == 0:
            cx = x0 + text_width(sub, f) + 4
            c.drawRect(skia.Rect.MakeXYWH(cx, y - size * 0.75, 3, size * 0.85), fill(rgb))
    return draw


def ink(path, rgb=INK, w=7, dur=0.6, dash=None, ease=in_out, a=1.0):
    def draw(c, age):
        p = ease(age / dur)
        if p <= 0:
            return
        pt = stroke(rgb, w, a)
        if dash:
            dashed(pt, *dash)
        c.drawPath(partial(path, p), pt)
    return draw


def arrow(p0, p1, bend=0.2, rgb=INK, w=7, dur=0.6, head=26, dash=None):
    path = curve(p0, p1, bend)

    def draw(c, age):
        p = in_out(age / dur)
        if p <= 0:
            return
        pt = stroke(rgb, w)
        if dash:
            dashed(pt, *dash)
        c.drawPath(partial(path, p), pt)
        (hx, hy), ang = point_on(path, p)
        q = clamp01((age - dur * 0.85) / 0.2)
        if q > 0:
            a = math.radians(ang)
            for s in (-0.5, 0.5):
                c.drawLine(hx, hy, hx - head * q * math.cos(a + s), hy - head * q * math.sin(a + s), stroke(rgb, w))
    return draw


def cross(cx, cy, size=26, rgb=RUST, w=10, dur=0.4):
    a = poly([(cx - size, cy - size), (cx + size, cy + size)])
    b = poly([(cx + size, cy - size), (cx - size, cy + size)])

    def draw(c, age):
        c.drawPath(partial(a, smooth(age / (dur * 0.55))), stroke(rgb, w))
        c.drawPath(partial(b, smooth((age - dur * 0.45) / (dur * 0.55))), stroke(rgb, w))
    return draw


def check(cx, cy, s=1.0, rgb=INK, w=10, dur=0.35):
    return ink(poly([(cx - 26 * s, cy), (cx - 7 * s, cy + 20 * s), (cx + 30 * s, cy - 26 * s)]), rgb, w * s, dur)


def underline(x0, x1, y, rgb=RUST, w=7, dur=0.45):
    return ink(curve((x0, y), (x1, y + 3), 0.03), rgb, w, dur)


def counter(v0, v1, x, y, size=120, dur=1.4, fmt="{:.0f}", rgb=INK, align="center", suffix="", f=None):
    f = f or head_font(size)

    def draw(c, age):
        p = out_cubic(age / dur)
        a = min(1, age / 0.2)
        if a <= 0:
            return
        text(c, fmt.format(lerp(v0, v1, p)) + suffix, x, y, f, rgb, a, align)
    return draw


def panel(rect, rgb=CREAM, a=0.92, r=22, dur=0.4, border=True):
    """A rounded paper panel that unfolds from its top edge."""
    x, y, w, h = rect

    def draw(c, age):
        p = out_cubic(age / dur)
        if p <= 0:
            return
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h * p), r, r)
        c.drawRRect(rr, shadow_paint(0.22, 14))
        c.drawRRect(rr, fill(rgb, a))
        if border:
            c.drawRRect(rr, stroke(INK, 4, p))
    return draw


def burst(cx, cy, r0=30, r1=110, n=10, rgb=MUSTARD, dur=0.5, w=6):
    """Radial lines that shoot out once and vanish."""
    def draw(c, age):
        p = clamp01(age / dur)
        if p >= 1:
            return
        for i in range(n):
            a = 2 * math.pi * i / n
            s0, s1 = lerp(r0, r1, out_cubic(p) * 0.6), lerp(r0, r1, out_cubic(p))
            c.drawLine(cx + s0 * math.cos(a), cy + s0 * math.sin(a), cx + s1 * math.cos(a), cy + s1 * math.sin(a),
                       stroke(rgb, w * (1 - p)))
    return draw


def light_shafts(x, rgb=CREAM, a=0.18, n=3, seed=0):
    """Soft diagonal shafts of light, breathing slowly (camera-independent atmosphere)."""
    def draw(c, age):
        for i in range(n):
            k = 0.5 + 0.5 * math.sin(age * 0.5 + i * 1.7 + seed)
            x0 = x + i * 230
            p = poly([(x0, -40), (x0 + 120, -40), (x0 + 520, H + 40), (x0 + 300, H + 40)], True)
            pt = fill(rgb, a * (0.5 + 0.5 * k))
            pt.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30))
            c.drawPath(p, pt)
    return draw


# ---------------------------------------------------------------- photo cards (spec 4.4)

class Photo:
    def __init__(self, pid, meta, path):
        arr = load_rgba(path)
        self.pid, self.meta = pid, meta
        self.native = (arr.shape[1], arr.shape[0])
        self.low_res = bool(meta.get("low_res"))
        self.matte = dark_tone(arr)
        if max(arr.shape[:2]) > 2400:  # a downsampled copy for drawing; the photograph is not cropped or altered
            from PIL import Image
            k = 2400 / max(arr.shape[:2])
            arr = np.asarray(Image.fromarray(arr).resize((int(arr.shape[1] * k), int(arr.shape[0] * k)), Image.LANCZOS))
        self.img = to_skia(arr)
        self.caption = meta.get("caption")


def photo_card(ph, cx, cy, w, entry="slide_up", dur=0.7, tilt=0.0, scale_drift=0.015, hold=None, view=1.0):
    """A photograph mounted as a card: thin matte from its own dark tones, soft shadow, caption on the matte
    at lower left. The image is fitted whole (never cropped), drawn untouched; graphics never sit over it.
    Low-res photos are capped at 94% of native size on screen: `view` is the most the camera magnifies
    this station's pixels while the card is up (zoom x station scale), so drift keeps them under native."""
    iw, ih = ph.native
    if ph.low_res:
        w = min(w, iw * 0.94 / view)
    h = w * ih / iw
    m = max(8, w * 0.018)
    cap_h = 46 if ph.caption else 0
    cw, ch = w + 2 * m, h + 2 * m + cap_h

    def draw(c, age):
        p = clamp01(age / dur)
        dx = dy = 0.0
        r = tilt
        s = 1.0
        a = 1.0
        if entry == "slide_up":
            dy = (H * 0.75) * (1 - out_cubic(p))
        elif entry == "slide_left":
            dx = -W * 0.8 * (1 - out_cubic(p))
        elif entry == "slide_right":
            dx = W * 0.8 * (1 - out_cubic(p))
        elif entry == "drop":
            dy = -H * 0.8 * (1 - out_back(p, 1.1))
            r = tilt + 6 * (1 - out_cubic(p))
        elif entry == "flip":
            s = 1.0
            fx = math.cos(math.pi * (1 - out_cubic(p)) / 2)
        elif entry == "pin":
            s = lerp(1.18, 1.0, out_back(p, 2.2))
            a = min(1, p * 4)
            r = tilt - 5 * (1 - out_cubic(p))
        elif entry == "grow":
            s = lerp(0.6, 1.0, out_cubic(p))
            a = min(1, p * 3)
        # contents move at most 6% in scale over their time on screen (card drift plus camera <= 6%)
        s *= 1 + scale_drift * clamp01(age / max(hold or 8, 1))
        if ph.low_res:
            s = min(s, 1.0)
        c.save()
        c.translate(cx + dx, cy + dy)
        c.rotate(max(-4, min(4, r)))
        if entry == "flip":
            c.scale(max(0.001, fx), 1)
        c.scale(s, s)
        if a < 1:
            c.saveLayerAlpha(None, int(255 * a))
        card = skia.Rect.MakeXYWH(-cw / 2, -ch / 2, cw, ch)
        c.drawRect(card.makeOffset(10, 16), shadow_paint(0.35, 18))
        c.drawRect(card, fill(ph.matte))
        c.drawImageRect(ph.img, skia.Rect.MakeXYWH(-cw / 2 + m, -ch / 2 + m, w, h), CUBIC, skia.Paint(AntiAlias=True))
        if ph.caption:  # mandatory where present: lower left, sans-serif ~26px, off-white 85%, soft shadow
            f = body_font(26)
            tx, ty = -cw / 2 + m + 2, ch / 2 - 15
            sp = fill((0, 0, 0), 0.6)
            sp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 3))
            c.drawString(ph.caption, tx + 1, ty + 2, f, sp)
            c.drawString(ph.caption, tx, ty, f, fill(OFFWHITE, 0.85))
        if a < 1:
            c.restore()
        c.restore()
    draw.size = (cw, ch)
    return draw


# ---------------------------------------------------------------- cast rigs

class Rig:
    """body / head / armL / armR cut from one keyed pose, with pivots in the pose image's pixels."""

    def __init__(self, folder):
        self.name = os.path.basename(folder)
        d = json.load(open(os.path.join(folder, "rig.json")))
        self.piv = d["pivots"]
        self.parts = {}
        for n, meta in d["parts"].items():
            self.parts[n] = (to_skia(load_rgba(os.path.join(folder, f"{n}.png"))), meta["offset"])
        self.feet = self.piv["feet"]
        self.height = self.feet[1] - self.piv["top"]


def actor(rig, x, y, height, flip=False, motion=None, seed=0.0, enter=None, dur=0.6, tint=None, idle=True):
    """Draw a rig standing with its feet at (x, y), `height` pixels tall.
    motion(age) -> dict(dx, dy, rot, head, squash) for actions; idle breathing and a slow head
    sway always run (the animation clock stops them in still beats). enter: fade | pop | rise | None."""
    k = height / rig.height
    fx, fy = rig.feet

    def part(c, name, rot=0.0, piv=None):
        if name not in rig.parts:
            return
        img, (ox, oy) = rig.parts[name]
        c.save()
        if piv and rot:
            c.translate(*piv)
            c.rotate(rot)
            c.translate(-piv[0], -piv[1])
        c.drawImage(img, ox, oy, SAMPLING, skia.Paint(AntiAlias=True))
        c.restore()

    def draw(c, age):
        m = motion(age) if motion else {}
        ph = age + seed
        breath = math.sin(ph * 2.1) * 0.008 if idle else 0.0
        a = 1.0
        s_in = 1.0
        dy_in = 0.0
        if enter:
            p = clamp01(age / dur)
            if enter == "fade":
                a = smooth(p)
            elif enter == "pop":
                s_in = out_back(p)
            elif enter == "rise":
                dy_in = 60 * (1 - out_cubic(p))
                a = out_cubic(p)
        if a <= 0 or s_in <= 0:
            return
        c.save()
        c.translate(x + m.get("dx", 0), y + m.get("dy", 0) + dy_in)
        c.rotate(m.get("rot", 0))
        ks = k * s_in * m.get("scale", 1.0)
        if ks <= 0.001:
            c.restore()
            return
        c.scale(ks * (-1 if flip else 1), ks)
        sq = m.get("squash", 0)
        c.scale(1 - sq * 0.5, 1 + breath + sq)
        c.translate(-fx, -fy)
        layered = a < 1 or tint is not None
        if layered:  # tint: the figure as a flat silhouette in one colour (a back-lit figure, "back to us")
            lp = skia.Paint(Alphaf=a)
            if tint is not None:
                lp.setColorFilter(skia.ColorFilters.Blend(col(tint).toColor(), skia.BlendMode.kSrcIn))
            c.saveLayer(None, lp)
        part(c, "body")
        # arms stay exactly as posed: rotating cut-out arms showed seams at the shoulders (review, sample v1)
        part(c, "armL")
        part(c, "armR")
        c.save()
        c.translate(0, -breath * rig.height * 0.6)
        part(c, "head", m.get("head", 0) + (math.sin(ph * 0.8) * 2.0 if idle else 0), rig.piv.get("neck"))
        c.restore()
        if layered:
            c.restore()
        c.restore()
    return draw


def walk(x0, x1, t0, t1, bob=10, swing=9):
    """Motion: walk from x0 to x1 (relative dx) between t0 and t1 (ages), bobbing (arms stay as posed)."""
    def m(age):
        p = clamp01((age - t0) / max(t1 - t0, 1e-3))
        moving = 0 < p < 1
        ph = (age - t0) * 7.5
        return {"dx": lerp(x0, x1, in_out(p)), "dy": -abs(math.sin(ph)) * bob if moving else 0,
                "rot": math.sin(ph) * 1.2 if moving else 0}
    return m


def keys(*frames):
    """Motion from keyframes [(age, {param: value})], eased between them."""
    frames = sorted(frames, key=lambda f: f[0])

    def m(age):
        if age <= frames[0][0]:
            return dict(frames[0][1])
        for (a0, v0), (a1, v1) in zip(frames, frames[1:]):
            if age < a1:
                u = in_out((age - a0) / (a1 - a0))
                ks = set(v0) | set(v1)
                return {k: lerp(v0.get(k, 0), v1.get(k, 0), u) for k in ks}
        return dict(frames[-1][1])
    return m


# ---------------------------------------------------------------- camera

class Camera:
    """Keyframed camera: [(t, (cx, cy, z), how)] where how is 'move' (eased log-zoom swoop from the
    previous key), 'cut' (jump at t) or 'hold' (linear drift from the previous key, for slow pushes)."""

    def __init__(self):
        self.keys = []

    def key(self, t, pos, how="move"):
        self.keys.append((t, tuple(pos), how))

    def at(self, t):
        ks = sorted(self.keys, key=lambda k: k[0])
        if t <= ks[0][0]:
            return ks[0][1]
        for (t0, A, _), (t1, B, how) in zip(ks, ks[1:]):
            if t < t1:
                if how == "cut":
                    return A
                u = (t - t0) / max(t1 - t0, 1e-6)
                if how == "hold":
                    return (lerp(A[0], B[0], u), lerp(A[1], B[1], u), math.exp(lerp(math.log(A[2]), math.log(B[2]), u)))
                return swoop(A, B, u)
        return ks[-1][1]

    def matrix(self, t):
        cx, cy, z = self.at(t)
        m = skia.Matrix()
        m.setTranslate(W / 2, H / 2)
        m.preScale(z, z)
        m.preTranslate(-cx, -cy)
        return m


def swoop(A, B, u):
    ax, ay, az = A
    bx, by, bz = B
    e = smooth(u)
    d = math.hypot(bx - ax, by - ay) * min(az, bz) / W
    k = min(0.9, 0.42 * math.log1p(d))
    z = math.exp(lerp(math.log(az), math.log(bz), e) - k * math.sin(math.pi * e))
    if abs(math.log(bz / az)) > 0.6 and d < 1.2:
        za = math.exp(lerp(math.log(az), math.log(bz), e))
        w = (1 / za - 1 / az) / (1 / bz - 1 / az)
    else:
        w = e
    return (lerp(ax, bx, w), lerp(ay, by, w), z)


def frame_on(st, lx=W / 2, ly=H / 2, zoom=1.0):
    """Camera position that frames station-local point (lx, ly) at `zoom` x the station's full view."""
    wx, wy = st.world(lx, ly)
    return (wx, wy, zoom / st.s)


# ---------------------------------------------------------------- subtitles (spec 7)

def wrap(text, n=42):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > n:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    if cur:
        lines.append(cur)
    return lines


def cues(tl, ids=None):
    """Per segment: lines of <= 42 characters, at most two on screen, timed by the speech model.
    Before a structural silence the strip leaves when the voice stops."""
    out = []
    for sid in ids or tl.order:
        s = tl.segs[sid]
        lines = wrap(s["text"])
        groups = [lines[i:i + 2] for i in range(0, len(lines), 2)]
        txt = s["text"]
        cu = tl._units(txt)
        pos, t_prev = 0, s["start"]
        for gi, g in enumerate(groups):
            chunk = " ".join(g)
            pos = txt.find(chunk, pos) + len(chunk)
            t_end = s["start"] + (s["end"] - s["start"]) * cu[min(pos, len(txt))] / cu[-1]
            if gi == len(groups) - 1:
                t_end = s["end"] if s["pause_after"] >= 2000 else min(s["end"] + 0.35, tl.next_start(sid) - 0.05)
            out.append({"id": sid, "start": t_prev, "end": t_end, "lines": g,
                        "first": gi == 0, "last": gi == len(groups) - 1})
            t_prev = t_end
    return out


def srt_time(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


def write_srt(cs, path, offset=0.0):
    with open(path, "w", encoding="utf-8") as f:
        for i, q in enumerate(cs, 1):
            f.write(f"{i}\n{srt_time(q['start'] - offset)} --> {srt_time(q['end'] - offset)}\n"
                    + "\n".join(q["lines"]) + "\n\n")


def draw_subtitle(c, q, t):
    """A small strip near the bottom: ink band, cream text."""
    a = min(1, (t - q["start"]) / 0.15 if q.get("first") else 1, (q["end"] - t) / 0.15 if q.get("last") else 1)
    if a <= 0:
        return
    f = body_font(31, bold=False)
    lh = 39
    lines = q["lines"]
    wmax = max(f.measureText(l) for l in lines)
    y_last = H - 46
    top = y_last - lh * (len(lines) - 1) - 31
    band = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(W / 2 - wmax / 2 - 22, top - 6, W / 2 + wmax / 2 + 22,
                                                    y_last + 14), 10, 10)
    c.drawRRect(band, fill(INK, 0.78 * a))
    for i, l in enumerate(lines):
        text(c, l, W / 2, y_last - lh * (len(lines) - 1 - i), f, CREAM, a, "center")


def strike(x0, x1, y, rgb=RUST, w=6, dur=0.35):
    """A line struck through a word."""
    return ink(poly([(x0, y), (x1, y)]), rgb, w, dur)
