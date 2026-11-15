import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

PINE = [30, 32, 35, 38, 40, 42, 45, 48, 230]
MAPLE = [50, 52, 55, 58, 60, 62, 65, 68, 70]
PX_OFF = RIGHT * 16  # Pine Hill section lives 16 units to the right of Maple's


def skyline(kind):
    g = VGroup()
    if kind == "maple":
        for i, (w, h) in enumerate([(0.7, 1.0), (0.9, 1.5), (0.6, 0.8), (1.0, 1.9), (0.7, 1.2), (0.8, 1.4)]):
            b = Rectangle(width=w, height=h).set_stroke(INK2, 3).set_fill(BG, 1)
            g.add(b)
        g.arrange(RIGHT, buff=0.08, aligned_edge=DOWN)
        for b in g:
            wins = VGroup(*[Square(0.11).set_stroke(INK2, 2) for _ in range(int(b.height / 0.35) * 2)])
            wins.arrange_in_grid(cols=2, buff=0.12).move_to(b).shift(UP * 0.05)
            b.add(wins)
        trees = VGroup(*[VGroup(Line(ORIGIN, UP * 0.35), Circle(0.22).shift(UP * 0.55)).set_stroke(AQUA, 3)
                         for _ in range(3)])
        for t, x in zip(trees, (-2.2, 0.15, 2.3)):
            t.move_to(g.get_bottom() + RIGHT * x, aligned_edge=DOWN)
        g.add(trees)
    else:
        hill = Arc(radius=3.2, start_angle=PI * 0.36, angle=PI * 0.28).set_stroke(INK2, 3)
        small = VGroup(*[house(0.5) for _ in range(5)]).arrange(RIGHT, buff=0.12)
        small.next_to(hill, DOWN, buff=-0.05).shift(LEFT * 0.4)
        mans = house(0.6, mansion=True).set_stroke(ORANGE_, 3).move_to(hill.get_top(), aligned_edge=DOWN)
        pines = VGroup(*[Triangle().scale(0.22).stretch(1.6, 1).set_stroke(AQUA, 3) for _ in range(3)])
        for p, x in zip(pines, (-2.4, 2.1, 2.5)):
            p.move_to(small.get_bottom() + RIGHT * x, aligned_edge=DOWN)
        g.add(hill, small, mans, pines)
        g.mansion = mans
    return g


def counter(tr, color=WARN, size=64):
    return always_redraw(lambda: TB(f"${tr.get_value():.0f}k", size=size, color=color))


