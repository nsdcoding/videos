// Shot list. Each sentence of the narration gets its own visual beat.
const SAMPLE_END = 70.0 + LEAD;

function chapterCard(i, num, trans = 'wipe', extra) {
  const s = S(i);
  const L = layer(s.a - 0.3, s.next, trans);
  el('div', L.cam, { position: 'absolute', inset: 0, background: INK });
  const stripe = el('div', L.cam, { position: 'absolute', left: 0, top: '0', width: '100%', height: '100%', background: MUSTARD,
    clipPath: 'polygon(0 0, 46% 0, 34% 100%, 0 100%)' });
  TL.fromTo(stripe, { x: -900 }, { x: 0, duration: 0.6, ease: 'power3.out' }, s.a - 0.3);
  const n = text(L.cam, num, 330, 330, { fontSize: '300px', color: INK, fontFamily: "'Rozha One'", fontWeight: 400 });
  pop(n, s.a - 0.1, { rot: -15 });
  const hd = text(L.cam, s.text, 1330, 520, { fontSize: '80px', color: CREAM, whiteSpace: 'normal', width: '900px' });
  rise(hd, s.a);
  const u = inkPath(L.cam, 'M920 690 Q1330 715 1740 680', {}, { color: MUSTARD, width: 10 });
  draw(u, s.a + 0.3, 0.7);
  const lab = text(L.cam, 'अध्याय ' + num, 1330, 330, { fontSize: '34px', color: MUSTARD, fontFamily: "'Mukta'", fontWeight: 700, letterSpacing: '4px' });
  rise(lab, s.a + 0.15, { from: 20 });
  camMove(L, { scale: 1.0 }, { scale: 1.06 });
  if (extra) extra(L, s);
  return L;
}

