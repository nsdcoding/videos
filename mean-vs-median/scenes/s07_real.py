import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

RT = [80, 90, 95, 100, 105, 110, 115, 120, 125, 130, 140, 150, 160, 170, 850, 960]  # illustrative response times (ms)


def icon(kind, c=INK):
    if kind == "fin":
        g = VGroup(Circle(0.5), T("$", 48, c, weight=BOLD))
    elif kind == "cs":
        scr = RoundedRectangle(corner_radius=0.06, width=1.1, height=0.72)
        g = VGroup(scr, Line(DOWN * 0.36, DOWN * 0.56), Line(LEFT * 0.3 + DOWN * 0.56, RIGHT * 0.3 + DOWN * 0.56),
                   T("</>", 26, c, weight=BOLD).move_to(scr))
    elif kind == "ds":
        g = VGroup(*[Rectangle(width=0.36, height=0.22) .move_to(np.array([(i - 1) * 0.36, (1 - j) * 0.22, 0]))
                     for i in range(3) for j in range(3)])
    else:
        nodes = [np.array(p) for p in ((-0.45, 0.3, 0), (-0.45, -0.3, 0), (0, 0.4, 0), (0, 0, 0), (0, -0.4, 0), (0.45, 0, 0))]
        g = VGroup(*[Line(nodes[a], nodes[b], stroke_width=2) for a in (0, 1) for b in (2, 3, 4)],
                   *[Line(nodes[a], nodes[5], stroke_width=2) for a in (2, 3, 4)],
                   *[Dot(p, radius=0.07, color=c) for p in nodes])
    g.set_stroke(c, 3)
    for t in g:
        if isinstance(t, Text): t.set_stroke(width=0)
    return g


def report_card(title, headline, kind_icon):
    box = RoundedRectangle(corner_radius=0.16, width=6.3, height=2.6, stroke_color=INK2, stroke_width=2,
                           fill_color="#22221f", fill_opacity=1)
    box.qa_container = True
    t = T(title, 24, MUTED).move_to(box.get_corner(UL) + RIGHT * 0.3 + DOWN * 0.35, aligned_edge=LEFT)
    h = T(headline, 30, VIOLET, weight=BOLD).next_to(t, DOWN, buff=0.3, aligned_edge=LEFT)
    lines = VGroup(*[Line(ORIGIN, RIGHT * w, stroke_width=6, color="#3a3a37") for w in (4.6, 3.8, 2.4)])
    lines.arrange(DOWN, buff=0.18, aligned_edge=LEFT).next_to(h, DOWN, buff=0.35, aligned_edge=LEFT)
    kind_icon.scale(0.6).move_to(box.get_corner(DR) + UL * 0.55)
    return VGroup(box, t, h, lines, kind_icon)


def person(s=1.0, c=INK):
    return VGroup(Circle(0.12 * s).shift(UP * 0.3 * s), Arc(radius=0.22 * s, start_angle=0, angle=PI).shift(DOWN * 0.05 * s)).set_stroke(c, 3)


def curve_on(ax, f, x0, x1, ymax, color):
    xs = np.linspace(x0, x1, 241)
    pts = [ax.c2p(x, f(x)) for x in xs if f(x) <= ymax]
    v = VMobject(color=color, stroke_width=4)
    if len(pts) > 1:
        v.set_points_smoothly(pts)
    return v


