// Sections 2–17: reusable shot templates + a data-driven shot list.
// Each shot starts at the sentence containing `k` and lasts until the next shot.

let CUR = 0;
function I(sub) {
  for (let i = CUR; i < TIMING.length; i++) if (TIMING[i].text.includes(sub)) return i;
  throw new Error('sentence not found: ' + sub);
}
// time of a word within the shot's span (number = seconds after shot start)
function WT(sp, w) {
  if (w === undefined || w === null) return sp.a + 0.4;
  if (typeof w === 'number') return sp.a + 0.2 + w;
  for (let i = sp.i0; i <= sp.i1; i++) if (TIMING[i].text.includes(w)) return W_(i, w);
  console.error('word not found in span: ' + w + ' @' + sp.i0);
  return sp.a + 0.4;
}
const CAMS = [
  [{ scale: 1.0 }, { scale: 1.07 }], [{ scale: 1.09 }, { scale: 1.0 }],
  [{ scale: 1.06, x: 45 }, { scale: 1.06, x: -45 }], [{ scale: 1.06, x: -45 }, { scale: 1.06, x: 45 }],
  [{ scale: 1.0, y: 18 }, { scale: 1.06, y: -12 }],
];
const TRANS = ['wipe', 'iris', 'diag', 'push', 'zoom', 'wipeUp', 'fade'];

function thought(parent, str, x, y, t) {
  const b = box(parent, x, y, { fontFamily: "'Baloo 2'", fontWeight: 700, fontSize: '34px', color: OLIVE, background: CREAM,
    padding: '10px 28px 4px', borderRadius: '40px', border: `4px dashed ${INK}`, whiteSpace: 'nowrap' });
  b.innerHTML = str + `<div style="position:absolute;left:46%;bottom:-30px;width:20px;height:20px;border-radius:50%;background:${CREAM};border:4px solid ${INK}"></div>
    <div style="position:absolute;left:43%;bottom:-52px;width:12px;height:12px;border-radius:50%;background:${CREAM};border:3px solid ${INK}"></div>`;
  pop(b, t); return b;
}
function stamp(parent, str, x, y, t, size = 96) {
  const st = text(parent, str, x, y, { fontSize: size + 'px', color: RUST, border: `10px solid ${RUST}`, padding: '0 34px', borderRadius: '18px', background: 'rgba(243,231,207,.94)' });
  TL.fromTo(st, { scale: 3, rotation: -25, autoAlpha: 0 }, { scale: 1, rotation: -7, autoAlpha: 1, duration: 0.32, ease: 'power4.in' }, t);
  return st;
}
function heart(parent, x, y, size, t) { const h = text(parent, '♥', x, y, { fontSize: size + 'px', color: RUST, fontFamily: 'serif' }); pop(h, t); return h; }

function mkGuy(L, sp, p, x, y, s) {
  const g = Guy(L.cam, x, y, s, { head: p.head || 'head', mouth: p.mouth || (p.head && p.head !== 'head' ? 'neutral' : 'smile') });
  if (!p.noEnter) TL.fromTo(g.g, { autoAlpha: 0, x: -70 }, { autoAlpha: 1, x: 0, duration: 0.5, ease: 'power3.out', immediateRender: false }, sp.a + 0.15);
  for (const [w, h] of (p.heads || [])) g.headSwap(WT(sp, w), h);
  if (p.talk === true) g.say(sp.a + 0.2, sp.b);
  else if (typeof p.talk === 'string') { const i = I2(sp, p.talk); g.say(TIMING[i].start + LEAD, TIMING[i].end + LEAD); }
  return g;
}
function I2(sp, sub) { for (let i = sp.i0; i <= sp.i1; i++) if (TIMING[i].text.includes(sub)) return i; return sp.i0; }

// shared decorations available to every template
function deco(L, sp, p) {
  const C = L.cam;
  if (p.title) { const [w, s] = p.title; const e = tag(C, s, 960, 110, { fontSize: '46px', background: MUSTARD }); pop(e, WT(sp, w)); }
  if (p.badge) { const e = tag(C, p.badge, 190, 90, { fontSize: '36px', background: RUST, color: CREAM, borderColor: INK }); pop(e, sp.a + 0.3, { rot: -12 }); }
  (p.cast || []).forEach(([n, x, h, w], k) => {
    const e = person(C, n, x, 1010, h, k + 3);
    TL.fromTo(e, { x: x > 960 ? 420 : -420, autoAlpha: 0 }, { x: 0, autoAlpha: 1, duration: 0.55, ease: 'power3.out', immediateRender: false }, WT(sp, w) + k * 0.12);
    TL.set(e, { autoAlpha: 0 }, 0);
  });
  (p.props || []).forEach(([n, x, y, w, wd, mv], k) => {
    const e = img(C, n, x, y, w); const t = WT(sp, wd); pop(e, t, { rot: k % 2 ? 10 : -10 });
    if (mv) TL.to(e, { x: mv.x || 0, y: mv.y || 0, duration: 0.8, ease: 'power2.inOut' }, WT(sp, mv.at));
    else float(e, t, L.t1, 5, k + 1);
  });
  (p.tags || []).forEach(([w, s, x, y], k) => pop(tag(C, s, x, y, { fontSize: '38px' }), WT(sp, w), { rot: k % 2 ? 7 : -7 }));
  (p.bubbles || []).forEach(([w, s, x, y]) => bubble(C, s, x, y, WT(sp, w)));
  (p.thought || []).forEach(([w, s, x, y]) => thought(C, s, x, y, WT(sp, w)));
  (p.texts || []).forEach(([w, s, x, y, size, color]) => {
    const e = s === '♥' ? text(C, s, x, y, { fontSize: size + 'px', color: color || RUST, fontFamily: 'serif' })
      : s.length < 3 ? text(C, s, x, y, { fontSize: (size || 60) + 'px', color: color || INK })
      : tag(C, s, x, y, { fontSize: Math.min(size || 60, 50) + 'px', color: color || INK, boxShadow: 'none', border: `3px solid ${INK}` });
    pop(e, WT(sp, w), { rot: s.length < 3 ? 18 : 4 });
  });
  (p.checks || []).forEach(([w, x, y]) => check(C, x, y, 1.6, WT(sp, w), '#4d7a3a'));
  (p.crosses || []).forEach(([w, x, y]) => cross(C, x, y, 1.6, WT(sp, w)));
  if (p.stamp) stamp(C, p.stamp[1], p.stamp[2] || 960, p.stamp[3] || 520, WT(sp, p.stamp[0]), p.stamp[4] || 96);
  if (p.loop) {
    const [w, cx, cy, labels] = p.loop; const t = WT(sp, w), r = 175;
    const ring = el('svg', C, { position: 'absolute', left: (cx - r) + 'px', top: (cy - r) + 'px', width: 2 * r + 'px', height: 2 * r + 'px', overflow: 'visible' }, { viewBox: `0 0 ${2 * r} ${2 * r}` });
    ring.innerHTML = `<circle cx="${r}" cy="${r}" r="${r - 6}" fill="none" stroke="${RUST}" stroke-width="8" stroke-dasharray="40 22"/>`;
    TL.set(ring, { autoAlpha: 0 }, 0); TL.fromTo(ring, { autoAlpha: 0, scale: 0.4 }, { autoAlpha: 1, scale: 1, duration: 0.5, ease: 'back.out(2)', immediateRender: false }, t);
    HOOKS.push(tt => { if (tt > t - 0.5 && tt < L.t1 + 1) gsap.set(ring, { rotation: (tt - t) * 60 }); });
    labels.forEach((s, k) => { const an = -Math.PI / 2 + k * 2 * Math.PI / labels.length;
      pop(tag(C, s, cx + Math.cos(an) * r, cy + Math.sin(an) * r, { fontSize: '32px' }), t + 0.3 + k * 0.35); });
  }
}
function setTime(L) {}