function maleSym(parent, x, y, s) {
  const b = box(parent, x, y, { width: s + 'px', height: s + 'px' });
  b.innerHTML = `<svg viewBox="0 0 100 100" width="${s}" height="${s}"><circle cx="40" cy="60" r="26" fill="none" stroke="${INK}" stroke-width="10"/>
    <path d="M58 42 L84 16 M62 16 L84 16 L84 38" fill="none" stroke="${INK}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
  return b;
}
function build() {
  // ---------------- INTRO (cover) ----------------
  {
    const L = layer(0, LEAD, 'cut', 'bg_paper');
    camMove(L, { scale: 1.08 }, { scale: 1.0 }, 'power2.out');
    const nail = el('div', L.cam, { position: 'absolute', left: '1390px', top: '250px', width: '1px', height: '1px' });
    const mask = img(L.cam, 'mask', 1390, 560, 470, { transformOrigin: '62% 3%' });
    TL.fromTo(mask, { y: -900, rotation: 30 }, { y: 0, rotation: 0, duration: 1.1, ease: 'bounce.out' }, 0.2);
    HOOKS.push(t => { if (t > 1.3 && t < LEAD + 1) gsap.set(mask, { rotation: Math.sin((t - 1.3) * 2.4) * 5 * Math.exp(-(t - 1.3) * 0.5) }); });
    const t1 = text(L.cam, 'अच्छा दिखना', 640, 380, { fontSize: '150px' });
    const t2 = text(L.cam, 'छोड़िए', 640, 560, { fontSize: '170px', color: RUST });
    rise(t1, 0.3); rise(t2, 0.6);
    const u = inkPath(L.cam, 'M330 680 Q640 705 950 670', {}, { width: 12 });
    draw(u, 1.1, 0.6);
    const sub = text(L.cam, 'No More Mr Nice Guy · रॉबर्ट ग्लोवर', 640, 760, { fontSize: '40px', fontFamily: "'Mukta'", fontWeight: 700 });
    const sub2 = tag(L.cam, 'हिंदी सारांश', 640, 850, { fontSize: '34px' });
    rise(sub, 1.3, { from: 20 }); pop(sub2, 1.6);
  }

  // 0: heading — chapter card; smile flips at "ख़ुद"
  chapterCard(0, '01', 'wipe', (L, s) => {
    L.cam.querySelector('div:nth-child(2)'); // stripe
    const hg = el('div', L.cam, { position: 'absolute', left: '200px', top: '640px', width: '482px', height: '708px', transformOrigin: '0 0' });
    gsap.set(hg, { scale: 0.5 });
    // a floating head that keeps smiling... until "ख़ुद नहीं"
    const g = Guy(L.cam, 330, 1500, 1.0); gsap.set(g.g, { visibility: 'hidden' });
    const head = img(L.cam, 'head', 330, 760, 230);
    const m = el('svg', L.cam, { position: 'absolute', left: (330 - 115 + 244 * 230 / 482 - 38) + 'px', top: (760 - 169 + 509 * 230 / 482 - 19) + 'px', width: '77px', height: '38px' }, { viewBox: '0 0 160 80' });
    m.innerHTML = MOUTH.smile;
    pop(head, s.a + 0.2); pop(m, s.a + 0.2);
    const tk = W_(0, 'ख़ुद');
    TL.set(head, { attr: { src: A('head_tired') } }, tk);
    TL.call(() => {}, null, tk);
    HOOKS.push(t => { m.innerHTML = t >= tk ? '' : MOUTH.smile; });
    TL.fromTo(head, { rotation: 0 }, { rotation: -6, duration: 0.4, ease: 'back.out' }, tk);
  });

  // 1: Glover the therapist — same kind of people kept coming for years
  {
    const s = S(1); const L = layer(s.a - 0.2, s.next, 'iris', 'bg_clinic');
    camMove(L, { scale: 1.12, x: 80 }, { scale: 1.0, x: -40 });
    const door = tag(L.cam, 'मनोचिकित्सक', 1560, 280, { fontSize: '32px' });
    pop(door, s.a + 0.2);
    const guys = [];
    [520, 760, 1000, 1240].forEach((x, k) => {
      const g = Guy(L.cam, x, 960, 0.78);
      guys.push(g);
      g.face(0, k % 2 ? 'neutral' : 'smile');
      TL.fromTo(g.g, { autoAlpha: 0, y: 40 }, { autoAlpha: 1, y: 0, duration: 0.4, ease: 'back.out(2)' }, s.a + 0.6 + k * 0.65);
    });
    // tear-off calendar = years passing
    const cal = box(L.cam, 300, 300, { width: '170px', height: '190px' });
    cal.innerHTML = `<div style="position:absolute;inset:0;background:${CREAM};border:5px solid ${INK};border-radius:10px"></div>
      <div style="position:absolute;left:0;right:0;top:0;height:46px;background:${RUST};border:5px solid ${INK};border-radius:10px 10px 0 0"></div>`;
    pop(cal, s.a + 0.3);
    for (let k = 0; k < 6; k++) {
      const pg = el('div', cal, { position: 'absolute', left: '5px', right: '5px', top: '46px', bottom: '5px', background: CREAM, transformOrigin: '50% 0',
        fontFamily: "'Rozha One'", fontSize: '64px', color: INK, textAlign: 'center', lineHeight: '130px' });
      pg.textContent = 'साल';
      TL.to(pg, { rotationX: 100, autoAlpha: 0, duration: 0.35, ease: 'power2.in' }, s.a + 0.8 + k * 0.5);
    }
  }

  // 2: from outside, nothing seemed wrong — magnifier sweep, checks
  {
    const s = S(2); const L = layer(s.a - 0.2, s.next, 'push', 'bg_paper');
    camMove(L, { scale: 1.0 }, { scale: 1.08 });
    const g = Guy(L.cam, 960, 1010, 1.25);
    const mg = img(L.cam, 'magnifier', 700, 400, 300);
    TL.fromTo(mg, { x: -300, y: 300, rotation: -20 }, { x: 560, y: 120, rotation: 10, duration: s.b - s.a, ease: 'sine.inOut' }, s.a);
    [[620, 320], [1320, 420], [1290, 700]].forEach(([x, y], k) => check(L.cam, x, y, 1.4, s.a + 0.6 + k * 0.5));
    const q = text(L.cam, 'सब ठीक?', 1540, 220, { fontSize: '70px', color: RUST });
    pop(q, s.a + 1.6);
  }

  // 3: polite, helpful, no fights, useful to all, everyone calls him good
  {
    const s = S(3); const L = layer(s.a - 0.2, s.next, 'diag', 'bg_office');
    camMove(L, { scale: 1.05, x: 0 }, { scale: 1.12, x: -60 });
    bgDrift(L, -50);
    const g = Guy(L.cam, 520, 1000, 1.05);
    g.pose(W_(3, 'मददगार'), 'explain');
    const words = [['विनम्र', 'विनम्र', 300, 260], ['मददगार', 'मददगार', 760, 200], ['झगड़ा', 'झगड़ा नहीं', 300, 420], ['काम आते', 'सबके काम आते', 790, 360]];
    words.forEach(([key, label, x, y], k) => pop(tag(L.cam, label, x, y, { fontSize: '38px' }), W_(3, key) - 0.1, { rot: k % 2 ? 8 : -8 }));
    const tg = W_(3, 'सब उन्हें');
    [['w_office', 1180, 1], ['elder', 1440, 2], ['m_hoodie', 1700, 3]].forEach(([n, x, sd], k) => {
      const p = person(L.cam, n, x, 1010, 560, sd);
      TL.fromTo(p, { x: 500, autoAlpha: 0 }, { x: 0, autoAlpha: 1, duration: 0.5, ease: 'power3.out' }, tg - 1.2 + k * 0.15);
    });
    bubble(L.cam, 'कितना अच्छा इंसान!', 1440, 380, tg + 0.1);
    [1220, 1700].forEach((x, k) => { const h = text(L.cam, '♥', x, 470, { fontSize: '80px', color: RUST, fontFamily: 'serif' }); pop(h, tg + 0.4 + k * 0.2);
      TL.to(h, { y: -60, autoAlpha: 0, duration: 1.4, ease: 'power1.in' }, tg + 1.2 + k * 0.2); });
  }

  // 4: inside — tired, angry, not getting what he wanted. Split: outside vs inside
  {
    const s = S(4); const L = layer(s.a - 0.2, s.next, 'wipe');
    el('div', L.cam, { position: 'absolute', inset: 0, background: MUSTARD });
    const right = el('div', L.cam, { position: 'absolute', left: '960px', top: 0, width: '960px', height: '1080px', background: '#3d4a37', overflow: 'hidden' });
    reveal(right, s.a + 0.1, 'inset(0 0 100% 0)', 'inset(0 0 0% 0)');
    const l1 = text(L.cam, 'बाहर', 480, 120, { fontSize: '56px' }); rise(l1, s.a);
    const l2 = text(L.cam, 'भीतर', 1440, 120, { fontSize: '56px', color: CREAM }); rise(l2, s.a + 0.3);
    const g1 = Guy(L.cam, 480, 1020, 1.1);
    const g2 = Guy(L.cam, 1440, 1020, 1.1, { head: 'head_tired', mouth: 'frown' });
    TL.fromTo(g2.g, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.4 }, s.a + 0.4);
    // battery draining at "थके"
    const bt = W_(4, 'थके');
    const bat = box(L.cam, 1700, 330, { width: '150px', height: '70px', border: `6px solid ${CREAM}`, borderRadius: '10px' });
    const lvl = el('div', bat, { position: 'absolute', left: '6px', top: '6px', bottom: '6px', width: '126px', background: '#8fb069', transformOrigin: '0 50%' });
    el('div', bat, { position: 'absolute', right: '-20px', top: '18px', width: '12px', height: '22px', background: CREAM, borderRadius: '3px' });
    pop(bat, bt - 0.3);
    TL.to(lvl, { scaleX: 0.12, backgroundColor: RUST, duration: 1.6, ease: 'power1.in' }, bt);
    // storm cloud at "नाराज़"
    const ct = W_(4, 'नाराज़');
    const cl = img(L.cam, 'cloud', 1200, 330, 280);
    pop(cl, ct - 0.2);
    HOOKS.push(t => { if (t > ct && t < s.next + 1) gsap.set(cl, { x: Math.sin(t * 40) * (t < ct + 0.6 ? 6 : 1.5) }); });
    const bolt = inkPath(L.cam, 'M1210 420 L1180 490 L1220 490 L1190 560', {}, { color: MUSTARD, width: 10 });
    draw(bolt, ct + 0.3, 0.25);
    // "what he wanted" — question mark blooms
    const qt = W_(4, 'नहीं मिल');
    const q = text(L.cam, '?', 1640, 620, { fontSize: '220px', color: MUSTARD, fontFamily: "'Rozha One'", fontWeight: 400 });
    pop(q, qt, { rot: 20 });
    camMove(L, { scale: 1.0 }, { scale: 1.05, x: -20 });
  }

  // 5: distance in relationships · behind at work · silent anger that bursts
  {
    const s = S(5); const L = layer(s.a - 0.2, s.next, 'zoom', 'bg_living');
    camMove(L, { scale: 1.0 }, { scale: 1.06 });
    // beat a: couple drifting apart
    const ta = W_(5, 'रिश्तों');
    const grpA = el('div', L.cam, { position: 'absolute', inset: 0 });
    const g = Guy(grpA, 900, 1010, 0.95, { mouth: 'neutral' });
    const w = person(grpA, 'w_kurta', 1080, 1010, 590, 4);
    TL.to(g.g, { x: -260, duration: 2.2, ease: 'power2.inOut' }, ta + 0.2);
    TL.to(w, { x: 260, duration: 2.2, ease: 'power2.inOut' }, ta + 0.2);
    const crack = inkPath(grpA, 'M990 300 L1010 420 L975 520 L1015 640 L985 760 L1005 900', {}, { color: INK, width: 8 });
    draw(crack, ta + 0.8, 1.0);
    const dl = tag(grpA, 'दूरी', 995, 220, { fontSize: '42px' }); pop(dl, ta + 1.2);
    // beat b: falling behind at work — bar race panel slides in
    const tb = W_(5, 'काम में');
    const pb = box(L.cam, 960, 540, { width: '1920px', height: '1080px', background: CREAM });
    reveal(pb, tb - 0.3, 'inset(0 0 0 100%)', 'inset(0 0 0 0%)', 0.5);
    const base = inkPath(pb, 'M360 860 L1560 860', {}, { width: 8 }); draw(base, tb, 0.4);
    const bars = [[540, 520, OLIVE], [800, 600, OLIVE], [1060, 470, OLIVE], [1320, 170, RUST]];
    bars.forEach(([x, hh, c], k) => {
      const b = el('div', pb, { position: 'absolute', left: (x - 80) + 'px', bottom: '220px', width: '160px', height: hh + 'px', background: c,
        border: `6px solid ${INK}`, borderBottom: 'none', borderRadius: '12px 12px 0 0', transformOrigin: '50% 100%' });
      TL.fromTo(b, { scaleY: 0 }, { scaleY: 1, duration: k === 3 ? 1.6 : 0.9, ease: 'power2.out' }, tb + 0.1 + k * 0.12);
    });
    const hd = img(pb, 'head_tired', 1320, 600, 130); pop(hd, tb + 1.0);
    const lb = text(pb, 'पीछे', 1320, 940, { fontSize: '48px', color: RUST }); rise(lb, tb + 1.1, { from: 20 });
    // beat c: pressure cooker of silent anger
    const tc = W_(5, 'सबसे बड़ी');
    const pc = box(L.cam, 960, 540, { width: '1920px', height: '1080px', background: '#3d4a37' });
    reveal(pc, tc - 0.3, 'circle(0% at 50% 60%)', 'circle(80% at 50% 60%)', 0.6, 'power2.in');
    const ck = img(pc, 'cooker', 960, 600, 430);
    const gauge = box(pc, 1430, 420, { width: '220px', height: '220px', borderRadius: '50%', background: CREAM, border: `8px solid ${INK}` });
    const red = el('div', gauge, { position: 'absolute', inset: '0', borderRadius: '50%', background: `conic-gradient(from 60deg, transparent 0deg 170deg, ${RUST} 170deg 240deg, transparent 240deg)` });
    const needle = el('div', gauge, { position: 'absolute', left: '104px', top: '30px', width: '12px', height: '80px', background: INK, borderRadius: '6px', transformOrigin: '50% 100%' });
    pop(gauge, tc + 0.2);
    const tf = W_(5, 'फूट');
    TL.fromTo(needle, { rotation: -110 }, { rotation: 100, duration: tf - tc - 0.2, ease: 'power1.in' }, tc + 0.2);
    const lbl = text(pc, 'चुपचाप जमा होता गुस्सा', 960, 160, { fontSize: '54px', color: CREAM }); rise(lbl, tc + 0.4);
    HOOKS.push(t => { if (t < tc || t > s.next + 1) return; const k = Math.min(1, (t - tc) / (tf - tc));
      gsap.set(ck, { x: Math.sin(t * 50) * k * k * 8, rotation: Math.sin(t * 37) * k * k * 2 }); });
    // burst
    for (let k = 0; k < 9; k++) {
      const p = el('div', pc, { position: 'absolute', left: '930px', top: '330px', width: '90px', height: '90px', borderRadius: '50%', background: CREAM, opacity: 0 });
      const an = -Math.PI / 2 + (k - 4) * 0.28;
      TL.fromTo(p, { x: 0, y: 0, scale: 0.3, opacity: 0.95 }, { x: Math.cos(an) * 520, y: Math.sin(an) * 320, scale: 2.6, opacity: 0, duration: 1.2, ease: 'power2.out', immediateRender: false }, tf + k * 0.03);
    }
    const flash = el('div', pc, { position: 'absolute', inset: 0, background: CREAM, opacity: 0 });
    TL.fromTo(flash, { opacity: 0.8 }, { opacity: 0, duration: 0.4, immediateRender: false }, tf);
    TL.fromTo(L.cam, { x: -18 }, { x: 0, duration: 0.5, ease: 'elastic.out(1,0.2)', immediateRender: false }, tf);
  }

  // 6: Glover saw a pattern and gave it a name
  {
    const s = S(6); const L = layer(s.a - 0.2, s.next, 'wipeUp', 'bg_paper');
    camMove(L, { scale: 1.12 }, { scale: 1.0 });
    const pts = [];
    for (let r = 0; r < 3; r++) for (let c = 0; c < 6; c++) {
      const x = 360 + c * 240, y = 270 + r * 230, h = img(L.cam, (r + c) % 3 ? 'head' : 'head_tired', x, y, 130);
      pop(h, s.a + (r * 6 + c) * 0.05, { dur: 0.35 }); pts.push([x, y]);
    }
    const d = 'M' + pts.filter((_, k) => k % 2 === 0).map(p => p.join(' ')).join(' L');
    draw(inkPath(L.cam, d, { opacity: 0.5 }, { width: 6, color: RUST }), s.a + 0.9, 1.2);
    const tn = W_(6, 'नाम');
    const st = text(L.cam, 'NICE GUY', 960, 520, { fontSize: '170px', color: RUST, border: `12px solid ${RUST}`, padding: '0 40px', borderRadius: '20px', background: 'rgba(243,231,207,.92)', fontFamily: "'Baloo 2'" });
    TL.fromTo(st, { scale: 3, rotation: -25, autoAlpha: 0 }, { scale: 1, rotation: -8, autoAlpha: 1, duration: 0.35, ease: 'power4.in' }, tn - 0.2);
    TL.fromTo(L.cam, { y: 14 }, { y: 0, duration: 0.4, ease: 'elastic.out(1,0.25)', immediateRender: false }, tn + 0.15);
  }

  // 7: the problem is not being good
  {
    const s = S(7); const L = layer(s.a - 0.2, s.next, 'push', 'bg_paper');
    const t1 = text(L.cam, 'अच्छा होना', 960, 430, { fontSize: '150px' }); rise(t1, s.a);
    check(L.cam, 1450, 420, 2.2, s.a + 0.6, '#4d7a3a');
    const t2 = text(L.cam, 'समस्या नहीं है', 960, 640, { fontSize: '80px', color: OLIVE }); rise(t2, W_(7, 'समस्या') - 0.1);
    camMove(L, { scale: 1.0 }, { scale: 1.07 });
  }

  // 8: the problem is when LOOKING good becomes a strategy → approval & avoiding conflict
  {
    const s = S(8); const L = layer(s.a - 0.2, s.next, 'cut', 'bg_paper');
    const t1 = text(L.cam, 'अच्छा होना', 960, 430, { fontSize: '150px' });
    TL.to(t1, { x: -560, y: -150, scale: 0.45, duration: 0.6, ease: 'power3.inOut' }, s.a + 0.2);
    cross(L.cam, 520, 280, 0.9, s.a + 0.8, OLIVE);
    TL.set(t1, { opacity: 0.55 }, s.a + 0.8);
    const tD = W_(8, 'दिखना');
    const t2 = text(L.cam, 'अच्छा <span style="color:#b5522f">दिखना</span>', 960, 260, { fontSize: '120px' }); rise(t2, tD - 0.3);
    const mk = img(L.cam, 'mask', 960, 560, 250); pop(mk, tD + 0.2);
    float(mk, s.a, s.next, 6, 3);
    const tR = W_(8, 'रणनीति');
    const rt = tag(L.cam, 'एक रणनीति', 960, 780, { fontSize: '40px', background: MUSTARD }); pop(rt, tR);
    const tA = W_(8, 'स्वीकृति'), tT = W_(8, 'टकराव');
    arrow(L.cam, 820, 600, 470, 640, tA - 0.3, { bend: 0.2, width: 8 });
    const a1 = tag(L.cam, '👍 स्वीकृति पाना', 330, 700, { fontSize: '40px' }); pop(a1, tA);
    arrow(L.cam, 1100, 600, 1450, 640, tT - 0.3, { bend: -0.2, width: 8 });
    const a2 = tag(L.cam, '🛡 टकराव से बचना', 1590, 700, { fontSize: '40px' }); pop(a2, tT);
    camMove(L, { scale: 1.0, y: 0 }, { scale: 1.05, y: -10 });
  }

  // 9: "one thing should be clear at the start" — host shot, he talks to camera
  {
    const s = S(9); const L = layer(s.a - 0.2, S(10).next, 'iris', 'bg_living');
    TL.fromTo(L.cam, { scale: 1.0 }, { scale: 1.12, duration: s.next - s.a + 0.5, ease: 'sine.inOut' }, s.a);
    const g = Guy(L.cam, 680, 1560, 1.75);
    g.say(s.a, S(10).b);
    g.pose(s.a + 0.3, 'explain');
    const nt = img(L.cam, 'note', 1350, 400, 380); pop(nt, s.a + 0.4, { rot: 12 });
    const nx = text(L.cam, 'एक ज़रूरी बात', 1340, 430, { fontSize: '42px', rotate: '-4deg' }); pop(nx, s.a + 0.6);
    // 10: book written for men, language of its era — book replaces note
    const s2 = S(10);
    out(nt, s2.a - 0.2); out(nx, s2.a - 0.2);
    const bk = img(L.cam, 'book', 1380, 470, 330); pop(bk, s2.a, { rot: 15 }); float(bk, s2.a, s2.next, 6, 2);
    const ms = maleSym(L.cam, 1390, 440, 120); pop(ms, W_(10, 'पुरुषों'));
    const era = tag(L.cam, 'पुराने दौर की भाषा', 1380, 760, { fontSize: '40px', background: MUSTARD }); pop(era, W_(10, 'भाषा'));
    g.pose(W_(10, 'भाषा'), 'point');
    // sepia "old era" wash
    const sep = el('div', L.cam, { position: 'absolute', inset: 0, background: 'rgba(120,80,20,.25)', mixBlendMode: 'multiply', opacity: 0 });
    TL.to(sep, { opacity: 1, duration: 0.6 }, W_(10, 'भाषा'));
    TL.to(L.cam, { scale: 1.0, duration: 0.8, ease: 'power2.inOut' }, s2.a - 0.3);
  }

  // 11: but the pattern isn't bound to gender — ♂ dissolves into everyone
  {
    const s = S(11); const L = layer(s.a - 0.2, s.next, 'wipe', 'bg_paper');
    camMove(L, { scale: 1.06 }, { scale: 1.0 });
    const ms = maleSym(L.cam, 960, 470, 260); pop(ms, s.a);
    const tg = W_(11, 'लिंग');
    TL.to(ms, { scale: 0, rotation: 180, autoAlpha: 0, duration: 0.4, ease: 'back.in(2)' }, tg - 0.2);
    const ppl = [['w_kurta', 360], ['elder', 620], ['mother', 1300], ['m_hoodie', 1560], ['w_office', 1820]];
    ppl.forEach(([n, x], k) => { const p = person(L.cam, n, x, 1030, 600, k + 2);
      TL.fromTo(p, { y: 700 }, { y: 0, duration: 0.5, ease: 'back.out(1.6)' }, tg + 0.1 + k * 0.12); });
    const g = Guy(L.cam, 960, 1030, 0.98);
    TL.fromTo(g.g, { y: 700 }, { y: 0, duration: 0.5, ease: 'back.out(1.6)' }, tg + 0.35);
    const l = text(L.cam, 'सब पर लागू', 960, 160, { fontSize: '80px', color: RUST }); rise(l, tg + 0.6);
  }

  // 12: pleasing people, hiding needs, hidden expectations — can happen to anyone
  {
    const s = S(12); const L = layer(s.a - 0.2, s.next + 0.4, 'diag');
    el('div', L.cam, { position: 'absolute', inset: 0, background: INK });
    const items = [['ख़ुश', 'mask', 'ख़ुश रखने की आदत'], ['छिपाना', 'chest', 'ज़रूरतें छिपाना'], ['उम्मीदें', 'contract', 'छिपी उम्मीदें']];
    items.forEach(([key, im, label], k) => {
      const x = 400 + k * 560, t = W_(12, key) - 0.3;
      const card = box(L.cam, x, 470, { width: '460px', height: '560px', background: CREAM, borderRadius: '24px', border: `6px solid ${MUSTARD}` });
      TL.fromTo(card, { rotationY: 90, autoAlpha: 0 }, { rotationY: 0, autoAlpha: 1, duration: 0.5, ease: 'back.out(1.4)' }, t);
      const p = img(card, im, 230, 230, 260); float(p, t, s.next, 6, k);
      const tx = text(card, label, 230, 470, { fontSize: '40px' });
    });
    const tAny = W_(12, 'किसी के');
    const any = text(L.cam, 'किसी के भी साथ', 960, 870, { fontSize: '64px', color: MUSTARD }); rise(any, tAny);
    camMove(L, { scale: 1.0 }, { scale: 1.05 });
  }

  buildRest();
  buildSubs(1e9);
}
