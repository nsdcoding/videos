// "दिमाग़ के पाँच धोखे" — paper-cut theme. Data-driven shots over the narration timing.
const SHADOW = '0 14px 30px rgba(5,10,25,.5)';
let CUR = 0;
function I(sub) { for (let i = CUR; i < TIMING.length; i++) if (TIMING[i].text.includes(sub)) return i; throw new Error('sentence not found: ' + sub); }
function WT(sp, w) {
  if (w === undefined || w === null) return sp.a + 0.4;
  if (typeof w === 'number') return sp.a + 0.2 + w;
  for (let i = sp.i0; i <= sp.i1; i++) if (TIMING[i].text.includes(w)) return W_(i, w);
  console.error('word not found: ' + w + ' @' + sp.i0); return sp.a + 0.4;
}
const CAMS = [[{ scale: 1.0 }, { scale: 1.07 }], [{ scale: 1.09 }, { scale: 1.0 }], [{ scale: 1.06, x: 45 }, { scale: 1.06, x: -45 }],
  [{ scale: 1.06, x: -45 }, { scale: 1.06, x: 45 }], [{ scale: 1.0, y: 18 }, { scale: 1.06, y: -12 }]];
const TRANS = ['wipe', 'iris', 'diag', 'push', 'zoom', 'wipeUp', 'fade'];

// ---------- paper helpers ----------
function card(parent, x, y, w, h, bg = CREAM, css = {}) {
  return box(parent, x, y, Object.assign({ width: w + 'px', height: h + 'px', background: bg, borderRadius: '20px', boxShadow: SHADOW }, css));
}
function label(parent, s, x, y, size = 40, color = INK, bg = CREAM) {
  return tag(parent, s, x, y, { fontSize: size + 'px', color, background: bg });
}
function title(parent, s, x, y, size = 72, color = CREAM) { return text(parent, s, x, y, { fontSize: size + 'px', color, textShadow: '0 6px 18px rgba(0,0,0,.45)' }); }
function thought(parent, str, x, y, t) {
  const b = box(parent, x, y, { fontFamily: "'Hind'", fontWeight: 600, fontSize: '34px', color: INK, background: CREAM, opacity: 0.97,
    padding: '12px 30px 6px', borderRadius: '44px', boxShadow: SHADOW, whiteSpace: 'nowrap' });
  b.innerHTML = str + `<div style="position:absolute;left:46%;bottom:-30px;width:22px;height:22px;border-radius:50%;background:${CREAM}"></div>
    <div style="position:absolute;left:42%;bottom:-54px;width:13px;height:13px;border-radius:50%;background:${CREAM}"></div>`;
  pop(b, t); return b;
}
function stamp(parent, str, x, y, t, size = 90) {
  const st = text(parent, str, x, y, { fontSize: size + 'px', color: CREAM, background: RUST, padding: '6px 40px 0', borderRadius: '16px', boxShadow: SHADOW });
  TL.fromTo(st, { scale: 2.6, rotation: -20, autoAlpha: 0 }, { scale: 1, rotation: -5, autoAlpha: 1, duration: 0.32, ease: 'power4.in' }, t);
  return st;
}
// paper rings decoration (layered circles)
function rings(parent, x, y, r, t, cols = [TEAL, RUST, MUSTARD, CREAM]) {
  cols.forEach((c, k) => {
    const rr = r - k * r * 0.18;
    const e = box(parent, x, y, { width: 2 * rr + 'px', height: 2 * rr + 'px', borderRadius: '50%', background: c, boxShadow: SHADOW, opacity: 0.95 });
    TL.set(e, { scale: 0 }, 0);
    TL.to(e, { scale: 1, duration: 0.6, ease: 'back.out(1.7)' }, t + k * 0.08);
    HOOKS.push(tt => { if (tt > t) gsap.set(e, { rotation: Math.sin(tt * 0.6 + k) * 6 }); });
  });
}
// a figure image standing on the floor, with optional pose swaps
function figure(L, sp, pose, x, h, swaps = [], enter = true) {
  const first = person(L.cam, pose, x, 1015, h, x / 100);
  const all = [[null, first]];
  if (enter) { TL.set(first, { autoAlpha: 0 }, 0); TL.fromTo(first, { y: 40, autoAlpha: 0 }, { y: 0, autoAlpha: 1, duration: 0.5, ease: 'power3.out', immediateRender: false }, sp.a + 0.15); }
  let prev = first;
  for (const [w, p, hh] of swaps) {
    const e = person(L.cam, p, x, 1015, hh || h, x / 100 + 1); const t = WT(sp, w);
    TL.set(e, { autoAlpha: 0 }, 0);
    TL.to(prev, { autoAlpha: 0, duration: 0.25 }, t); TL.fromTo(e, { autoAlpha: 0, scale: 0.96 }, { autoAlpha: 1, scale: 1, duration: 0.3, immediateRender: false }, t);
    prev = e;
  }
  return first;
}

function deco(L, sp, p) {
  const C = L.cam;
  if (p.title) { const [w, s] = p.title; const e = label(C, s, 960, 110, 44, INK, MUSTARD); pop(e, WT(sp, w)); }
  if (p.badge) { const e = label(C, p.badge, 200, 90, 34, CREAM, RUST); pop(e, sp.a + 0.3, { rot: -10 }); }
  (p.cast || []).forEach(([n, x, h, w], k) => {
    const e = person(C, n, x, 1015, h, k + 3);
    TL.set(e, { autoAlpha: 0 }, 0);
    TL.fromTo(e, { x: x > 960 ? 400 : -400, autoAlpha: 0 }, { x: 0, autoAlpha: 1, duration: 0.55, ease: 'power3.out', immediateRender: false }, WT(sp, w) + k * 0.12);
  });
  (p.props || []).forEach(([n, x, y, w, wd, mv], k) => {
    const e = img(C, n, x, y, w); const t = WT(sp, wd); e.style.filter = 'drop-shadow(0 12px 16px rgba(5,10,25,.5))';
    pop(e, t, { rot: k % 2 ? 10 : -10 });
    if (mv) TL.to(e, { x: mv.x || 0, y: mv.y || 0, rotation: mv.r || 0, scale: mv.s || 1, duration: 0.8, ease: 'power2.inOut' }, WT(sp, mv.at));
    else float(e, t, L.t1, 6, k + 1);
  });
  (p.tags || []).forEach(([w, s, x, y, bg], k) => pop(label(C, s, x, y, 38, bg === RUST || bg === TEAL ? CREAM : INK, bg || CREAM), WT(sp, w), { rot: k % 2 ? 6 : -6 }));
  (p.bubbles || []).forEach(([w, s, x, y]) => bubble(C, s, x, y, WT(sp, w)));
  (p.thought || []).forEach(([w, s, x, y]) => thought(C, s, x, y, WT(sp, w)));
  (p.texts || []).forEach(([w, s, x, y, size, color]) => {
    const e = s.length < 3 ? text(C, s, x, y, { fontSize: (size || 80) + 'px', color: color || RUST, textShadow: '0 6px 14px rgba(0,0,0,.4)' })
      : label(C, s, x, y, Math.min(size || 44, 48), color === CREAM ? INK : (color || INK), color === RUST ? CREAM : CREAM);
    if (s.length >= 3 && color === RUST) { e.style.background = RUST; e.style.color = CREAM; }
    pop(e, WT(sp, w), { rot: s.length < 3 ? 18 : 4 });
  });
  (p.checks || []).forEach(([w, x, y]) => check(C, x, y, 1.6, WT(sp, w), '#7fd3a8'));
  (p.crosses || []).forEach(([w, x, y]) => cross(C, x, y, 1.6, WT(sp, w), RUST));
  if (p.stamp) stamp(C, p.stamp[1], p.stamp[2] || 960, p.stamp[3] || 520, WT(sp, p.stamp[0]), p.stamp[4] || 90);
}

