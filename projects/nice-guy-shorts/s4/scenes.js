// Short 4 — सीमा के तीन नियम
function build() {
  const END = endT();
  const nx = i => (i + 1 < TIMING.length ? S(i + 1).a - 0.2 : END);
  const rule = (L, n, lab) => ruleCard(L.cam, n, lab, 540, 300, L.t0 + 0.3, { h: 170, fs: 52 });

  // 0 — tired of saying yes to everyone
  { const s = S(0); const L = layer(0, nx(0), 'cut', 'bg_office');
    camMove(L, { scale: 1.14 }, { scale: 1.0 }, 'power2.out');
    const g = Guy(L.cam, 540, 1580, 1.15); g.headSwap(W_(0, 'थक'), 'head_tired');
    [[220, 380], [820, 340], [300, 620], [800, 600], [190, 860], [880, 860], [540, 300]].forEach(([x, y], k) =>
      pop(tag(L.cam, 'हाँ!', x, y, { fontSize: '56px', background: k % 2 ? MUSTARD : CREAM }), 0.1 + k * 0.28, { rot: k % 2 ? 10 : -10 }));
    const sk = img(L.cam, 'sack', 820, 1230, 200); pop(sk, 1.2);
  }
  // 1 — a boundary isn't a wall; it's being clear
  { const s = S(1); const L = layer(s.a - 0.2, nx(1), 'wipe', 'bg_paper');
    camMove(L, { scale: 1.06 }, { scale: 1.0 });
    const wl = text(L.cam, 'दीवार', 540, 420, { fontSize: '120px', color: INK, background: '#a9573a', padding: '10px 60px', border: `8px solid ${INK}`, borderRadius: '10px', color: CREAM });
    pop(wl, s.a + 0.1); strike(L.cam, 540, 420, 420, W_(1, 'नहीं है'));
    const fn = img(L.cam, 'fence', 540, 900, 520); pop(fn, W_(1, 'मतलब है'));
    rise(big(L.cam, 'सीमा = साफ़ होना', 540, 1230, 96, '#3f6b30'), W_(1, 'साफ़'));
  }
  // 2 — three rules
  { const s = S(2); const L = layer(s.a - 0.2, nx(2), 'iris'); solid(L, INK);
    camMove(L, { scale: 1.0 }, { scale: 1.08 });
    person(L.cam, 'psych', 290, 1560, 800, 3);
    const n = text(L.cam, '3', 760, 740, { fontSize: '460px', color: MUSTARD, fontFamily: "'Rozha One'", fontWeight: 400 }); pop(n, W_(2, 'तीन'), { rot: -15 });
    rise(big(L.cam, 'नियम', 760, 1060, 110, CREAM, { width: '500px' }), W_(2, 'नियम'));
    pop(tag(L.cam, 'रॉबर्ट ग्लोवर', 540, 300, { fontSize: '52px', background: MUSTARD }), s.a);
  }
  // 3 — rule 1: don't say yes instantly — "let me check and tell you"
  { const s = S(3); const L = layer(s.a - 0.2, nx(3), 'push', 'bg_office');
    camMove(L, { scale: 1.0 }, { scale: 1.05 }); rule(L, 1, 'तुरंत हाँ मत कहिए');
    const g = Guy(L.cam, 310, 1580, 1.0, { head: 'head_calm' }); g.headSwap(W_(3, 'मैं देखकर'), 'head'); g.say(W_(3, 'मैं देखकर'), s.b);
    person(L.cam, 'boss', 790, 1580, 760, 2);
    const sk = img(L.cam, 'sack', 640, 1160, 160); pop(sk, s.a + 0.3);
    bubble(L.cam, 'मैं देखकर बताता हूँ।', 420, 560, W_(3, 'मैं देखकर'), { fontSize: '52px', background: MUSTARD });
  }
  // 4 — rule 2: no long explanations; each one opens the next argument
  { const s = S(4); const L = layer(s.a - 0.2, nx(4), 'wipeUp', 'bg_paper');
    camMove(L, { scale: 1.06 }, { scale: 1.0 }); rule(L, 2, 'लंबी सफ़ाई नहीं');
    const ct = img(L.cam, 'contract', 300, 780, 360); pop(ct, W_(4, 'लंबी'), { rot: -10 });
    ['क्योंकि…', 'असल में…', 'और फिर…'].forEach((w, k) => pop(tag(L.cam, w, 300 + (k - 1) * 40, 640 + k * 110, { fontSize: '40px' }), W_(4, 'सफ़ाई') + k * 0.2));
    cross(L.cam, 300, 780, 2.2, W_(4, 'मत दीजिए'));
    const ok = tag(L.cam, '“इस बार नहीं।”', 780, 760, { fontSize: '56px', background: '#3f6b30', color: CREAM }); pop(ok, W_(4, 'मत दीजिए') + 0.3);
    rise(big(L.cam, 'हर सफ़ाई = अगली बहस', 540, 1200, 80, RUST), W_(4, 'हर सफ़ाई'));
    arrow(L.cam, 300, 960, 400, 1120, W_(4, 'दरवाज़ा') - 0.3, { color: RUST, width: 8, bend: 0.2 });
  }
  // 5 — rule 3: once stated, keep it
  { const s = S(5); const L = layer(s.a - 0.2, nx(5), 'zoom', 'bg_park');
    camMove(L, { scale: 1.0 }, { scale: 1.06 }); rule(L, 3, 'बताई है, तो निभाइए');
    const g = Guy(L.cam, 540, 1580, 1.1, { head: 'head_calm' });
    const fn = img(L.cam, 'fence', 540, 1330, 620); pop(fn, W_(5, 'सीमा'));
    check(L.cam, 860, 620, 1.6, W_(5, 'निभाइए'), '#3f6b30');
  }
  // 6 — a broken boundary is worse than none
  { const s = S(6); const L = layer(s.a - 0.2, nx(6), 'diag', 'bg_paper');
    camMove(L, { scale: 1.08 }, { scale: 1.0 });
    const l = img(L.cam, 'fence', 540, 760, 560, { clipPath: 'inset(0 50% 0 0)' });
    const r = img(L.cam, 'fence', 540, 760, 560, { clipPath: 'inset(0 0 0 50%)' });
    pop(l, s.a); pop(r, s.a);
    TL.to(l, { x: -60, rotation: -14, duration: 0.4, ease: 'power3.out' }, W_(6, 'टूटी') + 0.2);
    TL.to(r, { x: 60, rotation: 16, y: 40, duration: 0.4, ease: 'power3.out' }, W_(6, 'टूटी') + 0.2);
    shake(L, W_(6, 'टूटी'));
    rise(big(L.cam, 'टूटी सीमा', 540, 300, 110, RUST), W_(6, 'टूटी'));
    rise(big(L.cam, 'कोई सीमा न होने से भी बुरी', 540, 1170, 70, INK), W_(6, 'कोई सीमा'));
  }
  // 7 — boundaries come from clarity, not anger
  { const s = S(7); const L = layer(s.a - 0.2, END, 'iris'); solid(L, '#33402f');
    camMove(L, { scale: 1.0 }, { scale: 1.06 });
    const cl = img(L.cam, 'cloud', 540, 420, 380); pop(cl, s.a + 0.2);
    text(L.cam, 'गुस्सा', 540, 430, { fontSize: '70px', color: CREAM });
    TL.fromTo(L.cam.lastChild, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.3 }, s.a + 0.4);
    strike(L.cam, 540, 430, 300, W_(7, 'स्पष्टता') - 0.3);
    const mg = img(L.cam, 'magnifier', 540, 880, 300); pop(mg, W_(7, 'स्पष्टता'), { rot: 20 });
    rise(big(L.cam, 'स्पष्टता से', 540, 1180, 120, MUSTARD), W_(7, 'स्पष्टता'));
  }
  window.VIDEO_END = END;
  buildSubs(1e9);
}
