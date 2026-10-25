"""One-world motion engine: a paper world with stations, a log-zoom camera, graphic primitives.

Coordinates: each station is a 1920x1080 "card" placed in the world at centre (x, y) and scale s.
Elements are drawn in card-local pixels. The camera frames a card when zoom = 1 / s.

Rules carried from BUILD_SPEC and the brief:
- archival photos are never cropped, tinted or overlaid; their on-screen motion during the shot
  follows the spec table, computed over the shot's full duration so it never exceeds spec speed
- structural silences (pause_after >= 2000) freeze the camera and every animation clock
- transitions are camera moves, except shots marked `transition: cut`, which jump
"""
import json, math, os, re
import numpy as np
import skia

W, H, FPS = 1920, 1080, 30
DAY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLING = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear)

INTER = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-{}.ttf"
CJK = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
_tf = {}


def font(path, size):
    if path not in _tf:
        _tf[path] = skia.Typeface.MakeFromFile(path)
    f = skia.Font(_tf[path], size)
    f.setSubpixel(True)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    return f


def sans(weight, size):
    return font(INTER.format(weight), size)


def serif(style, size):
    return font(SERIF.format(style), size)


# palette: warm grey and ink, one red accent (the seal)
INK = (0.17, 0.16, 0.15)
GREY = (0.40, 0.38, 0.35)
PAPER_LIGHT = (0.93, 0.91, 0.87)
RED = (0.66, 0.16, 0.12)
OFFWHITE = (0.95, 0.93, 0.89)


def col(rgb, a=1.0):
    return skia.Color4f(rgb[0], rgb[1], rgb[2], max(0.0, min(1.0, a)))


def stroke(rgb, w, a=1.0, cap=skia.Paint.kRound_Cap):
    return skia.Paint(Color=col(rgb, a), AntiAlias=True, Style=skia.Paint.kStroke_Style,
                      StrokeWidth=w, StrokeCap=cap, StrokeJoin=skia.Paint.kRound_Join)


def fill(rgb, a=1.0):
    return skia.Paint(Color=col(rgb, a), AntiAlias=True)


# ---------------------------------------------------------------- easing

def clamp01(x):
    return 0.0 if x < 0 else 1.0 if x > 1 else x


def smooth(x):
    x = clamp01(x)
    return x * x * x * (x * (6 * x - 15) + 10)


def out_cubic(x):
    x = clamp01(x)
    return 1 - (1 - x) ** 3


def out_back(x, k=1.4):
    x = clamp01(x)
    return 1 + (k + 1) * (x - 1) ** 3 + k * (x - 1) ** 2


def lerp(a, b, t):
    return a + (b - a) * t


# ---------------------------------------------------------------- timing

class Timeline:
    """Segment timings from audio/timings.json, word-time estimates and structural freezes."""

    def __init__(self):
        d = json.load(open(os.path.join(DAY, "audio", "timings.json")))
        self.total = d["total"]
        self.segs = {s["id"]: s for s in d["segments"]}
        self.order = [s["id"] for s in d["segments"]]
        self.freezes = [(s["end"], s["end"] + s["pause_after"] / 1000)
                        for s in d["segments"] if s["pause_after"] >= 2000]

    def start(self, sid):
        return self.segs[sid]["start"]

    def end(self, sid):
        return self.segs[sid]["end"]

    def next_start(self, sid):
        s = self.segs[sid]
        return s["end"] + s["pause_after"] / 1000

    def _units(self, text):
        # speech-time model: one unit per character, extra for punctuation pauses
        u = []
        for i, ch in enumerate(text):
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
        """Estimated time at which `phrase` begins in segment `sid`."""
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
        """Animation clock: stopped inside structural silences."""
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
    """Background sampled from the image's own dark tones, never pure black (spec 3)."""
    rgb = arr[..., :3].reshape(-1, 3).astype(float)
    lum = rgb @ [0.299, 0.587, 0.114]
    sel = rgb[lum <= np.percentile(lum, 12)]
    c = sel.mean(0) / 255
    return tuple(max(v, 0.07) for v in c)


def mean_tone(arr):
    return tuple(arr[..., :3].reshape(-1, 3).mean(0) / 255)


