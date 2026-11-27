// Short 6 — हर बात पर सॉरी?
function build() {
  const END = endT();
  const nx = i => (i + 1 < TIMING.length ? S(i + 1).a - 0.2 : END);

  // 0 — do you say sorry for everything?
  { const s = S(0); const L = layer(0, nx(0), 'cut', 'bg_office');
    camMove(L, { scale: 1.14 }, { scale: 1.0 }, 'power2.out');
    const g = Guy(L.cam, 540, 1580, 1.15); g.say(0.3, s.b);
    [[230, 380], [840, 330], [290, 640], [820, 600], [200, 880], [880, 860]].forEach(([x, y], k) =>
      pop(tag(L.cam, 'सॉरी!', x, y, { fontSize: '54px', background: k % 2 ? MUSTARD : CREAM }), 0.1 + k * 0.28, { rot: k % 2 ? 10 : -10 }));
  }
  // 1 — needless apology isn't politeness, it lowers your worth
  { const s = S(1); const L = layer(s.a - 0.2, nx(1), 'wipe', 'bg_paper');
    camMove(L, { scale: 1.06 }, { scale: 1.0 });
    rise(big(L.cam, 'बेवजह की माफ़ी', 540, 300, 100), s.a);
    const v = text(L.cam, 'विनम्रता', 540, 520, { fontSize: '90px', color: INK }); pop(v, W_(1, 'विनम्रता'));
    strike(L.cam, 540, 520, 420, W_(1, 'नहीं है'));
    const pr = tag(L.cam, 'आपकी क़ीमत', 540, 760, { fontSize: '70px', background: MUSTARD }); pop(pr, W_(1, 'क़ीमत'));
    TL.to(pr, { y: 380, rotation: 12, duration: 0.9, ease: 'bounce.out' }, W_(1, 'घटाना'));
    arrow(L.cam, 860, 760, 860, 1150, W_(1, 'घटाना'), { color: RUST, width: 12 });
  }
  // 2 — but stopping apologies entirely breaks relationships
  { const s = S(2); const L = layer(s.a - 0.2, nx(2), 'push', 'bg_living');
    camMove(L, { scale: 1.0 }, { scale: 1.06 });
    Guy(L.cam, 300, 1580, 1.0, { head: 'head_angry' });
    person(L.cam, 'w_kurta', 790, 1580, 720, 3);
    pop(tag(L.cam, 'माफ़ी? कभी नहीं!', 540, 380, { fontSize: '54px' }), W_(2, 'बंद'));
    const crack = inkPath(L.cam, 'M545 620 L510 760 L570 860 L520 1000 L580 1120 L530 1300', {}, { color: RUST, width: 12 });
    draw(crack, W_(2, 'रिश्ते'), 0.5); shake(L, W_(2, 'टूटते'));
    pop(tag(L.cam, 'रिश्ते टूटते हैं', 540, 540, { fontSize: '56px', background: RUST, color: CREAM }), W_(2, 'रिश्ते'));
  }
  // 3 — ask yourself one question first
  { const s = S(3); const L = layer(s.a - 0.2, nx(3), 'iris'); solid(L, INK);
    camMove(L, { scale: 1.0 }, { scale: 1.08 });
    const mg = img(L.cam, 'magnifier', 540, 820, 420); pop(mg, s.a + 0.1, { rot: 20 }); float(mg, s.a, L.t1, 8, 2);
    rise(big(L.cam, 'माफ़ी से पहले', 540, 330, 100, CREAM), s.a);
    rise(big(L.cam, 'एक सवाल', 540, 1200, 120, MUSTARD), W_(3, 'एक सवाल'));
  }
  // 4 — did I really do something wrong?
  { const s = S(4); const L = layer(s.a - 0.2, nx(4), 'zoom', 'bg_paper');
    camMove(L, { scale: 1.06 }, { scale: 1.0 });
    const mr = img(L.cam, 'mirror', 540, 900, 300); pop(mr, s.a);
    const hd = img(L.cam, 'head', 540, 800, 150); TL.set(hd, { autoAlpha: 0 }, 0); TL.to(hd, { autoAlpha: 0.75, duration: 0.4 }, s.a + 0.3);
    band(L, 380, 200, s.a);
    rise(big(L.cam, 'क्या मैंने सचमुच<br>कुछ ग़लत किया?', 540, 380, 74), s.a + 0.05);
  }
  // 5 — or do I just want the discomfort to end?
  { const s = S(5); const L = layer(s.a - 0.2, nx(5), 'wipe', 'bg_night');
    camMove(L, { scale: 1.0 }, { scale: 1.06 });
    Guy(L.cam, 540, 1580, 1.15, { head: 'head_tired' });
    const cl = img(L.cam, 'cloud', 540, 380, 380); pop(cl, s.a);
    pop(tag(L.cam, 'या बस यह असहजता<br>ख़त्म करनी है?', 540, 640, { fontSize: '52px', lineHeight: 1.25 }), s.a + 0.2);
  }
  // 6 — if wrong: admit clearly, no excuses, say what changes
  { const s = S(6); const L = layer(s.a - 0.2, nx(6), 'wipeUp', 'bg_paper');
    camMove(L, { scale: 1.06 }, { scale: 1.0 });
    rise(big(L.cam, 'ग़लती है, तो…', 540, 290, 100, INK), s.a);
    [['साफ़ मानिए', 'साफ़'], ['बिना बहाने', 'बहाने'], ['आगे क्या बदलेगा', 'आगे']].forEach(([lab, w], k) =>
      ruleCard(L.cam, k + 1, lab, 540, 580 + k * 270, W_(6, w) - 0.15, { disc: '#3f6b30', fromX: k % 2 ? -700 : 700 }));
  }
  // 7 — if not: it needs a conversation, not an apology
  { const s = S(7); const L = layer(s.a - 0.2, END, 'iris', 'bg_cafe');
    camMove(L, { scale: 1.0 }, { scale: 1.06 });
    Guy(L.cam, 300, 1580, 1.0, { head: 'head_calm' });
    person(L.cam, 'w_kurta', 790, 1580, 720, 4);
    band(L, 420, 300, s.a);
    const a = big(L.cam, 'माफ़ी नहीं,', 540, 350, 90, RUST); rise(a, W_(7, 'माफ़ी'));
    const b = big(L.cam, 'बातचीत', 540, 480, 120, '#3f6b30'); rise(b, W_(7, 'बातचीत'));
  }
  window.VIDEO_END = END;
  buildSubs(1e9);
}
