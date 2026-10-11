// Deterministic motion engine: one paused GSAP timeline + per-frame hooks.
// window.renderFrame(t) seeks everything to time t (seconds of video).
const W = 1920, H = 1080, FPS = 30;
const LEAD = 4.0;                       // intro seconds before narration starts
const INK = '#26392b', MUSTARD = '#d4a640', CREAM = '#f3e7cf', OLIVE = '#6d6a3a', RUST = '#b5522f', SKIN = '#caa143';
const TL = gsap.timeline({ paused: true });
const HOOKS = [];
const A = n => `../assets/${n}.png`;
let ENV = [], TIMING = [];

// ---------- small utils ----------
function el(tag, parent, css = {}, attrs = {}) {
  const e = tag === 'svg' ? document.createElementNS('http://www.w3.org/2000/svg', 'svg') : document.createElement(tag);
  Object.assign(e.style, css);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
}
function rnd(seed) { const x = Math.sin(seed * 12.9898) * 43758.5453; return x - Math.floor(x); }
function envAt(t) { const i = Math.floor((t - LEAD) * FPS); return i >= 0 && i < ENV.length ? ENV[i] : 0; }

// image placed by centre (x,y) with width w
function img(parent, name, x, y, w, css = {}) {
  const e = el('img', parent, Object.assign({ position: 'absolute', left: x + 'px', top: y + 'px', width: w + 'px' }, css),
    { src: name.includes('/') ? name : A(name) });
  gsap.set(e, { xPercent: -50, yPercent: -50 });
  return e;
}
function box(parent, x, y, css = {}) {
  const e = el('div', parent, Object.assign({ position: 'absolute', left: x + 'px', top: y + 'px' }, css));
  gsap.set(e, { xPercent: -50, yPercent: -50 });
  return e;
}
function text(parent, str, x, y, css = {}) {
  const e = box(parent, x, y, Object.assign({ fontFamily: "'Baloo 2'", fontWeight: 800, color: INK, fontSize: '64px',
    whiteSpace: 'nowrap', lineHeight: 1.15, textAlign: 'center' }, css));
  e.innerHTML = str;
  return e;
}
function tag(parent, str, x, y, css = {}) {
  return text(parent, str, x, y, Object.assign({ fontSize: '40px', background: CREAM, color: INK, padding: '6px 26px 2px',
    borderRadius: '14px', border: `4px solid ${INK}`, boxShadow: `6px 6px 0 ${INK}` }, css));
}
// svg overlay with a path that draws on (stroke-dashoffset with pathLength=1)
function inkPath(parent, d, css = {}, opts = {}) {
  const s = el('svg', parent, Object.assign({ position: 'absolute', left: 0, top: 0, width: W + 'px', height: H + 'px', overflow: 'visible', pointerEvents: 'none' }, css));
  s.setAttribute('viewBox', `0 0 ${W} ${H}`);
  s.innerHTML = `<path d="${d}" pathLength="1" fill="${opts.fill || 'none'}" stroke="${opts.color || INK}" stroke-width="${opts.width || 9}"
     stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1" stroke-dashoffset="1"/>`;
  return s.firstChild;
}
function draw(path, t, dur = 0.6) { TL.to(path, { strokeDashoffset: 0, duration: dur, ease: 'power2.inOut' }, t); }
function pop(e, t, opts = {}) {
  TL.fromTo(e, { scale: 0, rotation: opts.rot || -8, autoAlpha: 0 },
    { scale: 1, rotation: 0, autoAlpha: 1, duration: opts.dur || 0.5, ease: 'back.out(2)' }, t);
}
function rise(e, t, opts = {}) {
  TL.fromTo(e, { y: opts.from || 60, autoAlpha: 0 }, { y: 0, autoAlpha: 1, duration: opts.dur || 0.6, ease: 'power3.out' }, t);
}
function out(e, t, dur = 0.3) { TL.to(e, { autoAlpha: 0, scale: 0.8, duration: dur, ease: 'power2.in' }, t); }
function check(parent, x, y, s, t, color = INK) {
  const p = inkPath(parent, `M${x - 30 * s} ${y} L${x - 8 * s} ${y + 24 * s} L${x + 36 * s} ${y - 30 * s}`, {}, { color, width: 12 * s });
  draw(p, t, 0.35); return p;
}
function cross(parent, x, y, s, t, color = RUST) {
  const a = inkPath(parent, `M${x - 30 * s} ${y - 30 * s} L${x + 30 * s} ${y + 30 * s}`, {}, { color, width: 12 * s });
  const b = inkPath(parent, `M${x + 30 * s} ${y - 30 * s} L${x - 30 * s} ${y + 30 * s}`, {}, { color, width: 12 * s });
  draw(a, t, 0.2); draw(b, t + 0.15, 0.2);
}
function arrow(parent, x1, y1, x2, y2, t, opts = {}) {
  const bend = opts.bend || 0;
  const mx = (x1 + x2) / 2 - (y2 - y1) * bend, my = (y1 + y2) / 2 + (x2 - x1) * bend;
  const ang = Math.atan2(y2 - my, x2 - mx), L = 28;
  const p = inkPath(parent, `M${x1} ${y1} Q${mx} ${my} ${x2} ${y2}`, {}, opts);
  const h = inkPath(parent, `M${x2 - L * Math.cos(ang - 0.5)} ${y2 - L * Math.sin(ang - 0.5)} L${x2} ${y2} L${x2 - L * Math.cos(ang + 0.5)} ${y2 - L * Math.sin(ang + 0.5)}`, {}, opts);
  draw(p, t, opts.dur || 0.5); draw(h, t + (opts.dur || 0.5) - 0.05, 0.2);
}
// clip-path reveal that stays fully hidden before it starts
function reveal(e, t, from, to, dur = 0.6, ease = 'power3.inOut') {
  TL.set(e, { visibility: 'hidden' }, 0);
  TL.set(e, { visibility: 'inherit' }, t);
  TL.fromTo(e, { clipPath: from }, { clipPath: to, duration: dur, ease, immediateRender: false }, t);
}
// subtle continuous wobble so held objects never freeze
function float(e, t0, t1, amp = 8, seed = 1) {
  HOOKS.push(t => { if (t < t0 - 1 || t > t1 + 1) return;
    gsap.set(e, { y: Math.sin((t + seed) * 1.7) * amp, rotation: Math.sin((t + seed * 2) * 1.1) * amp * 0.25 }); });
}