// ---------------- templates ----------------
const T = {};
T.scene = (L, sp, p) => { if (p.fig) figure(L, sp, p.fig[0], p.fig[1] || 600, p.fig[2] || 640, p.poses || []); deco(L, sp, p); };
T.face = (L, sp, p) => {
  const x = p.x || 620;
  const back = box(L.cam, x, 560, { width: '760px', height: '760px', borderRadius: '50%', background: p.ring || TEAL, boxShadow: SHADOW });
  TL.set(back, { scale: 0 }, 0); TL.to(back, { scale: 1, duration: 0.6, ease: 'back.out(1.6)' }, sp.a);
  const imgs = [[0, p.head || 'h_neutral'], ...(p.heads || [])].map(([w, h], k) => {
    const e = img(L.cam, h, x, 640, 720); TL.set(e, { autoAlpha: 0 }, 0);
    const t = k === 0 ? sp.a + 0.15 : WT(sp, w);
    TL.fromTo(e, { autoAlpha: 0, y: k === 0 ? 60 : 0 }, { autoAlpha: 1, y: 0, duration: 0.35, immediateRender: false }, t);
    return [t, e];
  });
  imgs.forEach(([t, e], k) => { if (imgs[k + 1]) TL.to(e, { autoAlpha: 0, duration: 0.2 }, imgs[k + 1][0] + 0.15); });
  imgs.forEach(([t, e], k) => HOOKS.push(tt => gsap.set(e, { rotation: Math.sin(tt * 0.8 + k) * 1.5 })));
  deco(L, sp, p);
};
T.icon = (L, sp, p) => {
  if (p.title) rise(title(L.cam, p.title, 960, 160, 72), sp.a + 0.1);
  if (p.ring !== false && p.prop) rings(L.cam, p.x || 960, p.y || 500, 260, sp.a, [TEAL, NAVY]);
  if (p.prop) { const e = img(L.cam, p.prop, p.x || 960, p.y || 500, p.w || 360); e.style.filter = 'drop-shadow(0 16px 22px rgba(5,10,25,.55))';
    const t = WT(sp, p.at); pop(e, t); float(e, t, L.t1, 7, 2); }
  if (p.sub) pop(label(L.cam, p.sub[1], 960, 800, 46, INK, MUSTARD), WT(sp, p.sub[0]));
  (p.side || []).forEach(s => (p.props = p.props || []).push(s));
  deco(L, sp, Object.assign({}, p, { title: null }));
};
T.big = (L, sp, p) => {
  if (p.bgc) el('div', L.cam, { position: 'absolute', inset: 0, background: p.bgc });
  const cx = p.prop ? 780 : 960;
  const hs = p.lines.map(l => (l[2] || 80) * 1.35);
  let y = 480 - hs.reduce((a, b) => a + b, 0) / 2;
  p.lines.forEach(([w, s, size, color], k) => { const e = title(L.cam, s, cx, y + hs[k] / 2, size || 80, color || CREAM); rise(e, WT(sp, w)); y += hs[k]; });
  const u = inkPath(L.cam, `M${cx - 300} ${y + 22} Q${cx} ${y + 46} ${cx + 300} ${y + 14}`, {}, { color: RUST, width: 12 });
  draw(u, WT(sp, p.lines[p.lines.length - 1][0]) + 0.3, 0.6);
  if (p.prop) { const [n, x, yy, w, wd] = p.prop; rings(L.cam, x, yy, 220, sp.a, [TEAL, NAVY]); const e = img(L.cam, n, x, yy, w);
    e.style.filter = 'drop-shadow(0 16px 22px rgba(5,10,25,.55))'; pop(e, WT(sp, wd)); float(e, sp.a, L.t1, 7, 4); }
  deco(L, sp, Object.assign({}, p, { title: null }));
};
T.list = (L, sp, p) => {
  el('div', L.cam, { position: 'absolute', inset: 0, background: p.bgc || '#16213b' });
  rise(title(L.cam, p.title, 960, 120, 60, MUSTARD), sp.a + 0.1);
  const n = p.items.length, cw = Math.min(460, (1760 - (n - 1) * 40) / n), x0 = 960 - ((n - 1) * (cw + 40)) / 2;
  const cards = [];
  const cols = [TEAL, RUST, MUSTARD, '#5b7bb5', '#8a6fb0'];
  p.items.forEach(([w, lab, im], k) => {
    const x = x0 + k * (cw + 40), t = WT(sp, w);
    const c = card(L.cam, x, 520, cw, 540, CREAM, { display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '24px', borderTop: `18px solid ${cols[k % 5]}` });
    const pic = el('img', c, { maxWidth: (cw * 0.62) + 'px', maxHeight: '280px', filter: 'drop-shadow(0 10px 12px rgba(5,10,25,.35))' }, { src: A(im) });
    el('div', c, { fontFamily: "'Hind'", fontWeight: 700, fontSize: (n > 3 ? 34 : 40) + 'px', color: INK, textAlign: 'center', padding: '0 14px', lineHeight: 1.2 }).textContent = lab;
    const num = text(c, String(k + 1), 44, 30, { fontSize: '44px', color: CREAM, background: cols[k % 5], borderRadius: '50%', width: '70px', height: '70px', lineHeight: '84px' });
    TL.set(c, { autoAlpha: 0 }, 0);
    TL.fromTo(c, { y: 140, rotation: k % 2 ? 6 : -6, autoAlpha: 0 }, { y: 0, rotation: 0, autoAlpha: 1, duration: 0.55, ease: 'back.out(1.4)', immediateRender: false }, t);
    float(pic, t, L.t1, 5, k);
    cards.forEach(cc => TL.to(cc, { scale: 0.93, opacity: 0.6, duration: 0.3 }, t));
    cards.push(c);
  });
  if (p.end) { const t = WT(sp, p.end[0]); TL.to(cards, { scale: 0.85, opacity: 1, y: -40, duration: 0.4 }, t); pop(label(L.cam, p.end[1], 960, 880, 40, INK, MUSTARD), t + 0.2); }
  deco(L, sp, Object.assign({}, p, { title: null }));
};
T.compare = (L, sp, p) => {
  const C = L.cam;
  el('div', C, { position: 'absolute', inset: 0, background: '#16213b' });
  const R = el('div', C, { position: 'absolute', left: '960px', top: 0, width: '960px', height: '1080px', background: '#24365d', overflow: 'hidden' });
  const ty = p.head ? 210 : 140;
  if (p.head) { const e = label(C, p.head[1], 960, 70, 42, INK, MUSTARD); e.style.zIndex = 5; pop(e, WT(sp, p.head[0])); }
  [[p.left, 480], [p.right, 1440]].forEach(([side, x], k) => {
    const t = WT(sp, side.at !== undefined ? side.at : (k ? 0.4 : 0));
    const grp = el('div', C, { position: 'absolute', inset: 0 });
    if (k === 1) reveal(R, t - 0.2, 'inset(0 0 100% 0)', 'inset(0 0 0% 0)');
    TL.set(grp, { autoAlpha: 0 }, 0); TL.set(grp, { autoAlpha: 1 }, t);
    rise(title(grp, side.title, x, ty, 56, k ? MUSTARD : CREAM), t);
    if (side.prop) { rings(grp, x, 540, 200, t, k ? [RUST, '#24365d'] : [TEAL, '#16213b']); const e = img(grp, side.prop, x, 540, side.w || 300); pop(e, t + 0.15); float(e, t, L.t1, 6, k); }
    if (side.fig) { const e = person(grp, side.fig, x, 1015, side.h || 600, k); rise(e, t + 0.1); }
    if (side.bubble) bubble(grp, side.bubble, x, ty + 110, t + 0.5, { fontSize: '32px' });
    const mt = WT(sp, side.markAt !== undefined ? side.markAt : (side.at !== undefined ? side.at : 0)) + 0.6;
    if (side.mark === 'check') check(grp, x + 300, ty + 230, 1.7, mt, '#7fd3a8');
    if (side.mark === 'cross') cross(grp, x + 300, ty + 230, 1.7, mt, RUST);
    if (side.note) pop(label(grp, side.note, x, 870, 40, INK, k ? MUSTARD : CREAM), mt + 0.2);
  });
  if (p.footer) { const e = label(C, p.footer[1], 960, 880, 44, CREAM, RUST); e.style.zIndex = 5; pop(e, WT(sp, p.footer[0])); }
  deco(L, sp, Object.assign({}, p, { title: null, head: null }));
};
T.step = (L, sp, p) => {
  if (p.fig) figure(L, sp, p.fig[0], p.fig[1] || 1450, p.fig[2] || 640, p.poses || []);
  deco(L, sp, p);
  const pan = el('div', L.cam, { position: 'absolute', left: 0, top: 0, width: '700px', height: '1080px', background: 'rgba(22,33,59,.96)', zIndex: 50, boxShadow: '20px 0 40px rgba(5,10,25,.45)' });
  TL.set(pan, { x: -740 }, 0); TL.to(pan, { x: 0, duration: 0.5, ease: 'power3.out' }, sp.a + 0.1);
  rings(pan, 350, 370, 170, sp.a + 0.3, [TEAL, RUST, MUSTARD]);
  const n = text(pan, p.n, 350, 395, { fontSize: '170px', color: INK }); pop(n, sp.a + 0.6, { rot: -20 });
  rise(title(pan, p.label, 350, 700, 54, CREAM), sp.a + 0.6); pan.lastChild.style.whiteSpace = 'normal'; pan.lastChild.style.width = '600px';
};
T.days = (L, sp, p) => {
  for (let k = 0; k < 7; k++) {
    const on = k === p.day, done = k < p.day;
    const b = card(L.cam, 175 + k * 262, 120, 228, 120, on ? MUSTARD : CREAM, { opacity: on ? 1 : 0.55, textAlign: 'center', fontFamily: "'Yatra One'", color: INK, zIndex: 40 });
    b.innerHTML = `<div style="font-size:26px;margin-top:14px;font-family:Hind;font-weight:700">दिन</div><div style="font-size:52px;line-height:1">${k + 1}</div>`;
    TL.set(b, { autoAlpha: 0 }, 0);
    TL.fromTo(b, { y: -160, autoAlpha: 0 }, { y: 0, autoAlpha: on ? 1 : 0.55, duration: 0.45, ease: 'back.out(1.6)', immediateRender: false }, sp.a + 0.05 + k * 0.05);
    if (on) TL.fromTo(b, { scale: 1 }, { scale: 1.12, duration: 0.4, ease: 'back.out(3)', immediateRender: false }, sp.a + 0.6);
    if (done) check(L.cam, 175 + k * 262 + 80, 80, 0.8, sp.a + 0.5, '#2f8f5b');
  }
  if (p.fig) figure(L, sp, p.fig[0], p.fig[1] || 520, p.fig[2] || 560, p.poses || []);
  if (p.task) pop(label(L.cam, p.task, p.tx || 1200, 330, 44, INK, CREAM), sp.a + 0.7);
  deco(L, sp, p);
};
// ----- custom visuals -----
T.batball = (L, sp, p) => {
  const C = L.cam;
  const bb = img(C, 'batball', 520, 520, 420); pop(bb, sp.a + 0.2); float(bb, sp.a, L.t1, 6, 1);
  const eq = [['बल्ला + गेंद = ₹110', 'एक सौ दस'], ['बल्ला = गेंद + ₹100', 'सौ रुपये महँगा'], ['गेंद = ?', 'कितने की']];
  eq.forEach(([s, w], k) => pop(label(C, s, 1300, 260 + k * 120, 50, INK, k === 2 ? MUSTARD : CREAM), WT(sp, w)));
  const wrong = title(C, '₹10 ?', 1300, 660, 110, RUST); pop(wrong, WT(sp, 'दस रुपये'));
  cross(C, 1300, 660, 2, WT(sp, 'ग़लत'));
  TL.to(wrong, { opacity: 0.35, duration: 0.3 }, WT(sp, 'ग़लत') + 0.4);
  pop(label(C, '10 + 110 = 120 ✗', 1300, 790, 40, CREAM, RUST), WT(sp, 'एक सौ बीस'));
  const right = title(C, '₹5 ✓', 1300, 660, 120, '#7fd3a8'); TL.set(right, { autoAlpha: 0 }, 0);
  TL.to(wrong, { autoAlpha: 0, duration: 0.2 }, WT(sp, 'पाँच रुपये') - 0.1); pop(right, WT(sp, 'पाँच रुपये'));
  pop(label(C, '5 + 105 = 110 ✓', 1300, 900, 40, INK, '#7fd3a8'), WT(sp, 'पाँच रुपये') + 0.5);
};
T.anchor = (L, sp, p) => {
  const C = L.cam;
  const tagi = img(C, 'pricetag', 760, 470, 420); pop(tagi, sp.a + 0.2);
  HOOKS.push(t => { if (t > sp.a) gsap.set(tagi, { rotation: Math.sin((t - sp.a) * 2.2) * 6 }); });
  const old = title(C, '₹4,000', 760, 470, 96, INK); old.style.textShadow = 'none'; pop(old, WT(sp, 'चार हज़ार'));
  const strike = inkPath(C, 'M610 480 L910 455', {}, { color: RUST, width: 12 }); draw(strike, WT(sp, 'काटकर'), 0.35);
  const nw = title(C, '₹2,000', 1350, 470, 130, MUSTARD); pop(nw, WT(sp, 'दो हज़ार'));
  pop(label(C, 'सस्ता लगता है!', 1350, 620, 44, CREAM, RUST), WT(sp, 'सस्ता'));
  if (p.anchorTag) pop(label(C, 'एंकर = पहली संख्या', 960, 820, 44, INK, MUSTARD), WT(sp, p.anchorTag));
  deco(L, sp, p);
};
T.curve = (L, sp, p) => {
  const C = L.cam;
  rise(title(C, 'रोज़ 1% का फ़र्क़', 960, 110, 64, MUSTARD), sp.a);
  const ax = inkPath(C, 'M300 880 L1650 880 M300 880 L300 200', {}, { color: CREAM, width: 6 }); draw(ax, sp.a + 0.2, 0.5);
  const up = [], dn = [];
  for (let d = 0; d <= 365; d += 5) { const x = 300 + d / 365 * 1350; up.push(`${x} ${880 - Math.pow(1.01, d) / 38 * 660}`); dn.push(`${x} ${880 - Math.pow(0.99, d) * 260}`); }
  const pu = inkPath(C, 'M' + up.join(' L'), {}, { color: '#7fd3a8', width: 12 }); draw(pu, WT(sp, 'सैंतीस') - 2.2, 2.2);
  pop(label(C, '1.01³⁶⁵ ≈ 37.8', 1500, 210, 44, INK, '#7fd3a8'), WT(sp, 'सैंतीस'));
  const pd = inkPath(C, 'M' + dn.join(' L'), {}, { color: RUST, width: 12 }); draw(pd, WT(sp, 'बिगड़ते'), 2.2);
  pop(label(C, '0.99³⁶⁵ ≈ 0.03', 1500, 800, 44, CREAM, RUST), WT(sp, 'शून्य'));
  pop(label(C, '1 साल', 1650, 940, 34, INK, CREAM), sp.a + 0.8);
};
T.ice = (L, sp, p) => {
  const C = L.cam;
  const ice = img(C, 'ice', 820, 560, 380); pop(ice, sp.a + 0.2);
  const th = card(C, 1420, 520, 120, 560, CREAM, { borderRadius: '60px' });
  const fill = el('div', th, { position: 'absolute', left: '35px', bottom: '35px', width: '50px', height: '120px', borderRadius: '25px', background: '#5b7bb5', transformOrigin: '50% 100%' });
  pop(th, sp.a + 0.3);
  const temp = title(C, '-5°', 1600, 520, 80, CREAM); pop(temp, sp.a + 0.5);
  const vals = ['-4°', '-3°', '-2°', '-1°', '0°', '1°'];
  const t0 = WT(sp, 'माइनस चार'), t1 = WT(sp, 'शून्य पार');
  vals.forEach((v, k) => { const t = t0 + (t1 - t0) * k / 4; TL.call(() => {}, null, t); TL.set(temp, { innerHTML: v, color: k >= 5 ? RUST : CREAM }, t);
    TL.to(fill, { height: 120 + (k + 1) * 60, background: k >= 4 ? RUST : '#5b7bb5', duration: 0.4 }, t); });
  TL.set(temp, { innerHTML: '-5°' }, 0);
  pop(label(C, 'कोई बदलाव नहीं दिखता…', 820, 820, 40, INK, CREAM), WT(sp, 'कोई बदलाव'));
  TL.to(ice, { scaleY: 0.55, scaleX: 1.15, y: 90, filter: 'brightness(1.15)', duration: 2.5, ease: 'power1.in' }, t1 + 0.3);
  pop(label(C, 'मेहनत जमा हो रही थी', 820, 820, 42, CREAM, RUST), WT(sp, 'जमा हो'));
};
T.residue = (L, sp, p) => {
  const C = L.cam;
  const a = card(C, 560, 480, 520, 360, CREAM); const b = card(C, 1360, 480, 520, 360, CREAM);
  title(a, 'रिपोर्ट', 260, 70, 54, INK); title(b, 'मैसेज', 260, 70, 54, INK);
  const ai = img(a, 'laptop', 260, 220, 230), bi = img(b, 'phone', 260, 220, 130);
  pop(a, sp.a + 0.2); pop(b, WT(sp, 'मैसेज'));
  arrow(C, 830, 380, 1090, 380, WT(sp, 'मैसेज') + 0.2, { bend: -0.25, width: 8, color: MUSTARD });
  arrow(C, 1090, 600, 830, 600, WT(sp, 'लौटने') , { bend: -0.25, width: 8, color: MUSTARD });
  // attention meter
  const bar = card(C, 960, 830, 900, 60, '#24365d', { borderRadius: '30px', overflow: 'hidden' });
  const f1 = el('div', bar, { position: 'absolute', left: 0, top: 0, bottom: 0, width: '100%', background: '#7fd3a8' });
  const f2 = el('div', bar, { position: 'absolute', right: 0, top: 0, bottom: 0, width: '0%', background: RUST });
  pop(bar, sp.a + 0.5);
  pop(label(C, 'ध्यान', 420, 830, 34, INK, CREAM), sp.a + 0.6);
  TL.to(f2, { width: '35%', duration: 0.8 }, WT(sp, 'अटका'));
  pop(label(C, 'ध्यान का अवशेष', 1240, 930, 38, CREAM, RUST), WT(sp, 'अटका') + 0.3);
  if (p.twenty) { const t = WT(sp, 'बीस बार'); TL.to(f2, { width: '55%', duration: 0.8 }, t); pop(label(C, 'आधा ध्यान', 960, 160, 54, CREAM, RUST), WT(sp, 'आधे ध्यान')); }
  deco(L, sp, p);
};
T.thread = (L, sp, p) => {
  const C = L.cam;
  const books = [['काह्नमन', 'तेज़ दिमाग़ पर आँख मूँदकर भरोसा नहीं', TEAL], ['क्लियर', 'छोटे क़दम, सही माहौल', RUST], ['न्यूपोर्ट', 'ध्यान की रक्षा', MUSTARD], ['हाउज़ल', 'धैर्य और काफ़ी', '#5b7bb5'], ['फ़्रैंकल', 'प्रतिक्रिया चुनने की आज़ादी', '#8a6fb0']];
  const keys = ['काह्नमन कहते', 'क्लियर कहते', 'न्यूपोर्ट कहते', 'हाउज़ल कहते', 'फ़्रैंकल कहते'];
  const xs = [250, 605, 960, 1315, 1670];
  const path = inkPath(C, `M${xs[0]} 420 C 430 300, 780 540, ${xs[2]} 420 S 1490 300, ${xs[4]} 420`, {}, { color: MUSTARD, width: 7 });
  books.forEach(([n, msg, c], k) => {
    const t = WT(sp, keys[k]);
    const bk = card(C, xs[k], 420, 250, 320, c, { borderRadius: '12px 26px 26px 12px', borderLeft: `20px solid rgba(0,0,0,.25)` });
    title(bk, n, 125, 120, 44, CREAM);
    TL.set(bk, { autoAlpha: 0 }, 0); TL.fromTo(bk, { y: -300, rotation: -15, autoAlpha: 0 }, { y: 0, rotation: 0, autoAlpha: 1, duration: 0.5, ease: 'back.out(1.5)', immediateRender: false }, t);
    const m = label(C, msg, xs[k], k % 2 ? 760 : 690, 30, INK, CREAM); m.style.whiteSpace = 'normal'; m.style.width = '300px'; pop(m, t + 0.4);
  });
  draw(path, WT(sp, 'साझा संदेश'), 1.4);
  pop(label(C, 'छोटे, रोज़ के चुनाव', 960, 160, 52, INK, MUSTARD), WT(sp, 'छोटे, रोज़'));
};
T.chapter = (L, sp, p) => {
  const C = L.cam;
  rings(C, 470, 540, 330, sp.a - 0.2, [TEAL, RUST, MUSTARD, CREAM]);
  const n = text(C, p.n, 470, 560, { fontSize: '230px', color: INK }); pop(n, sp.a + 0.2, { rot: -15 });
  if (p.kicker) rise(text(C, p.kicker, 1300, 330, { fontSize: '40px', color: MUSTARD, fontFamily: "'Hind'", fontWeight: 700, letterSpacing: '3px' }), sp.a);
  const hd = title(C, TIMING[sp.i0].text, 1300, 520, 78, CREAM); hd.style.whiteSpace = 'normal'; hd.style.width = '900px'; rise(hd, sp.a + 0.1);
  draw(inkPath(C, 'M900 690 Q1300 715 1700 680', {}, { color: RUST, width: 12 }), sp.a + 0.4, 0.7);
};