def make_paper(size=1024, seed=3, base=(0.80, 0.77, 0.71)):
    """Tileable warm-grey paper: soft mottling plus fine grain."""
    rng = np.random.default_rng(seed)
    f = np.zeros((size, size))
    for k, amp in ((4, 0.035), (16, 0.02), (64, 0.012), (size, 0.018)):
        n = rng.normal(0, 1, (k, k))
        n = np.kron(n, np.ones((size // k, size // k)))
        if k < size:  # wrap-blur keeps it tileable
            from scipy.ndimage import gaussian_filter
            n = gaussian_filter(n, size / k / 2, mode="wrap")
            n /= n.std() + 1e-9
        f += n * amp
    rgb = np.stack([base[0] + f, base[1] + f * 0.97, base[2] + f * 0.92], -1)
    a = np.clip(rgb * 255, 0, 255).astype(np.uint8)
    return np.dstack([a, np.full((size, size), 255, np.uint8)])


# ---------------------------------------------------------------- drawing primitives

def text(c, s, x, y, f, rgb, a=1.0, align="left", tracking=0.0):
    p = fill(rgb, a)
    if tracking == 0:
        w = f.measureText(s)
        x0 = x - (w if align == "right" else w / 2 if align == "center" else 0)
        c.drawString(s, x0, y, f, p)
        return w
    widths = [f.measureText(ch) + tracking for ch in s]
    w = sum(widths) - tracking
    x0 = x - (w if align == "right" else w / 2 if align == "center" else 0)
    for ch, cw in zip(s, widths):
        c.drawString(ch, x0, y, f, p)
        x0 += cw
    return w


def text_width(s, f, tracking=0.0):
    return sum(f.measureText(ch) + tracking for ch in s) - tracking if tracking else f.measureText(s)


def partial(path, p):
    """The first fraction p of a path (draw-on)."""
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
    """Quadratic arc from p0 to p1, bowed sideways by `bend` of its length."""
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    cx, cy = mx - dy * bend, my + dx * bend
    p = skia.Path()
    p.moveTo(*p0)
    p.quadTo(cx, cy, *p1)
    return p


def point_on(path, p):
    pm = skia.PathMeasure(path, False)
    pos, tan = pm.getPosTan(pm.getLength() * clamp01(p))
    return (pos.x(), pos.y())


def dashed(paint, on=10, off=8):
    paint.setPathEffect(skia.DashPathEffect.Make([on, off], 0))
    return paint


# ---------------------------------------------------------------- elements

class El:
    """A drawable that appears at t0 and stays (things stay where they were drawn)."""

    def __init__(self, t0, draw, until=None):
        self.t0, self.draw, self.until = t0, draw, until


class Station:
    def __init__(self, name, x, y, s, under=None):
        self.name, self.x, self.y, self.s = name, x, y, s
        self.els = []

    def add(self, t0, draw, until=None):
        self.els.append(El(t0, draw, until))
        return self

    def matrix(self):
        m = skia.Matrix()
        m.setTranslate(self.x - W * self.s / 2, self.y - H * self.s / 2)
        m.preScale(self.s, self.s)
        return m

    def to_world(self, lx, ly):
        return (self.x + (lx - W / 2) * self.s, self.y + (ly - H / 2) * self.s)

    def render(self, c, ta):
        c.save()
        c.concat(self.matrix())
        for e in self.els:
            if ta >= e.t0 and (e.until is None or ta < e.until):
                e.draw(c, ta - e.t0)
        c.restore()


# reusable element builders (card-local) ---------------------------------

def print_photo(img, rect, matte, shadow=True, border=10):
    """A photograph mounted on a matte cut from its own dark tones: fitted, never cropped."""
    iw, ih = img.width(), img.height()
    x, y, w, h = rect
    k = min(w / iw, h / ih)
    dw, dh = iw * k, ih * k
    dx, dy = x + (w - dw) / 2, y + (h - dh) / 2
    mount = skia.Rect.MakeXYWH(dx - border, dy - border, dw + 2 * border, dh + 2 * border)

    def draw(c, age):
        if shadow:
            sp = fill((0, 0, 0), 0.28)
            sp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14))
            c.drawRect(mount.makeOffset(0, 10), sp)
        c.drawRect(mount, fill(matte))
        c.drawImageRect(img, skia.Rect.MakeXYWH(dx, dy, dw, dh), SAMPLING, skia.Paint(AntiAlias=True))
    draw.bounds = (dx, dy, dw, dh)
    return draw


def print_plate(img, rect, feather=False, shadow=True):
    """A generated still laid into the world as a print (or feathered into the paper, for maps)."""
    x, y, w, h = rect
    r = skia.Rect.MakeXYWH(x, y, w, h)

    def draw(c, age):
        if shadow and not feather:
            sp = fill((0, 0, 0), 0.25)
            sp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 16))
            c.drawRect(r.makeOffset(0, 10), sp)
        c.drawImageRect(img, r, SAMPLING, skia.Paint(AntiAlias=True))
    return draw


