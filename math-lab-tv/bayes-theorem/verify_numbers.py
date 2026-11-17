#!/usr/bin/env python3
"""Checks every number used in the narration and on screen (running example + side examples)."""
from fractions import Fraction as F

N = 1000; prev = F(1, 100); sens = F(9, 10); fpr = F(1, 10)
sick = N * prev; healthy = N - sick
tp = sick * sens; fn = sick - tp; fp = healthy * fpr; tn = healthy - fp
pos = tp + fp; neg = fn + tn
post = tp / pos
assert (sick, healthy, tp, fn, fp, tn, pos, neg) == (10, 990, 9, 1, 99, 891, 108, 892)
assert post == F(1, 12)                        # "about one in twelve"
print("P(sick|+) =", post, float(post))         # 0.0833 -> "about eight percent"
assert round(float(post) * 100) == 8
assert float(post / prev) > 8                   # "more than eight times higher"
assert fp / tp == 11                            # "false alarms outnumber real cases eleven to one"
assert healthy / sick == 99                     # "ninety-nine to one"
acc = (tp + tn) / N; assert acc == F(9, 10)     # "ninety percent accurate" overall
pneg = fn / neg; print("P(sick|-) =", pneg, float(pneg)); assert 850 < 1 / pneg < 950  # "about one in nine hundred"
# Bayes formula, symbol by symbol
PB = sens * prev + fpr * (1 - prev); assert PB == F(108, 1000)
assert sens * prev / PB == post and sens * prev == F(9, 1000)
# second test (independent errors), x10 crowd
s2, h2 = 90 * sens, 990 * fpr; assert (s2, h2) == (81, 99)
p2 = s2 / (s2 + h2); assert p2 == F(45, 100); print("after 2 positives", float(p2))
# odds form
LR = sens / fpr; assert LR == 9
o0 = F(1, 99); o1 = o0 * LR; o2 = o1 * LR; o3 = o2 * LR
assert o1 == F(9, 99) and o2 == F(81, 99) and o3 == F(729, 99)
p3 = o3 / (1 + o3); print("after 3 positives", float(p3)); assert round(float(p3) * 100) == 88
assert o1 / (1 + o1) == post
# ML: accuracy of "always healthy"
assert F(990, 1000) == F(99, 100)
# precision / recall
assert tp / sick == F(9, 10) and tp / pos == post
# mistake two: base rate one in five (symptomatic patients)
s5 = 200; h5 = 800; tp5 = s5 * sens; fp5 = h5 * fpr; assert (tp5, fp5) == (180, 80)
p5 = tp5 / (tp5 + fp5); print("base rate 1/5:", float(p5)); assert round(float(p5) * 100) == 69
# what moves the answer: base-rate curve and dials
def ppv(b, se=sens, fp_=fpr): return se * b / (se * b + fp_ * (1 - b))
assert ppv(F(1, 10)) == F(1, 2)                 # one in ten -> fifty percent
assert ppv(F(1, 2)) == F(9, 10)                 # half -> ninety percent
assert ppv(F(1, 5)) == p5
lowfp = ppv(prev, fp_=F(1, 100)); print("fpr 1/100:", float(lowfp)); assert round(float(lowfp) * 100) == 48
assert 990 * F(1, 100) == F(99, 10)             # "about ten false alarms"
perfect = ppv(prev, se=F(1)); print("perfect hit rate:", float(perfect)); assert round(float(perfect) * 100) == 9
# grid
assert 40 * 25 == 1000
print("all numbers verified")
