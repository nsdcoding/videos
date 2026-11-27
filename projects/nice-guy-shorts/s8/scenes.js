// Short 8 — यह आदत आती कहाँ से है? (बचपन की जड़)
function build() {
  const END = endT();
  const nx = i => (i + 1 < TIMING.length ? S(i + 1).a - 0.2 : END);

  // 0 — where does the people-pleasing habit come from?
  { const s = S(0); const L = layer(0, nx(0), 'cut', 'bg_living');
    camMove(L, { scale: 1.12 }, { scale: 1.0 }, 'power2.out');
    Guy(L.cam, 540, 1580, 1.15);
    [[230, 760], [850, 720]].forEach(([x, y], k) => { const e = img(L.cam, ['gift', 'sack'][k], x, y, 170); pop(e, 0.2 + k * 0.3); float(e, 0, L.t1, 7, k); });
    band(L, 380, 260, 0);
    rise(big(L.cam, 'सबको ख़ुश रखने की आदत', 540, 320, 70), 0.15);
    rise(big(L.cam, 'आती कहाँ से है?', 540, 440, 96, RUST), W_(0, 'आती'));
  }
  // 1 — Glover sees the root in childhood
  { const s = S(1); const L = layer(s.a - 0.2, nx(1), 'iris'); solid(L, INK);
    camMove(L, { scale: 1.0 }, { scale: 1.08 });
    const sp = img(L.cam, 'sprout', 540, 620, 300); pop(sp, s.a);
    const roots = inkPath(L.cam, 'M540 760 L540 900 M540 840 Q470 900 420 1000 M540 860 Q620 930 660 1040 M540 900 Q520 1000 560 1120 M420 1000 Q380 1060 360 1120 M660 1040 Q700 1090 730 1140', {}, { color: MUSTARD, width: 9 });
    draw(roots, W_(1, 'जड़'), 0.9);
    const kid = img(L.cam, 'kid', 540, 1260, 120); pop(kid, W_(1, 'बचपन'));
    rise(big(L.cam, 'जड़: बचपन', 540, 300, 110, CREAM), W_(1, 'जड़'));
  }
  // 2 — if love only comes when you're useful, the child concludes…
  { const s = S(2); const L = layer(s.a - 0.2, nx(2), 'push', 'bg_childhome');
    camMove(L, { scale: 1.0 }, { scale: 1.06 });
    person(L.cam, 'mother', 760, 1580, 760, 3);
    const kid = person(L.cam, 'kid', 330, 1580, 460, 2);
    const sk = img(L.cam, 'sack', 330, 1060, 150); pop(sk, W_(2, 'काम आए'));
    band(L, 380, 170, s.a);
    rise(big(L.cam, 'प्यार = काम आना?', 540, 380, 88, RUST), W_(2, 'प्यार'));
    qmarks(L.cam, [[330, 900]], W_(2, 'निष्कर्ष'), 120);
  }
  // 3 — "I'm not enough the way I am"
  { const s = S(3); const L = layer(s.a - 0.2, nx(3), 'iris'); solid(L, '#33402f');
    camMove(L, { scale: 1.0 }, { scale: 1.08 });
    const kid = img(L.cam, 'kid', 540, 1100, 260); pop(kid, s.a);
    const t = big(L.cam, '“मैं जैसा हूँ,<br>वैसा काफ़ी नहीं हूँ।”', 540, 420, 90, CREAM); rise(t, s.a + 0.1);
  }
  // 4 — back then the strategy was wise; it kept him safe
  { const s = S(4); const L = layer(s.a - 0.2, nx(4), 'wipe', 'bg_childhome');
    camMove(L, { scale: 1.06 }, { scale: 1.0 });
    person(L.cam, 'kid', 540, 1580, 520, 2);
    const sh = img(L.cam, 'shield', 540, 820, 300); pop(sh, W_(4, 'सुरक्षा'));
    band(L, 380, 170, s.a);
    rise(big(L.cam, 'उस समय: समझदारी', 540, 380, 84, '#3f6b30'), W_(4, 'समझदारी') - 0.3);
    check(L.cam, 820, 820, 1.4, W_(4, 'सुरक्षा') + 0.3, '#3f6b30');
  }
  // 5 — but it keeps running when grown up
  { const s = S(5); const L = layer(s.a - 0.2, nx(5), 'zoom', 'bg_office');
    camMove(L, { scale: 1.0 }, { scale: 1.06 });
    const kid = person(L.cam, 'kid', 250, 1580, 460, 2);
    Guy(L.cam, 700, 1580, 1.1, { head: 'head_tired' });
    arrow(L.cam, 330, 1000, 560, 900, s.a + 0.3, { color: RUST, width: 10, bend: -0.2 });
    const sh = img(L.cam, 'shield', 700, 560, 200); pop(sh, W_(5, 'चलती'));
    band(L, 340, 170, s.a);
    rise(big(L.cam, 'बड़े होकर भी', 540, 340, 96), s.a + 0.05);
  }
  // 6 — hides his needs, and his flaws too
  { const s = S(6); const L = layer(s.a - 0.2, nx(6), 'diag', 'bg_paper');
    camMove(L, { scale: 1.08 }, { scale: 1.0 });
    const ch = img(L.cam, 'chest', 540, 1000, 460); pop(ch, s.a);
    [['ज़रूरतें', 'ज़रूरतें', 300], ['कमियाँ', 'कमियाँ', 780]].forEach(([lab, w, x], k) => {
      const e = tag(L.cam, lab, x, 520, { fontSize: '60px', background: MUSTARD }); pop(e, W_(6, w));
      TL.to(e, { x: 540 - x, y: 420, scale: 0.2, autoAlpha: 0, duration: 0.6, ease: 'power2.in' }, W_(6, w) + 0.7);
    });
    rise(big(L.cam, 'सब छिपा लिया', 540, 1330, 76, RUST), s.b - 0.3);
  }
  // 7 — and here's the biggest paradox
  { const s = S(7); const L = layer(s.a - 0.2, nx(7), 'iris'); solid(L, INK);
    camMove(L, { scale: 1.0 }, { scale: 1.1 });
    rise(big(L.cam, 'सबसे बड़ा', 540, 640, 110, CREAM), s.a);
    rise(big(L.cam, 'विरोधाभास', 540, 800, 150, MUSTARD), W_(7, 'विरोधाभास'));
  }
  // 8 — no one can truly accept someone no one gets to know
  { const s = S(8); const L = layer(s.a - 0.2, END, 'wipeUp', 'bg_living');
    camMove(L, { scale: 1.0 }, { scale: 1.06 });
    Guy(L.cam, 300, 1580, 1.0);
    const m = img(L.cam, 'mask', 300, 900, 160); pop(m, s.a + 0.1, { rot: -15 });
    person(L.cam, 'w_kurta', 790, 1580, 720, 4);
    qmarks(L.cam, [[790, 780]], s.a + 0.4, 110);
    band(L, 410, 280, s.a);
    rise(big(L.cam, 'जिसे कोई जान नहीं पाता,', 540, 350, 66), s.a + 0.05);
    rise(big(L.cam, 'उसे कोई अपना नहीं पाता', 540, 470, 70, RUST), W_(8, 'उसे कोई'));
  }
  window.VIDEO_END = END;
  buildSubs(1e9);
}
