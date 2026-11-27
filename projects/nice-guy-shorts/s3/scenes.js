// Short 3 — शिकायत नहीं, माँग
function build() {
  const END = endT();
  const nx = i => (i + 1 < TIMING.length ? S(i + 1).a - 0.2 : END);

  // 0 — "you never take care of me" — why doesn't it work?
  { const s = S(0); const L = layer(0, nx(0), 'cut', 'bg_living');
    camMove(L, { scale: 1.12 }, { scale: 1.0 }, 'power2.out');
    const g = Guy(L.cam, 300, 1580, 1.0, { head: 'head_angry' });
    person(L.cam, 'w_kurta', 790, 1580, 720, 3);
    bubble(L.cam, 'तुम मेरा ध्यान ही नहीं रखते!', 500, 420, 0.15, { fontSize: '50px', background: CREAM });
    pop(tag(L.cam, 'काम क्यों नहीं करती?', 540, 600, { fontSize: '54px', background: RUST, color: CREAM }), W_(0, 'काम क्यों'));
    qmarks(L.cam, [[820, 760]], W_(0, 'काम क्यों') + 0.3, 120);
  }
  // 1 — because it's a complaint, not a request
  { const s = S(1); const L = layer(s.a - 0.2, nx(1), 'wipe', 'bg_paper');
    camMove(L, { scale: 1.06 }, { scale: 1.0 });
    const a = box(L.cam, 540, 640, { width: '860px', height: '300px', background: CREAM, border: `6px solid ${INK}`, borderRadius: '28px', boxShadow: `10px 10px 0 ${INK}` });
    text(a, 'शिकायत', 430, 150, { fontSize: '120px', color: RUST });
    pop(a, s.a);
    cross(L.cam, 860, 640, 1.6, W_(1, 'शिकायत') + 0.4);
    const b = box(L.cam, 540, 1060, { width: '860px', height: '300px', background: 'rgba(243,231,207,.5)', border: `6px dashed ${INK}`, borderRadius: '28px' });
    text(b, 'माँग?', 430, 150, { fontSize: '120px', color: '#3f6b30' });
    pop(b, W_(1, 'माँग'));
  }
  // 2 — we assume: if they really cared, they'd just know
  { const s = S(2); const L = layer(s.a - 0.2, nx(2), 'zoom', 'bg_night');
    camMove(L, { scale: 1.0 }, { scale: 1.07 });
    Guy(L.cam, 540, 1580, 1.1, { head: 'head_tired' });
    const cl = img(L.cam, 'cloud', 540, 380, 380); pop(cl, s.a + 0.1); float(cl, s.a, L.t1, 6, 2);
    const t = tag(L.cam, 'परवाह होती, तो<br>अपने आप पता चल जाता', 540, 640, { fontSize: '50px', lineHeight: 1.25, whiteSpace: 'nowrap' });
    pop(t, W_(2, 'परवाह'));
  }
  // 3 — but people can't read minds
  { const s = S(3); const L = layer(s.a - 0.2, nx(3), 'iris'); solid(L, INK);
    camMove(L, { scale: 1.0 }, { scale: 1.08 });
    const hd = img(L.cam, 'head_calm', 540, 820, 380); pop(hd, s.a);
    qmarks(L.cam, [[260, 720], [820, 680], [540, 420]], s.a + 0.2, 150);
    rise(big(L.cam, 'लोग मन नहीं<br>पढ़ सकते', 540, 1220, 100, MUSTARD), W_(3, 'मन नहीं'));
  }
  // 4 — the request: "can you sit with me for half an hour this evening?"
  { const s = S(4); const L = layer(s.a - 0.2, nx(4), 'push', 'bg_park');
    camMove(L, { scale: 1.0 }, { scale: 1.06 });
    const g = Guy(L.cam, 300, 1580, 1.0, { head: 'head_calm' }); g.headSwap(W_(4, 'क्या तुम'), 'head'); g.say(W_(4, 'क्या तुम'), s.b);
    person(L.cam, 'w_kurta', 790, 1580, 720, 4);
    pop(tag(L.cam, 'अब यह सुनिए', 540, 300, { fontSize: '50px', background: INK, color: CREAM }), s.a);
    bubble(L.cam, 'क्या तुम आज शाम,<br>आधा घंटा मेरे साथ बैठ सकोगे?', 540, 480, W_(4, 'क्या तुम'), { fontSize: '46px', background: MUSTARD, whiteSpace: 'nowrap', textAlign: 'center', lineHeight: 1.25 });
    const cal = img(L.cam, 'calendar', 820, 760, 170); pop(cal, W_(4, 'आधा'), { rot: 15 });
  }
  // 5 — that's a request: clear, short, doable
  { const s = S(5); const L = layer(s.a - 0.2, nx(5), 'wipeUp', 'bg_paper');
    camMove(L, { scale: 1.06 }, { scale: 1.0 });
    rise(big(L.cam, 'यह माँग है', 540, 300, 120, '#3f6b30'), s.a);
    [['साफ़', 'साफ़'], ['छोटी', 'छोटी'], ['पूरी की जा सके', 'पूरी']].forEach(([lab, w], k) => {
      const y = 600 + k * 270;
      ruleCard(L.cam, k + 1, lab, 540, y, W_(5, w) - 0.15, { disc: '#3f6b30', fromX: k % 2 ? -700 : 700 });
      check(L.cam, 900, y - 70, 1.2, W_(5, w) + 0.4, '#3f6b30');
    });
  }
  // 6 — be ready to hear "no"
  { const s = S(6); const L = layer(s.a - 0.2, nx(6), 'diag', 'bg_living');
    camMove(L, { scale: 1.0 }, { scale: 1.06 });
    Guy(L.cam, 300, 1580, 1.0, { head: 'head_calm' });
    person(L.cam, 'w_kurta', 790, 1580, 720, 2);
    bubble(L.cam, 'आज नहीं हो पाएगा…', 640, 430, s.a + 0.2, { fontSize: '50px' });
    pop(tag(L.cam, '“ना” सुनने को तैयार', 540, 620, { fontSize: '54px', background: MUSTARD }), W_(6, 'ना सुनने'));
    const sh = img(L.cam, 'shield', 540, 900, 170); pop(sh, W_(6, 'तैयार'));
  }
  // 7 — one "no" doesn't mean you've been rejected
  { const s = S(7); const L = layer(s.a - 0.2, END, 'iris'); solid(L, '#33402f');
    camMove(L, { scale: 1.0 }, { scale: 1.06 });
    const a = text(L.cam, 'एक “ना”', 540, 380, { fontSize: '130px', color: CREAM }); rise(a, s.a + 0.1);
    const ne = text(L.cam, '≠', 540, 600, { fontSize: '200px', color: MUSTARD, fontFamily: "'Rozha One'" }); pop(ne, W_(7, 'मतलब'));
    const b = text(L.cam, 'ठुकराना', 540, 830, { fontSize: '130px', color: RUST }); rise(b, W_(7, 'ठुकरा'));
    const hd = img(L.cam, 'head_calm', 540, 1180, 230); pop(hd, W_(7, 'ठुकरा') + 0.3);
  }
  window.VIDEO_END = END;
  buildSubs(1e9);
}