def label(s, x, y, size=26, rgb=INK, weight="SemiBold", tracking=3.0, align="left", dur=0.5, rise=10,
          f=None):
    f = f or sans(weight, size)

    def draw(c, age):
        p = out_cubic(age / dur)
        text(c, s, x, y + rise * (1 - p), f, rgb, p, align, tracking)
    return draw


def serif_label(s, x, y, size=40, rgb=INK, style="Regular", align="left", dur=0.6, rise=8, tracking=0.0):
    return label(s, x, y, size, rgb, align=align, dur=dur, rise=rise, tracking=tracking, f=serif(style, size))


def line_on(path, rgb=INK, w=2.5, dur=0.8, a=1.0, dash=None, ease=smooth):
    def draw(c, age):
        p = ease(age / dur)
        if p <= 0:
            return
        pt = stroke(rgb, w, a)
        if dash:
            dashed(pt, *dash)
        c.drawPath(partial(path, p), pt)
    return draw


def ring_on(cx, cy, r, rgb=INK, w=2.5, dur=0.8, a=1.0, dash=None):
    return line_on(arc_path(cx, cy, r), rgb, w, dur, a, dash)


def pulse(cx, cy, r0=6, r1=60, rgb=RED, dur=1.4, w=2.5):
    """One expanding ring that finishes and is gone, leaving the dot (drawn separately)."""
    def draw(c, age):
        p = clamp01(age / dur)
        if p >= 1:
            return
        c.drawCircle(cx, cy, lerp(r0, r1, out_cubic(p)), stroke(rgb, w, 1 - p))
    return draw


def dot(cx, cy, r=9, rgb=RED, dur=0.35):
    def draw(c, age):
        p = out_back(age / dur)
        c.drawCircle(cx, cy, r * p, fill(rgb))
    return draw


def cross(cx, cy, size=26, rgb=RED, w=4, dur=0.45):
    a = poly([(cx - size, cy - size), (cx + size, cy + size)])
    b = poly([(cx + size, cy - size), (cx - size, cy + size)])

    def draw(c, age):
        c.drawPath(partial(a, smooth(age / (dur * 0.55))), stroke(rgb, w))
        c.drawPath(partial(b, smooth((age - dur * 0.45) / (dur * 0.55))), stroke(rgb, w))
    return draw


def strike(x0, x1, y, rgb=RED, w=3.5, dur=0.4):
    return line_on(poly([(x0, y), (x1, y)]), rgb, w, dur)


def counter(v0, v1, x, y, size=120, dur=1.2, fmt="{:.0f}", rgb=INK, align="left", f=None, suffix=""):
    f = f or sans("Light", size)

    def draw(c, age):
        p = out_cubic(age / dur)
        text(c, fmt.format(lerp(v0, v1, p)) + suffix, x, y, f, rgb, min(1, age / 0.25), align)
    return draw


def seal(cx, cy, r=46, dur=0.35, glyph="印", a=1.0):
    """The red seal impression: the film's guide object."""
    f = font(CJK, r * 1.05)

    def draw(c, age):
        p = clamp01(age / dur)
        k = lerp(1.35, 1.0, out_cubic(p))
        al = a * min(1, p * 1.6)
        c.save()
        c.translate(cx, cy)
        c.scale(k, k)
        c.drawCircle(0, 0, r, stroke(RED, r * 0.11, al))
        c.drawCircle(0, 0, r * 0.80, fill(RED, al * 0.92))
        text(c, glyph, 0, r * 0.37, f, PAPER_LIGHT, al, "center")
        c.restore()
    return draw