class S07Real(Base):
    CHAPTER = "Real World"

    def construct(self):
        fr = self.camera.frame
        # ── s119 four places ──
        self.at("s119", 0.0)
        names = [("Finance", "fin", WARN), ("Computer Science", "cs", BLUE_), ("Data Science", "ds", AQUA), ("Machine Learning", "ml", VIOLET)]
        tilesg = VGroup()
        for n, k, c in names:
            box = RoundedRectangle(corner_radius=0.2, width=4.6, height=2.2, stroke_color=c, stroke_width=3, fill_color="#22221f", fill_opacity=1)
            box.qa_container = True
            ic = icon(k, c).move_to(box.get_center() + UP * 0.3)
            lb = T(n, 30, INK, weight=BOLD).next_to(ic, DOWN, buff=0.3)
            tilesg.add(VGroup(box, ic, lb))
        tilesg.arrange_in_grid(rows=2, cols=2, buff=(0.5, 0.4)).move_to(UP * 0.35)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.3) for t in tilesg], lag_ratio=0.2), run_time=1.4)
        # ── s120 money ──
        self.at("s120", 0.0)
        self.play(fr.animate.scale(0.42).move_to(tilesg[0]), run_time=0.9)
        self.play(FadeOut(tilesg), run_time=0.4)
        fr.scale(1 / 0.42).move_to(ORIGIN)
        # ── s121 right tail like Pine Hill ──
        self.at("s121", 0.0)
        ax = money_axis(); ax.shift(DOWN * 0.9 - ax.axis.get_center()); L = ax.axis
        dots = dot_plot(PINE, L, [BLUE_] * 8 + [ORANGE_])
        self.play(FadeIn(ax), FadeIn(dots, lag_ratio=0.05), run_time=0.8)
        f = lambda x: 2.6 * (x / 40) ** 2.2 * np.exp(-2.2 * (x / 40 - 1))
        curve = VMobject(color=WARN, stroke_width=5).set_points_smoothly([L.n2p(x) + UP * f(x) * 0.95 for x in np.linspace(0, 240, 120)])
        sh = T("incomes & house prices: the same lopsided shape", 30, WARN).move_to(UP * 2.4)
        self.until(word_time("s121", word_index("s121", "long")))
        self.play(Create(curve), FadeIn(sh), run_time=1.4)
        lt = T("long right tail", 26, ORANGE_).move_to([L.n2p(165)[0], 0.0, 0])
        self.play(FadeIn(lt, shift=RIGHT * 0.3), run_time=0.5)
        # ── s122 income report ──
        self.at("s122", 0.0)
        self.play(FadeOut(VGroup(ax, dots, curve, sh, lt)), run_time=0.5)
        rc1 = report_card("Census income report", "Median household income", icon("fin", INK2)).move_to(LEFT * 3.4 + UP * 0.5)
        self.play(FadeIn(rc1, shift=UP * 0.3), run_time=0.7)
        nm = T("not the mean", 28, RED_).next_to(rc1, DOWN, buff=0.25)
        self.until(word_time("s122", word_index("s122", "not")))
        self.play(FadeIn(nm), run_time=0.4)
        # ── s123 housing ──
        self.at("s123", 0.0)
        rc2 = report_card("Housing market report", "Median sale price", house(0.7, INK2)).move_to(RIGHT * 3.4 + UP * 0.5)
        self.play(FadeIn(rc2, shift=UP * 0.3), run_time=0.7)
        # ── s124 company average salary ──
        self.at("s124", 0.0)
        self.play(FadeOut(VGroup(rc1, rc2, nm)), run_time=0.5)
        sal = NumberLine(x_range=[0, 10, 1], length=11, color=INK2, include_tip=False, tick_size=0.07).move_to(DOWN * 0.9)
        st = T("salary (shape only)", 24, MUTED).next_to(sal, DOWN, buff=0.25).align_to(sal, LEFT)
        staff = VGroup(*[person(0.9, BLUE_).move_to(sal.n2p(x) + UP * 0.45) for x in (0.8, 1.1, 1.4, 1.7, 2.0, 2.3, 2.6, 2.9)])
        boss = person(1.5, ORANGE_).move_to(sal.n2p(9.3) + UP * 0.65)
        bl = T("boss", 26, ORANGE_).next_to(boss, UP, buff=0.1)
        self.play(Create(sal), FadeIn(st), LaggedStart(*[FadeIn(p, shift=DOWN * 0.3) for p in staff], lag_ratio=0.06), run_time=0.9)
        self.until(word_time("s124", word_index("s124", "boss's")) - 0.2)
        self.play(FadeIn(boss, shift=DOWN * 0.4), FadeIn(bl), run_time=0.6)
        mpos = (sum([0.8, 1.1, 1.4, 1.7, 2.0, 2.3, 2.6, 2.9]) + 9.3) / 9
        mk = marker(sal, 1.85, WARN, "average salary", height=1.6, fs=24)
        dm = diamond(sal, 1.85, VIOLET, "median", height=1.15, fs=24, label_dir=LEFT)
        self.play(FadeIn(mk), FadeIn(dm), run_time=0.5)
        self.until(word_time("s124", word_index("s124", "one")))
        self.play(mk.animate.shift((sal.n2p(mpos)[0] - mk.get_x() + 0.0) * RIGHT), run_time=1.2)
        # ── s125 computer science ──
        self.at("s125", 0.0)
        self.play(FadeOut(VGroup(sal, st, staff, boss, bl, mk, dm)), run_time=0.5)
        win = RoundedRectangle(corner_radius=0.15, width=6.0, height=3.4, stroke_color=INK2, stroke_width=3).move_to(UP * 0.5)
        bar = Line(win.get_corner(UL) + DOWN * 0.45, win.get_corner(UR) + DOWN * 0.45, color=INK2, stroke_width=2)
        dots3 = VGroup(*[Dot(radius=0.06, color=c).move_to(win.get_corner(UL) + RIGHT * (0.3 + 0.22 * i) + DOWN * 0.22)
                         for i, c in enumerate((RED_, WARN, AQUA))])
        url = RoundedRectangle(corner_radius=0.1, width=3.6, height=0.28, stroke_color=INK2, stroke_width=1.5).move_to(
            win.get_top() + DOWN * 0.22 + RIGHT * 0.4)
        spin = Arc(radius=0.45, start_angle=0, angle=1.6 * PI, color=BLUE_, stroke_width=8).move_to(win.get_center() + DOWN * 0.2)
        self.play(Create(win), Create(bar), FadeIn(dots3), Create(url), run_time=0.8)
        self.add(spin)
        self.play(Rotate(spin, -TAU, about_point=spin.get_arc_center()), run_time=1.3, rate_func=linear)
        # ── s126 response times ──
        self.at("s126", 0.0)
        self.play(FadeOut(VGroup(win, bar, dots3, url, spin)), run_time=0.4)
        rax = money_axis(x_max=1000, step=100, label="response time (ms) — illustration")
        rax.shift(DOWN * 0.9 - rax.axis.get_center()); RL = rax.axis
        rdots = dot_plot(RT, RL, [BLUE_] * 14 + [ORANGE_] * 2, r=0.09)
        self.play(FadeIn(rax), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.3) for d in rdots[:14]], lag_ratio=0.04), run_time=0.8)
        self.until(word_time("s126", word_index("s126", "now")))
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.3) for d in rdots[14:]], lag_ratio=0.3), run_time=0.8)
        stuck = T("stuck requests", 26, ORANGE_).next_to(rdots[14:], UP, buff=0.2)
        self.play(FadeIn(stuck), run_time=0.4)
        # ── s127 mean dragged ──
        self.at("s127", 0.0)
        mean_rt, med_rt = float(np.mean(RT)), float(np.median(RT))
        pat = T("the Pine Hill pattern again", 30, INK).move_to(UP * 2.3)
        self.play(FadeIn(pat), run_time=0.5)
        rmk = marker(RL, med_rt, WARN, "", height=1.0)
        self.add(rmk)
        self.until(word_time("s127", word_index("s127", "drag")))
        self.play(rmk.animate.shift((RL.n2p(mean_rt)[0] - rmk.get_x()) * RIGHT), run_time=1.0)
        ml = T(f"mean ≈ {mean_rt:.0f} ms", 26, WARN, weight=BOLD).next_to(rmk.tri, RIGHT, buff=0.15)
        self.play(FadeIn(ml), run_time=0.4)
        # ── s128 p50 and p99 ──
        self.at("s128", 0.0)
        p99 = float(np.percentile(RT, 99))
        d50 = diamond(RL, med_rt, VIOLET, f"p50 = {med_rt:.0f} ms", height=1.6, fs=24, label_dir=UP)
        d99 = diamond(RL, p99, ORANGE_, f"p99 ≈ {p99:.0f} ms", height=1.6, fs=24, label_dir=UP)
        self.play(FadeOut(pat), FadeIn(d50, shift=DOWN * 0.2), run_time=0.6)
        self.until(word_time("s128", word_index("s128", "p")) + 2.0)
        shade = Rectangle(width=RL.n2p(p99)[0] - RL.n2p(0)[0], height=0.35, stroke_width=0, fill_color=AQUA, fill_opacity=0.18)
        shade.move_to(RL.n2p(0), aligned_edge=LEFT).shift(UP * 0.18); shade.qa_ignore = True
        self.play(FadeIn(d99, shift=DOWN * 0.2), FadeIn(shade), FadeOut(stuck), run_time=0.7)
        nn = T("99% of requests are at least this fast", 24, AQUA).move_to(UP * 2.35 + RIGHT * 1.5)
        self.play(FadeIn(nn), run_time=0.4)
        # ── s129 data science: spreadsheet ──
        self.at("s129", 0.0)
        self.play(FadeOut(VGroup(rax, rdots, rmk, ml, d50, d99, shade, nn)), run_time=0.5)
        rows = VGroup()
        hdr = VGroup(T("household", 22, MUTED, weight=BOLD), T("income ($)", 22, MUTED, weight=BOLD))
        cw = (1.8, 2.4); rh = 0.36
        def row_of(a, b, col=INK):
            cells = VGroup()
            for i, (txt, w) in enumerate(zip((a, b), cw)):
                r = Rectangle(width=w, height=rh, stroke_color="#3a3a37", stroke_width=1.5, fill_color="#22221f", fill_opacity=1)
                r.qa_container = True
                t = T(txt, 22, col if i else INK2).move_to(r)
                cells.add(VGroup(r, t))
            return cells.arrange(RIGHT, buff=0)
        sheet = VGroup(row_of("household", "income ($)", MUTED), *[row_of(str(i + 1), f"{v * 1000:,}") for i, v in enumerate(PINE)])
        sheet.arrange(DOWN, buff=0).move_to(LEFT * 3.6 + UP * 0.45)
        self.play(FadeIn(sheet, lag_ratio=0.05), run_time=1.0)
        # ── s130 the typo ──
        self.at("s130", 0.0)
        cell = sheet[9][1]
        self.play(Indicate(cell, color=ORANGE_), run_time=0.7)
        self.until(word_time("s130", word_index("s130", "two")))
        typo = T("2,300,000", 22, RED_, weight=BOLD).move_to(cell[1])
        self.play(Transform(cell[1], typo), cell[0].animate.set_stroke(RED_, 2.5), run_time=0.6)
        ez = T("one extra zero", 26, RED_).next_to(cell, RIGHT, buff=0.3)
        self.play(FadeIn(ez, shift=LEFT * 0.2), run_time=0.4)
        # ── s131 mean jumps, median doesn't ──
        self.at("s131", 0.0)
        r1 = VGroup(T("mean:", 34, WARN, weight=BOLD), T("60  →  290", 34, WARN)).arrange(RIGHT, buff=0.3)
        r2 = VGroup(T("median:", 34, VIOLET, weight=BOLD), T("40  →  40", 34, VIOLET)).arrange(RIGHT, buff=0.3)
        rr = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 2.4 + UP * 1.4)
        self.play(FadeIn(r1, shift=LEFT * 0.3), run_time=0.6)
        self.until(word_time("s131", word_index("s131", "median")))
        self.play(FadeIn(r2, shift=LEFT * 0.3), run_time=0.6)
        # ── s132 checks + fill missing with median ──
        self.at("s132", 0.0)
        chk = VGroup(T("✓  big gap between mean and median?", 24, AQUA), T("     → check for typos & outliers", 24, INK2)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        chk.next_to(rr, DOWN, buff=0.5).align_to(rr, LEFT)
        self.play(FadeIn(chk, shift=UP * 0.2), run_time=0.7)
        self.until(word_time("s132", word_index("s132", "filling")))
        miss = row_of("10", "?", RED_).next_to(sheet, DOWN, buff=0)
        self.play(FadeIn(miss, shift=UP * 0.2), FadeOut(ez), run_time=0.5)
        fill = T("40,000 (median)", 22, VIOLET, weight=BOLD).move_to(miss[1][1])
        self.play(Transform(miss[1][1], fill), miss[1][0].animate.set_stroke(VIOLET, 2.5), run_time=0.7)
        sk = VGroup(T("missing value in skewed data", 24, VIOLET), T("→ fill it with the median", 24, VIOLET)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(chk, DOWN, buff=0.4).align_to(chk, LEFT)
        self.play(FadeIn(sk), run_time=0.5)
        # ── s133 machine learning ──
        self.at("s133", 0.0)
        self.play(FadeOut(VGroup(sheet, miss, rr, chk, sk)), run_time=0.5)
        mli = icon("ml", VIOLET).scale(1.4).move_to(UP * 1.2)
        lf = chip("loss function = how we score mistakes", VIOLET, 34).next_to(mli, DOWN, buff=0.5)
        self.play(FadeIn(mli, scale=0.8), run_time=0.5)
        self.play(FadeIn(lf, shift=UP * 0.2), run_time=0.6)
        # ── s134 one guess for everyone ──
        self.at("s134", 0.0)
        self.play(FadeOut(VGroup(mli, lf)), run_time=0.4)
        top = money_axis(x_max=240, step=40, length=7.6, font_size=18); top.title.set_opacity(0)
        top.shift(UP * 2.75 + RIGHT * 1.6 - top.axis.get_center()); TL = top.axis
        tdots = dot_plot(PINE, TL, [BLUE_] * 8 + [ORANGE_], r=0.08)
        tname = T("Pine Hill", 24, INK2, weight=BOLD).next_to(TL, LEFT, buff=0.3)
        self.play(FadeIn(top), FadeIn(tdots), FadeIn(tname), run_time=0.6)
        c = ValueTracker(0.0)
        out = ValueTracker(230.0)
        vals = lambda: PINE[:8] + [out.get_value()]
        gline = always_redraw(lambda: Line(TL.n2p(c.get_value()) + DOWN * 0.08, TL.n2p(c.get_value()) + UP * 0.55,
                                           color=AQUA, stroke_width=5))
        glab = always_redraw(lambda: T(f"guess {c.get_value():.0f}", 20, AQUA).next_to(gline, UP, buff=0.05))
        self.add(gline, glab)
        self.play(c.animate.set_value(90), run_time=1.2)
        self.play(c.animate.set_value(20), run_time=1.0)
        # ── s135 two scorecards ──
        self.at("s135", 0.0)
        A1 = xy_axes([0, 120, 20], [0, 800, 200], 5.0, 2.8, "guess (thousand $)", "total distance", font_size=18, y_vertical=True)
        A2 = xy_axes([0, 120, 20], [0, 100, 20], 5.0, 2.8, "guess (thousand $)", "squared distance (thousands)", font_size=18, y_vertical=True)
        A1.move_to(LEFT * 3.3 + DOWN * 0.25); A2.move_to(RIGHT * 3.6 + DOWN * 0.25)
        ax1, ax2 = A1.ax, A2.ax
        t1 = T("① absolute error", 26, VIOLET, weight=BOLD).next_to(ax1, UP, buff=0.25).align_to(ax1, LEFT)
        t2 = T("② squared error", 26, WARN, weight=BOLD).next_to(ax2, UP, buff=0.25).align_to(ax2, LEFT)
        self.play(FadeIn(A1), FadeIn(A2), run_time=0.7)
        # ── s136 absolute error ──
        self.at("s136", 0.0)
        self.play(FadeIn(t1), run_time=0.4)
        ab = lambda x: sum(abs(v - x) for v in vals())
        sq = lambda x: sum((v - x) ** 2 for v in vals()) / 1000
        dl = always_redraw(lambda: VGroup(*[Line(TL.n2p(c.get_value()) + UP * (0.1 + 0.05 * i), TL.n2p(v) + UP * (0.1 + 0.05 * i),
                                                   color=VIOLET, stroke_width=2) for i, v in enumerate(vals())]))
        self.play(FadeIn(dl), c.animate.set_value(0), run_time=0.8)
        p1 = always_redraw(lambda: Dot(ax1.c2p(c.get_value(), min(ab(c.get_value()), 800)), radius=0.09, color=VIOLET))
        self.add(p1)
        # ── s137 slide: min at 40 ──
        self.at("s137", 0.0)
        cv1 = always_redraw(lambda: curve_on(ax1, ab, 0, c.get_value(), 800, VIOLET))
        self.add(cv1)
        self.play(c.animate.set_value(120), run_time=2.0, rate_func=linear)
        cv1.clear_updaters()
        cv1full = curve_on(ax1, ab, 0, 120, 800, VIOLET); self.remove(cv1); self.add(cv1full)
        self.play(c.animate.set_value(40), run_time=0.9)
        m1 = VGroup(DashedLine(ax1.c2p(40, 0), ax1.c2p(40, 230), color=VIOLET, stroke_width=2),
                    T("min at 40 = the median", 22, VIOLET, weight=BOLD).move_to(ax1.c2p(85, 110)))
        self.play(FadeIn(m1), Flash(ax1.c2p(40, 230), color=VIOLET), run_time=0.7)
        # ── s138 squared error ──
        self.at("s138", 0.0)
        self.play(FadeIn(t2), c.animate.set_value(0), FadeOut(dl), run_time=0.8)
        sqs = always_redraw(lambda: VGroup(*[Square(side_length=abs(TL.n2p(v)[0] - TL.n2p(c.get_value())[0]), color=WARN,
                                                    stroke_width=1.5, fill_opacity=0.06).move_to(TL.n2p((v + c.get_value()) / 2), aligned_edge=DOWN)
                                             for v in vals()[:8]]))
        self.play(FadeIn(sqs), FadeOut(glab), run_time=0.5)
        self.play(c.animate.set_value(30), run_time=0.8)
        # ── s139 min at 60 ──
        self.at("s139", 0.0)
        self.play(FadeOut(sqs), c.animate.set_value(0), FadeIn(glab), run_time=0.4)
        p2 = always_redraw(lambda: Dot(ax2.c2p(c.get_value(), min(sq(c.get_value()), 100)), radius=0.09, color=WARN))
        cv2 = always_redraw(lambda: curve_on(ax2, sq, 0, max(c.get_value(), 0.5), 100, WARN))
        self.add(p2, cv2)
        self.play(c.animate.set_value(120), run_time=1.3, rate_func=linear)
        cv2.clear_updaters()
        self.play(c.animate.set_value(60), run_time=0.7)
        m2 = VGroup(DashedLine(ax2.c2p(60, 0), ax2.c2p(60, 32.8), color=WARN, stroke_width=2),
                    T("min at 60 = mean", 22, WARN, weight=BOLD).move_to(ax2.c2p(94, 14)))
        self.play(FadeIn(m2), Flash(ax2.c2p(60, 32.8), color=WARN), run_time=0.7)
        # ── s140 general rule ──
        self.at("s140", 0.0)
        rule = VGroup(T("for ANY data:", 30, INK2),
                      T("minimise squared error  →  the mean", 34, WARN, weight=BOLD),
                      T("minimise absolute error  →  the median", 34, VIOLET, weight=BOLD),
                      T("(even count: anywhere between the two middle values)", 24, INK2)).arrange(DOWN, buff=0.22)
        box = RoundedRectangle(corner_radius=0.2, width=rule.width + 0.8, height=rule.height + 0.6, stroke_color=INK2,
                               stroke_width=2, fill_color="#22221f", fill_opacity=0.97).move_to(DOWN * 0.3)
        box.qa_container = True
        rule.move_to(box)
        dim = VGroup(A1, A2, t1, t2, cv1full, cv2, m1, m2)
        veil = Rectangle(width=16, height=9, stroke_width=0, fill_color=BG, fill_opacity=0.85); veil.qa_ignore = True
        self.qa_mute(VGroup(dim, top, tdots, tname, gline, glab))
        self.play(FadeOut(p1), FadeOut(p2), FadeIn(veil), FadeIn(box), FadeIn(rule[0]), run_time=0.6)
        self.until(word_time("s140", word_index("s140", "minimising")))
        self.play(FadeIn(rule[1], shift=UP * 0.2), run_time=0.5)
        self.until(word_time("s140", word_index("s140", "absolute")) - 0.3)
        self.play(FadeIn(rule[2], shift=UP * 0.2), run_time=0.5)
        self.until(word_time("s140", word_index("s140", "even")))
        self.play(FadeIn(rule[3]), run_time=0.5)
        # ── s141 MSE / MAE ──
        self.at("s141", 0.0)
        self.play(FadeOut(VGroup(box, rule, veil)), run_time=0.5)
        self.qa_mute(VGroup(dim, top, tdots, tname), False)
        mse = chip("MSE → aims for the mean", WARN, 24).next_to(ax2, UP, buff=0.15).align_to(ax2, LEFT)
        mae = chip("MAE → aims for the median", VIOLET, 24).next_to(ax1, UP, buff=0.15).align_to(ax1, LEFT)
        self.play(FadeOut(t1), FadeOut(t2), FadeIn(mae, shift=DOWN * 0.2), run_time=0.5)
        self.until(word_time("s141", word_index("s141", "mean")) - 0.4)
        self.play(FadeIn(mse, shift=DOWN * 0.2), run_time=0.5)
        # ── s142 outlier grows: MSE chases, MAE shrugs ──
        self.at("s142", 0.0)
        self.remove(cv1full)
        self.play(FadeOut(m1), FadeOut(m2), run_time=0.3)
        self.drop(m1, m2)
        cvA = always_redraw(lambda: curve_on(ax1, ab, 0, 120, 800, VIOLET))
        cvB = always_redraw(lambda: curve_on(ax2, sq, 0, 120, 100, WARN))
        minA = always_redraw(lambda: Dot(ax1.c2p(40, ab(40)), radius=0.1, color=VIOLET))
        mB = lambda: sum(vals()) / 9
        minB = always_redraw(lambda: Dot(ax2.c2p(mB(), sq(mB())), radius=0.1, color=WARN))
        self.remove(cv2, gline, glab)
        self.add(cvA, cvB, minA, minB)
        olab = always_redraw(lambda: T(f"outlier: {out.get_value():.0f}", 20, ORANGE_).next_to(TL.n2p(min(out.get_value(), 240)), UP, buff=0.3).shift(LEFT * 0.4))
        self.add(olab)
        self.play(out.animate.set_value(330), run_time=2.2, rate_func=there_and_back_with_pause)
        self.play(out.animate.set_value(330), run_time=1.6)
        cA = T("minimum stays at 40", 22, VIOLET, weight=BOLD).move_to(ax1.c2p(85, 110))
        cB = T("minimum moves to ≈ 71", 22, WARN, weight=BOLD).move_to(ax2.c2p(72, 16))
        self.play(FadeIn(cA), FadeIn(cB), run_time=0.5)
        self.finish()
