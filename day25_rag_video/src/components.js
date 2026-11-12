// ============================================================
// Reusable building blocks: DOM helpers, animation verbs,
// a VS Code replica with editor + terminal, HUD and subtitles.
// ============================================================
const WORLD = () => document.getElementById('world');
let __uid = 0;
const uid = (p = 'u') => p + (++__uid);

// add HTML into the world (or into a parent id)
function add(html, parent) {
  const host = parent ? document.getElementById(parent) : WORLD();
  host.insertAdjacentHTML('beforeend', html);
}
// a board: a 1920x1080 area in world coordinates
const BOARDS = {};
function board(id, gx, gy, inner = '') {
  const x = gx, y = gy;
  BOARDS[id] = { x, y, cx: x + 960, cy: y + 540 };
  add(`<div class="board" id="${id}" style="left:${x}px;top:${y}px">${inner}</div>`);
  return BOARDS[id];
}
// camera helpers in board-local coordinates
function camB(t, dur, b, lx = 960, ly = 540, z = 1, opt = {}) {
  const B = BOARDS[b]; cam(t, dur, { x: B.x + lx, y: B.y + ly, z, r: opt.r || 0 }, opt);
}

// ---------- animation verbs ----------
function popIn(id, t, d = .55, s0 = .5) { ft(id, t, d, { o: 0, s: s0 }, { o: 1, s: 1 }, 'back'); }
function fadeIn(id, t, d = .5) { ft(id, t, d, { o: 0 }, { o: 1 }, 'out'); }
function fadeUp(id, t, d = .6, dy = 50) { ft(id, t, d, { o: 0, y: dy }, { o: 1, y: 0 }, 'out'); }
function fadeDown(id, t, d = .6, dy = 50) { ft(id, t, d, { o: 0, y: -dy }, { o: 1, y: 0 }, 'out'); }
function slideL(id, t, d = .6, dx = 140) { ft(id, t, d, { o: 0, x: -dx }, { o: 1, x: 0 }, 'out'); }
function slideR(id, t, d = .6, dx = 140) { ft(id, t, d, { o: 0, x: dx }, { o: 1, x: 0 }, 'out'); }
function out(id, t, d = .4) { to(id, t, d, { o: 0 }, 'out'); }
function wipe(id, t, d = .6) { ft(id, t, d, { cw: 0 }, { cw: 1 }, 'io'); }
function drop(id, t, d = .6) { ft(id, t, d, { ch: 0 }, { ch: 1 }, 'io'); }
function drawIn(id, t, d = .8) { ft(id, t, d, { dr: 0 }, { dr: 1 }, 'io'); }
function typeIn(id, t, d) { const el = document.getElementById(id); const n = (el.dataset.full ?? el.textContent).length; ft(id, t, d ?? Math.max(.3, n * .035), { ty: 0 }, { ty: n }, 'lin'); }
function count(id, t, d, a, b, ease = 'out') { ft(id, t, d, { n: a }, { n: b }, ease); }
function pulse(id, t, k = 1.14, d = .5) { to(id, t, d * .4, { s: k }, 'out'); to(id, t + d * .4, d * .6, { s: 1 }, 'io'); }
function shake(id, t, a = 14) { const seq = [a, -a, a * .7, -a * .7, a * .4, 0]; seq.forEach((v, i) => to(id, t + i * .06, .06, { x: v }, 'lin')); }
function glow(id, t, d = .5, v = 1) { to(id, t, d, { gl: v }, 'out'); }
function bob(id, t0, t1, amp = 8, per = 1.6) { for (let t = t0, k = 0; t < t1; t += per / 2, k++) to(id, t, per / 2, { y: k % 2 ? 0 : -amp }, 'sine'); }
function spinTo(id, t, d, r) { to(id, t, d, { r }, 'io'); }
function stag(ids, t, gap, fn) { ids.forEach((id, i) => fn(id, t + i * gap)); }
function hideAll(ids, t, d = .4) { ids.forEach(id => out(id, t, d)); }