// ---------------- templates ----------------
const T = {};
T.scene = (L, sp, p) => {
  if (p.guy !== false) mkGuy(L, sp, p, p.gx || 560, p.gy || 1010, p.gs || 1.05);
  deco(L, sp, p);
};
T.icon = (L, sp, p) => {
  if (p.title) { const e = text(L.cam, p.title, 960, 165, { fontSize: '76px' }); rise(e, sp.a + 0.1); }
  if (p.prop) { const e = img(L.cam, p.prop, p.x || 960, p.y || 490, p.w || 340); const t = WT(sp, p.at); pop(e, t); float(e, t, L.t1, 6, 2); }
  if (p.sub) { const e = tag(L.cam, p.sub[1], 960, 790, { fontSize: '48px', background: MUSTARD }); pop(e, WT(sp, p.sub[0])); }
  (p.side || []).forEach(s => (p.props = p.props || []).push(s));
  deco(L, sp, Object.assign({}, p, { title: null }));
};
T.big = (L, sp, p) => {
  if (p.bgc) el('div', L.cam, { position: 'absolute', inset: 0, background: p.bgc });
  const cx = p.prop ? 780 : 960;
  const hs = p.lines.map(l => (l[2] || 80) * 1.3);
  let y = 470 - hs.reduce((a, b) => a + b, 0) / 2;
  p.lines.forEach(([w, s, size, color], k) => {
    const e = text(L.cam, s, cx, y + hs[k] / 2, { fontSize: (size || 80) + 'px', color: color || INK });
    rise(e, WT(sp, w)); y += hs[k];
  });
  const u = inkPath(L.cam, `M${cx - 330} ${y + 20} Q${cx} ${y + 45} ${cx + 330} ${y + 12}`, {}, { color: p.bgc === INK ? MUSTARD : RUST, width: 10 });
  draw(u, WT(sp, p.lines[p.lines.length - 1][0]) + 0.3, 0.6);
  if (p.prop) { const [n, x, yy, w, wd] = p.prop; const e = img(L.cam, n, x, yy, w); pop(e, WT(sp, wd)); float(e, sp.a, L.t1, 7, 4); }
  deco(L, sp, Object.assign({}, p, { title: null }));
};
T.list = (L, sp, p) => {
  el('div', L.cam, { position: 'absolute', inset: 0, background: p.bgc || INK });
  const tt = text(L.cam, p.title, 960, 120, { fontSize: '62px', color: MUSTARD }); rise(tt, sp.a + 0.1);
  const n = p.items.length, cw = Math.min(470, (1760 - (n - 1) * 40) / n), x0 = 960 - ((n - 1) * (cw + 40)) / 2;
  const cards = [];
  p.items.forEach(([w, label, im], k) => {
    const x = x0 + k * (cw + 40), t = WT(sp, w);
    const card = box(L.cam, x, 520, { width: cw + 'px', height: '540px', background: CREAM, borderRadius: '24px', border: `6px solid ${MUSTARD}`,
      display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '24px' });
    const pic = el('img', card, { maxWidth: (cw * 0.62) + 'px', maxHeight: '290px' }, { src: A(im) });
    el('div', card, { fontFamily: "'Baloo 2'", fontWeight: 800, fontSize: (n > 3 ? 34 : 40) + 'px', color: INK, textAlign: 'center', padding: '0 14px', lineHeight: 1.15 }).textContent = label;
    const num = text(card, String(k + 1), 40, 40, { fontSize: '40px', color: CREAM, background: RUST, borderRadius: '50%', width: '64px', height: '64px', lineHeight: '70px', fontFamily: "'Rozha One'", fontWeight: 400 });
    TL.set(card, { autoAlpha: 0 }, 0);
    TL.fromTo(card, { rotationY: 90, autoAlpha: 0 }, { rotationY: 0, autoAlpha: 1, duration: 0.5, ease: 'back.out(1.4)', immediateRender: false }, t);
    float(pic, t, L.t1, 5, k);
    cards.forEach(c => TL.to(c, { scale: 0.93, opacity: 0.55, duration: 0.3 }, t));
    TL.fromTo(card, { scale: 1 }, { scale: 1.05, duration: 0.3, immediateRender: false }, t + 0.5);
    if (cards.length) TL.to(cards[cards.length - 1], { scale: 0.93, duration: 0.3 }, t);
    cards.push(card);
  });
  if (p.end) {
    const t = WT(sp, p.end[0]);
    TL.to(cards, { scale: 0.85, opacity: 1, y: -40, duration: 0.4 }, t);
    const e = tag(L.cam, p.end[1], 960, 880, { fontSize: '40px', background: MUSTARD }); pop(e, t + 0.2);
  }
  deco(L, sp, Object.assign({}, p, { title: null }));
};
T.compare = (L, sp, p) => {
  const C = L.cam;
  el('div', C, { position: 'absolute', inset: 0, background: MUSTARD });
  const R = el('div', C, { position: 'absolute', left: '960px', top: 0, width: '960px', height: '1080px', background: '#33402f', overflow: 'hidden' });
  const ty = p.head ? 200 : 140;
  if (p.head) { const e = tag(C, p.head[1], 960, 70, { fontSize: '42px', zIndex: 5 }); pop(e, WT(sp, p.head[0])); }
  [[p.left, 480, MUSTARD, INK, C], [p.right, 1440, '#33402f', CREAM, C]].forEach(([side, x, bgc, fg, par], k) => {
    const t = k === 0 ? WT(sp, side.at !== undefined ? side.at : 0) : WT(sp, side.at !== undefined ? side.at : 0.4);
    const grp = el('div', par, { position: 'absolute', inset: 0 });
    if (k === 1) reveal(R, t - 0.2, 'inset(0 0 100% 0)', 'inset(0 0 0% 0)');
    TL.set(grp, { autoAlpha: 0 }, 0); TL.set(grp, { autoAlpha: 1 }, t);
    const ti = text(grp, side.title, x, ty, { fontSize: '58px', color: fg }); rise(ti, t);
    if (side.prop) { const e = img(grp, side.prop, x, 540, side.w || 300); pop(e, t + 0.15); float(e, t, L.t1, 6, k); }
    if (side.person) { const e = person(grp, side.person, x, 980, side.h || 560, k); rise(e, t + 0.1); }
    if (side.guy) { const g = Guy(grp, x, 1060, 0.86, { head: side.guy.head || 'head', mouth: 'neutral' }); TL.fromTo(g.g, { y: 80, autoAlpha: 0 }, { y: 0, autoAlpha: 1, duration: 0.5, ease: 'power3.out', immediateRender: false }, t + 0.1); }
    if (side.bubble) bubble(grp, side.bubble, x, ty + 110, t + 0.5, { fontSize: '32px' });
    const mt = WT(sp, side.markAt !== undefined ? side.markAt : (side.at !== undefined ? side.at : 0)) + 0.6;
    if (side.mark === 'check') check(grp, x + 300, ty + 230, 1.7, mt, k ? '#9cc27a' : '#3f6b30');
    if (side.mark === 'cross') cross(grp, x + 300, ty + 230, 1.7, mt, k ? '#e07a52' : RUST);
    if (side.note) { const e = tag(grp, side.note, x, 870, { fontSize: '40px', background: k ? MUSTARD : CREAM }); pop(e, mt + 0.2); }
  });
  if (p.footer) { const e = tag(C, p.footer[1], 960, 880, { fontSize: '44px', background: RUST, color: CREAM, zIndex: 5 }); pop(e, WT(sp, p.footer[0])); }
  deco(L, sp, Object.assign({}, p, { title: null }));
};
T.step = (L, sp, p) => {
  if (p.guy !== false) mkGuy(L, sp, p, p.gx || 1480, 1010, p.gs || 1.0);
  deco(L, sp, Object.assign({}, p));
  const pan = el('div', L.cam, { position: 'absolute', left: 0, top: 0, width: '700px', height: '1080px', background: 'rgba(38,57,43,.95)', zIndex: 50 });
  TL.fromTo(pan, { x: -720 }, { x: 0, duration: 0.5, ease: 'power3.out', immediateRender: false }, sp.a + 0.1); TL.set(pan, { x: -720 }, 0);
  const ring = box(pan, 350, 360, { width: '300px', height: '300px', borderRadius: '50%', border: `10px solid ${MUSTARD}` });
  const n = text(pan, p.n, 350, 380, { fontSize: '230px', color: MUSTARD, fontFamily: "'Rozha One'", fontWeight: 400 });
  pop(ring, sp.a + 0.3); pop(n, sp.a + 0.45, { rot: -20 });
  const lb = text(pan, p.label, 350, 680, { fontSize: '58px', color: CREAM, whiteSpace: 'normal', width: '580px' }); rise(lb, sp.a + 0.6);
};
T.weeks = (L, sp, p) => {
  const names = ['निगरानी', 'छोटी सच्चाइयाँ', 'माँग और सीमा', 'अपनापन'];
  names.forEach((nm, k) => {
    const on = k === p.week, done = k < p.week;
    const b = box(L.cam, 330 + k * 420, 120, { width: '380px', height: '130px', borderRadius: '18px', border: `5px solid ${INK}`,
      background: on ? MUSTARD : CREAM, opacity: on ? 1 : 0.55, textAlign: 'center', fontFamily: "'Baloo 2'", fontWeight: 800, color: INK, zIndex: 40 });
    b.innerHTML = `<div style="font-size:30px;margin-top:10px;font-family:Mukta">हफ़्ता ${k + 1}</div><div style="font-size:42px;line-height:1.1">${nm}</div>`;
    TL.set(b, { autoAlpha: 0 }, 0);
    TL.fromTo(b, { y: -160, autoAlpha: 0 }, { y: 0, autoAlpha: on ? 1 : 0.55, duration: 0.45, ease: 'back.out(1.6)', immediateRender: false }, sp.a + 0.1 + k * 0.08);
    if (on) TL.fromTo(b, { scale: 1 }, { scale: 1.1, duration: 0.4, ease: 'back.out(3)', immediateRender: false }, sp.a + 0.7);
    if (done) check(L.cam, 330 + k * 420 + 150, 80, 0.9, sp.a + 0.6, '#3f6b30');
  });
  if (p.guy !== false) mkGuy(L, sp, p, p.gx || 560, 1010, p.gs || 0.88);
  deco(L, sp, p);
};
T.balance = (L, sp, p) => {
  const C = L.cam;
  if (p.title) { const e = text(C, p.title, 960, 130, { fontSize: '64px' }); rise(e, sp.a + 0.1); }
  el('div', C, { position: 'absolute', left: '948px', top: '360px', width: '24px', height: '480px', background: INK, borderRadius: '10px' });
  el('div', C, { position: 'absolute', left: '800px', top: '820px', width: '320px', height: '40px', background: INK, borderRadius: '20px 20px 6px 6px' });
  const beam = el('div', C, { position: 'absolute', left: '460px', top: '350px', width: '1000px', height: '22px', background: INK, borderRadius: '11px', transformOrigin: '50% 50%' });
  const pans = [[p.left, 0], [p.right, 1000]].map(([lab, x]) => {
    const pn = el('div', beam, { position: 'absolute', left: (x - 170) + 'px', top: '11px', width: '340px', height: '330px', transformOrigin: '50% 0%' });
    pn.innerHTML = `<svg width="340" height="200" viewBox="0 0 340 200"><path d="M170 0 L40 170 M170 0 L300 170" stroke="${INK}" stroke-width="5"/>
      <path d="M20 170 Q170 240 320 170 Z" fill="${MUSTARD}" stroke="${INK}" stroke-width="7"/></svg>`;
    const tg = tag(pn, lab, 170, 270, { fontSize: '34px', whiteSpace: 'normal', width: '330px' });
    return pn;
  });
  pop(beam, sp.a + 0.2);
  const ang = p.tiltDir === 'right' ? 10 : -10;
  if (p.tiltAt) { const t = WT(sp, p.tiltAt); TL.to(beam, { rotation: ang, duration: 0.9, ease: 'elastic.out(1,0.5)' }, t); TL.to(pans, { rotation: -ang, duration: 0.9, ease: 'elastic.out(1,0.5)' }, t); }
  if (p.balanceAt) { const t = WT(sp, p.balanceAt); TL.to(beam, { rotation: 0, duration: 0.9, ease: 'elastic.out(1,0.5)' }, t); TL.to(pans, { rotation: 0, duration: 0.9, ease: 'elastic.out(1,0.5)' }, t);
    check(C, 960, 280, 1.4, t + 0.5, '#3f6b30'); }
  deco(L, sp, Object.assign({}, p, { title: null }));
};
T.cooker = (L, sp, p) => {
  const C = L.cam;
  el('div', C, { position: 'absolute', inset: 0, background: '#33402f' });
  const ck = img(C, 'cooker', 960, 600, 430); pop(ck, sp.a + 0.1);
  const gauge = box(C, 1430, 420, { width: '220px', height: '220px', borderRadius: '50%', background: CREAM, border: `8px solid ${INK}` });
  el('div', gauge, { position: 'absolute', inset: 0, borderRadius: '50%', background: `conic-gradient(from 60deg, transparent 0deg 170deg, ${RUST} 170deg 240deg, transparent 240deg)` });
  const needle = el('div', gauge, { position: 'absolute', left: '104px', top: '30px', width: '12px', height: '80px', background: INK, borderRadius: '6px', transformOrigin: '50% 100%' });
  pop(gauge, sp.a + 0.3);
  const lbl = text(C, p.label, 960, 170, { fontSize: '60px', color: CREAM }); rise(lbl, sp.a + 0.3);
  if (p.relief) {
    TL.fromTo(needle, { rotation: 100 }, { rotation: -100, duration: 3, ease: 'power2.inOut', immediateRender: false }, sp.a + 0.8); TL.set(needle, { rotation: 100 }, 0);
    const ok = tag(C, p.sub || 'राहत', 960, 860, { fontSize: '44px', background: MUSTARD }); pop(ok, sp.a + 3.2);
    for (let k = 0; k < 5; k++) { const pf = el('div', C, { position: 'absolute', left: '935px', top: '330px', width: '60px', height: '60px', borderRadius: '50%', background: CREAM, opacity: 0 });
      TL.fromTo(pf, { y: 0, scale: 0.5, opacity: 0.6 }, { y: -260, scale: 2, opacity: 0, duration: 2.4, ease: 'sine.out', immediateRender: false }, sp.a + 1 + k * 0.7); }
  } else {
    const tf = WT(sp, p.burst);
    TL.set(needle, { rotation: -110 }, 0);
    TL.fromTo(needle, { rotation: -110 }, { rotation: 100, duration: Math.max(0.5, tf - sp.a - 0.6), ease: 'power1.in', immediateRender: false }, sp.a + 0.4);
    HOOKS.push(t => { if (t < sp.a || t > L.t1 + 1) return; const k = Math.min(1, (t - sp.a) / (tf - sp.a));
      gsap.set(ck, { x: Math.sin(t * 50) * k * k * 8, rotation: Math.sin(t * 37) * k * k * 2 }); });
    for (let k = 0; k < 9; k++) {
      const pf = el('div', C, { position: 'absolute', left: '930px', top: '330px', width: '90px', height: '90px', borderRadius: '50%', background: CREAM, opacity: 0 });
      const an = -Math.PI / 2 + (k - 4) * 0.28;
      TL.fromTo(pf, { x: 0, y: 0, scale: 0.3, opacity: 0.95 }, { x: Math.cos(an) * 520, y: Math.sin(an) * 320, scale: 2.6, opacity: 0, duration: 1.2, ease: 'power2.out', immediateRender: false }, tf + k * 0.03);
    }
    const flash = el('div', C, { position: 'absolute', inset: 0, background: CREAM, opacity: 0 });
    TL.fromTo(flash, { opacity: 0.8 }, { opacity: 0, duration: 0.4, immediateRender: false }, tf);
  }
  deco(L, sp, Object.assign({}, p, { title: null }));
};
T.gender = (L, sp, p) => {
  const ms = maleSym(L.cam, 960, 470, 260); pop(ms, sp.a + 0.2);
  const tc = WT(sp, p.crossAt); cross(L.cam, 960, 470, 3, tc);
  const ta = WT(sp, p.allAt);
  TL.to(ms, { scale: 0, autoAlpha: 0, duration: 0.4, ease: 'back.in(2)' }, ta - 0.2);
  [['w_kurta', 360], ['elder', 620], ['mother', 1300], ['m_hoodie', 1560], ['w_office', 1820]].forEach(([n, x], k) => {
    const e = person(L.cam, n, x, 1030, 600, k + 2); TL.set(e, { y: 700 }, 0);
    TL.to(e, { y: 0, duration: 0.5, ease: 'back.out(1.6)' }, ta + k * 0.12); });
  const g = Guy(L.cam, 960, 1030, 0.98); TL.set(g.g, { y: 700 }, 0); TL.to(g.g, { y: 0, duration: 0.5, ease: 'back.out(1.6)' }, ta + 0.3);
  deco(L, sp, p);
};
T.chapter = null;