// ---------- shots / layers ----------
const world = () => document.getElementById('world');
let prevLayer = null;
function layer(t0, t1, trans = 'fade', bg = null) {
  const L = el('div', world(), { position: 'absolute', inset: 0, overflow: 'hidden', visibility: 'hidden' });
  const cam = el('div', L, { position: 'absolute', inset: 0, transformOrigin: '50% 50%' });
  if (bg) { const b = el('img', cam, { position: 'absolute', left: '-4%', top: '-4%', width: '108%', height: '108%', objectFit: 'cover' }, { src: A(bg) }); cam.bgImg = b; }
  const d = 0.6;
  TL.set(L, { visibility: 'visible', zIndex: Math.round(t0 * 10) }, t0);
  const fx = {
    fade: () => TL.fromTo(L, { opacity: 0 }, { opacity: 1, duration: d, ease: 'none' }, t0),
    wipe: () => TL.fromTo(L, { clipPath: 'inset(0% 100% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: d, ease: 'power3.inOut' }, t0),
    wipeUp: () => TL.fromTo(L, { clipPath: 'inset(100% 0% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: d, ease: 'power3.inOut' }, t0),
    iris: () => TL.fromTo(L, { clipPath: 'circle(0% at 50% 50%)' }, { clipPath: 'circle(80% at 50% 50%)', duration: d + 0.2, ease: 'power2.in' }, t0),
    diag: () => TL.fromTo(L, { clipPath: 'polygon(0% 0%, 0% 0%, 0% 0%, 0% 0%)' }, { clipPath: 'polygon(0% 0%, 200% 0%, 0% 200%, 0% 100%)', duration: d + 0.1, ease: 'power2.inOut' }, t0),
    push: () => TL.fromTo(L, { x: W }, { x: 0, duration: d, ease: 'power3.inOut' }, t0),
    zoom: () => TL.fromTo(L, { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: d, ease: 'power2.out' }, t0),
    cut: () => {},
  };
  (fx[trans] || fx.fade)();
  if (prevLayer) TL.set(prevLayer, { visibility: 'hidden' }, t0 + 1.0);
  prevLayer = L;
  L.cam = cam; L.t0 = t0; L.t1 = t1;
  return L;
}
// camera move over the shot
function camMove(L, from, to, ease = 'sine.inOut') {
  TL.fromTo(L.cam, from, Object.assign({ duration: L.t1 - L.t0 + 1, ease }, to), L.t0);
}
// parallax background drift
function bgDrift(L, dx = -40, dy = 0) {
  if (L.cam.bgImg) TL.fromTo(L.cam.bgImg, { x: 0, y: 0 }, { x: dx, y: dy, duration: L.t1 - L.t0 + 1, ease: 'none' }, L.t0);
}

// ---------- puppet ----------
// Rig in body.png pixel units (249x618). (x,y) = feet centre on stage, s = scale.
const MOUTH = {
  smile: `<path d="M18 30 Q80 62 142 30" stroke="${INK}" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M50 52 Q80 60 110 52" stroke="#8a5a2e" stroke-width="5" fill="none" stroke-linecap="round"/>`,
  neutral: `<path d="M34 40 Q80 46 126 40" stroke="${INK}" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M56 56 Q80 60 104 56" stroke="#8a5a2e" stroke-width="5" fill="none" stroke-linecap="round"/>`,
  frown: `<path d="M34 52 Q80 26 126 52" stroke="${INK}" stroke-width="9" fill="none" stroke-linecap="round"/>`,
};
function openMouth(o, round) {   // o: 0..1 openness
  const rx = round ? 26 + 8 * o : 50 - 6 * o, ry = 6 + 26 * o;
  const teeth = !round && o > 0.45 ? `<rect x="${80 - rx * 0.7}" y="${40 - ry + 3}" width="${rx * 1.4}" height="${ry * 0.35}" fill="${CREAM}"/>` : '';
  return `<clipPath id="mc"><ellipse cx="80" cy="40" rx="${rx}" ry="${ry}"/></clipPath>
   <ellipse cx="80" cy="40" rx="${rx}" ry="${ry}" fill="#3a1f17"/>
   <g clip-path="url(#mc)">${teeth}<ellipse cx="80" cy="${40 + ry * 0.9}" rx="${rx * 0.7}" ry="${ry * 0.5}" fill="#b0503c"/></g>
   <ellipse cx="80" cy="40" rx="${rx}" ry="${ry}" fill="none" stroke="${INK}" stroke-width="7"/>`;
}
let GUYN = 0;
function Guy(parent, x, y, s, opts = {}) {
  const id = ++GUYN;
  const g = el('div', parent, { position: 'absolute', left: (x - 124.5) + 'px', top: (y - 618) + 'px', width: '249px', height: '618px', transformOrigin: '50% 100%' });
  gsap.set(g, { scale: s });
  const P = (n, css) => el('img', g, Object.assign({ position: 'absolute' }, css), { src: A(n) });
  // jointed arms: shoulder -> upper arm -> elbow -> forearm+hand (always connected)
  const ARM = (side, left) => {
    const sh = el('div', g, { position: 'absolute', left, top: '116px', width: '73px', height: '133px', transformOrigin: '50% 4%' });
    el('img', sh, { position: 'absolute', left: 0, top: 0, width: '73px' }, { src: A(side + '_up') });
    const el_ = el('div', sh, { position: 'absolute', left: 0, top: '123px', width: '73px', height: '110px', transformOrigin: '50% 0%' });
    el('img', el_, { position: 'absolute', left: 0, top: '-9px', width: '73px' }, { src: A(side + '_lo') });
    // forearm sits under the upper arm so the elbow overlap is hidden
    sh.insertBefore(el_, sh.firstChild);
    sh.fore = el_;
    return sh;
  };
  const armL = ARM('armL', '-8px'), armR = ARM('armR', '184px');
  const hg = el('div', g, { position: 'absolute', left: '59px', top: '-150px', width: '482px', height: '708px', transformOrigin: '0 0' });
  const hk = 0.27; gsap.set(hg, { scale: hk });
  const headPivot = el('div', hg, { position: 'absolute', inset: 0, transformOrigin: '50% 90%' });
  const head = el('img', headPivot, { position: 'absolute', left: 0, top: 0, width: '482px' }, { src: A(opts.head || 'head') });
  const mouth = el('svg', headPivot, { position: 'absolute', left: '164px', top: '469px', width: '160px', height: '80px', overflow: 'visible' }, { viewBox: '0 0 160 80' });
  const lids = el('svg', headPivot, { position: 'absolute', left: 0, top: 0, width: '482px', height: '708px', overflow: 'visible', visibility: 'hidden' }, { viewBox: '0 0 482 708' });
  lids.innerHTML = [[151, 318], [333, 318]].map(([cx, cy]) =>
    `<ellipse cx="${cx}" cy="${cy}" rx="52" ry="24" fill="${SKIN}"/><path d="M${cx - 50} ${cy + 2} Q${cx} ${cy + 18} ${cx + 50} ${cy + 2}" stroke="${INK}" stroke-width="8" fill="none" stroke-linecap="round"/>`).join('');
  const body = P('body', { left: 0, top: 0, width: '249px' });
  const guy = { g, armL, armR, hg, headPivot, head, mouth, lids, body, talks: [], expr: [[0, opts.mouth || 'smile']], heads: [], lastM: '' };
  guy.say = (t0, t1) => guy.talks.push([t0, t1]);
  guy.face = (t, m) => guy.expr.push([t, m]);
  guy.headSwap = (t, n) => TL.set(head, { attr: { src: A(n) } }, t);
  guy.pose = () => {};   // arm gestures disabled by request: arms stay relaxed
  guy.walk = (t0, t1, fromX) => {
    TL.fromTo(g, { x: fromX - x }, { x: 0, duration: t1 - t0, ease: 'power1.out' }, t0);
    HOOKS.push(t => { if (t < t0 || t > t1) return; const p = (t - t0) * 9;
      gsap.set(g, { y: -Math.abs(Math.sin(p)) * 14 }); });
  };
  HOOKS.push(t => {
    if (g.closest('[style*="visibility: hidden"]') && 0) return;
    // breathing + idle head motion
    const ph = t + id * 1.3;
    gsap.set(body, { scaleY: 1 + Math.sin(ph * 2.2) * 0.006, transformOrigin: '50% 100%' });
    gsap.set(headPivot, { rotation: Math.sin(ph * 0.9) * 2.2, y: Math.sin(ph * 2.2) * -3 });
    // blink: deterministic every ~3s
    const cyc = 3.1 + rnd(id) * 1.2, k = (t + id) % cyc;
    lids.style.visibility = (k < 0.13 && head.getAttribute('src').endsWith('/head.png')) ? 'visible' : 'hidden';
    // mouth
    let m = guy.expr[0][1];
    for (const [tt, mm] of guy.expr) if (t >= tt) m = mm;
    const tired = !head.getAttribute('src').endsWith('/head.png');
    let html = tired ? '' : MOUTH[m];
    for (const [a, b] of guy.talks) if (t >= a && t <= b) {
      const e = envAt(t);
      if (e > 0.12) { const round = Math.floor(t * 7 + id) % 5 === 0; html = openMouth(Math.min(1, e * 0.9), round); }
      else html = MOUTH.neutral;
    }
    if (html !== guy.lastM) { mouth.innerHTML = html; guy.lastM = html; }
  });
  return guy;
}
// static cast member with idle sway
function person(parent, name, x, y, h, seed = 1) {
  const e = el('img', parent, { position: 'absolute', left: x + 'px', top: (y - h) + 'px', height: h + 'px', transformOrigin: '50% 100%' }, { src: A(name) });
  gsap.set(e, { xPercent: -50 });
  HOOKS.push(t => gsap.set(e, { rotation: Math.sin(t * 1.3 + seed) * 1.2, scaleY: 1 + Math.sin(t * 2 + seed) * 0.006 }));
  return e;
}
function bubble(parent, str, x, y, t, css = {}) {
  const b = box(parent, x, y, Object.assign({ fontFamily: "'Baloo 2'", fontWeight: 800, fontSize: '36px', color: INK, background: CREAM,
    padding: '10px 28px 4px', borderRadius: '30px', border: `4px solid ${INK}`, whiteSpace: 'nowrap' }, css));
  b.innerHTML = str + `<div style="position:absolute;left:30px;bottom:-22px;width:0;height:0;border-left:14px solid transparent;border-right:14px solid transparent;border-top:22px solid ${INK}"></div>`;
  pop(b, t); return b;
}

// ---------- sentence timing ----------
function S(i) { const s = TIMING[i]; const nx = TIMING[i + 1]; return { a: s.start + LEAD, b: s.end + LEAD, next: (nx ? nx.start : s.end + 0.6) + LEAD, text: s.text }; }
// approx time a word is spoken inside sentence i (by character position)
function W_(i, word, frac = 0) {
  const s = TIMING[i]; const idx = s.text.indexOf(word);
  const p = idx < 0 ? frac : idx / s.text.length;
  return s.start + LEAD + p * (s.end - s.start);
}

// ---------- subtitles ----------
function buildSubs(maxT) {
  const box_ = document.getElementById('subs');
  TIMING.forEach((s, i) => {
    if (s.start + LEAD > maxT) return;
    if (s.head) return;   // headings are shown as big cards
    const parts = []; let cur = '';
    for (const w of s.text.split(' ')) {
      if ((cur + ' ' + w).trim().length > 58 && cur) { parts.push(cur.trim()); cur = ''; }
      cur += ' ' + w;
      if (/[,،]$/.test(w) && cur.length > 30) { parts.push(cur.trim()); cur = ''; }
    }
    if (cur.trim()) parts.push(cur.trim());
    const total = parts.reduce((a, p) => a + p.length, 0);
    let t = s.start + LEAD; const dur = s.end - s.start;
    parts.forEach((p, k) => {
      const d = dur * p.length / total;
      const e = el('div', box_, { position: 'absolute', left: '50%', bottom: '0', transform: 'translateX(-50%)', whiteSpace: 'nowrap', visibility: 'hidden' });
      e.textContent = p;
      TL.set(e, { visibility: 'visible' }, t);
      const end = k === parts.length - 1 ? (TIMING[i + 1] ? Math.min(TIMING[i + 1].start + LEAD, s.end + LEAD + 0.5) : s.end + LEAD + 0.5) : t + d;
      TL.set(e, { visibility: 'hidden' }, end);
      t += d;
    });
  });
}

window.renderFrame = function (t) {
  TL.seek(t, false);
  for (const h of HOOKS) h(t);
  // print "boil": shift grain every 2 frames
  const f = Math.floor(t * FPS / 3);
  gsap.set('#grain', { backgroundPosition: `${Math.floor(rnd(f) * 400)}px ${Math.floor(rnd(f + 7) * 400)}px` });
};