// ---------- generic pieces ----------
const FILECOL = { txt: '#c9963b', pdf: '#e63946', html: '#ff9f43', png: '#f7a1b0', md: '#ffd9a0', docx: '#b07a2a', py: '#2fb872' };
function fileIcon(id, x, y, type, name = '', scale = 1) {
  const lines = [36, 58, 80, 102, 124].map((t, i) => `<div class="ln" style="top:${t}px;width:${[96, 80, 104, 70, 90][i]}px"></div>`).join('');
  return `<div class="file" id="${id}" style="left:${x}px;top:${y}px;transform:scale(${scale})"><div class="pg">${lines}</div>
    <div class="tag" style="background:${FILECOL[type] || '#888'}">${type.toUpperCase()}</div>${name ? `<div class="nm">${name}</div>` : ''}</div>`;
}
function chip(id, x, y, html, extra = '') { return `<div class="chip" id="${id}" style="left:${x}px;top:${y}px;${extra}">${html}</div>`; }
function pill(id, x, y, html, cls = 'bg-rose', extra = '') { return `<div class="pill ${cls}" id="${id}" style="left:${x}px;top:${y}px;${extra}">${html}</div>`; }
function div(id, x, y, w, h, html = '', cls = '', extra = '') {
  return `<div class="abs ${cls}" id="${id}" style="left:${x}px;top:${y}px;${w ? `width:${w}px;` : ''}${h ? `height:${h}px;` : ''}${extra}">${html}</div>`;
}
// an svg arrow/path drawn later; d in board-local coords
function path(id, d, color = '#ffd9a0', w = 5, extra = '') {
  return `<svg class="ov" width="10" height="10"><path id="${id}" class="draw" pathLength="1" d="${d}" stroke="${color}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round" ${extra}/></svg>`;
}
function arrow(id, x1, y1, x2, y2, color = '#ffd9a0', w = 5) {
  const a = Math.atan2(y2 - y1, x2 - x1), L = 18;
  const hx1 = x2 - L * Math.cos(a - .5), hy1 = y2 - L * Math.sin(a - .5), hx2 = x2 - L * Math.cos(a + .5), hy2 = y2 - L * Math.sin(a + .5);
  return path(id, `M${x1},${y1} L${x2},${y2} M${hx1},${hy1} L${x2},${y2} L${hx2},${hy2}`, color, w);
}
function curve(id, x1, y1, cx, cy, x2, y2, color = '#ffd9a0', w = 5, head = true) {
  let d = `M${x1},${y1} Q${cx},${cy} ${x2},${y2}`;
  if (head) { const a = Math.atan2(y2 - cy, x2 - cx), L = 18; d += ` M${x2 - L * Math.cos(a - .5)},${y2 - L * Math.sin(a - .5)} L${x2},${y2} L${x2 - L * Math.cos(a + .5)},${y2 - L * Math.sin(a + .5)}`; }
  return path(id, d, color, w);
}
// icons (simple, drawn in code)
const ICON = {
  check: (c = '#2fb872') => `<svg viewBox="0 0 48 48" width="100%" height="100%"><circle cx="24" cy="24" r="22" fill="${c}"/><path d="M13 25l7 7 15-16" stroke="#062a16" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  cross: (c = '#e63946') => `<svg viewBox="0 0 48 48" width="100%" height="100%"><circle cx="24" cy="24" r="22" fill="${c}"/><path d="M16 16l16 16M32 16L16 32" stroke="#fff" stroke-width="5" stroke-linecap="round"/></svg>`,
  warn: (c = '#f5b700') => `<svg viewBox="0 0 48 48" width="100%" height="100%"><path d="M24 4L46 43H2z" fill="${c}" stroke="${c}" stroke-width="3" stroke-linejoin="round"/><path d="M24 17v13" stroke="#2a2000" stroke-width="5" stroke-linecap="round"/><circle cx="24" cy="37" r="3" fill="#2a2000"/></svg>`,
  eye: (c = '#ffd9a0') => `<svg viewBox="0 0 64 40" width="100%" height="100%"><path d="M2 20C14 4 50 4 62 20C50 36 14 36 2 20z" fill="none" stroke="${c}" stroke-width="4"/><circle cx="32" cy="20" r="9" fill="${c}"/></svg>`,
  bell: (c = '#f5b700') => `<svg viewBox="0 0 48 48" width="100%" height="100%"><path d="M24 5c-8 0-13 6-13 14v9l-5 7h36l-5-7v-9c0-8-5-14-13-14z" fill="${c}"/><circle cx="24" cy="40" r="5" fill="${c}"/></svg>`,
  mute: (c = '#cfa999') => `<svg viewBox="0 0 48 48" width="100%" height="100%"><path d="M6 18h9l12-10v32L15 30H6z" fill="${c}"/><path d="M33 17l12 14M45 17L33 31" stroke="#e63946" stroke-width="4" stroke-linecap="round"/></svg>`,
  box: (c = '#f5b700') => `<svg viewBox="0 0 64 64" width="100%" height="100%"><path d="M32 4l26 12v32L32 60 6 48V16z" fill="${c}"/><path d="M6 16l26 12 26-12M32 28v32" stroke="#00000055" stroke-width="3" fill="none"/></svg>`,
  gear: (c = '#ffd9a0') => `<svg viewBox="0 0 64 64" width="100%" height="100%"><g fill="${c}"><circle cx="32" cy="32" r="14"/>${[0, 45, 90, 135, 180, 225, 270, 315].map(a => `<rect x="28" y="2" width="8" height="14" rx="2" transform="rotate(${a} 32 32)"/>`).join('')}</g><circle cx="32" cy="32" r="6" fill="#26050a"/></svg>`,
  lock: (c = '#cfa999') => `<svg viewBox="0 0 48 48" width="100%" height="100%"><rect x="8" y="21" width="32" height="24" rx="5" fill="${c}"/><path d="M15 21v-6a9 9 0 0118 0v6" stroke="${c}" stroke-width="5" fill="none"/></svg>`,
  bolt: (c = '#f5b700') => `<svg viewBox="0 0 48 48" width="100%" height="100%"><path d="M27 3L8 27h14l-3 18 21-26H26z" fill="${c}"/></svg>`,
  trash: (c = '#cfa999') => `<svg viewBox="0 0 48 48" width="100%" height="100%"><path d="M10 14h28l-3 30H13z" fill="${c}"/><rect x="7" y="8" width="34" height="5" rx="2" fill="${c}"/><rect x="19" y="3" width="10" height="5" rx="2" fill="${c}"/></svg>`,
  folder: (c = '#f5b700') => `<svg viewBox="0 0 64 52" width="100%" height="100%"><path d="M2 8a5 5 0 015-5h17l6 7h27a5 5 0 015 5v30a5 5 0 01-5 5H7a5 5 0 01-5-5z" fill="${c}"/></svg>`,
  plug: (c = '#2fb872') => `<svg viewBox="0 0 48 64" width="100%" height="100%"><rect x="12" y="2" width="6" height="16" rx="2" fill="${c}"/><rect x="30" y="2" width="6" height="16" rx="2" fill="${c}"/><path d="M6 16h36v14a18 18 0 01-36 0z" fill="${c}"/><rect x="20" y="46" width="8" height="16" rx="3" fill="${c}"/></svg>`,
  chat: (c = '#ffd9a0') => `<svg viewBox="0 0 64 56" width="100%" height="100%"><path d="M8 4h48a6 6 0 016 6v26a6 6 0 01-6 6H24L10 54V42H8a6 6 0 01-6-6V10a6 6 0 016-6z" fill="${c}"/></svg>`,
  db: (c = '#f7a1b0') => `<svg viewBox="0 0 64 72" width="100%" height="100%"><ellipse cx="32" cy="12" rx="28" ry="10" fill="${c}"/><path d="M4 12v48c0 6 13 10 28 10s28-4 28-10V12c0 6-13 10-28 10S4 18 4 12z" fill="${c}" opacity=".8"/><path d="M4 30c0 6 13 10 28 10s28-4 28-10M4 46c0 6 13 10 28 10s28-4 28-10" stroke="#26050a" stroke-width="3" fill="none"/></svg>`,
  scissors: (c = '#e63946') => `<svg viewBox="0 0 64 64" width="100%" height="100%"><circle cx="14" cy="48" r="9" stroke="${c}" stroke-width="5" fill="none"/><circle cx="14" cy="16" r="9" stroke="${c}" stroke-width="5" fill="none"/><path d="M21 22l40 28M21 42L61 14" stroke="${c}" stroke-width="5" stroke-linecap="round"/></svg>`,
  key: (c = '#f5b700') => `<svg viewBox="0 0 64 32" width="100%" height="100%"><circle cx="14" cy="16" r="11" stroke="${c}" stroke-width="5" fill="none"/><path d="M25 16h36M50 16v10M58 16v8" stroke="${c}" stroke-width="5" stroke-linecap="round"/></svg>`,
  broom: (c = '#2fb872') => `<svg viewBox="0 0 64 64" width="100%" height="100%"><path d="M50 4L30 34" stroke="${c}" stroke-width="5" stroke-linecap="round"/><path d="M22 30l16 10-6 20c-10-2-20-8-26-16z" fill="${c}"/></svg>`,
  person: (c = '#ffd9a0') => `<svg viewBox="0 0 48 64" width="100%" height="100%"><circle cx="24" cy="14" r="11" fill="${c}"/><path d="M4 62c0-16 9-26 20-26s20 10 20 26z" fill="${c}"/></svg>`,
  star: (c = '#f5b700') => `<svg viewBox="0 0 48 48" width="100%" height="100%"><path d="M24 3l6 14 15 1-12 10 4 15-13-8-13 8 4-15L3 18l15-1z" fill="${c}"/></svg>`,
};
function icon(id, x, y, size, name, color, extra = '') {
  return `<div class="abs" id="${id}" style="left:${x}px;top:${y}px;width:${size}px;height:${size}px;${extra}">${ICON[name](color)}</div>`;
}

// ---------- VS Code replica ----------
const VS = { x: 0, y: 0, LH: 25, chw: 10.2, codeL: 354 + 64, codeT: 36 + 66 + 6, eds: {} };
function buildVSCode(x, y) {
  VS.x = x; VS.y = y;
  const docs = ['expense_policy.txt', 'holiday_calendar_2026.png', 'insurance_benefits.pdf', 'it_security_handbook.pdf', 'leave_policy.txt', 'pluraldesk_release_notes.html', 'product_faq.txt', 'remote_work_policy.pdf', 'support_tickets.txt'];
  const ext = n => n.split('.').pop();
  const tree = [
    `<div id="tr_root" style="padding-left:10px;font-weight:700;font-size:13px;letter-spacing:.5px">⌄ RAG_CLASS</div>`,
    `<div id="tr_docs" style="padding-left:22px">⌄ <span class="fi" style="background:#e8b84a;border-radius:2px"></span>plural_labs_docs</div>`,
    ...docs.map((n, i) => `<div id="tr_f${i}" style="padding-left:52px"><span class="fi" style="background:${FILECOL[ext(n)]}"></span>${n}</div>`),
    `<div id="tr_env" style="padding-left:22px"><span class="fi" style="background:#e5c07b"></span>.env</div>`,
    `<div id="tr_d22" style="padding-left:22px"><span class="fi" style="background:#4b9ad6"></span>day22_rag.py</div>`,
    `<div id="tr_d25" style="padding-left:22px"><span class="fi" style="background:#4b9ad6"></span>day25_rag.py</div>`,
  ].join('');
  const acts = [56, 104, 152, 200, 248].map(t => `<b style="top:${t}px"></b>`).join('');
  add(`<div class="vsc" id="vsc" style="left:${x}px;top:${y}px">
    <div class="titlebar"><div class="dots"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i><i style="background:#28c840"></i></div><span id="vs_title">day25_rag.py — rag_class</span></div>
    <div class="act">${acts}</div>
    <div class="side"><div class="hd">EXPLORER</div><div class="tree">${tree}</div>
       <div id="tr_hl" class="abs" style="left:0;top:0;width:300px;height:26px;background:rgba(155,27,35,.35);border-left:3px solid var(--vio)"></div></div>
    <div class="main">
      <div class="tabs"><div class="tab" id="tab22"><span class="py">py</span>day22_rag.py</div><div class="tab" id="tab25"><span class="py">py</span>day25_rag.py</div></div>
      <div class="crumbs" id="crumbs">day25_rag.py › …</div>
      <div class="ed" id="ed22"></div><div class="ed" id="ed25"></div>
      <div class="mini" id="mini"></div>
      <div class="panel" id="panel"><div class="ph"><span>PROBLEMS</span><span>OUTPUT</span><b>TERMINAL</b><span>PORTS</span></div><div class="term" id="term"><div class="termin" id="termin"></div></div></div>
    </div>
    <div class="status"><span>⎇ main</span><span>⊗ 0  ⚠ 0</span><span style="margin-left:auto">Ln 1, Col 1</span><span>Spaces: 4</span><span>UTF-8</span><span>Python 3.14.0</span><span style="margin-right:20px">🔔</span></div>
  </div>`);
  buildEditor('day22_rag', 'ed22'); buildEditor('day25_rag', 'ed25');
  // minimap: tiny bars for each line of day25
  let mm = ''; RAW['day25_rag'].forEach((l, i) => { const ind = l.length - l.trimStart().length; if (l.trim()) mm += `<div style="position:absolute;left:${8 + ind * 1.2}px;top:${i * 2.2}px;width:${Math.min(90, l.trim().length * 1.2)}px;height:1.6px;background:${l.trim().startsWith('#') ? '#4b6b3f' : '#8a8a8a'}"></div>`; });
  add(`<div id="mmin" class="abs" style="left:0;top:0;width:110px">${mm}</div><div id="mmview" class="abs" style="left:0;top:0;width:110px;height:80px;background:rgba(121,121,121,.18)"></div>`, 'mini');
  // measure char width
  const probe = document.createElement('span'); probe.style.cssText = 'font:400 17px "JetBrains Mono";white-space:pre;position:absolute;visibility:hidden';
  probe.textContent = 'x'.repeat(100); document.body.appendChild(probe); VS.chw = probe.getBoundingClientRect().width / 100; probe.remove();
}
function buildEditor(name, host) {
  const key = name === 'day22_rag' ? '22' : '25';
  const lines = CODE[name].map((h, i) => `<div class="cl"><span class="no">${i + 1}</span>${h}</div>`).join('');
  add(`<div class="codein" id="cin${key}">
     <div class="hlbox" id="hl${key}" style="top:0;height:25px"></div>
     ${lines}
     <div class="dim" id="dt${key}" style="top:0;height:0"></div><div class="dim" id="db${key}" style="top:0;height:30000px"></div>
     <div id="mk${key}"></div>
   </div>`, host);
  VS.eds[key] = { name, n: CODE[name].length, scroll: 0 };
  init('hl' + key, { o: 0, y: 0, h: 25 }); init('dt' + key, { o: 0, h: 0 }); init('db' + key, { o: 0, y: 0 });
  init('cin' + key, { y: 0 }); init('tr_hl', { o: 0, y: 36 });
}
// which file is visible
function showTab(t, key) {
  const other = key === '25' ? '22' : '25';
  set('ed' + key, t, { o: 1 }); set('ed' + other, t, { o: 0 });
  cls('tab' + key, t, 'on', true); cls('tab' + other, t, 'on', false);
  txt('crumbs', t, key === '25' ? 'day25_rag.py › …' : 'day22_rag.py › …');
  txt('vs_title', t, (key === '25' ? 'day25_rag.py' : 'day22_rag.py') + ' — rag_class');
}
// screen rect of a code line range in world coordinates, assuming scroll s (in lines)
function lineWorld(L, s, col = 0) {
  return { x: VS.x + VS.codeL + col * VS.chw, y: VS.y + VS.codeT + (L - 1 - s) * VS.LH };
}
let PANEL_H = 0;
// focus lines L1..L2 of editor key: scroll, spotlight, and (optionally) move camera
function focus(t, key, L1, L2, opt = {}) {
  const ed = VS.eds[key], LH = VS.LH;
  const visRows = Math.floor((1012 - 36 - 26 - 66 - PANEL_H) / LH);
  const n = L2 - L1 + 1;
  let s = opt.scroll ?? Math.max(0, Math.min(ed.n - visRows + 3, L1 - 1 - Math.max(2, Math.floor((visRows - n) * (opt.rowFrac ?? .35)))));
  const sd = opt.sd ?? .9;
  if (s !== ed.scroll) { to('cin' + key, t, sd, { y: -s * LH }, 'io'); to('mmin', t, sd, { y: -s * 2.2 * .4 }, 'io'); to('mmview', t, sd, { y: s * 2.2 * .6 }, 'io'); }
  ed.scroll = s;
  const hy = (L1 - 1) * LH, hh = n * LH;
  const ht = t + (s !== ed.scroll ? .2 : 0);
  if (opt.hl !== false) {
    to('hl' + key, ht + .3, .55, { o: 1, y: hy, h: hh }, 'io');
    to('dt' + key, ht + .3, .55, { o: opt.dim === false ? 0 : 1, h: hy }, 'io');
    to('db' + key, ht + .3, .55, { o: opt.dim === false ? 0 : 1, y: hy + hh }, 'io');
  }
  if (opt.cam !== false) {
    let maxLen = 0; for (let L = L1; L <= L2; L++) maxLen = Math.max(maxLen, (RAW[ed.name][L - 1] || '').length);
    maxLen = Math.max(maxLen, opt.minCols || 30);
    const wpx = (maxLen + 9) * VS.chw, hpx = (n + 2) * LH;
    let z = Math.min(1700 / wpx, 760 / hpx, opt.zmax || 2.3); z = Math.max(z, opt.zmin || .62);
    const a = lineWorld(L1, s);
    const cx = opt.cx ?? (VS.x + VS.codeL - 30 + wpx / 2);
    const cy = a.y + n * LH / 2 + (opt.dy || 0);
    cam(t + (opt.camDelay || 0), opt.cd || 1.1, { x: cx, y: cy, z: opt.z || z, r: opt.r || 0 }, { dip: opt.dip || 0, ease: opt.ease });
  }
  return s;
}
function unfocus(t, key) { to('hl' + key, t, .5, { o: 0 }); to('dt' + key, t, .5, { o: 0 }); to('db' + key, t, .5, { o: 0 }); }
// a yellow box around columns c1..c2 of line L (1-based cols, inclusive start, exclusive end)
function mark(t, key, L, c1, c2, color = 'var(--sun)', d = .45) {
  const id = uid('mk');
  const x = 64 + c1 * VS.chw - 5, w = (c2 - c1) * VS.chw + 10, y = (L - 1) * VS.LH - 1;
  add(`<div class="mark" id="${id}" style="left:${x}px;top:${y}px;width:${w}px;height:${VS.LH + 2}px;border-color:${color}"></div>`, 'mk' + key);
  ft(id, t, d, { o: 0, cw: 0 }, { o: 1, cw: 1 }, 'out');
  return id;
}
// zoom the camera onto a token (line L, cols c1..c2) of editor key
function camTok(t, key, L, c1, c2, z = 2.6, d = .9, opt = {}) {
  const s = VS.eds[key].scroll; const a = lineWorld(L, s, (c1 + c2) / 2);
  cam(t, d, { x: a.x + (opt.dx || 0), y: a.y + VS.LH / 2 + (opt.dy || 0), z, r: opt.r || 0 }, opt);
}
// camera framing the whole VS Code window
// a callout pill living inside the editor (scrolls with the code)
function note(t, key, L, col, html, color = 'var(--sun)', opt = {}) {
  const id = opt.id || uid('nt');
  const x = 64 + col * VS.chw, y = (L - 1) * VS.LH - 6 + (opt.dy || 0);
  add(`<div class="abs" id="${id}" style="left:${x}px;top:${y}px;padding:4px 14px;border-radius:9px;background:${color};color:#2a0509;font:700 19px var(--sans);white-space:nowrap;box-shadow:0 8px 24px rgba(0,0,0,.5)">${html}</div>`, 'mk' + key);
  ft(id, t, .5, { o: 0, x: -30 }, { o: 1, x: 0 }, 'back');
  return id;
}
function camVS(t, d = 1.2, z = .93, opt = {}) { cam(t, d, { x: VS.x + 900 + (opt.dx || 0), y: VS.y + 506 + (opt.dy || 0), z, r: 0 }, opt); }
function sideHL(t, idx) { // highlight explorer row (0=root,1=docs,2..10 files, 11 env, 12 d22, 13 d25)
  to('tr_hl', t, .4, { o: 1, y: 36 + idx * 26 }, 'out');
}

// ---------- terminal ----------
const TERM = { n: 0, rows: 0, scroll: 0, lines: [] };
function panel(t, h, d = .6) { PANEL_H = h; to('panel', t, d, { h }, 'io'); TERM.rows = Math.floor((h - 50) / 27); }
function termLine(t, html, opt = {}) {
  const id = uid('tl');
  add(`<div class="tl" id="${id}">${html}</div>`, 'termin');
  TERM.lines.push(id); TERM.n++; init(id, { h: 27 });
  if (opt.type) { /* typed command */ }
  ft(id, t, opt.d ?? .12, { o: 0, x: opt.dx ?? 0 }, { o: 1, x: 0 }, 'out');
  // keep the newest line in view
  const over = TERM.n - TERM.rows;
  if (TERM.rows > 0 && over > TERM.scroll) { TERM.scroll = over; to('termin', t, .25, { y: -TERM.scroll * 27 }, 'out'); }
  return id;
}
const PROMPT = '<span class="pr">rag_class %</span> ';
function termCmd(t, cmd, speed = .045) {
  const id = termLine(t, PROMPT + `<span id="${uid('tc')}"></span>`);
  const inner = document.getElementById(id).lastElementChild;
  inner.textContent = cmd; inner.id = inner.id; typeIn(inner.id, t + .15, Math.max(.4, cmd.length * speed));
  return t + .15 + Math.max(.4, cmd.length * speed) + .25;
}
function termClear(t) { TERM.lines.forEach(id => set(id, t, { o: 0, h: 0 })); TERM.n = 0; TERM.scroll = 0; set('termin', t, { y: 0 }); TERM.lines = []; }

// ---------- HUD ----------
function buildHUD() {
  document.getElementById('hud').innerHTML = `<div id="wipe"><i></i></div><div id="ccard"><div class="eyebrow" id="cc_eye"></div><div id="cc_t"></div><div id="cc_steps"></div></div><div id="prog"></div><div id="chap"><span class="dot"></span><span class="day">DAY 25</span><span id="chapname"></span></div><div id="brand">PLURAL LABS · AI DEVELOPER PROGRAM</div><div id="sub"></div>`;
  const sub = document.getElementById('sub'), cn = document.getElementById('chapname'), pg = document.getElementById('prog');
  const lines = window.LINES;
  let cur = null;
  // chapter title cards + wipe transitions for camera cuts
  const chaps = lines.filter(l => l.chapStart);
  const cc = document.getElementById('ccard'), wp = document.getElementById('wipe');
  const steps = ['LOAD', 'CHUNK', 'EMBED', 'STORE', 'RETRIEVE', 'RANK', 'AUGMENT', 'GENERATE'];
  const allChaps = [...new Set(lines.map(l => l.chap))];
  let ccShown = null;
  const ease = p => p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
  everyFrame((t) => {
    let card = null, a = 0;
    for (const l of chaps) { const t0 = l.start - 3.0, t1 = l.start + .5; if (t >= t0 && t <= t1 + .35) { card = l; a = Math.min(1, (t - t0) / .35, (t1 + .35 - t) / .35); } }
    if (card !== ccShown) {
      ccShown = card;
      if (card) {
        const idx = allChaps.indexOf(card.chap); const k = card.chap.split(' ')[0];
        document.getElementById('cc_eye').textContent = `Day 25 · chapter ${String(idx + 1).padStart(2, '0')} / ${allChaps.length}`;
        document.getElementById('cc_t').textContent = card.chap.replace(/^c\d+\s*/, '');
        const lit = k === 'c9' ? [1, 2, 3, 4, 5, 6, 7] : k === 'c10' ? [0, 1, 2, 3, 4, 5, 6, 7] : [0];
        document.getElementById('cc_steps').innerHTML = steps.map((s, i) => `<span class="${lit.includes(i) ? 'on' : ''}">${i + 1} · ${s}</span>`).join('');
      }
    }
    cc.style.opacity = card ? Math.max(0, a).toFixed(3) : 0;
    cc.style.visibility = card ? 'visible' : 'hidden';
    const tt = document.getElementById('cc_t'); if (card) tt.style.transform = `translateY(${((1 - Math.min(1, (t - card.start + 3.0) / .8)) * 40).toFixed(1)}px)`;
    let wx = null;
    for (const c of (window.CUTS || [])) {
      if (t > c - .34 && t < c + .34 && !chaps.some(l => c > l.start - 3.1 && c < l.start + .8)) wx = ease((t - (c - .34)) / .68);
    }
    wp.style.visibility = wx === null ? 'hidden' : 'visible';
    if (wx !== null) wp.style.transform = `translateX(${(-130 + wx * 260).toFixed(2)}%) skewX(-14deg)`;
  });
  everyFrame((t) => {
    let L = null; for (const l of lines) { if (l.start - .15 <= t && t <= l.end + .3) { L = l; break; } }
    if (L !== cur) {
      cur = L;
      sub.innerHTML = L ? L.text.split(' ').map(w => `<span class="w">${w.replace(/</g, '&lt;')}</span>`).join(' ') : '';
      sub.style.opacity = L ? 1 : 0;
    }
    if (L) {
      const words = sub.children; const total = L.text.length; let acc = 0;
      const p = Math.min(1, Math.max(0, (t - L.start) / L.dur)) * total;
      for (const w of words) { const wl = w.textContent.length + 1; w.className = 'w' + (acc + wl * .5 <= p ? ' on' : '') + (acc <= p && p < acc + wl ? ' cur' : ''); acc += wl; }
    }
    const ch = (L || lines.find(l => l.start > t) || lines[lines.length - 1]).chap || '';
    const name = ch.replace(/^c\d+\s*/, '');
    if (cn.textContent !== name) cn.textContent = name;
    pg.style.width = (t / window.TOTAL * 1920).toFixed(1) + 'px';
  });
}
