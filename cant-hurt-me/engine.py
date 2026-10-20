"""One-continuous-shot renderer: a single world of placed images, one moving camera.

The world is a big plane of paper. Images ("panels") sit at fixed world positions and
sizes, some nested inside others for zoom-throughs. The camera is (x, y, w): the centre
of the view and the visible world width. Overlays (text, counters, strokes, a running
figure) live in world space too, so they stay where they were drawn.
"""
import math, os, subprocess
from functools import lru_cache

import cairo
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 30
ASPECT = H / W
HERE = os.path.dirname(os.path.abspath(__file__))
INK = (0.08, 0.08, 0.08)
RED = (0.60, 0.07, 0.11)
PAPER = (208, 203, 195)  # warm grey paper; every panel (cover too) is colour-matched to it

FONTS = {
    "title": "fonts/NotoSansDevanagari-ExtraCondensedBlack.ttf",
    "label": "fonts/NotoSansDevanagari-CondensedBold.ttf",
    "sub": "fonts/NotoSansDevanagari-SemiBold.ttf",
    "num": "fonts/NotoSans-ExtraCondensedBlack.ttf",
}


def font(kind, size):
    return ImageFont.truetype(os.path.join(HERE, FONTS[kind]), size,
                              layout_engine=ImageFont.Layout.RAQM)


# ---------------------------------------------------------------- easing / maths
def clamp(v, a=0.0, b=1.0):
    return a if v < a else b if v > b else v


def smooth(u):
    u = clamp(u)
    return u * u * (3 - 2 * u)


def ease_io(u):  # cubic in-out
    u = clamp(u)
    return 4 * u ** 3 if u < 0.5 else 1 - (-2 * u + 2) ** 3 / 2


def ease_out(u):
    u = clamp(u)
    return 1 - (1 - u) ** 3


def back_out(u, s=1.7):
    u = clamp(u) - 1
    return 1 + (s + 1) * u ** 3 + s * u ** 2


def ramp(t, t0, dur=0.4):
    return clamp((t - t0) / dur)


# ---------------------------------------------------------------- images
_KEEP = []