// ---------------- shot list ----------------
const SHOTS = [
  // 2 — the real problem
  { k: 'असली समस्या क्या है', ch: '02' },
  { k: 'बहुत ज़रूरी भेद', t: 'big', p: { lines: [[0, 'एक ज़रूरी भेद', 130, INK], ['ग़लत मतलब', 'इसे समझे बिना → ग़लत मतलब', 54, RUST]], prop: ['magnifier', 1560, 520, 280, 0.4] } },
  { k: 'भला होना, उदार', t: 'scene', bg: 'bg_living', p: { gx: 520, tags: [['भला', 'भला होना', 1250, 260], ['उदार', 'उदार होना', 1550, 380], ['परवाह', 'परवाह करना', 1250, 500]], checks: [['भला', 1430, 250], ['उदार', 1730, 370], ['परवाह', 1430, 490]], stamp: ['ख़िलाफ़', 'ये अच्छे गुण हैं', 1400, 720, 64] } },
  { k: 'सौदा बन जाता', t: 'icon', p: { prop: 'contract', title: 'जब भलाई बन जाए…', sub: ['सौदा', 'एक सौदा'], side: [['gift', 560, 540, 220, 0.3], ['trophy_env', 1360, 540, 240, 'सौदा']] } },
  { k: 'यानी मैं आपके लिए', t: 'scene', bg: 'bg_living', p: { gx: 500, talk: true, cast: [['w_kurta', 1600, 600]], bubbles: [['कर रहा', 'मैंने तुम्हारे लिए इतना किया…', 1000, 250]], tags: [['स्वीकार', 'तो मुझे स्वीकार करो', 1050, 430], ['तारीफ़', 'मेरी तारीफ़ करो', 1050, 550], ['ज़रूरत', 'मेरी ज़रूरत पूरी करो', 1050, 670]] } },
  { k: 'कभी कहा नहीं', t: 'icon', p: { prop: 'contract', title: 'और यह सौदा…', stamp: ['कहा', 'कभी कहा नहीं जाता', 960, 560, 80] } },
  { k: 'छिपा हुआ अनुबंध कहते', t: 'big', p: { bgc: INK, lines: [[0, 'छिपा हुआ', 110, MUSTARD], [0.5, 'अनुबंध', 170, CREAM], ['केंद्र', '— पूरी किताब का केंद्र', 50, MUSTARD]], prop: ['contract', 1550, 500, 300, 0.3] } },
  { k: 'तीन ख़ासियतें', t: 'list', p: { title: 'छिपे अनुबंध की 3 ख़ासियतें', items: [['पहली', 'सामने वाले को पता ही नहीं', 'contract'], ['दूसरी', 'आहत और नाराज़', 'cloud'], ['तीसरी', 'ताने, चुप्पी, विस्फोट', 'cooker']] } },
  { k: 'हैरान रह जाते', t: 'scene', bg: 'bg_living', p: { gx: 1350, head: 'head_angry', cast: [['w_kurta', 480, 590], ['elder', 780, 610]], texts: [['हैरान', '?', 480, 330, 140, RUST], ['हैरान', '?', 780, 310, 140, RUST]] } },
  { k: 'कोई समझौता हुआ ही नहीं', t: 'icon', p: { prop: 'contract', title: 'उनकी नज़र में…', crosses: [['समझौता', 960, 490]], sub: ['नहीं था', 'कोई समझौता हुआ ही नहीं'] } },
  // 3 — how the pattern forms
  { k: 'यह पैटर्न बनता कैसे है', ch: '03' },
  { k: 'जड़ बचपन', t: 'scene', bg: 'bg_childhome', p: { guy: false, cast: [['kid', 1300, 400]], title: [0, 'जड़: बचपन'], props: [['sprout', 800, 760, 200, 'जड़']] } },
  { k: 'पूरी तरह अपने बड़ों पर', t: 'scene', bg: 'bg_childhome', p: { guy: false, cast: [['mother', 560, 620], ['kid', 960, 390], ['elder', 1360, 630]], tags: [['निर्भर', 'पूरी तरह निर्भर', 960, 300]], texts: [['स्वीकार', '♥', 960, 470, 150, RUST]], title: ['सबसे बड़ी', 'सबसे बड़ी ज़रूरत: स्वीकृति'] } },
  { k: 'अगर घर में उसे', t: 'list', p: { title: 'अगर घर में…', items: [['डाँट', 'ज़रूरत बताई → डाँट', 'cloud'], ['भावनाओं', 'भावनाओं को महत्व नहीं', 'mirror'], ['प्यार', 'प्यार तभी, जब उपयोगी', 'trophy_env']], end: ['निष्कर्ष', '…तो बच्चा एक निष्कर्ष निकालता है'] } },
  { k: 'मैं जैसा हूँ वैसा', t: 'scene', bg: 'bg_childhome', p: { guy: false, cast: [['kid', 760, 400]], thought: [[0, 'मैं जैसा हूँ, वैसा काफ़ी नहीं…', 1250, 300]], props: [['mask', 772, 655, 96, 'बनना पड़ेगा']], tags: [['बनना पड़ेगा', 'जो दूसरों को चाहिए, वही बनूँगा', 1250, 520]] } },
  { k: 'बुद्धिमानी', t: 'icon', p: { prop: 'shield', title: 'उस समय यह बुद्धिमानी थी', sub: ['सुरक्षा', 'इससे सुरक्षा मिली'], checks: [['सुरक्षा', 1250, 470]] } },
  { k: 'बड़े होने के बाद भी', t: 'compare', p: { left: { title: 'बचपन में', person: 'kid', h: 420, mark: 'check' }, right: { title: 'आज भी वही रणनीति', guy: { head: 'head_tired' }, at: 'बड़े होने', mark: 'cross', markAt: 'ज़रूरत नहीं', note: 'अब ज़रूरत नहीं' } } },
  { k: 'दो चीज़ें सीख', t: 'list', p: { title: 'व्यक्ति दो चीज़ें सीख लेता है', items: [['ज़रूरतें छिपाना', 'अपनी ज़रूरतें छिपाना', 'chest'], ['कमियों', 'अपनी कमियाँ छिपाना', 'mask']] } },
  { k: 'सबसे बड़ा विरोधाभास', t: 'big', p: { bgc: INK, lines: [[0, 'सबसे बड़ा विरोधाभास', 80, MUSTARD], ['जान ही', 'जिसे कोई जान ही नहीं पाता', 66, CREAM], ['स्वीकार', 'उसे कोई स्वीकार भी नहीं कर सकता', 66, '#e07a52']], prop: ['mirror', 1650, 540, 190, 'जान ही'] } },
  // 4 — signs
  { k: 'पहचानने के संकेत', ch: '04' },
  { k: 'व्यवहार गिनाते', t: 'icon', p: { prop: 'magnifier', x: 760, title: 'पहचानने के संकेत', texts: [[1.0, '8', 1250, 480, 300, RUST]], sub: ['पहचाना', 'ये व्यवहार दिखें, तो ध्यान दें'] } },
  { k: 'शायद ही कभी मना', t: 'scene', bg: 'bg_office', p: { badge: 'संकेत 1/8', gx: 560, cast: [['boss', 1550, 700]], bubbles: [[0.2, 'ये काम भी कर दोगे?', 1500, 250], ['मना', 'जी, हो जाएगा!', 980, 330]], props: [['sack', 900, 700, 170, 'मना']], heads: [['अपराधबोध', 'head_tired']], texts: [['अपराधबोध', 'अपराधबोध', 980, 470, 50, RUST]] } },
  { k: 'असली राय छिपाकर', t: 'scene', bg: 'bg_cafe', p: { badge: 'संकेत 2/8', gx: 560, cast: [['friend', 1450, 640]], bubbles: [[0.2, 'कैसी लगी फ़िल्म?', 1450, 250], ['सुनना चाहता', 'बहुत बढ़िया!', 950, 360]], thought: [['असली राय', '(असल में: बिलकुल पसंद नहीं)', 760, 140]] } },
  { k: 'टकराव से हर क़ीमत', t: 'scene', bg: 'bg_night', p: { badge: 'संकेत 3/8', gx: 1450, head: 'head_tired', tags: [[0.3, 'टकराव? नहीं!', 600, 220]], loop: ['दोहराते', 650, 560, ['काश कह देता…', 'उसने ऐसा क्यों कहा?', 'अब क्या करूँ?']] } },
  { k: 'किसी ने सराहा नहीं', t: 'scene', bg: 'bg_living', p: { badge: 'संकेत 4/8', gx: 520, head: 'head_tired', props: [['sack', 850, 760, 170, 0.2], ['gift', 1060, 820, 140, 0.5], ['journal', 1250, 800, 150, 0.8]], tags: [['बहुत कुछ', 'बहुत कुछ किया…', 1050, 300]], texts: [['सराहा', '…पर किसी ने सराहा नहीं', 1200, 470, 60, RUST]] } },
  { k: 'अपनी ग़लतियाँ छिपाते', t: 'icon', p: { badge: 'संकेत 5/8', prop: 'chest', title: 'ग़लतियाँ छिपाना', sub: ['छोटी', 'छोटी-छोटी भी'], side: [['note', 560, 470, 170, 0.4, { x: 380, y: 40, at: 1.4 }], ['note', 1360, 520, 150, 'छोटी', { x: -380, y: 0, at: 'छोटी' }]] } },
  { k: 'बिना माँगे मदद', t: 'scene', bg: 'bg_cafe', p: { badge: 'संकेत 6/8', gx: 520, cast: [['friend', 1450, 640]], props: [['gift', 850, 720, 160, 0.3, { x: 420, at: 1.0 }]], thought: [['उम्मीद', '…अब बदले में कुछ मिलेगा?', 760, 140]], tags: [[0.2, 'बिना माँगे मदद', 1450, 250]] } },
  { k: 'शिकायत सीधे नहीं', t: 'scene', bg: 'bg_living', p: { badge: 'संकेत 7/8', gx: 520, talk: true, cast: [['w_kurta', 1450, 590]], bubbles: [[0.2, 'हाँ हाँ, सब तो मैं ही करता हूँ…', 1000, 260]], texts: [['इशारों', '?', 1450, 330, 140, RUST]] } },
  { k: 'और सबसे बड़ा संकेत', t: 'cooker', p: { badge: 'संकेत 8/8', label: 'बिना पते का गुस्सा', burst: 'छोटी बात' } },
  { k: 'चरित्र की कमी नहीं', t: 'big', p: { lines: [[0, 'यह चरित्र की कमी नहीं', 100, INK], ['सीखी', 'यह एक सीखी हुई रणनीति है', 66, OLIVE], ['बदली', 'और सीखी चीज़ बदली जा सकती है', 66, RUST]], prop: ['sprout', 1620, 600, 230, 'बदली'] } },
  // 5 — first change: self-approval
  { k: 'पहला बदलाव, अपनी स्वीकृति', ch: '05' },
  { k: 'पहला सुझाव सबसे', t: 'scene', bg: 'bg_park', p: { gx: 960, gs: 1.0, cast: [['w_office', 380, 560], ['elder', 620, 580], ['m_hoodie', 1320, 580], ['mother', 1560, 570]], texts: [[0.3, '♥', 380, 380, 90], [0.45, '♥', 620, 360, 90], [0.6, '♥', 1320, 360, 90], [0.75, '♥', 1560, 380, 90]], stamp: ['बंद', 'बाहर से स्वीकृति माँगना बंद', 960, 260, 70] } },
  { k: 'परवाह नहीं करनी', t: 'icon', p: { title: 'इसका मतलब यह नहीं…', texts: [[0.2, '♥', 960, 470, 280]], sub: ['परवाह', 'परवाह करना ठीक है'], checks: [['परवाह', 1220, 400]] } },
  { k: 'आपकी क़ीमत', t: 'balance', p: { title: 'आपकी क़ीमत किस पर टिकी है?', left: 'आपकी अपनी नज़र', right: 'दूसरों की प्रतिक्रिया', tiltAt: 'टिकी न' } },
  { k: 'ठोस अभ्यास', t: 'big', p: { lines: [[0, '3 ठोस अभ्यास', 140, INK]], prop: ['journal', 1500, 540, 320, 0.3] } },
  { k: 'पहला, अपने बारे में', t: 'step', bg: 'bg_night', p: { n: '1', label: 'छिपाई बातें लिखिए', gx: 1550, props: [['journal', 1080, 760, 260, 'लिखिए']], thought: [[0.6, 'मैं क्या छिपाता हूँ?', 1100, 300]] } },
  { k: 'भरोसेमंद व्यक्ति को उनमें', t: 'scene', bg: 'bg_cafe', p: { gx: 560, talk: true, cast: [['friend', 1400, 640]], bubbles: [[0.2, 'एक बात बताऊँ…?', 950, 330]] } },
  { k: 'सबसे तेज़ी से काम', t: 'icon', p: { prop: 'chest', x: 700, title: 'सबसे तेज़ असर', texts: [['सबूत', 'हर छिपी बात = एक "सबूत"', 960, 800, 54, RUST]], side: [['chain', 1350, 500, 320, 'सबूत']], crosses: [['स्वीकार्य', 1350, 500]] } },
  { k: 'दूसरा, दिन में एक बार', t: 'step', bg: 'bg_meeting', p: { n: '2', label: 'रोज़ एक बार असली राय', gx: 1350, talk: true, cast: [['w_office', 1760, 560]], bubbles: [['अलग है', 'मेरी राय थोड़ी अलग है', 1000, 300]] } },
  { k: 'तीसरा, तारीफ़', t: 'step', bg: 'bg_office', p: { n: '3', label: 'तारीफ़ सीधे स्वीकारिए', gx: 1250, cast: [['w_office', 1720, 560]], bubbles: [['तारीफ़', 'बहुत बढ़िया काम!', 1650, 230], ['धन्यवाद', 'धन्यवाद!', 920, 330]], talk: 'धन्यवाद' } },
  { k: 'इसे टालना विनम्रता', t: 'compare', p: { left: { title: 'टालना', bubble: 'अरे, कुछ नहीं था…', guy: { head: 'head_tired' }, mark: 'cross' }, right: { title: 'स्वीकारना', bubble: 'धन्यवाद!', guy: { head: 'head_calm' }, at: 0.4, mark: 'check' }, footer: ['असुरक्षा', 'टालना = असुरक्षा, विनम्रता नहीं'] } },
  // 6 — second change: state your needs
  { k: 'दूसरा बदलाव, अपनी ज़रूरतें', ch: '06' },
  { k: 'सबसे व्यावहारिक सलाह', t: 'big', p: { bgc: MUSTARD, lines: [[0, 'सबसे व्यावहारिक', 100, INK], [0.5, 'सलाह', 160, RUST]], prop: ['note', 1550, 520, 260, 0.4] } },
  { k: 'अपने आप पता चल जाता', t: 'scene', bg: 'bg_living', p: { gx: 520, head: 'head_tired', cast: [['w_kurta', 1450, 590]], thought: [[0.3, 'अगर सच में परवाह होती, तो ख़ुद समझ जाती…', 860, 140]], texts: [['अपने आप', '?', 1450, 330, 140, RUST]] } },
  { k: 'हर रिश्ते को नुक़सान', t: 'icon', p: { title: 'लोग मन नहीं पढ़ सकते', prop: 'head', w: 260, crosses: [['मन नहीं', 1180, 400]], texts: [[0.3, '?', 680, 420, 160, RUST], [0.6, '?', 1260, 640, 120, RUST]], sub: ['नुक़सान', 'रिश्तों को नुक़सान'] } },
  { k: 'तीन क़दमों', t: 'big', p: { lines: [[0, 'इलाज: 3 क़दम', 140, INK]], prop: ['sprout', 1550, 560, 230, 0.3] } },
  { k: 'पहला, अपनी ज़रूरत पहचानिए', t: 'step', bg: 'bg_night', p: { n: '1', label: 'अपनी ज़रूरत पहचानिए', gx: 1580, head: 'head_tired', props: [['journal', 1080, 780, 240, 'लिखना'], ['calendar', 1180, 470, 200, 'हफ़्ते']], tags: [['दबा रहे', 'बरसों से दबी ज़रूरतें', 1150, 250]], bubbles: [['कमी लगी', 'आज किस चीज़ की कमी लगी?', 1150, 140]] } },
  { k: 'दूसरा, उसे साफ़', t: 'compare', p: { head: [0, 'साफ़ और छोटे शब्दों में माँगिए'], left: { title: 'शिकायत', bubble: 'तुम मेरा ध्यान नहीं रखते', guy: { head: 'head_angry' }, at: 'शिकायत', mark: 'cross', markAt: 'शिकायत' }, right: { title: 'माँग', bubble: 'आज शाम आधा घंटा साथ बैठोगे?', guy: { head: 'head_calm' }, at: 'आधा घंटा', mark: 'check', markAt: 'माँग है' } } },
  { k: 'तीसरा, ना सुनने', t: 'scene', bg: 'bg_living', p: { gx: 480, cast: [['w_kurta', 1550, 590]], bubbles: [[0.3, 'आज नहीं हो पाएगा', 1500, 250]], heads: [['कठिन', 'head_tired']], texts: [['कठिन', 'सबसे कठिन हिस्सा', 1000, 160, 56, RUST]], loop: ['पुराना चक्र', 1010, 560, ['माँगना बंद', 'चुप्पी', 'नाराज़गी']] } },
  // 7 — third change: boundaries
  { k: 'तीसरा बदलाव, सीमाएँ', ch: '07' },
  { k: 'सीमा का मतलब दीवार नहीं', t: 'compare', p: { left: { title: 'दीवार', prop: 'chain', w: 340, mark: 'cross' }, right: { title: 'सीमा', prop: 'fence', w: 380, at: 'साफ़ होना', mark: 'check' }, footer: ['स्वीकार', 'क्या करेंगे · क्या नहीं · क्या स्वीकार करेंगे'] } },
  { k: 'कोई सीमा नहीं होती', t: 'scene', bg: 'bg_office', p: { gx: 960, head: 'head_tired', cast: [['boss', 400, 700], ['w_office', 1500, 560], ['m_hoodie', 1740, 580]], props: [['sack', 740, 720, 140, 1.0], ['sack', 1180, 740, 140, 2.0], ['note', 1250, 420, 110, 3.0], ['sack', 960, 860, 160, 4.0]], tags: [['नीयत', 'नीयत ख़राब होना ज़रूरी नहीं', 960, 140], ['लेते जाते', 'लोग बस लेते जाते हैं', 1500, 260]] } },
  { k: 'सीमा बनाने के लिए तीन', t: 'big', p: { lines: [[0, 'सीमा बनाने के 3 तरीक़े', 110, INK]], prop: ['fence', 1560, 600, 320, 0.3] } },
  { k: 'पहली, तुरंत हाँ', t: 'step', bg: 'bg_office', p: { n: '1', label: 'तुरंत हाँ मत कहिए', gx: 1300, talk: 'देखकर बताता', cast: [['boss', 1760, 700]], bubbles: [['देखकर बताता', 'मैं देखकर बताता हूँ', 950, 300]], tags: [['डर के बजाय', 'डर नहीं, सोच से जवाब', 1100, 520]] } },
  { k: 'लंबी सफ़ाई', t: 'step', bg: 'bg_living', p: { n: '2', label: 'लंबी सफ़ाई मत दीजिए', gx: 1300, talk: 'लंबी सफ़ाई', cast: [['w_kurta', 1760, 590]], bubbles: [[0.4, 'नहीं, इस बार नहीं।', 950, 300]], texts: [['दरवाज़ा', 'हर सफ़ाई = अगली बहस का दरवाज़ा', 1250, 140, 44, RUST]] } },
  { k: 'सीमा तय करने के बाद', t: 'step', bg: 'bg_park', p: { n: '3', label: 'सीमा निभाइए', guy: false, props: [['fence', 1300, 700, 440, 0.3]], crosses: [['तोड़ी', 1300, 640]], texts: [['बुरी', 'टूटी सीमा, सीमा न होने से भी बुरी', 1300, 280, 46, RUST]] } },
  { k: 'स्पष्टता से', t: 'compare', p: { left: { title: 'नाराज़गी से', guy: { head: 'head_angry' }, mark: 'cross', note: '= लड़ाई', markAt: 'लड़ाई' }, right: { title: 'स्पष्टता से', guy: { head: 'head_calm' }, at: 'स्पष्टता', mark: 'check', note: '= सीमा' } } },
  // 8 — fourth change: feelings
  { k: 'चौथा बदलाव, भावनाओं', ch: '08' },
  { k: 'भावनाओं से कट', t: 'scene', bg: 'bg_night', p: { gx: 960, head: 'head_tired', props: [['chain', 960, 600, 520, 'कट']], tags: [['गुस्से', 'ख़ास तौर पर गुस्से से', 960, 130], ['दूर होते', 'गुस्सा दिखाया = लोग दूर', 1500, 300]] } },
  { k: 'दबाई हुई भावना ग़ायब', t: 'list', p: { title: 'दबी भावना ग़ायब नहीं होती, वह जाती है…', items: [['शरीर', 'शरीर में', 'dumbbell'], ['चुप्पी', 'चुप्पी में', 'chest'], ['तानों', 'तानों में', 'cloud'], ['विस्फोट', 'विस्फोट में', 'cooker']] } },
  { k: 'नाम देना सीखिए', t: 'scene', bg: 'bg_night', p: { gx: 1480, head: 'head_calm', props: [['journal', 760, 780, 300, 0.3]], tags: [['नाम', 'भावना को नाम दीजिए', 760, 230], ['नाप-तौल', 'उसी समय, नाप-तौलकर', 760, 350]], texts: [['तीन बार', 'दिन में 3 बार: "अभी मैं क्या महसूस कर रहा हूँ?"', 860, 520, 36, RUST]] } },
  { k: 'गुस्से के बारे में', t: 'big', p: { bgc: INK, lines: [[0, 'गुस्सा बुरा नहीं', 110, CREAM], ['संकेत', 'वह एक संकेत है', 80, MUSTARD], ['सीमा', 'कि कोई सीमा लाँघी गई', 64, '#e07a52']], prop: ['fence', 1600, 640, 280, 'सीमा'] } },
  { k: 'कभी महसूस नहीं होने', t: 'scene', bg: 'bg_park', p: { gx: 600, head: 'head_tired', props: [['fence', 1300, 790, 380, 0.2], ['shield', 1300, 470, 180, 'रक्षा']], crosses: [['रक्षा', 1300, 470]], tags: [[0.3, 'गुस्सा दबाया = सीमा असुरक्षित', 1250, 200]] } },
  // 9 — giving vs caretaking
  { k: 'देना और देखभाल में', ch: '09' },
  { k: 'बहुत काम का है', t: 'compare', p: { left: { title: 'देना', prop: 'gift' }, right: { title: 'बोझ उठा लेना', prop: 'sack', at: 'बोझ' } } },
  { k: 'देना वह है', t: 'scene', bg: 'bg_park', p: { gx: 640, head: 'head_calm', cast: [['friend', 1450, 640]], props: [['gift', 980, 730, 170, 0.4, { x: 280, at: 1.4 }]], tags: [['हल्के', 'हल्का महसूस ✓', 640, 140]], texts: [['करना चाहते', 'क्योंकि आप करना चाहते हैं', 1100, 300, 44, OLIVE]] } },
  { k: 'बोझ उठा लेना वह', t: 'scene', bg: 'bg_office', p: { gx: 960, head: 'head_tired', props: [['sack', 960, 160, 240, 0.5]], cast: [['m_hoodie', 1550, 580]], tags: [['बिना माँगे', 'बिना माँगे', 460, 330], ['थके', 'थके + नाराज़', 460, 460]] } },
  { k: 'सादा कसौटी', t: 'big', p: { lines: [[0, 'एक सादी कसौटी', 110, INK], ['भीतर देखिए', 'काम के बाद, भीतर देखिए', 70, OLIVE]], prop: ['mirror', 1600, 540, 210, 0.4] } },
  { k: 'अगर संतोष है', t: 'compare', p: { left: { title: 'संतोष', guy: { head: 'head_calm' }, mark: 'check', note: '= देना' }, right: { title: 'हल्की नाराज़गी', guy: { head: 'head_tired' }, at: 'नाराज़गी', mark: 'cross', note: '= छिपा सौदा', markAt: 'कुछ करना' } } },
  { k: 'सामने वाला कमज़ोर', t: 'scene', bg: 'bg_living', p: { gx: 520, head: 'head_tired', cast: [['m_hoodie', 1500, 560]], props: [['sack', 900, 760, 150, 0.3]], tags: [['कमज़ोर', 'सामने वाला कमज़ोर होता है', 1150, 220], ['सीखने', 'वह सीख ही नहीं पाता', 1150, 340]], bubbles: [['कोई कुछ नहीं', 'यहाँ कोई कुछ नहीं करता!', 900, 480]] } },
  { k: 'मदद करने से पहले पूछि', t: 'scene', bg: 'bg_cafe', p: { gx: 520, talk: true, cast: [['friend', 1450, 640]], bubbles: [['मदद चाहिए', 'मदद चाहिए, या बस बताना था?', 1000, 230], ['किस तरह', 'किस तरह की मदद?', 1000, 370]] } },
  { k: 'नियंत्रण', t: 'big', p: { bgc: INK, lines: [[0, 'बिना पूछे मदद', 110, CREAM], ['नियंत्रण', '= नियंत्रण', 140, '#e07a52']], prop: ['chain', 1560, 540, 320, 'नियंत्रण'] } },
  // 10 — relapse
  { k: 'जब पुराना पैटर्न वापस', ch: '10' },
  { k: 'हार मानते', t: 'icon', p: { title: 'यहीं ज़्यादातर लोग हार मानते हैं', prop: 'calendar', w: 340 } },
  { k: 'कुछ हफ़्तों तक', t: 'scene', bg: 'bg_living', p: { gx: 560, head: 'head_calm', heads: [['पूरी ताक़त', 'head_tired']], cast: [['w_kurta', 1500, 590]], props: [['cloud', 1500, 260, 240, 'नाराज़']], tags: [['बेहतर', 'कुछ हफ़्ते: सब बेहतर ✓', 1000, 150], ['पूरी ताक़त', 'पुराना व्यवहार लौट आया', 1000, 420]], bubbles: [['माफ़ी', 'हाँ… सॉरी… ठीक है…', 960, 290]] } },
  { k: 'सामान्य हिस्सा', t: 'big', p: { lines: [[0, 'यह प्रक्रिया का', 80, OLIVE], [0.4, 'सामान्य हिस्सा है', 110, INK], ['बरसों', 'बरसों में बना, हफ़्तों में नहीं मिटेगा', 54, RUST]], prop: ['sprout', 1620, 620, 220, 0.3] } },
  { k: 'पुराने रास्ते कमज़ोर', t: 'scene', bg: 'bg_park', p: { guy: false, tags: [['मिटते नहीं', 'पुराने रास्ते: कमज़ोर पड़ते हैं, मिटते नहीं', 960, 200], ['दबाव', 'दबाव में फिर सक्रिय', 960, 330]] } },
  { k: 'तीन चीज़ें काम आती', t: 'big', p: { lines: [[0, 'ऐसे समय: 3 उपाय', 120, INK]], prop: ['shield', 1600, 540, 240, 0.3] } },
  { k: 'पहली, बाद में लौटना', t: 'step', bg: 'bg_living', p: { n: '1', label: 'बाद में लौटिए', gx: 1450, talk: 'मैंने कल जो', cast: [['w_kurta', 1820, 590]], bubbles: [['मैंने कल', 'कल की बात पर मैंने सोचा…', 1050, 240]], texts: [['गिनता', 'देर से सुधार भी गिनता है ✓', 1150, 600, 42, RUST]], props: [['calendar', 1000, 440, 150, 'कुछ घंटे']] } },
  { k: 'शर्मिंदगी को बढ़ने', t: 'step', bg: 'bg_night', p: { n: '2', label: 'शर्मिंदगी मत बढ़ाइए', gx: 1580, head: 'head_tired', heads: [['कोसता', 'head_angry']], loop: ['कोसता', 1100, 470, ['फिसलन', 'ख़ुद को कोसना', 'शर्म']] } },
  { k: 'अपने संकेत पहचानिए', t: 'step', bg: 'bg_meeting', p: { n: '3', label: 'अपने संकेत पहचानिए', guy: false, cast: [['boss', 1050, 680], ['mother', 1400, 580], ['elder', 1720, 600]], props: [['magnifier', 1350, 430, 260, 'ख़ास लोगों']], texts: [['आधी तैयारी', 'पहले से जानना = आधी तैयारी', 1300, 140, 46, RUST]] } },
  // 11 — fifth change: build your own life
  { k: 'पाँचवाँ बदलाव', ch: '11' },
  { k: 'एक और बात पर ज़ोर', t: 'scene', bg: 'bg_living', p: { gx: 960, head: 'head_tired', cast: [['w_kurta', 460, 590], ['mother', 1460, 580], ['boss', 1720, 690]], tags: [['दूसरों के इर्द', 'पूरी ज़िंदगी दूसरों के इर्द-गिर्द', 960, 130], ['बोझ', 'हर रिश्ते पर ज़्यादा बोझ', 960, 250]] } },
  { k: 'सिर्फ़ आपका हो', t: 'big', p: { lines: [[0, 'कुछ ऐसा', 90, OLIVE], [0.4, 'जो सिर्फ़ आपका हो', 110, INK]], prop: ['sprout', 1620, 600, 240, 0.3] } },
  { k: 'कोई काम या लक्ष्य', t: 'list', p: { title: 'अपनी ज़िंदगी के 4 खंभे', items: [['लक्ष्य', 'काम या लक्ष्य', 'trophy_env'], ['दोस्त', 'सच्चे दोस्त', 'friend'], ['शरीर', 'शरीर की देखभाल', 'dumbbell'], ['आनंद', 'अपना आनंद', 'guitar']], end: ['साधारण', 'पहचान किसी एक की स्वीकृति पर न टिके'] } },
  // 12 — apology & honesty
  { k: 'माफ़ी और ईमानदारी', ch: '12' },
  { k: 'एक आख़िरी छोटी बात', t: 'big', p: { lines: [[0, 'माफ़ी', 150, INK], ['अतियों', 'दो अतियों के बीच झूलना', 64, RUST]], prop: ['scale_stand', 1600, 560, 240, 0.3] } },
  { k: 'हर बात के लिए माफ़ी', t: 'compare', p: { left: { title: 'हर बात पर माफ़ी', guy: { head: 'head_tired' }, bubble: 'सॉरी… सॉरी…', mark: 'cross', markAt: 'दोनों' }, right: { title: 'कभी माफ़ी नहीं', guy: { head: 'head_angry' }, at: 'बिलकुल', bubble: 'मैं क्यों माफ़ी माँगूँ?', mark: 'cross', markAt: 'दोनों' }, footer: ['दोनों', 'दोनों ही ग़लत'] } },
  { k: 'बेवजह की माफ़ी', t: 'balance', p: { title: 'सही रास्ता बीच में', left: 'बेवजह माफ़ी: क़ीमत घटती है', right: 'माफ़ी न माँगना: रिश्ते टूटते हैं', tiltAt: 'तोड़ता', tiltDir: 'right', balanceAt: 'बीच में' } },
  { k: 'साफ़ मानिए', t: 'scene', bg: 'bg_living', p: { gx: 560, talk: true, cast: [['w_kurta', 1500, 590]], bubbles: [['मानिए', 'ग़लती मेरी थी। आगे से…', 1000, 250]], tags: [['बहाने', 'बिना बहाने', 1050, 420], ['अलग होगा', 'आगे क्या अलग होगा', 1050, 540]] } },
  { k: 'माहौल हल्का', t: 'icon', p: { title: 'ग़लती नहीं? तो बेवजह माफ़ी नहीं', prop: 'note', w: 300, texts: [['महत्व नहीं', 'बेवजह माफ़ी = "मेरी बात का कोई महत्व नहीं"', 960, 800, 44, RUST]], crosses: [['माहौल', 960, 480]] } },
  { k: 'एक सादा जाँच', t: 'compare', p: { head: [0, 'माफ़ी से पहले पूछिए'], left: { title: 'सच में ग़लती की?', prop: 'mirror', w: 200, mark: 'check', note: '→ माफ़ी', at: 'सचमुच' }, right: { title: 'बस असहजता मिटानी है?', prop: 'cloud', at: 'असहजता', mark: 'cross', note: '→ बातचीत', markAt: 'बातचीत' } } },
  // 13 — at work
  { k: 'काम की जगह पर यही', ch: '13' },
  { k: 'निजी रिश्तों पर बात', t: 'scene', bg: 'bg_office', p: { gx: 960, cast: [['boss', 480, 700], ['w_office', 1460, 560]], tags: [['महँगा', 'दफ़्तर में यह पैटर्न महँगा पड़ता है', 960, 130]] } },
  { k: 'पहला रूप, हर काम', t: 'step', bg: 'bg_office', p: { n: '1', label: 'हर काम के लिए हाँ', gx: 1550, head: 'head_tired', props: [['note', 1000, 320, 120, 0.5], ['note', 1060, 450, 120, 1.0], ['note', 990, 580, 120, 1.5], ['sack', 1150, 760, 180, 2.0], ['note', 1220, 360, 110, 2.5]], texts: [['पिछड़ने', 'मुख्य काम पिछड़ा', 1150, 140, 48, RUST], ['पता भी नहीं', 'किसी को पता भी नहीं', 1150, 900, 40, OLIVE]] } },
  { k: 'दूसरा रूप, श्रेय', t: 'step', bg: 'bg_meeting', p: { n: '2', label: 'श्रेय न माँगना', gx: 1560, props: [['trophy_env', 1100, 500, 260, 0.4]], crosses: [['ऐसा नहीं', 1100, 500]], thought: [['अपने आप', 'अच्छा काम ख़ुद दिख जाएगा…', 1150, 180]], texts: [['दिखावा', 'काम बताना = जानकारी, दिखावा नहीं', 1200, 860, 38, RUST]] } },
  { k: 'तीसरा रूप, असहमति', t: 'step', bg: 'bg_meeting', p: { n: '3', label: 'असहमति छिपाना', gx: 1150, cast: [['boss', 1560, 700], ['w_office', 1800, 560]], thought: [['चुप', '(बैठक में चुप…)', 1150, 140]], bubbles: [['आलोचना', 'वो फ़ैसला ग़लत था!', 960, 300]] } },
  { k: 'चौथा रूप, वेतन', t: 'step', bg: 'bg_office', p: { n: '4', label: 'वेतन या पद की बात न उठाना', gx: 1560, props: [['trophy_env', 1060, 480, 240, 0.4]], thought: [['उम्मीद', 'कोई दिन ख़ुद देगा…', 1150, 180]], texts: [['छिपा हुआ सौदा', '= वही छिपा सौदा', 1100, 800, 52, RUST]] } },
  { k: 'इन सबका इलाज वही', t: 'list', p: { title: 'इलाज वही है', items: [['सीमा साफ़', 'सीमा साफ़', 'fence'], ['माँग साफ़', 'माँग साफ़', 'note'], ['असहमति', 'असहमति उसी समय, उसी जगह', 'shield']] } },
  // 14 — limits of the book
  { k: 'जहाँ यह किताब सीमित', ch: '14' },
  { k: 'ईमानदार सारांश', t: 'big', p: { lines: [[0, 'किताब की 3 सीमाएँ', 120, INK]], prop: ['book', 1600, 540, 260, 0.3] } },
  { k: 'लिंग-केंद्रित', t: 'gender', bg: 'bg_paper', p: { crossAt: 'टिकता', allAt: 'किसी के भी', tags: [[0.3, 'बहुत लिंग-केंद्रित ढाँचा', 960, 120]] } },
  { k: 'ज़्यादा गंभीर', t: 'scene', bg: 'bg_night', p: { guy: false, props: [['phone', 960, 520, 260, 0.2]], texts: [[0.6, '!', 1150, 360, 180, RUST]], tags: [[0.3, 'दूसरी — ज़्यादा गंभीर', 960, 140]] } },
  { k: 'इंटरनेट पर', t: 'scene', bg: 'bg_night', p: { guy: false, props: [['phone', 620, 540, 260, 0.1]], tags: [['भला होना बेकार', '"भला होना बेकार है"', 1250, 330], ['कमज़ोरी', '"परवाह = कमज़ोरी"', 1250, 470]], stamp: ['उलटा', 'किताब का उलटा', 1250, 700, 70] } },
  { k: 'दयालु मत बनिए', t: 'big', p: { bgc: MUSTARD, lines: [[0, '"दयालु मत बनिए" — नहीं!', 70, OLIVE], ['ईमानदार', 'ईमानदार बनिए', 130, INK], ['बिना छिपे', 'दीजिए बिना सौदे के · माँगिए साफ़', 50, RUST]], prop: ['gift', 1620, 560, 230, 'ईमानदार'] } },
  { k: 'जिन जड़ों की बात', t: 'scene', bg: 'bg_clinic', p: { guy: false, cast: [['m_hoodie', 760, 580], ['psych', 1160, 640]], tags: [['जड़ों', 'बचपन के अनुभव · गहरी शर्म', 960, 130], ['अवसाद', 'अवसाद · चिंता · दुर्व्यवहार', 960, 250], ['मदद लेना', 'योग्य विशेषज्ञ से मदद लें ✓', 1450, 400]] } },
  // 15 — Indian context
  { k: 'भारतीय संदर्भ में', ch: '15' },
  { k: 'जोड़ लेना ज़रूरी', t: 'scene', bg: 'bg_living', p: { guy: false, cast: [['mother', 420, 580], ['elder', 700, 610], ['w_kurta', 1020, 590], ['kid', 1260, 400], ['friend', 1520, 630]], tags: [[0.3, 'भारतीय संदर्भ', 960, 130]] } },
  { k: 'परिवार और समाज की अपेक्षाएँ', t: 'scene', bg: 'bg_living', p: { gx: 960, gs: 0.95, head: 'head_tired', cast: [['mother', 380, 580], ['elder', 620, 610], ['boss', 1320, 690], ['w_kurta', 1560, 590]], texts: [[0.5, '!', 380, 350, 110, RUST], [0.7, '!', 620, 330, 110, RUST], [0.9, '!', 1320, 270, 110, RUST], [1.1, '!', 1560, 350, 110, RUST]], tags: [['धीरे-धीरे', 'धीरे-धीरे · छोटी बातों से · नरम भाषा में', 960, 130]], heads: [['धीरे-धीरे', 'head_calm']] } },
  { k: 'त्याग को बहुत ऊँचा', t: 'compare', p: { head: [0, 'त्याग बनाम छिपा सौदा'], left: { title: 'बिना उम्मीद का त्याग', prop: 'gift', w: 260, at: 0.3, mark: 'check', note: '= उदारता' }, right: { title: 'उम्मीद वाला त्याग', prop: 'contract', w: 260, at: 'इस उम्मीद', mark: 'cross', note: '= शिकायत' } } },
  { k: 'भावनाओं पर बात करना', t: 'scene', bg: 'bg_cafe', p: { gx: 560, head: 'head_calm', cast: [['friend', 1450, 640]], tags: [['पुरुषों', 'भावनाओं पर बात: अब भी कम आम', 960, 130]], bubbles: [['भरोसेमंद', 'यार, एक बात कहूँ?', 960, 320]], texts: [['कठिन', 'ज़रूरी भी, कठिन भी', 1450, 260, 44, RUST]] } },
  // 16 — 30-day plan
  { k: 'तीस दिन का ख़ाका', ch: '16' },
  { k: 'पहला हफ़्ता, निगरानी', t: 'weeks', p: { week: 0, gx: 1500, props: [['journal', 700, 640, 280, 'एक पंक्ति']], tags: [['बदलिए मत', 'कुछ बदलिए मत', 700, 400], ['किन लोगों', 'किन लोगों, किन हालात में?', 760, 880]] } },
  { k: 'दूसरा हफ़्ता, छोटी', t: 'weeks', p: { week: 1, gx: 560, talk: 'दिन में एक बार', cast: [['friend', 1450, 640]], bubbles: [['खाने', 'मुझे तो दाल-चावल पसंद है!', 1000, 400], ['फ़िल्म', 'फ़िल्म मुझे ठीक नहीं लगी', 1000, 540]] } },
  { k: 'तीसरा हफ़्ता, माँग', t: 'weeks', p: { week: 2, gx: 560, cast: [['w_kurta', 1500, 590]], tags: [['तीन बार', 'हफ़्ते में 3 छोटी माँगें', 1050, 330], ['मना कीजिए', '1 बार "ना", बिना सफ़ाई', 1050, 460]], props: [['fence', 1050, 700, 280, 'मना']] } },
  { k: 'चौथा हफ़्ता, अपनापन', t: 'weeks', p: { week: 3, gx: 560, head: 'head_calm', cast: [['friend', 1500, 640]], props: [['chest', 1030, 520, 200, 'छिपाई'], ['guitar', 1030, 780, 200, 'सिर्फ़ आपके']], tags: [['दो बार', 'हफ़्ते में 2 बार: सिर्फ़ अपने लिए', 1050, 330]] } },
  { k: 'पूरे महीने एक ही सवाल', t: 'scene', bg: 'bg_night', p: { gx: 1500, head: 'head_calm', props: [['journal', 700, 780, 280, 0.3], ['calendar', 700, 470, 200, 0.1]], bubbles: [['आज मैंने', 'आज कौन-सी बात इसलिए नहीं कही कि कोई नाराज़ न हो?', 860, 200]] } },
  // 17 — final word
  { k: 'आख़िरी बात', ch: '17' },
  { k: 'शीर्षक से उलट', t: 'icon', p: { prop: 'book', title: 'सबसे बड़ा संदेश', sub: ['उलट', 'शीर्षक से उलट'] } },
  { k: 'यह नहीं कहती कि अच्छा बनना', t: 'big', p: { lines: [[0, 'अच्छा बनना छोड़िए? नहीं।', 80, OLIVE], ['दिखना छोड़', 'अच्छा दिखना छोड़िए', 120, INK], ['असली बनि', 'असली बनिए', 150, RUST]], prop: ['mask', 1620, 520, 250, 'दिखना छोड़'] } },
  { k: 'असली बनने का मतलब', t: 'list', p: { title: 'असली बनने का मतलब', items: [['अपनी राय', 'अपनी राय कहना', 'note'], ['ज़रूरत माँगना', 'अपनी ज़रूरत माँगना', 'gift'], ['सीमा रखना', 'अपनी सीमा रखना', 'fence'], ['कमियों', 'कमियाँ न छिपाना', 'mirror']] } },
  { k: 'सुंदर विरोधाभास', t: 'scene', bg: 'bg_park', p: { gx: 960, head: 'head_calm', cast: [['w_kurta', 460, 590], ['friend', 1420, 640], ['mother', 1680, 580]], texts: [['बेहतर', '♥', 460, 360, 90], ['बेहतर', '♥', 1420, 320, 90]], tags: [[0.2, 'एक सुंदर विरोधाभास', 960, 130], ['ख़ुश रखने', 'सबको ख़ुश रखना छोड़ा → रिश्ते बेहतर', 960, 250]], props: [['mask', 1210, 900, 110, 0.6]] } },
  { k: 'इसकी वजह सीधी', t: 'compare', p: { head: [0, 'अब लोग जुड़ते हैं…'], left: { title: 'किरदार से', prop: 'mask', w: 260, mark: 'cross', markAt: 'किरदार' }, right: { title: 'असली इंसान से', guy: { head: 'head_calm' }, at: 'जुड़', mark: 'check' } } },
  { k: 'सबसे बड़ी राहत', t: 'cooker', p: { relief: true, label: 'सबसे बड़ी राहत', sub: 'असली बात कही = भीतर गुस्सा जमा नहीं' } },
  { k: 'स्वतंत्र हिंदी सारांश', t: 'icon', p: { prop: 'book', w: 280, y: 450, title: 'अच्छा दिखना छोड़िए', texts: [[0.5, 'रॉबर्ट ग्लोवर की किताब के विचारों पर आधारित स्वतंत्र हिंदी सारांश', 960, 720, 38, OLIVE], ['आलोचनात्मक', 'आलोचनात्मक टिप्पणियाँ · भारतीय संदर्भ', 960, 790, 36, OLIVE], ['विकल्प नहीं', 'यह मानसिक स्वास्थ्य उपचार का विकल्प नहीं है', 960, 860, 36, RUST]] } },
];