// ---------------- shot list ----------------
const SHOTS = [
  { k: 'आपका दिमाग़ आपसे क्या छिपाता है', t: 'chapter', bg: 'bg_plain', p: { n: '0', kicker: 'शुरुआत' } },
  { k: 'अनन्या सत्ताईस साल', t: 'scene', bg: 'bg_rooftop', p: { fig: ['a_stand', 700, 660], tags: [[0.3, 'अनन्या · 27', 700, 230, MUSTARD], ['मेहनती', 'मेहनती', 1250, 330], ['समझदार', 'समझदार', 1500, 450]], bubbles: [['बड़े-बड़े वादे', 'इस साल सब बदल दूँगी!', 1150, 220]] } },
  { k: 'इस साल वह रोज़ सुबह', t: 'list', p: { title: 'नए साल के तीन वादे', items: [['दौड़ेगी', 'रोज़ सुबह दौड़ना', 'shoes'], ['पैसे', 'हर महीने बचत', 'piggy'], ['भाषा', 'नई भाषा सीखना', 'notebook']] } },
  { k: 'फ़रवरी आते-आते', t: 'scene', bg: 'bg_bedroom', p: { fig: ['a_worried', 1200, 660], props: [['calendar', 560, 420, 300, 0.2]], stamp: ['ग़ायब', 'फ़रवरी', 560, 700, 70], thought: [['कमी है', 'शायद मुझमें ही कुछ कमी है…', 1150, 200]] } },
  { k: 'पर सच्चाई कुछ और है', t: 'face', bg: 'bg_plain', p: { head: 'h_neutral', heads: [['कोई कमी नहीं', 'h_aha']], texts: [['कोई कमी नहीं', 'कमी उसमें नहीं', 1400, 380, 48, RUST], ['हज़ारों', 'हज़ारों साल पुराना दिमाग़', 1400, 520, 44]], props: [['bulb', 1450, 760, 150, 'हज़ारों']] } },
  { k: 'पिछले कुछ दशकों में', t: 'icon', bg: 'bg_plain', p: { prop: 'books', title: 'पाँच किताबें, एक दिमाग़', texts: [['मनोविज्ञान', 'मनोविज्ञान', 360, 300], ['आदतें', 'आदतें', 360, 450], ['ध्यान', 'ध्यान', 360, 600], ['पैसा', 'पैसा', 1560, 380], ['अर्थ', 'जीवन का अर्थ', 1560, 530]] } },
  { k: 'आज हम ऐसी ही पाँच', t: 'big', bg: 'bg_plain', p: { lines: [[0, 'दिमाग़ के', 90, CREAM], [0.6, 'पाँच धोखे', 160, MUSTARD], ['बचा कैसे', '…और उनसे बचने के तरीक़े', 54, '#7fd3a8']], prop: ['compass', 1560, 520, 300, 'बचा कैसे'] } },
  // 1 — System 1/2
  { k: 'पहला धोखा, मैं सोच', t: 'chapter', bg: 'bg_plain', p: { n: '1', kicker: 'धोखा 1' } },
  { k: 'पहली किताब है डैनियल', t: 'icon', bg: 'bg_plain', p: { prop: 'books', w: 300, title: 'Thinking, Fast and Slow', sub: ['नोबेल', 'डैनियल काह्नमन · मनोवैज्ञानिक · नोबेल (अर्थशास्त्र)'] } },
  { k: 'उनकी सबसे मशहूर बात', t: 'compare', p: { head: [0, 'सोचने के दो तरीक़े'], left: { title: 'सिस्टम 1: तेज़', prop: 'hare', at: 'तेज़ है', note: 'अपने आप · बिना मेहनत · पल भर में', markAt: 'पल भर' }, right: { title: 'सिस्टम 2: धीमा', prop: 'tortoise', at: 'धीमा है', note: 'ध्यान · मेहनत · थक जाता है', markAt: 'थक' } } },
  { k: 'एक छोटा-सा सवाल लीजिए', t: 'batball', bg: 'bg_plain', p: {} },
  { k: 'यही है सिस्टम वन का खेल', t: 'face', bg: 'bg_plain', p: { head: 'h_aha', ring: RUST, props: [['hare', 1420, 420, 320, 0.2]], texts: [['भरोसे', 'इतना भरोसा कि जाँच ही नहीं', 1420, 700, 44, RUST]] } },
  { k: 'तेज़ दिमाग़ के जाल', t: 'chapter', bg: 'bg_plain', p: { n: '1', kicker: 'धोखा 1 · आगे' } },
  { k: 'सिस्टम वन बुरा नहीं', t: 'scene', bg: 'bg_city', p: { props: [['wheel', 620, 560, 320, 0.4], ['hare', 1300, 560, 280, 0.2]], checks: [['गाड़ी', 820, 420], ['मूड', 1480, 420]], tags: [['गाड़ी', 'गाड़ी चलाते हुए बात', 620, 820], ['मूड', 'चेहरा देखकर मूड', 1300, 820]] } },
  { k: 'समस्या तब होती है', t: 'scene', bg: 'bg_office', p: { fig: ['a_think', 1350, 650], props: [['hare', 560, 560, 300, 0.2]], tags: [['बड़े फ़ैसले', 'बड़े फ़ैसले?', 560, 300, RUST]], crosses: [['भरोसे', 760, 420]] } },
  { k: 'एक उदाहरण है एंकरिंग', t: 'anchor', bg: 'bg_market', p: { anchorTag: 'पहली संख्या', title: [0, 'एंकरिंग'] } },
  { k: 'दूसरा जाल है, जो दिख रहा', t: 'scene', bg: 'bg_plain', p: { props: [['bulb', 600, 480, 260, 0.2], ['key', 1300, 480, 200, 'ग़ायब']], tags: [['जो दिख रहा', 'जो दिख रहा है…', 600, 760], ['बस वही', '…बस वही सब कुछ है', 600, 860, MUSTARD]], crosses: [['सोचते ही नहीं', 1300, 480]], texts: [['ग़ायब', 'ग़ायब जानकारी', 1300, 760, 44, RUST]], stamp: ['अच्छी कहानी', 'कहानी > आँकड़ा', 960, 200, 64] } },
  { k: 'तीसरा जाल है नुक़सान', t: 'scene', bg: 'bg_plain', p: { props: [['coins', 560, 520, 260, 0.3], ['coins', 1360, 520, 260, 'ख़ुशी']], texts: [['खोने', '−₹100', 560, 300, 90, RUST], ['ख़ुशी', '+₹100', 1360, 300, 90, '#7fd3a8'], ['दोगुना', '😣 दुख ≈ 2 × ख़ुशी', 960, 800, 48, RUST]], tags: [['घाटे वाले', 'घाटे वाला शेयर बेच नहीं पाते', 960, 160], ['खींचते', 'बेकार योजना भी खींचते रहते हैं', 960, 920]] } },
  { k: 'तो इलाज क्या है', t: 'scene', bg: 'bg_desk', p: { fig: ['a_think', 1400, 650], props: [['tortoise', 600, 640, 260, 'पहचानिए']], crosses: [['असंभव', 600, 300]], texts: [['हर बात', 'हर बात पर धीमे सोचना? असंभव', 600, 250, 40]], tags: [['पैसे', 'पैसे का बड़ा फ़ैसला', 650, 820], ['नौकरी', 'नौकरी बदलना', 650, 900], ['गुस्से', 'गुस्से में जवाब', 650, 980]] } },
  { k: 'ऐसे पलों में एक छोटा', t: 'face', bg: 'bg_plain', p: { head: 'h_neutral', heads: [['जाँचा', 'h_aha']], thought: [['भरोसे', 'मैं इतने भरोसे से क्यों बोल रहा हूँ?', 1300, 280]], texts: [['जाँचा', 'क्या मैंने जाँचा?', 1400, 600, 54, RUST]] } },
  // 2 — habits
  { k: 'दूसरा धोखा, बड़ा बदलाव', t: 'chapter', bg: 'bg_plain', p: { n: '2', kicker: 'धोखा 2' } },
  { k: 'अब लौटते हैं अनन्या', t: 'scene', bg: 'bg_rooftop', p: { fig: ['a_worried', 600, 650], props: [['books', 1350, 420, 260, 'एटॉमिक']], tags: [['एटॉमिक', 'Atomic Habits · जेम्स क्लियर', 1350, 640, MUSTARD]], texts: [['लक्ष्य बनाए', 'लक्ष्य ✓', 1250, 800, 48], ['सिस्टम नहीं', 'सिस्टम ✗', 1550, 800, 48, RUST]] } },
  { k: 'क्लियर का सबसे मशहूर गणित', t: 'curve', bg: 'bg_plain', p: {} },
  { k: 'बात गणित की नहीं है', t: 'scene', bg: 'bg_park', p: { props: [['sapling', 960, 640, 300, 0.4]], tags: [['दिखते ही नहीं', 'शुरू में बदलाव दिखते नहीं', 960, 250]], texts: [['बेकार समझकर', 'इसलिए हम छोड़ देते हैं', 960, 380, 44, RUST]] } },
  { k: 'क्लियर इसे बर्फ़', t: 'ice', bg: 'bg_plain', p: {} },
  { k: 'आदतें कैसे बदलती हैं', t: 'chapter', bg: 'bg_plain', p: { n: '2', kicker: 'धोखा 2 · आगे' } },
  { k: 'क्लियर एक और गहरी', t: 'compare', p: { head: [0, 'सबसे टिकाऊ बदलाव कहाँ से आता है?'], left: { title: 'नतीजा', at: 'नतीजा है', bubble: '"मुझे 10 किलो घटाना है"', prop: 'scale', w: 240, mark: 'cross', markAt: 'नतीजा है' }, right: { title: 'पहचान', at: 'ऐसा इंसान', bubble: '"मैं अपना ख़याल रखता हूँ"', fig: 'a_happy', h: 560, mark: 'check', markAt: 'पहचान है' } } },
  { k: 'हर छोटी आदत एक वोट', t: 'scene', bg: 'bg_park', p: { fig: ['a_run', 520, 600], props: [['notebook', 1350, 560, 260, 0.3]], texts: [['पाँच मिनट', '5 मिनट दौड़ = 1 वोट', 1350, 300, 46], ['पक्ष में', '"मैं दौड़ने वाली हूँ" +1', 1350, 820, 44, '#7fd3a8']] } },
  { k: 'दूसरी बात, माहौल', t: 'scene', bg: 'bg_bedroom', p: { fig: ['a_phone', 1350, 640], props: [['phone', 640, 600, 160, 'फ़ोन बिस्तर'], ['shoes', 640, 820, 220, 'जूते']], texts: [['माहौल', 'माहौल > इच्छाशक्ति', 960, 160, 54, RUST]], tags: [['आसान और सामने', 'चाहिए: आसान + सामने', 640, 300, '#7fd3a8'], ['मुश्किल', 'नहीं चाहिए: मुश्किल + दूर', 640, 400, RUST]] } },
  { k: 'तीसरी बात, शुरुआत इतनी छोटी', t: 'compare', p: { left: { title: 'रोज़ एक घंटा', prop: 'clock', mark: 'cross', at: 0 }, right: { title: 'रोज़ एक पन्ना', prop: 'notebook', mark: 'check', at: 'एक पन्ना' }, footer: ['पन्ना', 'शुरुआत इतनी छोटी कि मना न कर सकें'] } },
  { k: 'चौथी बात, नई आदत को', t: 'scene', bg: 'bg_cafe', p: { props: [['bell', 960, 300, 160, 'घंटी']], tags: [['चाय', 'चाय ☕ → 2 मिनट स्ट्रेचिंग', 960, 520], ['दाँत', 'ब्रश 🪥 → कल का एक काम लिखना', 960, 650]], texts: [['घंटी', 'पुरानी आदत = नई आदत की घंटी', 960, 820, 44, RUST]] } },
  { k: 'अनन्या ने यही किया', t: 'scene', bg: 'bg_bedroom', p: { fig: ['a_shoes', 760, 600], poses: [['दौड़ भी', 'a_run', 600]], tags: [['जूते', 'नियम: सिर्फ़ जूते पहनकर दरवाज़े तक', 1300, 260, MUSTARD]], checks: [['दौड़ भी', 1300, 500]] } },
  // 3 — attention
  { k: 'तीसरा धोखा, मैं एक साथ', t: 'chapter', bg: 'bg_plain', p: { n: '3', kicker: 'धोखा 3' } },
  { k: 'तीसरी किताब है कैल', t: 'icon', bg: 'bg_plain', p: { prop: 'books', w: 300, title: 'Deep Work', sub: ['प्रोफ़ेसर', 'कैल न्यूपोर्ट · कंप्यूटर साइंस प्रोफ़ेसर'] } },
  { k: 'उनका दावा है कि आज', t: 'scene', bg: 'bg_desk', p: { fig: ['a_desk', 1250, 560], props: [['lantern', 560, 450, 220, 0.3]], tags: [['क़ीमती', 'सबसे क़ीमती क्षमता: गहरा ध्यान', 600, 200, MUSTARD]], texts: [['ख़त्म', 'और यही तेज़ी से ख़त्म हो रही है', 600, 720, 40, RUST]] } },
  { k: 'हम मानते हैं कि हम मल्टी', t: 'scene', bg: 'bg_office', p: { fig: ['a_phone', 1450, 620], props: [['laptop', 500, 560, 260, 0.2], ['phone', 900, 400, 120, 0.5, { x: -300, y: 200, at: 'कूदता' }], ['bell', 900, 700, 120, 0.7]], texts: [['मल्टीटास्किंग', 'मल्टीटास्किंग?', 700, 200, 54, RUST]], tags: [['कूदता', 'असल में: एक काम से दूसरे पर छलांग', 760, 880]] } },
  { k: 'और हर छलांग की', t: 'residue', bg: 'bg_plain', p: { twenty: true, title: [0, 'हर छलांग की क़ीमत · सोफ़ी लेरॉय'] } },
  { k: 'गहरे काम का अभ्यास', t: 'chapter', bg: 'bg_plain', p: { n: '3', kicker: 'धोखा 3 · आगे' } },
  { k: 'न्यूपोर्ट इसका इलाज', t: 'big', bg: 'bg_plain', p: { lines: [[0, 'ध्यान = मांसपेशी', 110, CREAM], ['रोज़ अभ्यास', 'जिसे रोज़ अभ्यास चाहिए', 60, MUSTARD]], prop: ['lantern', 1560, 520, 240, 'मांसपेशी'] } },
  { k: 'पहला, दिन में एक तय समय', t: 'step', bg: 'bg_desk', p: { n: '1', label: 'रोज़ एक तय गहरा समय', fig: ['a_desk', 1350, 560], props: [['clock', 980, 300, 170, 'एक घंटा'], ['phone', 1800, 300, 110, 'दूसरे कमरे', { x: 300, at: 'दूसरे कमरे' }]] } },
  { k: 'दूसरा, बोरियत से भागना', t: 'step', bg: 'bg_market', p: { n: '2', label: 'बोरियत से मत भागिए', fig: ['a_phone', 1400, 620], texts: [['लाइन', 'लाइन में खड़े… फ़ोन!', 1100, 220, 44, RUST]], tags: [['ख़ाली न रहे', 'दिमाग़ को ख़ाली पल भी चाहिए', 1150, 880]] } },
  { k: 'तीसरा, उथले कामों', t: 'step', bg: 'bg_office', p: { n: '3', label: 'उथले काम एक साथ', props: [['bell', 1000, 400, 150, 0.3], ['phone', 1250, 420, 110, 0.5], ['laptop', 1550, 420, 220, 0.7]], tags: [['दो-तीन', 'ईमेल/मैसेज: दिन में 2–3 बार', 1250, 720, MUSTARD]], crosses: [['हर पल', 1250, 420]] } },
  { k: 'चौथा, दिन के आख़िर में', t: 'step', bg: 'bg_desk', p: { n: '4', label: 'काम बंद करने की रस्म', props: [['notebook', 1100, 560, 280, 0.3]], tags: [['अधूरे', 'अधूरे कामों की सूची', 1450, 300], ['योजना', 'कल की योजना', 1450, 420], ['ख़त्म', '"आज का काम ख़त्म"', 1450, 540, MUSTARD]], texts: [['घूमता', 'रात को दिमाग़ शांत', 1300, 820, 44, '#7fd3a8']] } },
  { k: 'अनन्या ने जब पहली बार', t: 'scene', bg: 'bg_desk', p: { fig: ['a_desk', 1300, 560], props: [['phone', 520, 700, 120, 0.2, { x: -500, at: 0.6 }], ['clock', 560, 330, 170, 0.3]], texts: [['बेचैनी', 'पहले 20 मिनट: बेचैनी', 600, 560, 44, RUST], ['पूरा किया', '3 दिन का काम, 1 घंटे में ✓', 600, 820, 44, '#7fd3a8']] } },
  // 4 — money
  { k: 'चौथा धोखा, ज़्यादा पैसा', t: 'chapter', bg: 'bg_plain', p: { n: '4', kicker: 'धोखा 4' } },
  { k: 'चौथी किताब है मॉर्गन', t: 'icon', bg: 'bg_plain', p: { prop: 'books', w: 300, title: 'The Psychology of Money', sub: ['व्यवहार', 'मॉर्गन हाउज़ल · गणित से कम, व्यवहार से ज़्यादा'] } },
  { k: 'उनका पहला सबक़ है', t: 'scene', bg: 'bg_plain', p: { props: [['hourglass', 520, 520, 260, 0.3], ['coins', 1000, 700, 160, 'पचास-साठ'], ['coins', 1250, 620, 240, 'टिके रहना'], ['coins', 1520, 520, 320, 'चक्रवृद्धि']], tags: [[0.2, 'सबक़ 1: धैर्य + समय', 960, 160, MUSTARD], ['पचास-साठ', 'बफ़ेट: ज़्यादातर दौलत 50–60 की उम्र के बाद', 960, 280]], texts: [['टिके रहना', 'राज़: लंबे समय तक टिके रहना', 1150, 900, 44, '#7fd3a8']] } },
  { k: 'दूसरा सबक़, असली दौलत', t: 'compare', p: { left: { title: 'जो दिखता है', prop: 'key', w: 200, note: 'महँगी गाड़ी', mark: 'cross', markAt: 'बैंक' }, right: { title: 'जो दिखता नहीं', prop: 'piggy', at: 'ख़र्च नहीं', note: 'बचा हुआ पैसा = आज़ादी', mark: 'check' } } },
  { k: 'तीसरा सबक़ सबसे गहरा', t: 'scene', bg: 'bg_mountain', p: { fig: ['a_think', 560, 620], props: [['scale', 1300, 540, 300, 0.3]], tags: [[0.2, 'सबक़ 3: "काफ़ी" की समझ', 1300, 220, MUSTARD]], texts: [['ऊपर खिसकता', 'लक्ष्य खिसकता रहे → कभी काफ़ी नहीं', 1300, 820, 40, RUST]] } },
  { k: 'चौथा सबक़ है ग़लती', t: 'scene', bg: 'bg_plain', p: { props: [['compass', 560, 520, 260, 0.3], ['piggy', 1350, 560, 280, 'आपात']], tags: [[0.2, 'सबक़ 4: ग़लती की गुंजाइश', 960, 160, MUSTARD]], texts: [['भविष्य', 'भविष्य कोई नहीं जानता', 560, 800, 44], ['बीमा', 'आपात फ़ंड = योजना का बीमा', 1350, 820, 44, '#7fd3a8']] } },
  { k: 'पैसा और आज़ादी', t: 'chapter', bg: 'bg_plain', p: { n: '4', kicker: 'धोखा 4 · आगे' } },
  { k: 'हाउज़ल के अनुसार पैसे', t: 'scene', bg: 'bg_office', p: { fig: ['a_happy', 600, 640], cast: [['c_manager', 1450, 660]], props: [['hourglass', 1000, 320, 170, 0.3]], tags: [['अधिकार', 'अपने समय पर अधिकार', 1000, 160, MUSTARD], ['छह महीने', '6 महीने की बचत', 600, 230]], texts: [['मजबूरी', 'मजबूरी में फ़ैसला नहीं', 1000, 860, 44, '#7fd3a8']] } },
  { k: 'अनन्या के कई दोस्त', t: 'scene', bg: 'bg_cafe', p: { cast: [['c_phone', 500, 640], ['c_colleague', 820, 620]], props: [['phone', 1250, 400, 120, 'नया फ़ोन'], ['coins', 1500, 600, 200, 'तनख़्वाह', { y: 300, s: 0.4, at: 'बाहर खाना' }]], tags: [['तनख़्वाह', 'तनख़्वाह ↑ = ख़र्च ↑', 1350, 200, RUST], ['कपड़ा', 'नया कपड़ा', 1250, 560], ['बाहर खाना', 'हर हफ़्ते बाहर खाना', 1300, 700]] } },
  { k: 'अनन्या ने एक सीधा नियम', t: 'scene', bg: 'bg_desk', p: { fig: ['a_happy', 520, 640], props: [['coins', 960, 380, 200, 0.4, { x: 380, y: 200, s: 0.6, at: 'अपने आप' }], ['piggy', 1400, 640, 300, 0.3]], tags: [['नियम', 'तनख़्वाह आते ही → अपने आप बचत', 1150, 200, MUSTARD]], texts: [['इच्छाशक्ति', 'इच्छाशक्ति पर नहीं टिका', 1300, 900, 42, '#7fd3a8']] } },
  { k: 'ध्यान दीजिए, यह वही बात', t: 'scene', bg: 'bg_plain', p: { props: [['books', 960, 520, 260, 0.2]], tags: [['क्लियर', 'क्लियर: सही काम आसान बनाइए', 960, 220, TEAL], ['काह्नमन से', 'काह्नमन: तेज़ दिमाग़ को पहले से सही दिशा दीजिए', 960, 820, RUST]] } },
  // 5 — meaning
  { k: 'पाँचवाँ धोखा, हालात', t: 'chapter', bg: 'bg_plain', p: { n: '5', kicker: 'धोखा 5' } },
  { k: 'पाँचवीं किताब बाक़ी', t: 'icon', bg: 'bg_plain', p: { prop: 'books', w: 300, title: "Man's Search for Meaning", sub: ['ऑस्ट्रिया', 'विक्टर फ़्रैंकल · मनोचिकित्सक, ऑस्ट्रिया'] } },
  { k: 'दूसरे विश्व युद्ध में', t: 'scene', bg: 'bg_dawn', p: { tags: [[0.4, 'दूसरा विश्व युद्ध · नाज़ी यातना शिविर', 960, 160]] } },
  { k: 'वहाँ उन्होंने एक बात देखी', t: 'scene', bg: 'bg_dawn', p: { props: [['lantern', 960, 520, 220, 'जीने की']], tags: [['जीने की', 'जीने की एक वजह', 960, 230, MUSTARD], ['इंतज़ार', 'कोई इंतज़ार करता इंसान', 520, 760], ['अधूरा काम', 'कोई अधूरा काम', 1400, 760]] } },
  { k: 'उनका सबसे मशहूर विचार', t: 'big', bg: 'bg_dawn', p: { lines: [[0, 'सब कुछ छीना जा सकता है…', 64, CREAM], ['सिवाय', 'सिवाय एक चीज़ के', 70, MUSTARD], ['रवैया', 'अपना रवैया चुनने की आज़ादी', 76, '#7fd3a8']], prop: ['key', 1580, 520, 200, 'रवैया'] } },
  { k: 'फ़्रैंकल कहते हैं कि हर घटना', t: 'scene', bg: 'bg_plain', p: { tags: [[0.3, 'घटना', 420, 520, RUST], ['प्रतिक्रिया', 'प्रतिक्रिया', 1500, 520, TEAL]], props: [['key', 960, 520, 170, 'जगह']], texts: [['जगह', 'बीच की छोटी-सी जगह', 960, 340, 44, MUSTARD], ['आज़ादी', 'यहीं हमारी आज़ादी है', 960, 760, 48, '#7fd3a8']] } },
  { k: 'फ़्रैंकल ने यह भी देखा', t: 'scene', bg: 'bg_mountain', p: { fig: ['a_stand', 600, 560], props: [['lantern', 1350, 360, 200, 'मक़सद']], tags: [['मक़सद', 'भविष्य का मक़सद', 1350, 560, MUSTARD]], texts: [['कैसे को', '"क्यों" हो, तो "कैसे" सह लेते हैं', 1200, 800, 44, '#7fd3a8']] } },
  { k: 'अर्थ कहाँ मिलता है', t: 'chapter', bg: 'bg_plain', p: { n: '5', kicker: 'धोखा 5 · आगे' } },
  { k: 'फ़्रैंकल के अनुसार जीवन', t: 'list', p: { title: 'जीवन का अर्थ: तीन स्रोत', items: [['पहला, कोई काम', 'कोई काम या रचना', 'laptop'], ['प्रेम', 'प्रेम और गहरा जुड़ाव', 'lantern'], ['रवैया', 'न बदलने वाले दुख के प्रति रवैया', 'compass']] } },
  { k: 'इसका मतलब यह नहीं कि दुख', t: 'compare', p: { head: [0, 'दुख अच्छा नहीं है'], left: { title: 'टाला जा सकता है', prop: 'bell', mark: 'check', note: '→ टालिए', at: 'टाला जा सकता' }, right: { title: 'टाला नहीं जा सकता', prop: 'lantern', at: 'टाला नहीं', note: '→ उसमें भी अर्थ ढूँढ़िए', mark: 'check', markAt: 'अर्थ' } } },
  { k: 'अनन्या की नौकरी', t: 'scene', bg: 'bg_bedroom', p: { fig: ['a_sad', 760, 420], poses: [['ख़ुद से पूछा', 'a_think', 640]], props: [['calendar', 1450, 380, 220, 'दो हफ़्ते']], thought: [['मेरे हाथ', 'इसमें मेरे हाथ में क्या है?', 1250, 600]] } },
  { k: 'जवाब छोटा था', t: 'list', p: { title: 'जवाब छोटा था', items: [['ढाँचा', 'रोज़ का ढाँचा', 'calendar'], ['सीखना', 'रोज़ 1 घंटा सीखना', 'notebook'], ['मिलना', 'हर हफ़्ते लोगों से मिलना', 'c_colleague']], end: ['बेबसी का एहसास', 'हालात नहीं, बेबसी बदली'] } },
  // synthesis
  { k: 'पाँचों धोखे, एक धागा', t: 'chapter', bg: 'bg_plain', p: { n: '★', kicker: 'सब एक साथ' } },
  { k: 'अब इन पाँचों किताबों', t: 'thread', bg: 'bg_plain', p: {} },
  { k: 'तीन आम ग़लतफ़हमियाँ', t: 'chapter', bg: 'bg_plain', p: { n: '?', kicker: 'सावधान' } },
  { k: 'इन विचारों को सुनकर', t: 'icon', bg: 'bg_plain', p: { prop: 'bulb', title: 'तीन ग़लतफ़हमियाँ' } },
  { k: 'पहली, कि भावनाएँ दुश्मन', t: 'compare', p: { left: { title: 'मशीन की तरह सोचो', prop: 'wheel', w: 240, mark: 'cross', markAt: 'ऐसा नहीं' }, right: { title: 'कब रुकना है, पहचानो', prop: 'tortoise', at: 'तेज़ दिमाग़', mark: 'check', markAt: 'रुककर' } } },
  { k: 'दूसरी, कि छोटी आदतों', t: 'scene', bg: 'bg_mountain', p: { fig: ['a_run', 520, 520], texts: [['छोटे सपने', 'छोटी आदत = छोटा सपना?', 1250, 250, 46, RUST], ['भरोसेमंद', 'छोटे क़दम = बड़े सपनों का रास्ता', 1250, 420, 46, '#7fd3a8']], crosses: [['असल में', 1640, 250]] } },
  { k: 'तीसरी, कि फ़्रैंकल की बात', t: 'scene', bg: 'bg_dawn', p: { props: [['chainbroken', 960, 520, 380, 'बदलिए']], texts: [['चुपचाप', 'दुख चुपचाप सहो?', 960, 230, 48, RUST], ['बदलिए', 'जो बदल सकता है, उसे बदलिए', 960, 780, 46, '#7fd3a8']], crosses: [['ख़ुद कहते', 1260, 230]], tags: [['बहाना', 'रवैया ≠ कोशिश छोड़ने का बहाना', 960, 900, MUSTARD]] } },
  // India
  { k: 'भारतीय संदर्भ में', t: 'chapter', bg: 'bg_plain', p: { n: '🇮🇳', kicker: 'हमारे यहाँ' } },
  { k: 'हमारे यहाँ कुछ बातें', t: 'scene', bg: 'bg_city', p: { fig: ['a_stand', 960, 600], tags: [[0.3, 'और भी ज़रूरी, क्योंकि…', 960, 160, MUSTARD]] } },
  { k: 'पहली, हमारे आसपास तुलना', t: 'scene', bg: 'bg_market', p: { fig: ['a_worried', 960, 620], cast: [['c_uncle', 450, 640], ['c_grandma', 1500, 580]], props: [['key', 450, 330, 120, 'गाड़ी'], ['notebook', 1500, 330, 150, 'नंबर']], tags: [['काफ़ी', '"काफ़ी" की समझ = सबसे बड़ी सुरक्षा', 960, 160, '#7fd3a8']] } },
  { k: 'दूसरी, सस्ते डेटा', t: 'scene', bg: 'bg_city', p: { fig: ['a_phone', 1350, 620], props: [['phone', 560, 500, 200, 0.2], ['bell', 760, 320, 110, 0.6], ['bell', 380, 300, 100, 0.9]], texts: [['आसान', 'सस्ता डेटा = आसान भटकाव', 560, 780, 44, RUST], ['ज़रूरत', 'गहरा काम: अब ज़रूरत', 560, 880, 44, '#7fd3a8']] } },
  { k: 'तीसरी, हमारे यहाँ धैर्य', t: 'icon', bg: 'bg_mountain', p: { prop: 'lantern', title: 'धैर्य और संयम की पुरानी परंपरा', sub: ['आज की भाषा', 'पुरानी समझ, आज की भाषा में'] } },
  // 7-day experiment
  { k: 'सात दिन का प्रयोग', t: 'chapter', bg: 'bg_plain', p: { n: '7', kicker: 'प्रयोग' } },
  { k: 'बातें समझना आसान', t: 'big', bg: 'bg_plain', p: { lines: [[0, 'समझना आसान', 90, CREAM], [0.8, 'जीना कठिन', 110, RUST], ['सात दिनों', 'एक छोटा प्रयोग: 7 दिन', 60, MUSTARD]], prop: ['calendar', 1560, 520, 300, 'सात दिनों'] } },
  { k: 'पहला दिन, एक बड़ा फ़ैसला', t: 'days', bg: 'bg_plain', p: { day: 0, fig: ['a_write', 520, 420], task: 'बड़ा फ़ैसला: पहला जवाब लिखिए, फिर जाँचिए', props: [['tortoise', 1300, 620, 240, 'जाँचिए']] } },
  { k: 'दूसरा दिन, एक आदत चुनिए', t: 'days', bg: 'bg_plain', p: { day: 1, fig: ['a_shoes', 520, 560], task: 'एक आदत → 2 मिनट का संस्करण', props: [['clock', 1250, 620, 220, 0.4]] } },
  { k: 'तीसरा दिन, अपने माहौल', t: 'days', bg: 'bg_plain', p: { day: 2, fig: ['a_happy', 520, 580], task: 'माहौल बदलिए', props: [['shoes', 1050, 640, 220, 'सामने रखिए'], ['phone', 1550, 640, 130, 'दूर', { x: 260, r: 20, at: 'दूर' }]], checks: [['सामने रखिए', 1050, 470]] } },
  { k: 'चौथा दिन, एक घंटा', t: 'days', bg: 'bg_plain', p: { day: 3, fig: ['a_desk', 600, 520], task: '1 घंटा, बिना फ़ोन, एक कठिन काम', props: [['clock', 1350, 620, 220, 0.4]] } },
  { k: 'पाँचवाँ दिन, अपने ख़र्च', t: 'days', bg: 'bg_plain', p: { day: 4, fig: ['a_think', 520, 580], task: 'ख़र्च देखिए · "काफ़ी" लिखिए', props: [['scale', 1300, 640, 280, 0.4]] } },
  { k: 'छठा दिन, अपनी तनख़्वाह', t: 'days', bg: 'bg_plain', p: { day: 5, fig: ['a_happy', 520, 580], task: 'तनख़्वाह का हिस्सा → अपने आप बचत', props: [['piggy', 1300, 640, 280, 0.4]] } },
  { k: 'सातवाँ दिन, अपनी किसी', t: 'days', bg: 'bg_plain', p: { day: 6, fig: ['a_think', 520, 580], task: 'एक परेशानी: "मेरे हाथ में क्या है?"', props: [['key', 1300, 640, 200, 0.4]] } },
  // ending
  { k: 'आख़िरी बात', t: 'chapter', bg: 'bg_plain', p: { n: '✦', kicker: 'आख़िर में' } },
  { k: 'अनन्या का अगला नया साल', t: 'scene', bg: 'bg_rooftop', p: { fig: ['a_happy', 700, 660], crosses: [['बड़ा वादा', 1350, 300]], texts: [['बड़ा वादा', 'बड़ा वादा', 1350, 300, 50, RUST]], tags: [['धोखों को पहचानेगी', 'धोखों को पहचानना', 1350, 480, '#7fd3a8'], ['छोटा, सही', 'हर दिन एक छोटा, सही चुनाव', 1350, 600, MUSTARD]] } },
  { k: 'यही इन पाँचों किताबों', t: 'face', bg: 'bg_plain', p: { head: 'h_happy', ring: TEAL, texts: [['दुश्मन नहीं', 'दिमाग़ दुश्मन नहीं', 1400, 320, 50, '#7fd3a8'], ['पुरानी मशीन', 'एक बहुत पुरानी मशीन', 1400, 460, 46]], props: [['bulb', 1450, 720, 170, 'समझकर']] } },
  { k: 'और जो इंसान अपने दिमाग़', t: 'scene', bg: 'bg_mountain', p: { props: [['wheel', 960, 520, 420, 0.3]], texts: [['ड्राइवर', 'ड्राइवर', 700, 820, 64, '#7fd3a8'], ['सवारी', 'सिर्फ़ सवारी नहीं', 1250, 820, 50, RUST]] } },
  { k: 'यह वीडियो इन पाँच', t: 'icon', bg: 'bg_plain', p: { prop: 'books', w: 280, y: 440, title: 'दिमाग़ के पाँच धोखे', texts: [[0.5, 'पाँच किताबों के विचारों पर आधारित स्वतंत्र प्रस्तुति · अनुवाद नहीं', 960, 700, 34], ['उदाहरण', 'उदाहरण समझाने के लिए हैं', 960, 780, 34], ['विकल्प नहीं', 'वित्तीय या मानसिक स्वास्थ्य सलाह का विकल्प नहीं', 960, 860, 34, RUST]] } },
];