def to_surface(rgba):
    """PIL RGBA -> cairo ARGB32 (premultiplied)."""
    a = np.asarray(rgba.convert("RGBA"), dtype=np.float32)
    al = a[..., 3:4] / 255.0
    bgra = np.empty(a.shape, np.uint8)
    bgra[..., 0] = (a[..., 2] * al[..., 0]).astype(np.uint8)
    bgra[..., 1] = (a[..., 1] * al[..., 0]).astype(np.uint8)
    bgra[..., 2] = (a[..., 0] * al[..., 0]).astype(np.uint8)
    bgra[..., 3] = a[..., 3].astype(np.uint8)
    h, w = bgra.shape[:2]
    stride = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_ARGB32, w)
    buf = np.zeros((h, stride // 4, 4), np.uint8)
    buf[:, :w] = bgra
    surf = cairo.ImageSurface.create_for_data(memoryview(buf), cairo.FORMAT_ARGB32, w, h, stride)
    _KEEP.append(buf)  # cairo does not own the pixels
    return surf


class Mips:
    """Mip pyramid so heavy downscales stay clean."""

    def __init__(self, im):
        self.w, self.h = im.size
        self.levels = []
        while True:
            self.levels.append((im.size[0], to_surface(im)))
            if min(im.size) < 48:
                break
            im = im.resize((max(1, im.size[0] // 2), max(1, im.size[1] // 2)), Image.LANCZOS)

    def pick(self, screen_w):
        for lw, s in reversed(self.levels):
            if lw >= screen_w * 0.9:
                return lw, s
        return self.levels[0]


def colour_match(im):
    a = np.asarray(im.convert("RGB"), np.float32)
    lum = a.mean(axis=2)
    paper = np.median(a[lum > np.percentile(lum, 70)], axis=0)
    gain = np.array(PAPER, np.float32) / np.maximum(paper, 1)
    return Image.fromarray(np.clip(a * gain, 0, 255).astype(np.uint8))


def feather_mask(size, kind="rect", f=0.12):
    w, h = size
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    u, v = (x + 0.5) / w, (y + 0.5) / h
    if kind == "ellipse":
        r = np.sqrt(((u - 0.5) / 0.5) ** 2 + ((v - 0.5) / 0.5) ** 2)
        m = 1 - np.clip((r - (1 - 2 * f)) / (2 * f), 0, 1)
    else:
        fx, fy = f, f * w / h
        m = np.minimum(np.minimum(u, 1 - u) / fx, np.minimum(v, 1 - v) / fy)
        m = np.clip(m, 0, 1)
    m = m * m * (3 - 2 * m)
    return Image.fromarray((m * 255).astype(np.uint8))


@lru_cache(maxsize=None)
def load_image(path, mask="rect", feather=0.12, match=True):
    full = os.path.join(HERE, path)
    if not os.path.exists(full):  # layout preview while images are still generating
        im = Image.new("RGB", (1344, 768), (170, 160, 150))
        ImageDraw.Draw(im).text((40, 40), os.path.basename(path), font=font("num", 90), fill=(60, 60, 60))
        return Mips(im.convert("RGBA"))
    im = Image.open(full)
    if im.mode == "RGBA" and mask is None:
        return Mips(im)
    rgb = colour_match(im) if match else im.convert("RGB")
    rgba = rgb.convert("RGBA")
    if mask:
        rgba.putalpha(feather_mask(rgba.size, mask, feather))
    return Mips(rgba)


# ---------------------------------------------------------------- camera
def zoom_path(p0, p1, rho=1.3):
    """van Wijk & Nuij smooth zoom/pan: long moves pull back mid-flight (a swoop)."""
    (x0, y0, w0), (x1, y1, w1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    d2 = dx * dx + dy * dy
    if d2 < 1e-6 * w0 * w0:
        k = math.log(w1 / w0)
        return lambda t: (x0 + dx * t, y0 + dy * t, w0 * math.exp(k * t))
    d1 = math.sqrt(d2)
    b0 = (w1 * w1 - w0 * w0 + rho ** 4 * d2) / (2 * w0 * rho ** 2 * d1)
    b1 = (w1 * w1 - w0 * w0 - rho ** 4 * d2) / (2 * w1 * rho ** 2 * d1)
    r0 = math.log(math.sqrt(b0 * b0 + 1) - b0)
    r1 = math.log(math.sqrt(b1 * b1 + 1) - b1)
    S = (r1 - r0) / rho

    def f(t):
        s = t * S
        u = w0 / (rho ** 2 * d1) * (math.cosh(r0) * math.tanh(rho * s + r0) - math.sinh(r0))
        return x0 + u * dx, y0 + u * dy, w0 * math.cosh(r0) / math.cosh(rho * s + r0)
    return f


def log_path(p0, p1):
    """Zoom on a log scale, keeping the zoom target fixed on screen while scaling."""
    (x0, y0, w0), (x1, y1, w1) = p0, p1
    if abs(math.log(w1 / w0)) < 1e-3:
        return lambda t: (x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, w0)
    def f(t):
        w = w0 * (w1 / w0) ** t
        # position moves in proportion to how far the zoom has gone, so the target stays put
        k = (w0 - w) / (w0 - w1)
        return x0 + (x1 - x0) * k, y0 + (y1 - y0) * k, w
    return f


class Camera:
    """keys: [(t, x, y, w, mode)], mode in {'vw' swoop, 'log' zoom, 'hold' drift}."""

    def __init__(self, keys, breath=0.012):
        self.keys = sorted(keys, key=lambda k: k[0])
        self.paths = []
        for a, b in zip(self.keys, self.keys[1:]):
            mode = b[4] if len(b) > 4 else "vw"
            p0, p1 = a[1:4], b[1:4]
            fn = zoom_path(p0, p1) if mode == "vw" else log_path(p0, p1)
            ease = {"vw": ease_io, "log": ease_io, "hold": lambda u: u}[mode]
            self.paths.append((a[0], b[0], fn, ease))
        self.breath = breath

    def __call__(self, t):
        if t <= self.keys[0][0]:
            x, y, w = self.keys[0][1:4]
        elif t >= self.keys[-1][0]:
            x, y, w = self.keys[-1][1:4]
        else:
            for t0, t1, fn, ease in self.paths:
                if t0 <= t <= t1:
                    x, y, w = fn(ease((t - t0) / (t1 - t0)))
                    break
        # a constant gentle drift so no frame is ever frozen
        w *= 1 + self.breath * math.sin(t * 2 * math.pi / 9.0)
        x += w * 0.004 * math.sin(t * 2 * math.pi / 13.0)
        y += w * 0.003 * math.sin(t * 2 * math.pi / 11.0 + 1)
        return x, y, w


# ---------------------------------------------------------------- world items
class Item:
    t0, t1 = -1e9, 1e9
    z = 0

    def bbox(self, t):  # world bbox (x0, y0, x1, y1) or None for always
        return None

    def draw(self, ctx, t, cam):
        pass


def paint_image(ctx, mips, cx, cy, w, alpha, scale_px, rot=0.0):
    """Draw mips centred at (cx, cy) with world width w. scale_px = screen px per world unit."""
    h = w * mips.h / mips.w
    lw, surf = mips.pick(w * scale_px)
    s = w / lw
    ctx.save()
    ctx.translate(cx, cy)
    if rot:
        ctx.rotate(rot)
    ctx.translate(-w / 2, -h / 2)
    ctx.scale(s, s)
    ctx.set_source_surface(surf, 0, 0)
    ctx.get_source().set_filter(cairo.FILTER_BILINEAR)
    ctx.paint_with_alpha(alpha)
    ctx.restore()


class Panel(Item):
    """A generated image at a fixed place in the world.

    reveal=(w_start, w_full): fades in as the camera zooms closer than w_start (nested details).
    pulse: callable t -> scale multiplier.
    """

    def __init__(self, path, cx, cy, w, mask="rect", feather=0.12, match=True,
                 reveal=None, pulse=None, z=0, t0=-1e9, t1=1e9, fade=0.6, pop=False):
        self.mips = load_image(path, mask, feather, match)
        self.pop = pop
        self.cx, self.cy, self.w = cx, cy, w
        self.h = w * self.mips.h / self.mips.w
        self.reveal, self.pulse, self.z, self.t0, self.t1, self.fade = reveal, pulse, z, t0, t1, fade

    def bbox(self, t):
        return (self.cx - self.w / 2, self.cy - self.h / 2, self.cx + self.w / 2, self.cy + self.h / 2)

    def draw(self, ctx, t, cam):
        a = min(ramp(t, self.t0, self.fade), 1 - ramp(t, self.t1 - self.fade, self.fade))
        if self.reveal:
            ws, wf = self.reveal
            a *= smooth(math.log(ws / cam[2]) / math.log(ws / wf))
        if a <= 0.003:
            return
        w = self.w * (self.pulse(t) if self.pulse else 1)
        if self.pop:
            w *= 0.85 + 0.15 * back_out(ramp(t, self.t0, 0.5))
        paint_image(ctx, self.mips, self.cx, self.cy, w, a, W / cam[2])


@lru_cache(maxsize=4096)
def text_image(text, kind, color, px=180, stroke=0):
    f = font(kind, px)
    l, t, r, b = f.getbbox(text, stroke_width=stroke)
    pad = px // 6
    im = Image.new("RGBA", (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((pad - l, pad - t), text, font=f, fill=color + (255,), stroke_width=stroke,
                            stroke_fill=color + (255,))
    return im


@lru_cache(maxsize=4096)
def text_mips(text, kind, color, px=180):
    return Mips(text_image(text, kind, color, px))


def rgb255(c):
    return tuple(int(v * 255) for v in c)


class Text(Item):
    """World-space text. anim: stamp | fade | wipe | rise. h = world height of the glyph box."""

    def __init__(self, text, x, y, h, t0, t1=1e9, kind="label", color=INK, anim="rise",
                 align="center", rot=0.0, z=5, dur=0.45):
        self.text, self.x, self.y, self.hh, self.t0, self.t1 = text, x, y, h, t0, t1
        self.kind, self.color, self.anim, self.align, self.rot, self.z, self.dur = \
            kind, rgb255(color), anim, align, rot, z, dur
        self.mips = text_mips(text, kind, self.color)
        self.ww = h * self.mips.w / self.mips.h

    def _cx(self):
        return {"center": self.x, "left": self.x + self.ww / 2, "right": self.x - self.ww / 2}[self.align]

    def bbox(self, t):
        cx = self._cx()
        return (cx - self.ww, self.y - self.hh, cx + self.ww, self.y + self.hh)

    def draw(self, ctx, t, cam):
        if t < self.t0 or t > self.t1 + 0.5:
            return
        u = ramp(t, self.t0, self.dur)
        out = 1 - ramp(t, self.t1, 0.5)
        cx, cy, w, a = self._cx(), self.y, self.ww, ease_out(u) * out
        if self.anim == "stamp":
            w *= 1 + 0.6 * (1 - back_out(u, 2.2)) if u < 1 else 1
            a = clamp(u * 3) * out
        elif self.anim == "rise":
            cy += self.hh * 0.35 * (1 - ease_out(u))
        elif self.anim == "wipe":
            x0 = cx - w / 2
            ctx.save()
            ctx.rectangle(x0 - w * 0.05, cy - self.hh, w * 1.1 * ease_io(u), self.hh * 2)
            ctx.clip()
            paint_image(ctx, self.mips, cx, cy, w, out, W / cam[2], self.rot)
            ctx.restore()
            return
        if a > 0.003:
            paint_image(ctx, self.mips, cx, cy, w, a, W / cam[2], self.rot)


class Counter(Item):
    """Number that counts up in world space."""

    def __init__(self, x, y, h, t0, t1, v0, v1, fmt="{:,.0f}", t_out=1e9, color=INK, z=5):
        self.x, self.y, self.hh, self.t0, self.t1 = x, y, h, t0, t1
        self.v0, self.v1, self.fmt, self.t_out, self.color, self.z = v0, v1, fmt, t_out, rgb255(color), z

    def bbox(self, t):
        return (self.x - self.hh * 4, self.y - self.hh, self.x + self.hh * 4, self.y + self.hh)

    def draw(self, ctx, t, cam):
        if t < self.t0 or t > self.t_out + 0.5:
            return
        u = ease_out((t - self.t0) / (self.t1 - self.t0))
        s = self.fmt.format(self.v0 + (self.v1 - self.v0) * u)
        m = text_mips(s, "num" if s.isascii() else "title", self.color)  # Hindi units need Devanagari
        a = clamp((t - self.t0) * 4) * (1 - ramp(t, self.t_out, 0.5))
        w = self.hh * m.w / m.h
        bump = 1 + 0.08 * math.exp(-((t - self.t1) * 6) ** 2)
        paint_image(ctx, m, self.x, self.y, w * bump, a, W / cam[2])


class Stroke(Item):
    """A path drawn on like ink. pts in world coords; or arc=(cx, cy, r, a0, a1)."""

    def __init__(self, t0, dur, pts=None, arc=None, width=6, color=RED, t1=1e9, z=6, dash=None):
        self.t0, self.dur, self.pts, self.arc, self.width, self.color, self.t1, self.z = \
            t0, dur, pts, arc, width, color, t1, z
        self.dash = dash

    def bbox(self, t):
        if self.arc:
            cx, cy, r = self.arc[:3]
            return (cx - r, cy - r, cx + r, cy + r)
        xs, ys = [p[0] for p in self.pts], [p[1] for p in self.pts]
        return (min(xs), min(ys), max(xs), max(ys))

    def draw(self, ctx, t, cam):
        u = ease_io((t - self.t0) / self.dur)
        if u <= 0 or t > self.t1 + 0.5:
            return
        a = 1 - ramp(t, self.t1, 0.5)
        ctx.save()
        ctx.set_source_rgba(*self.color, a)
        ctx.set_line_width(self.width)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        if self.arc:
            cx, cy, r, a0, a1 = self.arc
            ctx.arc(cx, cy, r, a0, a0 + (a1 - a0) * u)
        else:
            seg = [math.dist(p, q) for p, q in zip(self.pts, self.pts[1:])]
            total, acc = sum(seg) * u, 0
            ctx.move_to(*self.pts[0])
            for (p, q), L in zip(zip(self.pts, self.pts[1:]), seg):
                if acc + L >= total:
                    k = (total - acc) / L if L else 0
                    ctx.line_to(p[0] + (q[0] - p[0]) * k, p[1] + (q[1] - p[1]) * k)
                    break
                ctx.line_to(*q)
                acc += L
        ctx.stroke()
        ctx.restore()


class Dot(Item):
    """Filled circle that pops in (optionally pulsing glow)."""

    def __init__(self, x, y, r, t0, t1=1e9, color=RED, glow=False, z=4):
        self.x, self.y, self.r, self.t0, self.t1, self.color, self.glow, self.z = x, y, r, t0, t1, color, glow, z

    def bbox(self, t):
        return (self.x - self.r * 3, self.y - self.r * 3, self.x + self.r * 3, self.y + self.r * 3)

    def draw(self, ctx, t, cam):
        if t < self.t0 or t > self.t1 + 0.5:
            return
        a = clamp((t - self.t0) * 3) * (1 - ramp(t, self.t1, 0.5))
        if self.glow:
            k = 0.5 + 0.5 * math.sin((t - self.t0) * 2 * math.pi * 1.2)
            r = self.r * (1.6 + 0.8 * k)
            g = cairo.RadialGradient(self.x, self.y, 0, self.x, self.y, r)
            g.add_color_stop_rgba(0, *self.color, 0.55 * a)
            g.add_color_stop_rgba(1, *self.color, 0)
            ctx.set_source(g)
            ctx.arc(self.x, self.y, r, 0, 2 * math.pi)
            ctx.fill()
        else:
            ctx.set_source_rgba(*self.color, a)
            ctx.arc(self.x, self.y, self.r * back_out(clamp((t - self.t0) / 0.35)), 0, 2 * math.pi)
            ctx.fill()


class Runner(Item):
    """The guide: the cover's runner silhouette moving along a world path.

    path: [(t, x, y, h)] keyframes (h = figure height in world units).
    """

    def __init__(self, path, flip=False, z=8, sprite="assets/runner.png", bob=1.0):
        self.path, self.flip, self.z, self.bob = path, flip, z, bob
        self.mips = load_image(sprite, None)
        self.t0, self.t1 = path[0][0], path[-1][0]

    def state(self, t):
        p = self.path
        for a, b in zip(p, p[1:]):
            if a[0] <= t <= b[0]:
                u = (t - a[0]) / (b[0] - a[0])
                return tuple(a[i] + (b[i] - a[i]) * u for i in range(1, 3)) + \
                    (a[3] * (b[3] / a[3]) ** u,)
        return None

    def bbox(self, t):
        s = self.state(t)
        if not s:
            return (0, 0, 0, 0)
        x, y, h = s
        return (x - h, y - h, x + h, y + h)

    def draw(self, ctx, t, cam):
        s = self.state(t)
        if not s:
            return
        x, y, h = s
        a = min(clamp((t - self.t0) * 3), clamp((self.t1 - t) * 3))
        stride = abs(math.sin(t * math.pi * 2.6))
        w = h * self.mips.w / self.mips.h
        ctx.save()
        ctx.translate(x, y - h / 2 - h * 0.03 * stride * self.bob)
        if self.flip:
            ctx.scale(-1, 1)
        ctx.rotate(0.04 * self.bob * math.sin(t * math.pi * 2.6))
        paint_image(ctx, self.mips, 0, 0, w, a, W / cam[2])
        ctx.restore()


class Bar(Item):
    """Outlined bar that fills from f0 to f1 (fractions) between t0 and t0 + dur."""

    def __init__(self, x, y, w, h, t0, dur, f0=0.0, f1=1.0, color=RED, t1=1e9, z=6, steps=None):
        self.x, self.y, self.w, self.h, self.t0, self.dur, self.f0, self.f1 = x, y, w, h, t0, dur, f0, f1
        self.color, self.t1, self.z, self.steps = color, t1, z, steps

    def bbox(self, t):
        return (self.x, self.y, self.x + self.w, self.y + self.h)

    def draw(self, ctx, t, cam):
        if t < self.t0 or t > self.t1 + 0.5:
            return
        a = clamp((t - self.t0) * 3) * (1 - ramp(t, self.t1, 0.5))
        f = self.f0 + (self.f1 - self.f0) * ease_io((t - self.t0 - 0.3) / self.dur)
        lw = self.h * 0.08
        ctx.set_source_rgba(*INK, a)
        ctx.set_line_width(lw)
        ctx.rectangle(self.x, self.y, self.w, self.h)
        ctx.stroke()
        pad = lw * 1.8
        ctx.set_source_rgba(*self.color, a)
        ctx.rectangle(self.x + pad, self.y + pad, max(0, (self.w - 2 * pad) * f), self.h - 2 * pad)
        ctx.fill()


class Hill(Item):
    """The ridge he climbs: a black slope with a red band below, like the cover."""

    def __init__(self, pts, depth=1700, band=550, z=-1):
        self.pts, self.depth, self.band, self.z = pts, depth, band, z
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        self.box = (min(xs), min(ys), max(xs), max(ys) + depth + band + 3000)

    def bbox(self, t):
        return self.box

    def _shape(self, ctx, off0, off1):
        ctx.move_to(self.pts[0][0], self.pts[0][1] + off0)
        for x, y in self.pts[1:]:
            ctx.line_to(x, y + off0)
        for x, y in reversed(self.pts):
            ctx.line_to(x, y + off1)
        ctx.close_path()

    def draw(self, ctx, t, cam):
        ctx.set_source_rgb(*INK)
        self._shape(ctx, 0, self.depth)
        ctx.fill()
        ctx.set_source_rgb(0.08 * 0.6, 0.02, 0.03)
        self._shape(ctx, self.depth, self.depth + 120)
        ctx.fill()
        ctx.set_source_rgb(*RED)
        self._shape(ctx, self.depth + 120, self.depth + self.band)
        ctx.fill()


# ---------------------------------------------------------------- subtitles
def split_sub(parts, maxc=46):
    out = []
    for t0, t1, txt in parts:
        words = txt.split()
        if len(txt) <= maxc:
            out.append((t0, t1, txt))
            continue
        n = math.ceil(len(txt) / maxc)
        per = len(txt) / n
        lines, cur = [], ""
        for wd in words:
            if cur and len(cur) + len(wd) + 1 > per * 1.15 and len(lines) < n - 1:
                lines.append(cur)
                cur = wd
            else:
                cur = (cur + " " + wd).strip()
        lines.append(cur)
        tot = sum(len(l) for l in lines)
        acc = t0
        for l in lines:
            d = (t1 - t0) * len(l) / tot
            out.append((acc, acc + d, l))
            acc += d
    return out


@lru_cache(maxsize=512)
def sub_surface(text):
    f = font("sub", 38)
    l, t, r, b = f.getbbox(text)
    padx, pady = 28, 14
    tw, th = r - l, 46
    im = Image.new("RGBA", (tw + 2 * padx, th + 2 * pady), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius=10, fill=(16, 16, 16, 205))
    d.rounded_rectangle((0, im.height - 5, 90, im.height - 1), radius=2, fill=(155, 22, 32, 255))
    d.text((padx - l, pady + (th - (b - t)) // 2 - t + 2), text, font=f, fill=(240, 236, 228, 255))
    return to_surface(im), im.width, im.height


def draw_subs(ctx, t, subs):
    for t0, t1, txt in subs:
        if t0 - 0.12 <= t <= t1 + 0.12:
            a = min(clamp((t - t0 + 0.12) / 0.18), clamp((t1 + 0.12 - t) / 0.18))
            s, sw, sh = sub_surface(txt)
            ctx.save()
            ctx.translate((W - sw) / 2, H - sh - 46 + 8 * (1 - a))
            ctx.set_source_surface(s, 0, 0)
            ctx.paint_with_alpha(a)
            ctx.restore()
            break


# ---------------------------------------------------------------- frame + video
def make_grain(seed):
    rng = np.random.default_rng(seed)
    n = rng.normal(0, 1, (H // 2, W // 2))
    im = Image.fromarray(np.clip(128 + n * 40, 0, 255).astype(np.uint8)).resize((W, H), Image.NEAREST)
    g = np.asarray(im, np.float32) / 255
    dark = (g < 0.5)
    a = np.where(dark, (0.5 - g) * 0.16, (g - 0.5) * 0.10)
    rgba = np.zeros((H, W, 4), np.uint8)
    rgba[..., :3] = np.where(dark[..., None], 0, 255)
    rgba[..., 3] = (a * 255).astype(np.uint8)
    return to_surface(Image.fromarray(rgba))


def make_vignette():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    a = np.clip((r - 0.75) / 0.8, 0, 1) ** 1.6 * 0.33
    rgba = np.zeros((H, W, 4), np.uint8)
    rgba[..., 3] = (a * 255).astype(np.uint8)
    return to_surface(Image.fromarray(rgba))


class Film:
    def __init__(self, items, camera, subs):
        self.items = sorted(items, key=lambda i: i.z)
        self.camera, self.subs = camera, subs
        self.grain = [make_grain(i) for i in range(4)]
        self.vignette = make_vignette()

    def frame(self, t, surf=None):
        surf = surf or cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        ctx = cairo.Context(surf)
        ctx.set_source_rgb(*(c / 255 for c in PAPER))
        ctx.paint()
        cx, cy, cw = cam = self.camera(t)
        ch = cw * ASPECT
        vx0, vy0, vx1, vy1 = cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2
        ctx.save()
        ctx.scale(W / cw, W / cw)
        ctx.translate(-vx0, -vy0)
        for it in self.items:
            if t < it.t0 - 1 or t > it.t1 + 1:
                continue
            b = it.bbox(t)
            if b and (b[2] < vx0 or b[0] > vx1 or b[3] < vy0 or b[1] > vy1):
                continue
            # skip items far too small to see
            if b and (b[2] - b[0]) * W / cw < 1.5:
                continue
            it.draw(ctx, t, cam)
        ctx.restore()
        ctx.set_source_surface(self.vignette, 0, 0)
        ctx.paint()
        ctx.set_source_surface(self.grain[int(t * FPS / 2) % 4], 0, 0)
        ctx.paint()
        draw_subs(ctx, t, self.subs)
        return surf

    def render(self, out, t0, t1, crf=int(os.environ.get("CRF", 18))):
        n0, n1 = round(t0 * FPS), round(t1 * FPS)
        p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra",
                              "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                              "-preset", "medium", "-crf", str(crf), "-pix_fmt", "yuv420p", out],
                             stdin=subprocess.PIPE)
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        for n in range(n0, n1):
            self.frame(n / FPS, surf)
            surf.flush()
            p.stdin.write(surf.get_data())
        p.stdin.close()
        p.wait()

    def still(self, t, out):
        s = self.frame(t)
        s.write_to_png(out)
