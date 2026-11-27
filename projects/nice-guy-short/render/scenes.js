// YouTube Short (1080x1920): "छिपा हुआ अनुबंध" from the No More Mr Nice Guy video.
// Safe area: content kept between y≈220 and y≈1380 (Shorts UI covers top and bottom), x≈70–940.
const SH_END = 43.6;

function big(parent, s, x, y, size, color = INK, css = {}) {
  return text(parent, s, x, y, Object.assign({ fontSize: size + 'px', color, whiteSpace: 'normal', width: '940px', lineHeight: 1.15 }, css));
}

function build() {
  // 0 — hook: does everything for everyone, still angry inside
  {
    const s = S(0); const L = layer(0, S(1).a - 0.2, 'cut', 'bg_living');
    camMove(L, { scale: 1.15 }, { scale: 1.0 }, 'power2.out');
    const g = Guy(L.cam, 540, 1580, 1.2);
    const t1 = big(L.cam, 'सबके लिए', 540, 250, 100); pop(t1, 0.15);
    const t2 = big(L.cam, 'सब कुछ?', 540, 370, 130, RUST); pop(t2, 0.45);
    [['gift', 190, 820, 180, 0.7], ['sack', 890, 860, 180, 1.0], ['note', 200, 1120, 140, 1.3], ['journal', 880, 1160, 160, 1.6]]
      .forEach(([n, x, y, w, t], k) => { const e = img(L.cam, n, x, y, w); pop(e, t, { rot: k % 2 ? 12 : -12 }); float(e, t, L.t1, 7, k); });
    const tn = W_(0, 'नाराज़');
    g.headSwap(tn, 'head_angry');
    const cl = img(L.cam, 'cloud', 540, 560, 260); pop(cl, tn - 0.15);
    HOOKS.push(t => { if (t > tn && t < L.t1 + 1) gsap.set(cl, { x: Math.sin(t * 40) * (t < tn + 0.6 ? 7 : 2) }); });
    draw(inkPath(L.cam, 'M555 640 L525 700 L565 700 L535 770', {}, { color: MUSTARD, width: 10 }), tn + 0.25, 0.25);
  }
  // 1 — maybe you're keeping a hidden contract
  {
    const s = S(1); const L = layer(s.a - 0.2, S(2).a - 0.2, 'iris');
    el('div', L.cam, { position: 'absolute', inset: 0, background: INK });
    camMove(L, { scale: 1.0 }, { scale: 1.08 });
    const c = img(L.cam, 'contract', 540, 880, 520); pop(c, s.a + 0.1); float(c, s.a, L.t1, 8, 2);
    const a = big(L.cam, 'छिपा हुआ', 540, 330, 110, MUSTARD); rise(a, W_(1, 'छिपा'));
    const b = big(L.cam, 'अनुबंध', 540, 470, 160, CREAM); rise(b, W_(1, 'अनुबंध'));
    draw(inkPath(L.cam, 'M260 560 Q540 590 820 552', {}, { color: RUST, width: 12 }), W_(1, 'अनुबंध') + 0.3, 0.5);
  }
  // 2 — Robert Glover's book explains it
  {
    const s = S(2); const L = layer(s.a - 0.2, S(3).a - 0.2, 'wipeUp', 'bg_paper');
    camMove(L, { scale: 1.08 }, { scale: 1.0 });
    const bk = img(L.cam, 'book', 540, 800, 440); pop(bk, s.a + 0.1, { rot: 10 }); float(bk, s.a, L.t1, 7, 3);
    pop(tag(L.cam, 'मनोचिकित्सक रॉबर्ट ग्लोवर', 540, 330, { fontSize: '50px' }), W_(2, 'रॉबर्ट'));
    const t = big(L.cam, 'No More Mr Nice Guy', 540, 1150, 84, RUST); rise(t, W_(2, 'नो मोर'));
    const mk = img(L.cam, 'mask', 820, 560, 210); pop(mk, W_(2, 'नो मोर') + 0.3, { rot: 20 }); float(mk, s.a, L.t1, 6, 5);
  }
  // 3 — "I'll do this for you, so you must praise me"
  {
    const s = S(3); const L = layer(s.a - 0.2, S(4).a - 0.2, 'push', 'bg_living');
    camMove(L, { scale: 1.0 }, { scale: 1.06 });
    const g = Guy(L.cam, 300, 1580, 1.0);
    g.say(s.a, s.b);
    const w = person(L.cam, 'w_kurta', 800, 1580, 720, 4);
    const gf = img(L.cam, 'gift', 470, 1300, 150); pop(gf, s.a + 0.3);
    TL.to(gf, { x: 220, y: -40, duration: 0.8, ease: 'power2.inOut' }, W_(3, 'यह करूँगा'));
    bubble(L.cam, 'मैं तुम्हारे लिए यह करूँगा…', 540, 330, W_(3, 'मैं तुम्हारे'), { fontSize: '44px' });
    bubble(L.cam, '…तो बदले में मेरी तारीफ़ करो!', 540, 470, W_(3, 'बदले'), { fontSize: '44px', background: MUSTARD });
  }
  // 4 — but the deal is never spoken
  {
    const s = S(4); const L = layer(s.a - 0.2, S(5).a - 0.2, 'diag', 'bg_paper');
    camMove(L, { scale: 1.1 }, { scale: 1.0 });
    const c = img(L.cam, 'contract', 540, 820, 480); pop(c, s.a);
    const st = text(L.cam, 'कभी कहा<br>नहीं जाता', 540, 820, { fontSize: '82px', color: RUST, border: `12px solid ${RUST}`, padding: '10px 40px', borderRadius: '20px', background: 'rgba(243,231,207,.94)', whiteSpace: 'nowrap' });
    TL.fromTo(st, { scale: 3, rotation: -25, autoAlpha: 0 }, { scale: 1, rotation: -8, autoAlpha: 1, duration: 0.32, ease: 'power4.in' }, W_(4, 'कहा') - 0.1);
    TL.fromTo(L.cam, { y: 16 }, { y: 0, duration: 0.4, ease: 'elastic.out(1,0.25)', immediateRender: false }, W_(4, 'कहा') + 0.25);
  }
  // 5 — the other person doesn't even know
  {
    const s = S(5); const L = layer(s.a - 0.2, S(6).a - 0.2, 'zoom', 'bg_living');
    camMove(L, { scale: 1.0 }, { scale: 1.07 });
    const w = person(L.cam, 'w_kurta', 540, 1580, 880, 2);
    [[300, 520, 160, 'पता'], [790, 470, 200, 'पता ही'], [560, 330, 130, 'इसलिए']].forEach(([x, y, sz, wd], k) => {
      const q = text(L.cam, '?', x, y, { fontSize: sz + 'px', color: RUST, fontFamily: "'Rozha One'", fontWeight: 400 }); pop(q, W_(5, wd) + k * 0.15, { rot: 20 });
    });
    const tg = tag(L.cam, 'उन्हें पता ही नहीं', 540, 620, { fontSize: '54px', background: MUSTARD }); pop(tg, W_(5, 'पता ही'));
    const ct = img(L.cam, 'contract', 840, 900, 200); pop(ct, W_(5, 'पूरा नहीं'));
    cross(L.cam, 840, 900, 1.5, W_(5, 'पूरा नहीं') + 0.3);
  }
  // 6 — resentment leaks out: taunts, silence, sudden anger
  {
    const s = S(6); const L = layer(s.a - 0.2, S(7).a - 0.2, 'wipe');
    el('div', L.cam, { position: 'absolute', inset: 0, background: '#33402f' });
    camMove(L, { scale: 1.0 }, { scale: 1.05 });
    const ck = img(L.cam, 'cooker', 540, 1020, 560); pop(ck, s.a);
    rise(big(L.cam, 'नाराज़गी', 540, 300, 120, CREAM), s.a + 0.1);
    const words = [['तानों', 'ताने', 230, 560], ['चुप्पी', 'चुप्पी', 850, 600], ['गुस्से', 'गुस्सा!', 540, 680]];
    words.forEach(([w, lab, x, y], k) => pop(tag(L.cam, lab, x, y, { fontSize: '56px', background: k === 2 ? RUST : CREAM, color: k === 2 ? CREAM : INK }), W_(6, w), { rot: k % 2 ? 8 : -8 }));
    const tf = W_(6, 'गुस्से');
    HOOKS.push(t => { if (t < s.a || t > L.t1 + 1) return; const k = Math.min(1, (t - s.a) / (tf - s.a));
      gsap.set(ck, { x: Math.sin(t * 50) * k * k * 10, rotation: Math.sin(t * 37) * k * k * 2.5 }); });
    for (let k = 0; k < 9; k++) {
      const p = el('div', L.cam, { position: 'absolute', left: '500px', top: '760px', width: '90px', height: '90px', borderRadius: '50%', background: CREAM, opacity: 0 });
      const an = -Math.PI / 2 + (k - 4) * 0.3;
      TL.fromTo(p, { x: 0, y: 0, scale: 0.3, opacity: 0.95 }, { x: Math.cos(an) * 420, y: Math.sin(an) * 420, scale: 2.4, opacity: 0, duration: 1.2, ease: 'power2.out', immediateRender: false }, tf + k * 0.03);
    }
    const fl = el('div', L.cam, { position: 'absolute', inset: 0, background: CREAM, opacity: 0 });
    TL.fromTo(fl, { opacity: 0.7 }, { opacity: 0, duration: 0.4, immediateRender: false }, tf);
  }
  // 7–10 — the cure: give without conditions, ask clearly, people can't read minds
  {
    const s = S(7); const L = layer(s.a - 0.2, S(11).a - 0.2, 'iris', 'bg_paper');
    camMove(L, { scale: 1.06 }, { scale: 1.0 });
    rise(big(L.cam, 'इलाज सीधा है', 540, 280, 110, INK), s.a + 0.05);
    draw(inkPath(L.cam, 'M240 360 Q540 390 840 352', {}, { color: RUST, width: 12 }), s.a + 0.4, 0.5);
    const cards = [[8, 'बिना शर्त दीजिए', 'gift', 'जो दीजिए'], [9, 'साफ़ शब्दों में माँगिए', 'note', 'साफ़']];
    cards.forEach(([i, lab, im, w], k) => {
      const y = 600 + k * 330;
      const c = box(L.cam, 540, y, { width: '900px', height: '280px', background: CREAM, borderRadius: '28px', border: `6px solid ${INK}`, boxShadow: `10px 10px 0 ${INK}` });
      img(c, im, 150, 140, 190);
      el('div', c, { position: 'absolute', left: '280px', top: '0', bottom: '0', right: '20px', display: 'flex', alignItems: 'center', fontFamily: "'Baloo 2'", fontWeight: 800, fontSize: '58px', color: INK, lineHeight: 1.1 }).textContent = lab;
      TL.set(c, { autoAlpha: 0 }, 0);
      TL.fromTo(c, { x: k ? 700 : -700, autoAlpha: 0 }, { x: 0, autoAlpha: 1, duration: 0.5, ease: 'back.out(1.4)', immediateRender: false }, W_(i, w) - 0.15);
      check(L.cam, 900, y - 90, 1.3, W_(i, w) + 0.5, '#3f6b30');
    });
    // 10 — people can't read minds
    const t10 = S(10).a;
    const hd = img(L.cam, 'head_calm', 540, 1290, 190); TL.set(hd, { autoAlpha: 0 }, 0); pop(hd, t10);
    [[380, 1250], [700, 1230]].forEach(([x, y], k) => { const q = text(L.cam, '?', x, y, { fontSize: '120px', color: RUST, fontFamily: "'Rozha One'", fontWeight: 400 }); pop(q, t10 + 0.2 + k * 0.15, { rot: 18 }); });
    const lab = tag(L.cam, 'लोग मन नहीं पढ़ सकते', 540, 1100, { fontSize: '50px', background: RUST, color: CREAM }); pop(lab, W_(10, 'मन नहीं'));
  }
  // 11 — bridge to the promo
  {
    const s = S(11); const L = layer(s.a - 0.2, SH_END, 'zoom', 'bg_paper');
    camMove(L, { scale: 1.06 }, { scale: 1.0 });
    const bk = img(L.cam, 'book', 540, 760, 400); pop(bk, s.a + 0.05); float(bk, s.a, L.t1, 7, 1);
    rise(big(L.cam, 'पूरा सारांश', 540, 300, 110, INK), s.a + 0.1);
    pop(tag(L.cam, 'हिंदी में', 540, 455, { fontSize: '56px', background: MUSTARD }), W_(11, 'हिंदी'));
    rise(big(L.cam, 'पढ़िए भी, सुनिए भी', 540, 1120, 80, RUST), W_(11, 'पढ़िए'));
    pop(tag(L.cam, 'पुस्तिका', 540, 1260, { fontSize: '64px', background: INK, color: CREAM }), W_(11, 'पुस्तिका'));
  }
  window.VIDEO_END = SH_END;
  buildSubs(1e9);
}