def loupe(cx, cy, r, anchor, rings, t_rings, rgb=INK, label_km="3 km", paper=PAPER_LIGHT):
    """A magnifier callout from an anchor point: concentric distance rings, red dot on the last one."""
    ax, ay = anchor

    def draw(c, age):
        p = out_back(age / 0.5, 1.0)
        if p <= 0:
            return
        c.drawPath(partial(poly([(ax, ay), (cx - (cx - ax) * r / math.hypot(cx - ax, cy - ay),
                                            cy - (cy - ay) * r / math.hypot(cx - ax, cy - ay))]), smooth(age / 0.4)),
                   stroke(rgb, 2, 0.8))
        rr = r * p
        sp = fill((0, 0, 0), 0.2)
        sp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10))
        c.drawCircle(cx, cy + 6, rr, sp)
        c.drawCircle(cx, cy, rr, fill(paper))
        c.drawCircle(cx, cy, rr, stroke(rgb, 3))
        n = len(rings)
        for i, frac in enumerate(rings):
            q = smooth((age - t_rings - i * 0.35) / 0.6)
            if q > 0:
                pt = stroke(rgb, 1.6, 0.75)
                if i < n - 1:
                    dashed(pt, 5, 6)
                c.drawPath(partial(arc_path(cx, cy, rr * frac), q), pt)
        c.drawCircle(cx, cy, 5 * p, fill(rgb))
        q = clamp01((age - t_rings - n * 0.35) / 0.4)
        if q > 0:
            ang = math.radians(-35)
            px, py = cx + rr * rings[-1] * math.cos(ang), cy + rr * rings[-1] * math.sin(ang)
            c.drawCircle(px, py, 9 * out_back(q), fill(RED))
            text(c, label_km, cx, cy + rr * 0.62, sans("SemiBold", r * 0.17), rgb, q, "center", 2)
    return draw


# ---------------------------------------------------------------- icons (card-local, stroke style)

def icon(kind, cx, cy, s=1.0, rgb=INK, w=3.0, dur=0.9):
    P = []
    def S(pts, closed=False):
        P.append(poly([(cx + x * s, cy + y * s) for x, y in pts], closed))

    def C(x, y, r, a0=-90, sw=360):
        P.append(arc_path(cx + x * s, cy + y * s, r * s, a0, sw))
    if kind == "helmet":
        C(0, 6, 34, 180, 180); S([(-46, 6), (46, 6)]); S([(-20, 6), (-26, 22)])
    elif kind == "flask":
        S([(-10, -38), (-10, -8), (-34, 34), (34, 34), (10, -8), (10, -38)]); S([(-16, -38), (16, -38)]); S([(-22, 14), (22, 14)])
    elif kind == "clock":
        C(0, 0, 40); S([(0, 0), (0, -26)]); S([(0, 0), (18, 0)])
    elif kind == "calendar":
        S([(-36, -30), (36, -30), (36, 36), (-36, 36)], True); S([(-36, -12), (36, -12)]); S([(-18, -40), (-18, -22)]); S([(18, -40), (18, -22)])
    elif kind == "doc":
        S([(-28, -38), (14, -38), (28, -24), (28, 38), (-28, 38)], True)
        for yy in (-14, 0, 14):
            S([(-16, yy), (16, yy)])
    elif kind == "house":
        S([(-34, -2), (0, -34), (34, -2)]); S([(-26, -8), (-26, 34), (26, 34), (26, -8)]); S([(-8, 34), (-8, 12), (8, 12), (8, 34)])
    elif kind == "bag":
        S([(-34, -14), (34, -14), (34, 30), (-34, 30)], True); S([(-12, -14), (-12, -28), (12, -28), (12, -14)])
    elif kind == "tram":
        S([(-46, -22), (46, -22), (46, 24), (-46, 24)], True); S([(-32, -10), (-12, -10), (-12, 6), (-32, 6)], True)
        S([(-4, -10), (16, -10), (16, 6), (-4, 6)], True); S([(24, -10), (38, -10), (38, 6), (24, 6)], True)
        S([(0, -22), (18, -52)]); C(-26, 30, 6); C(26, 30, 6)
    elif kind == "office":
        S([(-34, 36), (-34, -30), (34, -30), (34, 36)]); S([(-46, 36), (46, 36)])
        for yy in (-16, 2, 20):
            S([(-20, yy), (-8, yy)]); S([(8, yy), (20, yy)])
    elif kind == "ship":
        S([(-80, -6), (80, -6), (62, 22), (-66, 22)], True); S([(-40, -6), (-40, -24), (10, -24), (10, -6)]); S([(30, -6), (30, -40)])
    elif kind == "plane":
        S([(-40, 0), (40, 0)]); S([(-6, 0), (-22, -30), (-12, -30), (14, 0)]); S([(-6, 0), (-22, 30), (-12, 30), (14, 0)])
        S([(-40, 0), (-48, -12)]); S([(-40, 0), (-48, 12)])
    paths = P

    def draw(c, age):
        n = len(paths)
        for i, p in enumerate(paths):
            q = smooth((age - i * dur * 0.35 / n) / (dur * 0.65))
            if q > 0:
                c.drawPath(partial(p, q), stroke(rgb, w))
    return draw


# ---------------------------------------------------------------- camera

def log_lerp(a, b, t):
    return math.exp(lerp(math.log(a), math.log(b), t))