function build() {
  // intro
  {
    const L = layer(0, LEAD, 'cut', 'bg_plain');
    camMove(L, { scale: 1.08 }, { scale: 1.0 }, 'power2.out');
    rings(L.cam, 1380, 540, 360, 0.1, [TEAL, RUST, MUSTARD, CREAM]);
    const bk = img(L.cam, 'books', 1380, 560, 380); pop(bk, 0.6); float(bk, 0.6, LEAD + 1, 8, 2);
    rise(title(L.cam, 'दिमाग़ के', 600, 400, 110, CREAM), 0.3);
    rise(title(L.cam, 'पाँच धोखे', 600, 570, 170, MUSTARD), 0.6);
    pop(label(L.cam, '5 किताबें · 5 सबक़', 600, 760, 46, INK, CREAM), 1.4);
  }
  CUR = 0;
  const R = SHOTS.map(s => { const i = I(s.k); CUR = i; return Object.assign({ i }, s); });
  R.forEach((s, n) => {
    const nx = R[n + 1];
    const i1 = nx ? nx.i - 1 : TIMING.length - 1;
    const t0 = TIMING[s.i].start + LEAD - 0.2;
    const t1 = nx ? TIMING[nx.i].start + LEAD - 0.2 : TIMING[i1].end + LEAD + 0.6;
    const L = layer(t0, t1, s.t === 'chapter' ? (n % 2 ? 'wipe' : 'diag') : (s.tr || TRANS[n % TRANS.length]), s.bg || null);
    const sp = { a: t0 + 0.2, b: TIMING[i1].end + LEAD, i0: s.i, i1 };
    const cm = CAMS[n % CAMS.length];
    camMove(L, Object.assign({}, cm[0]), Object.assign({}, cm[1]));
    if (s.bg && s.bg !== 'bg_plain') bgDrift(L, n % 2 ? -40 : 40);
    T[s.t](L, sp, s.p || {});
  });
  // outro
  const last = TIMING[TIMING.length - 1], o0 = last.end + LEAD + 0.6;
  const L = layer(o0, o0 + 4, 'iris', 'bg_plain');
  camMove(L, { scale: 1.06 }, { scale: 1.0 });
  rings(L.cam, 1380, 540, 330, o0, [TEAL, RUST, MUSTARD, CREAM]);
  const wh = img(L.cam, 'wheel', 1380, 540, 360); pop(wh, o0 + 0.4);
  HOOKS.push(t => { if (t > o0) gsap.set(wh, { rotation: Math.sin((t - o0) * 1.5) * 25 }); });
  rise(title(L.cam, 'ड्राइवर बनिए', 620, 450, 130, MUSTARD), o0 + 0.3);
  rise(title(L.cam, 'धन्यवाद', 620, 640, 80, CREAM), o0 + 0.9);
  window.VIDEO_END = o0 + 4;
  buildSubs(1e9);
}
