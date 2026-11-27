// Short 7 — दफ़्तर वाला नाइस गाय
function build() {
  const END = endT();
  const nx = i => (i + 1 < TIMING.length ? S(i + 1).a - 0.2 : END);
  const rule = (L, n, lab) => ruleCard(L.cam, n, lab, 540, 300, L.t0 + 0.3, { h: 170, fs: 50 });

  // 0 — your hard work, someone else's promotion
  { const s = S(0); const L = layer(0, nx(0), 'cut', 'bg_office');
    camMove(L, { scale: 1.12 }, { scale: 1.0 }, 'power2.out');
    Guy(L.cam, 280, 1580, 1.0, { head: 'head_tired' });
    person(L.cam, 'w_office', 800, 1580, 720, 3);
    [0, 1, 2].forEach(k => { const e = img(L.cam, 'sack', 520, 1330 - k * 110, 140); pop(e, 0.1 + k * 0.2); });
    band(L, 400, 260, 0);
    rise(big(L.cam, 'मेहनत आपकी', 540, 340, 88), 0.15);
    rise(big(L.cam, 'तरक़्क़ी किसी और की?', 540, 460, 80, RUST), W_(0, 'तरक़्क़ी'));
    const tr = img(L.cam, 'trophy_env', 800, 760, 200); pop(tr, W_(0, 'तरक़्क़ी') + 0.2, { rot: 12 });
  }
  // 1 — maybe you're the office "nice guy"
  { const s = S(1); const L = layer(s.a - 0.2, nx(1), 'iris'); solid(L, INK);
    camMove(L, { scale: 1.0 }, { scale: 1.08 });
    Guy(L.cam, 540, 1580, 1.2);
    rise(big(L.cam, 'दफ़्तर वाले', 540, 330, 100, CREAM), s.a);
    rise(big(L.cam, 'Nice Guy', 540, 470, 130, MUSTARD), W_(1, 'नाइस'));
    const m = img(L.cam, 'mask', 860, 760, 190); pop(m, W_(1, 'नाइस') + 0.2, { rot: 20 }); float(m, s.a, L.t1, 8, 2);
  }
  // 2 — habit 1: yes to every task; your own work falls behind
  { const s = S(2); const L = layer(s.a - 0.2, nx(2), 'push', 'bg_office');
    camMove(L, { scale: 1.0 }, { scale: 1.05 }); rule(L, 1, 'हर काम के लिए हाँ');
    Guy(L.cam, 300, 1580, 1.0); person(L.cam, 'boss', 800, 1580, 760, 2);
    for (let k = 0; k < 5; k++) { const e = img(L.cam, 'sack', 560, 1310 - k * 90, 140); pop(e, s.a + 0.4 + k * 0.3); }
    pop(tag(L.cam, 'अपना काम पिछड़ा', 540, 520, { fontSize: '52px', background: RUST, color: CREAM }), W_(2, 'पिछड़'));
    const cal = img(L.cam, 'calendar', 820, 760, 170); pop(cal, W_(2, 'अपना काम'), { rot: 12 });
  }
  // 3 — habit 2: not claiming credit; good work isn't automatically seen
  { const s = S(3); const L = layer(s.a - 0.2, nx(3), 'wipe', 'bg_paper');
    camMove(L, { scale: 1.06 }, { scale: 1.0 }); rule(L, 2, 'श्रेय न माँगना');
    const tr = img(L.cam, 'trophy_env', 540, 820, 360); pop(tr, s.a + 0.3);
    const mg = img(L.cam, 'magnifier', 800, 760, 220); pop(mg, W_(3, 'अपने आप'), { rot: 20 });
    TL.to(mg, { x: -120, y: 60, duration: 1.2, ease: 'sine.inOut' }, W_(3, 'अपने आप') + 0.3);
    rise(big(L.cam, 'अच्छा काम अपने आप नहीं दिखता', 540, 1200, 70, RUST), W_(3, 'अच्छा काम'));
  }
  // 4 — habit 3: silent in the meeting, criticising the decision later
  { const s = S(4); const L = layer(s.a - 0.2, nx(4), 'zoom', 'bg_meeting');
    camMove(L, { scale: 1.0 }, { scale: 1.05 }); rule(L, 3, 'बैठक में चुप');
    const g = Guy(L.cam, 300, 1580, 1.0); g.say(W_(4, 'बाद में'), s.b);
    person(L.cam, 'boss', 800, 1580, 760, 2);
    bubble(L.cam, '…', 330, 560, W_(4, 'चुप'), { fontSize: '70px' });
    bubble(L.cam, 'वैसे वो फ़ैसला ग़लत था!', 480, 700, W_(4, 'बाद में'), { fontSize: '46px', background: MUSTARD });
  }
  // 5 — habit 4: never raising salary, hoping someone will just give it
  { const s = S(5); const L = layer(s.a - 0.2, nx(5), 'diag', 'bg_office');
    camMove(L, { scale: 1.06 }, { scale: 1.0 }); rule(L, 4, 'वेतन की बात नहीं');
    const g = Guy(L.cam, 300, 1580, 1.1, { head: 'head_tired' });
    const tr = img(L.cam, 'trophy_env', 740, 700, 260); pop(tr, W_(5, 'वेतन'));
    const cl = box(L.cam, 740, 700, { width: '320px', height: '320px', borderRadius: '50%', border: `8px dashed ${CREAM}` }); pop(cl, W_(5, 'उम्मीद'));
    pop(tag(L.cam, 'कोई ख़ुद देगा…', 740, 940, { fontSize: '50px' }), W_(5, 'उम्मीद'));
  }
  // 6 — the same hidden contract, office edition
  { const s = S(6); const L = layer(s.a - 0.2, nx(6), 'iris', 'bg_paper');
    camMove(L, { scale: 1.06 }, { scale: 1.0 });
    const c = img(L.cam, 'contract', 540, 800, 480); pop(c, s.a);
    rise(big(L.cam, 'वही छिपा हुआ सौदा', 540, 300, 96, RUST), W_(6, 'छिपा'));
    stamp(L.cam, 'दफ़्तर एडिशन', 540, 1160, W_(6, 'दफ़्तर'), INK, 70);
  }
  // 7 — stating your work clearly isn't showing off, it's information
  { const s = S(7); const L = layer(s.a - 0.2, END, 'wipeUp'); solid(L, '#33402f');
    camMove(L, { scale: 1.0 }, { scale: 1.06 });
    const jr = img(L.cam, 'journal', 540, 560, 420); pop(jr, s.a + 0.1);
    rise(big(L.cam, 'अपने काम का हिसाब बताना', 540, 300, 70, CREAM), s.a);
    const a = text(L.cam, 'दिखावा', 300, 900, { fontSize: '90px', color: CREAM }); pop(a, W_(7, 'दिखावा'));
    strike(L.cam, 300, 900, 300, W_(7, 'दिखावा') + 0.3);
    const b = text(L.cam, 'जानकारी', 780, 900, { fontSize: '90px', color: MUSTARD }); pop(b, W_(7, 'जानकारी'));
    check(L.cam, 780, 1060, 1.6, W_(7, 'जानकारी') + 0.3, MUSTARD);
  }
  window.VIDEO_END = END;
  buildSubs(1e9);
}
