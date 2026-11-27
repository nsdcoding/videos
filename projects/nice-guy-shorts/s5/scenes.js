// Short 5 — देना या छिपा सौदा? एक सवाल
function build() {
  const END = endT();
  const nx = i => (i + 1 < TIMING.length ? S(i + 1).a - 0.2 : END);

  // 0 — how do you feel after helping someone?
  { const s = S(0); const L = layer(0, nx(0), 'cut', 'bg_living');
    camMove(L, { scale: 1.12 }, { scale: 1.0 }, 'power2.out');
    Guy(L.cam, 300, 1580, 1.0);
    person(L.cam, 'w_kurta', 790, 1580, 720, 3);
    const gf = img(L.cam, 'gift', 470, 1290, 150); pop(gf, 0.1);
    TL.to(gf, { x: 220, y: -40, duration: 0.8, ease: 'power2.inOut' }, 0.6);
    band(L, 380, 250, 0);
    rise(big(L.cam, 'मदद के बाद…', 540, 320, 96), 0.15);
    rise(big(L.cam, 'कैसा लगता है?', 540, 440, 96, RUST), W_(0, 'कैसा'));
  }
  // 1 — one question tells: giving, or a hidden deal
  { const s = S(1); const L = layer(s.a - 0.2, nx(1), 'iris', 'bg_paper');
    camMove(L, { scale: 1.06 }, { scale: 1.0 });
    pop(tag(L.cam, 'एक सवाल', 540, 300, { fontSize: '58px', background: INK, color: CREAM }), s.a);
    const sc = img(L.cam, 'scale_stand', 540, 900, 560); pop(sc, s.a + 0.2);
    pop(tag(L.cam, 'देना', 300, 640, { fontSize: '62px', background: '#3f6b30', color: CREAM }), W_(1, 'देना'));
    pop(tag(L.cam, 'छिपा सौदा', 790, 640, { fontSize: '62px', background: RUST, color: CREAM }), W_(1, 'छिपा'));
    HOOKS.push(t => { if (t > s.a && t < L.t1 + 1) gsap.set(sc, { rotation: Math.sin(t * 2.2) * 6 }); });
  }
  // 2 — contentment, lightness → it was giving
  { const s = S(2); const L = layer(s.a - 0.2, nx(2), 'wipe', 'bg_park');
    camMove(L, { scale: 1.0 }, { scale: 1.06 });
    Guy(L.cam, 540, 1580, 1.15, { head: 'head_calm' });
    pop(tag(L.cam, 'संतोष', 260, 560, { fontSize: '60px', background: CREAM }), W_(2, 'संतोष'), { rot: -10 });
    pop(tag(L.cam, 'हल्कापन', 820, 640, { fontSize: '60px', background: CREAM }), W_(2, 'हल्कापन'), { rot: 10 });
    rise(big(L.cam, 'यह देना था', 540, 320, 110, '#3f6b30'), W_(2, 'देना'));
    check(L.cam, 870, 300, 1.4, W_(2, 'देना') + 0.3, '#3f6b30');
  }
  // 3 — a little resentment, "now they owe me" → it was a deal
  { const s = S(3); const L = layer(s.a - 0.2, nx(3), 'diag', 'bg_living');
    camMove(L, { scale: 1.06 }, { scale: 1.0 });
    const g = Guy(L.cam, 540, 1580, 1.15); g.headSwap(W_(3, 'नाराज़गी'), 'head_angry');
    const cl = img(L.cam, 'cloud', 540, 640, 300); pop(cl, W_(3, 'नाराज़गी'));
    bubble(L.cam, 'अब इन्हें भी कुछ करना चाहिए…', 540, 420, W_(3, 'अब इन्हें'), { fontSize: '46px' });
    stamp(L.cam, 'सौदा', 800, 900, W_(3, 'सौदा था'), RUST, 90);
  }
  // 4 — solving everyone's problems stops them from learning
  { const s = S(4); const L = layer(s.a - 0.2, nx(4), 'push', 'bg_childhome');
    camMove(L, { scale: 1.0 }, { scale: 1.06 });
    Guy(L.cam, 330, 1580, 1.0, { head: 'head_tired' });
    person(L.cam, 'kid', 760, 1580, 460, 2);
    const jr = img(L.cam, 'journal', 560, 1240, 240); pop(jr, s.a + 0.2);
    TL.to(jr, { x: -160, duration: 0.6, ease: 'power2.inOut' }, W_(4, 'हल करता'));
    pop(tag(L.cam, 'सबकी समस्या, मेरी समस्या', 540, 330, { fontSize: '50px' }), s.a + 0.1);
    pop(tag(L.cam, 'सीखने ही नहीं देता', 540, 500, { fontSize: '56px', background: RUST, color: CREAM }), W_(4, 'सीखने'));
    qmarks(L.cam, [[820, 920]], W_(4, 'सीखने') + 0.2, 110);
  }
  // 5 — unasked help is often control
  { const s = S(5); const L = layer(s.a - 0.2, nx(5), 'iris'); solid(L, INK);
    camMove(L, { scale: 1.0 }, { scale: 1.08 });
    rise(big(L.cam, 'बिना माँगे मदद', 540, 330, 100, CREAM), s.a);
    const ch = img(L.cam, 'chain', 540, 800, 600); pop(ch, W_(5, 'नियंत्रण') - 0.4);
    stamp(L.cam, 'नियंत्रण', 540, 1160, W_(5, 'नियंत्रण'), MUSTARD, 96);
  }
  // 6 — so ask before helping
  { const s = S(6); const L = layer(s.a - 0.2, nx(6), 'wipeUp', 'bg_cafe');
    camMove(L, { scale: 1.06 }, { scale: 1.0 });
    Guy(L.cam, 300, 1580, 1.0, { head: 'head_calm' });
    person(L.cam, 'friend', 790, 1580, 780, 4);
    band(L, 340, 170, s.a);
    rise(big(L.cam, 'मदद से पहले पूछिए', 540, 340, 88, '#3f6b30'), W_(6, 'पूछिए') - 0.3);
  }
  // 7 — "do you want help, or did you just want to tell me?"
  { const s = S(7); const L = layer(s.a - 0.2, END, 'cut', 'bg_cafe');
    TL.fromTo(L.cam, { scale: 1.0 }, { scale: 1.08, duration: END - s.a + 1, ease: 'sine.inOut' }, s.a - 0.2);
    const g = Guy(L.cam, 300, 1580, 1.0, { head: 'head_calm' }); g.headSwap(s.a, 'head'); g.say(s.a, s.b);
    person(L.cam, 'friend', 790, 1580, 780, 4);
    band(L, 340, 170, s.a - 0.2);
    big(L.cam, 'मदद से पहले पूछिए', 540, 340, 88, '#3f6b30');
    bubble(L.cam, 'तुम्हें मदद चाहिए,', 420, 560, s.a, { fontSize: '52px', background: MUSTARD });
    bubble(L.cam, 'या बस बताना चाहते थे?', 480, 700, W_(7, 'या तुम'), { fontSize: '52px', background: CREAM });
  }
  window.VIDEO_END = END;
  buildSubs(1e9);
}