class S01TwoTowns(Base):
    CHAPTER = "Two Towns"

    def construct(self):
        fr = self.camera.frame
        # ── s001 two skylines + truck ──
        maple, pine = skyline("maple"), skyline("pine")
        maple.move_to(LEFT * 3.8 + UP * 1.75); pine.move_to(RIGHT * 3.8 + UP * 1.75)
        ground = Line(LEFT * 7, RIGHT * 7, color=GRID, stroke_width=2).move_to(UP * 0.5)
        truck = VGroup(Rectangle(width=0.9, height=0.5), Rectangle(width=0.4, height=0.35).shift(RIGHT * 0.65 + DOWN * 0.075),
                       Circle(0.1).shift(LEFT * 0.25 + DOWN * 0.3), Circle(0.1).shift(RIGHT * 0.6 + DOWN * 0.3))
        truck.set_stroke(INK, 3).set_fill(BG, 1).move_to(LEFT * 8 + UP * 0.85)
        self.at("s001", 0.0)
        self.play(Create(ground), Create(maple, lag_ratio=0.1), Create(pine, lag_ratio=0.1), run_time=2.0)
        self.play(truck.animate.move_to(UP * 0.85), run_time=1.2, rate_func=smooth)
        # ── s002 name plates ──
        self.at("s002", 0.0)
        nm = TB("MAPLE", 40).next_to(maple, DOWN, buff=0.45)
        np_ = TB("PINE HILL", 40).next_to(pine, DOWN, buff=0.45).align_to(nm, UP)
        self.play(FadeIn(nm, shift=UP * 0.3), run_time=0.6)
        self.play(FadeIn(np_, shift=UP * 0.3), truck.animate.shift(UP * 0.0).scale(0.9), run_time=0.6)
        # ── s003 stat cards ──
        self.at("s003", 1.2)
        def card(anchor):
            box = RoundedRectangle(corner_radius=0.18, width=4.6, height=1.9, stroke_color=INK2, stroke_width=2,
                                   fill_color="#22221f", fill_opacity=1)
            box.qa_container = True
            lab = T("Average household income", 24, INK2).move_to(box.get_top() + DOWN * 0.36)
            return VGroup(box, lab).next_to(anchor, DOWN, buff=0.25)
        cA, cB = card(nm), card(np_)
        self.play(FadeOut(truck), LaggedStart(FadeIn(cA, shift=DOWN * 0.4), FadeIn(cB, shift=DOWN * 0.4), lag_ratio=0.3),
                  run_time=1.2)
        # ── s004 counters 0 → 60 ──
        self.at("s004", 0.0)
        tr = ValueTracker(0)
        nA = counter(tr).add_updater(lambda m: m.move_to(cA[0].get_center() + DOWN * 0.16))
        nB = counter(tr).add_updater(lambda m: m.move_to(cB[0].get_center() + DOWN * 0.16))
        self.add(nA, nB)
        self.play(tr.animate.set_value(60), run_time=1.4, rate_func=rate_functions.ease_out_cubic)
        nA.clear_updaters(); nB.clear_updaters()
        gA, gB = glow(nA.copy(), WARN), glow(nB.copy(), WARN)
        self.remove(nA, nB); self.add(gA, gB)
        yr = T("per year", 22, MUTED)
        yrA = yr.copy().next_to(gA, RIGHT, buff=0.2).align_to(gA, DOWN).shift(UP * 0.08)
        yrB = yr.copy().next_to(gB, RIGHT, buff=0.2).align_to(gB, DOWN).shift(UP * 0.08)
        self.play(FadeIn(yrA, shift=LEFT * 0.2), FadeIn(yrB, shift=LEFT * 0.2),
                  gA.animate.shift(LEFT * 0.6), gB.animate.shift(LEFT * 0.6),
                  yrA.animate.shift(LEFT * 0.6), yrB.animate.shift(LEFT * 0.6), run_time=0.5)
        # ── s005 '=' then '?' ──
        self.at("s005", 0.0)
        eq = TB("=", 96, INK).move_to((cA.get_center() + cB.get_center()) / 2)
        self.play(GrowFromCenter(eq), run_time=0.5)
        self.play(eq.animate.scale(1.25), rate_func=there_and_back, run_time=0.6)
        q = TB("?", 72, RED_).next_to(eq, UP, buff=0.3)
        self.at("s005", 1.6)
        self.play(FadeIn(q, shift=DOWN * 0.6), rate_func=rate_functions.ease_out_bounce, run_time=0.8)
        # ── s006 push into Maple ──
        self.at("s006", 0.0)
        self.play(*[FadeOut(m) for m in (pine, np_, cA, cB, gA, gB, yrA, yrB, eq, q, nm)], run_time=0.5)
        self.play(fr.animate.scale(0.45).move_to(maple), run_time=1.1, rate_func=smooth)
        self.play(FadeOut(ground), FadeOut(maple, scale=1.3), run_time=0.45)
        fr.scale(1 / 0.45).move_to(ORIGIN)

        # ── Maple section ──
        ax = money_axis(); ax.shift(DOWN * 0.3 - ax.axis.get_center())
        L = ax.axis
        title = TB("Maple", 44).to_corner(UR, buff=0.32)
        homes = VGroup(*[house(0.55) for _ in range(9)]).arrange(RIGHT, buff=0.45).move_to(UP * 2.25)
        self.at("s007", 0.0)
        cnt = ValueTracker(1)
        ctext = always_redraw(lambda: T(f"households: {int(cnt.get_value())}", 28, INK2).next_to(title, LEFT, buff=0.5))
        self.add(ctext)
        self.play(FadeIn(title, shift=LEFT * 0.4), LaggedStart(*[FadeIn(h, shift=UP * 0.5) for h in homes], lag_ratio=0.12),
                  cnt.animate.set_value(9), run_time=1.3, rate_func=linear)
        ctext.clear_updaters()
        # ── s008 axis + dots drop as each value is spoken ──
        self.at("s008", 0.0)
        self.play(Create(L), FadeIn(ax.nums, lag_ratio=0.05), FadeIn(ax.title), run_time=1.6)
        dots = dot_plot(MAPLE, L, [INK] * 9, r=0.1)
        vals = VGroup()
        k0 = word_index("s008", "fifty")
        for i, (d, h, v) in enumerate(zip(dots, homes, MAPLE)):
            self.until(word_time("s008", k0 + i) - 0.05)
            start = d.copy().move_to(h.get_bottom())
            lab = T(str(v), 24, INK).next_to(h, UP, buff=0.12)
            self.add(start)
            self.play(Transform(start, d), h.animate.set_stroke(INK), FadeIn(lab, shift=UP * 0.15),
                      run_time=0.55, rate_func=rate_functions.ease_in_quad)
            self.remove(start); self.add(d); vals.add(lab)

        # ── s009 bracket over cluster ──
        self.at("s009", 0.0)
        br = BraceBetweenPoints(L.n2p(70) + UP * 0.62, L.n2p(50) + UP * 0.62, direction=UP, color=AQUA)
        brt = T("all within 10 of 60", 28, AQUA).next_to(br, UP, buff=0.12)
        self.play(FadeOut(VGroup(homes, vals, ctext, title)), fr.animate.scale(0.6).move_to([L.n2p(60)[0], -0.15, 0]),
                  run_time=1.0)
        self.play(GrowFromCenter(br), FadeIn(brt, shift=UP * 0.2), run_time=0.7)
        maple_grp = VGroup(ax, dots, br, brt)

        # ── s010 pan to Pine Hill ──
        ax2 = money_axis(); ax2.shift(DOWN * 0.3 + PX_OFF - ax2.axis.get_center())
        L2 = ax2.axis
        title2 = TB("Pine Hill", 44).to_corner(UR, buff=0.5).shift(DOWN * 0.15 + PX_OFF)
        homes2 = VGroup(*[house(0.55) for _ in range(8)], house(0.5, mansion=True).set_stroke(ORANGE_, 3))
        homes2.arrange(RIGHT, buff=0.38, aligned_edge=DOWN).move_to(UP * 2.25 + PX_OFF)
        self.add(ax2, title2, homes2)
        self.at("s010", 0.0)
        self.play(fr.animate.scale(1 / 0.6).move_to(PX_OFF), run_time=1.6, rate_func=smooth)
        self.drop(maple_grp, homes, vals, ctext, title)
        self.play(Indicate(homes2[-1], color=ORANGE_, scale_factor=1.15), run_time=0.9)
        # ── s011 eight blue dots ──
        self.at("s011", 0.0)
        cols = [BLUE_] * 8 + [ORANGE_]
        dots2 = dot_plot(PINE, L2, cols, r=0.1)
        self.play(fr.animate.scale(0.6).move_to([L2.n2p(55)[0], -0.55, 0]), homes2[:8].animate.set_stroke(BLUE_), run_time=0.9)
        drops = []
        for d, h in zip(dots2[:8], homes2[:8]):
            s = d.copy().move_to(h.get_bottom())
            drops.append((s, d))
        self.add(*[s for s, _ in drops])
        self.play(LaggedStart(*[Transform(s, d) for s, d in drops], lag_ratio=0.15), run_time=1.8,
                  rate_func=rate_functions.ease_in_quad)
        for s, d in drops:
            self.remove(s); self.add(d)
        # ── s012 mansion dot flies to 230, camera zooms out ──
        self.at("s012", 0.3)
        md = dots2[8]
        s = md.copy().move_to(homes2[-1].get_bottom())
        self.add(s)
        self.play(fr.animate.scale(1 / 0.6).move_to(PX_OFF), Transform(s, md, path_arc=-0.6), run_time=1.6)
        self.remove(s); self.add(md)
        tag = T("230", 26, ORANGE_).next_to(md, UP, buff=0.15)
        self.play(FadeIn(tag, shift=UP * 0.2), Flash(md, color=ORANGE_, line_length=0.25), run_time=0.6)
        # ── s013 the mean marker at 60 ──
        self.at("s013", 1.2)
        tri = Triangle(color=WARN, fill_opacity=1).scale(0.16).rotate(PI).next_to(L2.n2p(60), UP, buff=1.0)
        stem = DashedLine(tri.get_bottom(), L2.n2p(60), color=WARN, stroke_width=3)
        mlab = T("average = 60", 28, WARN).next_to(tri, LEFT, buff=0.15)
        mk = VGroup(stem, tri)
        self.play(FadeIn(mk, shift=DOWN * 0.3), run_time=0.7)
        gml = glow(mlab, WARN)
        self.play(FadeIn(gml, shift=DOWN * 0.2), run_time=0.6)
        # ── s014 zoom to the cluster, pulse dots ──
        self.at("s014", 0.0)
        self.play(fr.animate.scale(0.55).move_to([L2.n2p(50)[0], 0.12, 0]), FadeOut(homes2), FadeOut(title2), run_time=1.0)
        self.play(LaggedStart(*[Indicate(d, color=BLUE_, scale_factor=1.6) for d in dots2[:8]], lag_ratio=0.1),
                  run_time=1.0)
        # ── s015 counter 8 of 9 below ──
        self.at("s015", 0.0)
        rings = VGroup(*[Circle(0.14, color=BLUE_, stroke_width=2.5).move_to(d) for d in dots2[:8]])
        k = ValueTracker(0)
        below = always_redraw(lambda: T(f"{int(k.get_value())} of 9 below the average", 30, BLUE_)
                              .move_to([L2.n2p(36)[0], 1.6, 0]))
        self.add(below)
        self.play(LaggedStart(*[d.animate(rate_func=there_and_back).scale(1.6) for d in dots2[:8]], lag_ratio=0.12),
                  k.animate(rate_func=linear).set_value(8), run_time=1.4)
        below.clear_updaters()
        nums = VGroup()
        # ── s016 empty zone ──
        self.at("s016", 0.0)
        self.play(fr.animate.scale(1 / 0.55).move_to(PX_OFF), FadeOut(nums), FadeIn(homes2), FadeIn(title2), run_time=1.1)
        zone = DashedVMobject(Rectangle(width=L2.n2p(218)[0] - L2.n2p(66)[0], height=1.0), num_dashes=60)
        zone.set_stroke(RED_, 3).move_to((L2.n2p(66) + L2.n2p(218)) / 2 + UP * 0.6)
        zlab = T("nobody lives near here", 30, RED_).move_to(L2.n2p(145) + UP * 0.6)
        self.at("s016", 2.0)
        self.play(Create(zone), run_time=0.9)
        self.play(FadeIn(zlab, shift=UP * 0.2), run_time=0.6)
        # ── s017 title card ──
        self.at("s017", 0.0)
        pine_grp = VGroup(ax2, title2, homes2, dots2, tag, mk, gml, below, zone, zlab)
        self.play(FadeOut(pine_grp, shift=UP * 0.5), run_time=0.8)
        self.drop(pine_grp)
        self.camera.frame.move_to(ORIGIN)
        wm = glow(TB("MEAN", 110, WARN), WARN)
        wd = glow(TB("MEDIAN", 110, VIOLET), VIOLET)
        vs = T("vs", 48, MUTED)
        row = VGroup(wm.copy(), vs.copy(), wd.copy()).arrange(RIGHT, buff=0.55).move_to(UP * 0.6)
        tm, tv, td = row[0].get_center(), row[1].get_center(), row[2].get_center()
        wm.move_to(LEFT * 11 + UP * 0.6); wd.move_to(RIGHT * 11 + UP * 0.6); vs.move_to(tv)
        self.until(word_time("s017", word_index("s017", "mean")) - 0.3)
        self.play(wm.animate.move_to(tm), run_time=0.7, rate_func=rate_functions.ease_out_back)
        self.until(word_time("s017", word_index("s017", "median")) - 0.3)
        sub = T("Which average is lying to you?", 44, INK).move_to(DOWN * 1.0)
        self.play(wd.animate.move_to(td), FadeIn(vs, scale=0.5), run_time=0.7,
                  rate_func=rate_functions.ease_out_back)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.5)
        self.finish()