class Camera:
    """Holds on stations with spec motion; eased log-zoom moves between them, swooping on long trips."""

    def __init__(self):
        self.holds = []   # (t_from, t_to, fn(t) -> (cx, cy, z))
        self.moves = []   # (t_from, t_to)

    def framing(self, st, motion, shot_t0, shot_t1, archival):
        dur = max(shot_t1 - shot_t0, 1e-3)

        def fn(t):
            p = clamp01((t - shot_t0) / dur)  # linear over the full shot: never faster than spec
            z, cx = 1.0 / st.s, st.x
            if motion == "slow_push_in":
                z *= 1 + 0.06 * p
            elif motion == "slow_pull_out":
                z *= 1.06 - 0.06 * p
            elif motion in ("slow_pan_left", "slow_pan_right"):
                z *= 1.04
                d = (0.02 - 0.04 * p) if motion == "slow_pan_left" else (-0.02 + 0.04 * p)
                cx = st.x + d * W * st.s
            elif motion == "hold_then_push":
                q = clamp01((p - 0.5) * 2)
                z *= (1 + 0.06 * q) if archival else (1 + 0.01 * p + 0.05 * q)
            elif motion == "static" and not archival:
                z *= 1 + 0.03 * p  # the camera never freezes on graphics (2-5%)
            elif motion == "drift":
                z *= 1 + 0.04 * p
            return (cx, st.y, z)
        return fn

    def at(self, t):
        for (a, b), (h0, h1) in zip(self.moves, zip(self.holds, self.holds[1:])):
            if a <= t < b:
                u = (t - a) / (b - a)
                A, B = h0[2](a), h1[2](b)
                return swoop(A, B, u)
        for a, b, fn in self.holds:
            if a <= t < b:
                return fn(t)
        if t < self.holds[0][0]:
            return self.holds[0][2](t)
        return self.holds[-1][2](t)

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
    # distance in screen widths at the smaller zoom decides how far to pull back mid-move
    d = math.hypot(bx - ax, by - ay) * min(az, bz) / W
    k = min(0.9, 0.42 * math.log1p(d))
    lz = lerp(math.log(az), math.log(bz), e) - k * math.sin(math.pi * e)
    z = math.exp(lz)
    # position follows the zoom so nested dives stay on target: weight by 1/z when zoom changes a lot
    if abs(math.log(bz / az)) > 0.6 and d < 1.2:
        w = (1 / log_lerp(az, bz, e) - 1 / az) / (1 / bz - 1 / az)
    else:
        w = e
    return (lerp(ax, bx, w), lerp(ay, by, w), z)


# ---------------------------------------------------------------- subtitles

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
    """Spec 5: per segment, lines of <= 42 chars, at most two on screen; long segments run as
    consecutive two-line cues timed by the same speech model used for word timing."""
    out = []
    ids = ids or tl.order
    for sid in ids:
        s = tl.segs[sid]
        lines = wrap(s["text"])
        groups = [lines[i:i + 2] for i in range(0, len(lines), 2)]
        # balance: avoid a lone short last line when we could split 3 lines as 2+1 differently
        txt = s["text"]
        cu = tl._units(txt)
        pos, t_prev = 0, s["start"]
        for gi, g in enumerate(groups):
            chunk = " ".join(g)
            pos = txt.find(chunk, pos) + len(chunk)
            t_end = s["start"] + (s["end"] - s["start"]) * cu[min(pos, len(txt))] / cu[-1]
            if gi == len(groups) - 1:
                t_end = min(s["end"] + 0.35, tl.next_start(sid) - 0.05)
            out.append({"id": sid, "start": t_prev, "end": t_end, "lines": g})
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
    """A small strip near the bottom: ink band, off-white Inter, quick fade at cue edges."""
    a = min(1, (t - q["start"]) / 0.15, (q["end"] - t) / 0.15)
    if a <= 0:
        return
    f = sans("Medium", 29)
    lh = 38
    lines = q["lines"]
    wmax = max(f.measureText(l) for l in lines)
    y_last = H - 44
    top = y_last - lh * (len(lines) - 1) - 30
    band = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(W / 2 - wmax / 2 - 22, top - 4, W / 2 + wmax / 2 + 22,
                                                    y_last + 13), 8, 8)
    c.drawRRect(band, fill((0.09, 0.085, 0.08), 0.62 * a))
    for i, l in enumerate(lines):
        text(c, l, W / 2, y_last - lh * (len(lines) - 1 - i), f, OFFWHITE, a, "center")
