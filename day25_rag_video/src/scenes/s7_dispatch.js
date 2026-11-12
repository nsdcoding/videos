// c7 : part C - the dispatch table
(window.SCENES = window.SCENES || []).push(function () {
  const G = (c, r) => [c * 2400, r * 1500];
  const fbox = (id, x, y, name, col) => `<div class="abs center" id="${id}" style="left:${x}px;top:${y}px;width:300px;height:96px;border-radius:16px;background:#3a0a12;border:3px solid ${col};gap:14px"><div style="width:44px;height:44px">${ICON.gear(col)}</div><b class="mono" style="font-size:30px;color:${col}">${name}</b></div>`;
  board('DISPATCH', ...G(2, 4), `
    ${div('dp_t', 110, 60, 0, 0, '<span class="eyebrow" style="display:block;margin-bottom:12px">Part C</span>A dictionary can hold <span class="sun">functions</span>', 'h1', 'font-size:60px')}
    <div class="card" id="dp_d1" style="left:110px;top:240px;width:820px;height:250px">
      <div class="abs small" style="left:30px;top:20px;letter-spacing:3px">YOU KNOW THIS</div>
      <div class="abs mono" style="left:30px;top:70px;font-size:36px;line-height:1.5">{<span style="color:#ce9178">"leaves"</span>: <span style="color:#b5cea8">24</span>,<br>&nbsp;<span style="color:#ce9178">"city"</span>: <span style="color:#ce9178">"Delhi"</span>}</div></div>
    <div class="card" id="dp_d2" style="left:990px;top:240px;width:820px;height:250px;border-color:var(--sun)">
      <div class="abs small" style="left:30px;top:20px;letter-spacing:3px;color:var(--sun)">AND NOW THIS</div>
      <div class="abs mono" style="left:30px;top:80px;font-size:34px"><span style="color:#ce9178">".txt"</span>:</div>${fbox('dp_f1', 190, 62, 'load_txt', 'var(--teal)')}
      <div class="abs mono" style="left:30px;top:170px;font-size:34px"><span style="color:#ce9178">".pdf"</span>:</div>${fbox('dp_f2', 190, 152, 'load_pdf', 'var(--rose)')}</div>
    <div class="card" id="dp_call" style="left:110px;top:550px;width:820px;height:440px">
      <div class="abs mono" style="left:30px;top:30px;font-size:48px">load_txt<span class="rose">()</span></div>
      ${div('dp_cl', 30, 110, 0, 0, 'brackets = CALL it right now', 'txt', 'font-size:30px')}
      <div class="abs" id="dp_g" style="left:60px;top:190px;width:150px;height:150px">${ICON.gear('#e63946')}</div>
      ${arrow('dp_ca', 240, 265, 340, 265, '#cfa999', 6)}
      <div class="abs mono" id="dp_res" style="left:360px;top:225px;padding:16px 22px;border-radius:12px;background:var(--rose);color:#fff;font-size:28px">[{"page": None, …}]</div>
      ${div('dp_rl', 360, 320, 0, 0, '→ you get the result', 'hand', 'font-size:40px;color:var(--rose)')}</div>
    <div class="card" id="dp_val" style="left:990px;top:550px;width:820px;height:440px">
      <div class="abs mono" style="left:30px;top:30px;font-size:48px">load_txt</div>
      ${div('dp_vl', 30, 110, 0, 0, 'no brackets = the function ITSELF, as a value', 'txt', 'font-size:30px')}
      <div class="abs" id="dp_tb" style="left:250px;top:200px;width:340px;height:200px;border-radius:12px;background:#7c3a12;border:4px solid #c2611f"></div>
      <div class="abs" id="dp_tool" style="left:340px;top:170px;width:160px;height:100px">${ICON.gear('#2fb872')}</div>
      ${div('dp_tl', 610, 260, 180, 0, 'in the box, not used yet', 'hand', 'font-size:34px;color:var(--teal)')}</div>
  `);
  const keys = [['.txt', 'var(--teal)'], ['.md', 'var(--sky)'], ['.pdf', 'var(--rose)']];
  board('SWITCH', ...G(3, 4), `
    ${div('sw_t', 110, 60, 0, 0, '<span class="mono">LOADERS</span> : extension → function', 'h1', 'font-size:58px')}
    ${keys.map(([k, c], i) => `<div class="abs mono center" id="sw_k${i}" style="left:140px;top:${220 + i * 170}px;width:240px;height:110px;border-radius:18px;background:#3a0a12;border:3px solid ${c};font-size:44px;color:${c}">"${k}"</div>`).join('')}
    ${fbox('sw_f0', 900, 270, 'load_txt', 'var(--teal)')}${fbox('sw_f1', 900, 560, 'load_pdf', 'var(--rose)')}
    ${curve('sw_w0', 385, 275, 640, 275, 895, 318, '#2fb872', 6)}${curve('sw_w1', 385, 445, 640, 400, 895, 330, '#ffd9a0', 6)}${curve('sw_w2', 385, 615, 640, 610, 895, 608, '#e63946', 6)}
    ${div('sw_md', 1240, 330, 0, 0, 'markdown is plain text too', 'hand', 'font-size:38px;color:var(--sky)')}
    ${div('sw_lbl', 140, 760, 0, 0, 'a <b class="sun">dispatch table</b> &nbsp;·&nbsp; a <b class="sun">registry</b>', 'h2', 'font-size:52px')}
    <div class="card" id="sw_if" style="left:110px;top:860px;width:800px;height:180px;overflow:hidden">
      <div class="abs mono" id="sw_ifc" style="left:24px;top:14px;font-size:22px;line-height:1.45;color:#cfa999;white-space:pre"><span class="kc" style="color:#c586c0">if</span> ext == ".txt": …
<span style="color:#c586c0">elif</span> ext == ".md": …
<span style="color:#c586c0">elif</span> ext == ".pdf": …
<span style="color:#c586c0">elif</span> ext == ".html": …   <span class="rose">← grows forever</span></div></div>
    <div class="card" id="sw_add" style="left:990px;top:780px;width:820px;height:260px;border-color:var(--teal)">
      <div class="abs small" style="left:30px;top:20px;letter-spacing:3px;color:var(--teal)">NEW FORMAT = ONE NEW LINE</div>
      <div class="abs mono" id="sw_new" style="left:30px;top:80px;font-size:34px;padding:10px 18px;border-radius:12px;border:3px dashed #ff9f43"><span style="color:#ce9178">".html"</span>: load_html,</div>
      <div class="abs" id="sw_lk" style="left:30px;top:170px;display:flex;align-items:center;gap:16px"><div style="width:50px;height:50px">${ICON.lock('#2fb872')}</div><span class="txt" style="font-size:28px">the loop never mentions pdf or txt → <b class="teal">never changes</b></span></div></div>
    <div class="abs" id="sw_frame" style="left:110px;top:190px;width:1110px;height:540px;border-radius:26px;border:4px solid var(--sun)"></div>
  `);

  // ================= animation =================
  let t = T('h01');
  focus(t, '25', 412, 416, { cd: 1.8, dip: .3, zmax: 2.0 });
  note(W('h01', 'chooses'), '25', 412, 13, 'replaces Day 22\'s if', 'var(--vio)');
  t = T('h02');
  camB(t, 1.8, 'DISPATCH', 960, 300, 1.05, { dip: .3 });
  wipe('dp_t', t + .5, .6); fadeUp('dp_d1', W('h02', 'numbers'), .5);
  t = T('h03');
  fadeUp('dp_d2', W('h03', 'functions'), .5); popIn('dp_f1', W('h03', 'functions') + .3, .4); popIn('dp_f2', W('h03', 'functions') + .5, .4);
  camB(t, 1.0, 'DISPATCH', 1400, 370, 1.5);
  t = T('h04');
  focus(t, '25', 413, 413, { cd: 1.8, dip: .3, zmax: 2.6, minCols: 30 });
  mark(W('h04', 'no brackets'), '25', 413, 12, 20, 'var(--sun)');
  t = T('h05');
  camB(t, 1.8, 'DISPATCH', 520, 770, 1.45, { dip: .3 });
  fadeIn('dp_call', t + .5, .3); fadeIn('dp_cl', W('h05', 'means'), .4);
  ft('dp_g', W('h05', 'call'), 2, { r: 0 }, { r: 360 }, 'io'); drawIn('dp_ca', W('h05', 'give me'), .3); popIn('dp_res', W('h05', 'result'), .45); fadeIn('dp_rl', W('h05', 'result') + .3, .4);
  t = T('h06');
  camB(t, 1.0, 'DISPATCH', 1400, 770, 1.45);
  fadeIn('dp_val', t, .3); fadeIn('dp_vl', W('h06', 'itself'), .4); fadeIn('dp_tb', W('h06', 'tool'), .3);
  ft('dp_tool', W('h06', 'tool'), .8, { o: 0, y: -160 }, { o: 1, y: 60 }, 'out'); fadeIn('dp_tl', W('h06', 'without using'), .4);
  t = T('h07');
  camB(t, 1.8, 'SWITCH', 700, 450, 1.0, { dip: .3 });
  wipe('sw_t', t + .5, .6);
  keys.forEach((k, i) => slideL('sw_k' + i, t + .8 + i * .2, .4, 60)); popIn('sw_f0', t + 1.4, .4); popIn('sw_f1', t + 1.6, .4);
  t = T('h08');
  drawIn('sw_w0', W('h08', 'goes to'), .5); pulse('sw_f0', W('h08', 'goes to') + .4, 1.08);
  drawIn('sw_w1', W('h08', 'markdown'), .6); fadeIn('sw_md', W('h08', 'plain text'), .4);
  drawIn('sw_w2', W('h08', 'And .pdf'), .5); pulse('sw_f1', W('h08', 'And .pdf') + .5, 1.08);
  t = T('h09');
  fadeUp('sw_lbl', t + .1, .5, 30); camB(t, 1.0, 'SWITCH', 700, 560, .95);
  t = T('h10');
  camB(t, 1.0, 'SWITCH', 960, 860, 1.1);
  fadeIn('sw_if', t, .3); ft('sw_ifc', t + .2, 2.4, { ch: 0 }, { ch: 1 }, 'lin');
  t = T('h11');
  fadeIn('sw_add', t, .3); ft('sw_new', W('h11', 'one line'), .6, { o: 0, x: -200 }, { o: 1, x: 0 }, 'back');
  camB(t, 1.0, 'SWITCH', 1400, 880, 1.5);
  t = T('h12');
  camB(t, 1.0, 'SWITCH', 700, 470, .95);
  ft('sw_frame', W('h12', 'one place'), .6, { o: 0, s: 1.1 }, { o: 1, s: 1 }, 'out'); to('sw_frame', W('h12', 'glance'), .3, { gl: .6 });
  t = T('h13');
  camB(t, 1.0, 'SWITCH', 1400, 900, 1.5);
  to('sw_frame', t, .4, { o: 0, gl: 0 }); slideR('sw_lk', W('h13', 'never mentions'), .5, 50); pulse('sw_lk', W('h13', 'never needs'), 1.06);
});
