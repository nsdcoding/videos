// ============================================================
// Tiny deterministic motion engine.
// Everything on screen is a pure function of time t, so any frame
// can be rendered in any order (lets us render in parallel).
// ============================================================
(function () {
  const PAUSE = window.PAUSE || {};
  const LINES = window.LINES;
  const LT = {};
  let t = 1.6, prev = null;
  for (const l of LINES) {
    if (prev && l.chap !== prev) { t += 3.4; l.chapStart = true; }
    l.start = t; l.end = t + l.dur; LT[l.id] = l;
    t = l.end + 0.34 + (PAUSE[l.id] || 0);
    prev = l.chap;
  }
  window.TOTAL = t + 7.5;
  window.LT = LT;

  // ---- time helpers ----
  window.T = (id, off = 0) => { if (!LT[id]) throw new Error('no line ' + id); return LT[id].start + off; };
  window.END = (id, off = 0) => LT[id].end + off;
  window.DUR = (id) => LT[id].dur;
  window.M = (id, frac) => LT[id].start + LT[id].dur * frac;
  // time at which a word is (approximately) spoken inside a line
  window.W = (id, word, off = 0) => {
    const l = LT[id]; const i = l.text.toLowerCase().indexOf(word.toLowerCase());
    if (i < 0) { console.warn('word not found', id, word); return l.start + off; }
    return l.start + l.dur * (i / l.text.length) * 0.97 + off;
  };

  // ---- easing ----
  const E = {
    lin: p => p,
    io: p => p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2,
    out: p => 1 - Math.pow(1 - p, 3),
    in: p => p * p * p,
    back: p => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2); },
    el: p => p === 0 ? 0 : p === 1 ? 1 : Math.pow(2, -10 * p) * Math.sin((p * 10 - .75) * (2 * Math.PI) / 3) + 1,
    step: p => p >= 1 ? 1 : 0,
    expo: p => p === 1 ? 1 : 1 - Math.pow(2, -10 * p),
    sine: p => -(Math.cos(Math.PI * p) - 1) / 2,
  };
  window.EASE = E;

  const DEF = { o: 1, x: 0, y: 0, s: 1, sx: 1, sy: 1, r: 0, cw: 1, ch: 1, cl: 0, bl: 0, dr: 1, n: 0, ty: 1e9, gl: 0, gs: 0, w: null, h: null, sc: 0, br: 1, sat: 1 };
  const tracks = new Map(); // id -> {el, props:{p:[segs]}}
  function tr(id) {
    let r = tracks.get(id);
    if (!r) {
      const el = document.getElementById(id);
      if (!el) throw new Error('missing element #' + id);
      r = { el, props: {}, last: {} }; tracks.set(id, r);
    }
    return r;
  }
  // add a segment: prop goes from v0 (null = current) to v1 between t0 and t0+dur
  function seg(id, p, t0, dur, v0, v1, ease) {
    const r = tr(id); (r.props[p] = r.props[p] || []).push({ t0, t1: t0 + Math.max(dur, 1e-4), v0, v1, e: E[ease] || E.io });
  }
  // animate to values
  window.to = (id, t0, dur, props, ease = 'io') => { for (const p in props) seg(id, p, t0, dur, null, props[p], ease); };
  // animate from explicit values to explicit values
  window.ft = (id, t0, dur, from, too, ease = 'io') => { for (const p in too) seg(id, p, t0, dur, from[p] ?? null, too[p], ease); };
  window.set = (id, t0, props) => { for (const p in props) seg(id, p, t0, 1e-4, null, props[p], 'lin'); };
  // initial values (before anything happens)
  window.init = (id, props) => { const r = tr(id); r.init = Object.assign(r.init || {}, props); };

  // class toggles and text swaps (step functions)
  const steps = [];
  window.cls = (id, t0, name, on = true) => steps.push({ id, t0, kind: 'cls', name, on });
  window.txt = (id, t0, html) => steps.push({ id, t0, kind: 'txt', html });

  // ---- camera ----
  const cam = { segs: [], start: { x: 960, y: 540, z: 1, r: 0 } };
  window.CAM = cam;
  // move camera to target {x,y,z,r}; dip = zoom-out amount mid flight (0..0.6)
  window.cam = (t0, dur, target, opt = {}) => cam.segs.push({ t0, t1: t0 + dur, to: target, dip: opt.dip || 0, e: E[opt.ease || 'io'], drift: opt.drift ?? 1, noCut: !!opt.noCut });
  window.camStart = (s) => Object.assign(cam.start, s);

  function build() {
    for (const [id, r] of tracks) {
      for (const p in r.props) {
        const segs = r.props[p].sort((a, b) => a.t0 - b.t0);
        let cur = r.init && p in r.init ? r.init[p] : DEF[p];
        if (cur === null) cur = p === 'h' ? r.el.offsetHeight : r.el.offsetWidth;
        for (const s of segs) { if (s.v0 === null) s.v0 = cur; cur = s.v1; }
        if (cur === null) cur = 0;
      }
    }
    for (const [id, r] of tracks) if (r.init) for (const p in r.init) if (!r.props[p]) r.props[p] = [{ t0: -1, t1: -0.999, v0: r.init[p], v1: r.init[p], e: E.lin }];
    steps.sort((a, b) => a.t0 - b.t0);
    for (const s of steps) { s.el = document.getElementById(s.id); if (!s.el) throw new Error('missing step el ' + s.id); }
    // camera: resolve from-states with drift between moves
    cam.segs.sort((a, b) => a.t0 - b.t0);
    let st = { ...cam.start }, tEnd = 0, driftOn = 1;
    window.CUTS = [];
    for (const s of cam.segs) {
      s.from = drifted(st, s.t0 - tEnd, driftOn);
      const tx = s.to.x ?? s.from.x, ty = s.to.y ?? s.from.y;
      const dist = Math.hypot(tx - s.from.x, ty - s.from.y);
      if (!s.noCut && (s.dip > 0 || dist > 2000)) { s.cut = true; s.t0 += .3; s.t1 = s.t0 + .001; s.dip = 0; CUTS.push(s.t0); }
      st = { x: s.to.x ?? s.from.x, y: s.to.y ?? s.from.y, z: s.to.z ?? s.from.z, r: s.to.r ?? 0 };
      s.toR = st; tEnd = s.t1; driftOn = s.drift;
    }
    cam.final = { st, tEnd, driftOn };
  }
  // slow continuous push-in while holding, so the frame is never frozen
  function drifted(st, dt, on) {
    return { ...st };
    if (dt <= 0 || !on) return { ...st };
    const k = 1 - Math.exp(-dt / 9);
    return { x: st.x + Math.sin(dt * 0.21) * 10 * on, y: st.y + (1 - Math.cos(dt * 0.17)) * 6 * on, z: st.z * (1 + 0.075 * k * on), r: st.r + Math.sin(dt * 0.13) * 0.25 * on };
  }
  function camAt(t) {
    const S = cam.segs;
    let i = -1;
    for (let k = 0; k < S.length; k++) { if (S[k].t0 <= t) i = k; else break; }
    if (i < 0) return { ...cam.start };
    const s = S[i];
    if (t < s.t1) {
      const p = s.e((t - s.t0) / (s.t1 - s.t0));
      const lerp = (a, b) => a + (b - a) * p;
      let z = Math.exp(lerp(Math.log(s.from.z), Math.log(s.toR.z)));
      if (s.dip) z *= 1 - s.dip * Math.sin(Math.PI * p);
      return { x: lerp(s.from.x, s.toR.x), y: lerp(s.from.y, s.toR.y), z, r: lerp(s.from.r, s.toR.r) };
    }
    return drifted(s.toR, t - s.t1, s.drift);
  }
  window.camAt = camAt;

  function valAt(segs, t) {
    let s = null;
    for (let k = 0; k < segs.length; k++) { if (segs[k].t0 <= t) s = segs[k]; else break; }
    if (!s) return segs[0].v0;
    if (t >= s.t1) return s.v1;
    const p = s.e((t - s.t0) / (s.t1 - s.t0));
    return s.v0 + (s.v1 - s.v0) * p;
  }

  const custom = {};
  window.onProp = (id, fn) => { custom[id] = fn; };
  const perFrame = [];
  window.everyFrame = (fn) => perFrame.push(fn);

  let built = false;
  window.renderAt = function (t) {
    if (!built) { build(); built = true; }
    // steps
    const stState = new Map();
    for (const s of steps) {
      if (s.t0 > t) continue;
      if (s.kind === 'cls') stState.set(s.id + '|c|' + s.name, [s, s.on]);
      else stState.set(s.id + '|t', [s, s.html]);
    }
    for (const s of steps) { // reset items that are not yet active
      const key = s.kind === 'cls' ? s.id + '|c|' + s.name : s.id + '|t';
      if (!stState.has(key)) stState.set(key, [s, s.kind === 'cls' ? !s.on : (s.el.dataset.orig ?? (s.el.dataset.orig = s.el.innerHTML))]);
    }
    for (const [key, [s, v]] of stState) {
      if (s.kind === 'cls') s.el.classList.toggle(s.name, !!v);
      else { if (s.el.dataset.orig === undefined) s.el.dataset.orig = s.el.innerHTML; if (s.el.__html !== v) { s.el.innerHTML = v; s.el.__html = v; } }
    }
    for (const [id, r] of tracks) {
      const v = {};
      for (const p in r.props) v[p] = valAt(r.props[p], t);
      apply(id, r, v);
    }
    const c = camAt(t);
    const world = document.getElementById('world');
    world.style.transform = `translate(960px,540px) rotate(${c.r}deg) scale(${c.z}) translate(${-c.x}px,${-c.y}px)`;
    for (const fn of perFrame) fn(t, c);
  };

  function apply(id, r, v) {
    const el = r.el, st = el.style;
    const g = (p) => (p in v ? v[p] : (r.init && p in r.init ? r.init[p] : DEF[p]));
    const o = g('o');
    const ostr = o.toFixed(3);
    if (r.last.o !== ostr) { st.opacity = ostr; st.visibility = o <= 0.001 ? 'hidden' : 'visible'; r.last.o = ostr; }
    if ('x' in v || 'y' in v || 's' in v || 'r' in v || 'sx' in v || 'sy' in v) {
      const s = g('s');
      const tf = `translate(${g('x').toFixed(2)}px,${g('y').toFixed(2)}px) rotate(${g('r').toFixed(2)}deg) scale(${(s * g('sx')).toFixed(4)},${(s * g('sy')).toFixed(4)})`;
      if (r.last.tf !== tf) { st.transform = tf; r.last.tf = tf; }
    }
    if ('cw' in v || 'ch' in v || 'cl' in v) {
      const cp = `inset(-40px ${((1 - g('cw')) * 100).toFixed(2)}% ${((1 - g('ch')) * 100).toFixed(2)}% ${(g('cl') * 100).toFixed(2)}% )`;
      const cp2 = (g('cw') >= 1 && g('ch') >= 1 && g('cl') <= 0) ? 'none' : `inset(-40px ${((1 - g('cw')) * 100).toFixed(2)}% ${((1 - g('ch')) * 100).toFixed(2)}% ${(g('cl') * 100).toFixed(2)}%)`;
      if (r.last.cp !== cp2) { st.clipPath = cp2; r.last.cp = cp2; }
    }
    if ('bl' in v || 'br' in v || 'sat' in v) {
      const f = `blur(${g('bl').toFixed(2)}px) brightness(${g('br').toFixed(3)}) saturate(${g('sat').toFixed(3)})`;
      if (r.last.f !== f) { st.filter = f; r.last.f = f; }
    }
    if ('dr' in v) { const d = (1 - g('dr')).toFixed(4); if (r.last.dr !== d) { st.strokeDashoffset = d; r.last.dr = d; } }
    if ('w' in v) { const w = v.w.toFixed(1) + 'px'; if (r.last.w !== w) { st.width = w; r.last.w = w; } }
    if ('h' in v) { const h = v.h.toFixed(1) + 'px'; if (r.last.h !== h) { st.height = h; r.last.h = h; } }
    if ('gl' in v) { const gl = v.gl; const s2 = gl <= 0.001 ? 'none' : `0 0 ${(gl * 46).toFixed(1)}px ${(gl * 8).toFixed(1)}px var(--glow, rgba(255,77,109,.55))`; if (r.last.gl !== s2) { st.boxShadow = s2; r.last.gl = s2; } }
    if ('n' in v) {
      const dec = +(el.dataset.dec || 0); let s = v.n.toFixed(dec);
      if (el.dataset.comma) s = Number(s).toLocaleString('en-IN', { minimumFractionDigits: dec, maximumFractionDigits: dec });
      s = (el.dataset.pre || '') + s + (el.dataset.suf || '');
      if (r.last.n !== s) { el.textContent = s; r.last.n = s; }
    }
    if ('ty' in v) {
      const full = el.dataset.full ?? (el.dataset.full = el.textContent);
      const k = Math.max(0, Math.floor(v.ty)); const s = full.slice(0, k);
      if (r.last.ty !== s) { el.textContent = s; r.last.ty = s; }
    }
    if (custom[id]) custom[id](el, v, g);
  }
})();