function buildRest() {
  CUR = 13;
  const resolved = SHOTS.map(s => { const i = I(s.k); CUR = i; return Object.assign({ i }, s); });
  resolved.forEach((s, n) => {
    const nx = resolved[n + 1];
    const i1 = nx ? nx.i - 1 : TIMING.length - 1;
    if (s.ch) { chapterCard(s.i, s.ch, n % 2 ? 'wipe' : 'diag'); return; }
    const t0 = TIMING[s.i].start + LEAD - 0.2;
    const t1 = nx ? TIMING[nx.i].start + LEAD - 0.2 : TIMING[i1].end + LEAD + 0.6;
    const bg = s.bg || (['icon', 'big', 'balance', 'gender', 'weeks'].includes(s.t) && !(s.p && s.p.bgc) ? 'bg_paper' : null);
    const L = layer(t0, t1, s.tr || TRANS[n % TRANS.length], bg);
    const sp = { a: t0 + 0.2, b: TIMING[i1].end + LEAD, i0: s.i, i1 };
    const cm = CAMS[n % CAMS.length];
    camMove(L, Object.assign({}, cm[0]), Object.assign({}, cm[1]));
    if (bg && bg !== 'bg_paper') bgDrift(L, n % 2 ? -40 : 40);
    T[s.t](L, sp, s.p || {});
  });
  // outro
  const last = TIMING[TIMING.length - 1];
  const o0 = last.end + LEAD + 0.6;
  const L = layer(o0, o0 + 4, 'iris', 'bg_paper');
  camMove(L, { scale: 1.06 }, { scale: 1.0 });
  const mask = img(L.cam, 'mask', 1390, 540, 420, { transformOrigin: '62% 3%' });
  TL.fromTo(mask, { y: -800 }, { y: 0, duration: 0.9, ease: 'bounce.out', immediateRender: false }, o0 + 0.1); TL.set(mask, { y: -800 }, 0);
  const t1 = text(L.cam, 'असली बनिए', 640, 440, { fontSize: '150px', color: RUST }); rise(t1, o0 + 0.4);
  const t2 = text(L.cam, 'धन्यवाद', 640, 640, { fontSize: '80px' }); rise(t2, o0 + 0.9);
  window.VIDEO_END = o0 + 4;
}
