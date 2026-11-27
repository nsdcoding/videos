// Short 2 — पाँच संकेत: क्या आप भी 'नाइस गाय' हैं?
function build() {
  const END = endT();
  const nx = i => (i + 1 < TIMING.length ? S(i + 1).a - 0.2 : END);
  const chip = (L, n) => pop(tag(L.cam, `संकेत ${n}/5`, 540, 250, { fontSize: '46px', background: INK, color: CREAM }), L.t0 + 0.3);

  // 0 — hook
  { const s = S(0); const L = layer(0, nx(0), 'cut', 'bg_living');
    camMove(L, { scale: 1.15 }, { scale: 1.0 }, 'power2.out');
    const g = Guy(L.cam, 540, 1580, 1.2); g.headSwap(W_(0, 'परेशान'), 'head_tired');
    band(L, 330, 290, 0);
    rise(big(L.cam, 'इतने अच्छे…', 540, 260, 110), 0.1);
    rise(big(L.cam, 'कि ख़ुद से परेशान?', 540, 400, 90, RUST), W_(0, 'कि ख़ुद'));
    const m = img(L.cam, 'mask', 850, 700, 190); pop(m, 0.6, { rot: 20 }); float(m, 0, L.t1, 8, 2);
    const cl = img(L.cam, 'cloud', 230, 680, 240); pop(cl, W_(0, 'परेशान'));
    float(cl, 0, L.t1, 6, 4);
  }
  // 1 — the psychiatrist lists five signs
  { const s = S(1); const L = layer(s.a - 0.2, nx(1), 'iris'); solid(L, INK);
    camMove(L, { scale: 1.0 }, { scale: 1.08 });
    person(L.cam, 'psych', 300, 1560, 800, 3);
    const n = text(L.cam, '5', 760, 760, { fontSize: '440px', color: MUSTARD, fontFamily: "'Rozha One'", fontWeight: 400 }); pop(n, W_(1, 'पाँच'), { rot: -15 });
    rise(big(L.cam, 'संकेत', 760, 1060, 110, CREAM, { width: '500px' }), W_(1, 'संकेत'));
    pop(tag(L.cam, 'रॉबर्ट ग्लोवर', 540, 300, { fontSize: '52px', background: MUSTARD }), W_(1, 'रॉबर्ट'));
    const mg = img(L.cam, 'magnifier', 860, 420, 200); pop(mg, s.a + 0.4, { rot: 25 }); float(mg, s.a, L.t1, 9, 1);
  }
  // 2 — can't say no, guilty when you do
  { const s = S(2); const L = layer(s.a - 0.2, nx(2), 'push', 'bg_office');
    camMove(L, { scale: 1.0 }, { scale: 1.06 }); chip(L, 1);
    const g = Guy(L.cam, 330, 1580, 1.0); g.say(s.a, s.b);
    person(L.cam, 'boss', 790, 1580, 760, 2);
    const sk = img(L.cam, 'sack', 600, 1150, 170); pop(sk, s.a + 0.2);
    TL.to(sk, { x: -200, y: 60, duration: 0.7, ease: 'power2.inOut' }, s.a + 0.7);
    pop(tag(L.cam, '“ना” नहीं निकलता', 540, 420, { fontSize: '58px', background: CREAM }), W_(2, 'मना नहीं'));
    pop(tag(L.cam, 'मना किया? अपराधबोध!', 540, 560, { fontSize: '50px', background: RUST, color: CREAM }), W_(2, 'अपराधबोध'));
    g.headSwap(W_(2, 'अपराधबोध'), 'head_tired');
  }
  // 3 — hides real opinion, says what others want to hear
  { const s = S(3); const L = layer(s.a - 0.2, nx(3), 'wipe', 'bg_cafe');
    camMove(L, { scale: 1.06 }, { scale: 1.0 }); chip(L, 2);
    const g = Guy(L.cam, 330, 1580, 1.0); g.say(W_(3, 'वही कहते'), s.b);
    person(L.cam, 'friend', 790, 1580, 780, 4);
    bubble(L.cam, 'हाँ हाँ, बिलकुल सही!', 430, 430, W_(3, 'वही कहते'), { fontSize: '50px', background: MUSTARD });
    const th = tag(L.cam, '(असल में: मैं सहमत नहीं…)', 540, 600, { fontSize: '42px', background: 'rgba(243,231,207,.85)', borderStyle: 'dashed', boxShadow: 'none' });
    pop(th, W_(3, 'असली राय'));
    const m = img(L.cam, 'mask', 330, 900, 150); pop(m, W_(3, 'छिपाकर'), { rot: -20 });
  }
  // 4 — avoids conflict, replays it in the head later
  { const s = S(4); const L = layer(s.a - 0.2, nx(4), 'zoom', 'bg_night');
    camMove(L, { scale: 1.0 }, { scale: 1.08 }); chip(L, 3);
    const g = Guy(L.cam, 540, 1580, 1.1, { head: 'head_tired' });
    pop(tag(L.cam, 'टकराव? बचो!', 540, 400, { fontSize: '58px' }), W_(4, 'टकराव'));
    const t0 = W_(4, 'बाद में');
    ['काश मैंने कहा होता…', 'काश मैंने कहा होता…', 'काश…'].forEach((q, k) => {
      const b = tag(L.cam, q, [300, 780, 330][k], [560, 670, 770][k], { fontSize: '42px', background: CREAM, opacity: 1 - k * 0.15 });
      pop(b, t0 + k * 0.45, { rot: k % 2 ? 8 : -8 });
    });
    const loop = inkPath(L.cam, 'M540 665 m-470 0 a470 190 0 1 0 940 0 a470 190 0 1 0 -940 0', {}, { color: MUSTARD, width: 8 });
    draw(loop, W_(4, 'दोहराते'), 0.9);
  }
  // 5 — hides even small mistakes
  { const s = S(5); const L = layer(s.a - 0.2, nx(5), 'diag', 'bg_paper');
    camMove(L, { scale: 1.08 }, { scale: 1.0 }); chip(L, 4);
    const ch = img(L.cam, 'chest', 540, 1000, 460); pop(ch, s.a);
    ['छोटी ग़लती', 'भूल', 'चूक'].forEach((w, k) => {
      const e = tag(L.cam, w, [300, 540, 780][k], 520, { fontSize: '46px', background: MUSTARD });
      pop(e, s.a + 0.3 + k * 0.25);
      TL.to(e, { x: 540 - [300, 540, 780][k], y: 420, scale: 0.2, autoAlpha: 0, duration: 0.6, ease: 'power2.in' }, W_(5, 'छिपाते') + k * 0.15);
    });
    rise(big(L.cam, 'सब छिपा लो', 540, 1330, 76, RUST), W_(5, 'छिपाते') + 0.6);
  }
  // 6 — complains in hints, not directly
  { const s = S(6); const L = layer(s.a - 0.2, nx(6), 'push', 'bg_living');
    camMove(L, { scale: 1.0 }, { scale: 1.06 }); chip(L, 5);
    const g = Guy(L.cam, 300, 1580, 1.0); g.say(W_(6, 'इशारों') - 0.4, s.b);
    person(L.cam, 'w_kurta', 800, 1580, 720, 4);
    bubble(L.cam, 'कोई बात नहीं… मैं ही कर लूँगा।', 520, 430, W_(6, 'शिकायत'), { fontSize: '44px' });
    pop(tag(L.cam, 'सीधे नहीं, इशारों में', 540, 600, { fontSize: '50px', background: RUST, color: CREAM }), W_(6, 'इशारों'));
    qmarks(L.cam, [[800, 780]], W_(6, 'इशारों') + 0.3, 120);
  }
  // 7 — not a character flaw
  { const s = S(7); const L = layer(s.a - 0.2, nx(7), 'iris', 'bg_paper');
    camMove(L, { scale: 1.06 }, { scale: 1.0 });
    rise(big(L.cam, 'कई बातें मिलती हैं?', 540, 330, 86), s.a + 0.05);
    const st = stamp(L.cam, 'चरित्र की कमी', 540, 820, W_(7, 'चरित्र'), INK, 86);
    cross(L.cam, 540, 820, 4.5, W_(7, 'नहीं है'));
    shake(L, W_(7, 'नहीं है'));
  }
  // 8 — a learned strategy, and learned things can change
  { const s = S(8); const L = layer(s.a - 0.2, END, 'wipeUp'); solid(L, '#33402f');
    camMove(L, { scale: 1.0 }, { scale: 1.06 });
    rise(big(L.cam, 'सीखी हुई रणनीति', 540, 330, 100, MUSTARD), W_(8, 'सीखी'));
    const sp = img(L.cam, 'sprout', 540, 900, 420);
    TL.fromTo(sp, { scaleY: 0, transformOrigin: '50% 100%', autoAlpha: 0 }, { scaleY: 1, autoAlpha: 1, duration: 0.9, ease: 'back.out(1.6)' }, W_(8, 'बदली') - 0.4);
    rise(big(L.cam, 'बदली जा सकती है', 540, 1270, 90, CREAM), W_(8, 'बदली'));
  }
  window.VIDEO_END = END;
  buildSubs(1e9);
}
