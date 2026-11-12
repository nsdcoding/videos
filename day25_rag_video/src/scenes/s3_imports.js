// c3 : the imports - os, re, from pypdf import PdfReader, classes and objects
(window.SCENES = window.SCENES || []).push(function () {
  const G = (c, r) => [c * 2400, r * 1500];
  const sp = (s) => `<span class="ws">${s}</span>`;
  // ---------- REGEX ----------
  board('REGEX', ...G(-1, 1), `
    ${div('rx_t', 110, 60, 0, 0, '<span class="mono rose">re</span> = <span class="grad-text">regular expressions</span>', 'h1', 'font-size:70px')}
    <div class="card" id="rx_a" style="left:110px;top:200px;width:800px;height:280px">
      <div class="abs small" style="left:30px;top:20px;letter-spacing:3px">EXACT TEXT</div>
      <div class="abs mono" style="left:30px;top:70px;font-size:36px">"the <span id="rx_cat" style="display:inline-block;color:var(--sun)">cat</span> sat"</div>
      ${chip('rx_code', 30, 140, 'text.<span class="fn">replace</span>(<span class="st">"cat"</span>, <span class="st">"dog"</span>)', 'font-size:28px')}
      <div class="abs mono" id="rx_res" style="left:450px;top:70px;font-size:36px">→ "the <span style="color:var(--teal)">dog</span> sat"</div>
      ${div('rx_ok', 540, 200, 0, 0, '✓ you know exactly what to look for', 'small', 'color:var(--teal);font-size:24px')}</div>
    <div class="card" id="rx_b" style="left:990px;top:200px;width:820px;height:280px">
      <div class="abs small" style="left:30px;top:20px;letter-spacing:3px">MESSY TEXT</div>
      <div class="abs mono" id="rx_m" style="left:30px;top:70px;font-size:32px;white-space:pre">Do${sp('··')}not turn${sp('↵')}it${sp('·····→')}off.</div>
      <div class="abs mono" id="rx_m2" style="left:30px;top:170px;font-size:32px;white-space:pre;color:var(--teal)">Do not turn it off.</div>
      ${div('rx_m3', 560, 176, 0, 0, '✓ one space each', 'small', 'color:var(--teal);font-size:24px')}</div>
    <div class="card" id="rx_c" style="left:110px;top:540px;width:800px;height:460px;overflow:hidden">
      <div class="abs small" style="left:30px;top:20px;letter-spacing:3px">WITH .replace() …</div>
      ${['"  "', '"   "', '"    "', '"\\n  "', '"\\t "', '" \\n"', '"\\n\\n"'].map((s, i) => chip('rx_r' + i, 30 + i * 22, 70 + i * 52, `text = text.<span class="fn">replace</span>(<span class="st">${s}</span>, <span class="st">" "</span>)`, 'font-size:22px;padding:8px 16px')).join('')}
      ${div('rx_inf', 560, 330, 0, 0, '∞ forever', 'hand', 'font-size:64px;color:var(--rose)')}</div>
    <div class="card" id="rx_d" style="left:990px;top:540px;width:820px;height:460px">
      <div class="abs h2" style="left:30px;top:24px">describe a <span class="sun">SHAPE</span>, not exact text</div>
      <div id="rx_s1" class="abs" style="left:30px;top:120px;display:flex;align-items:center;gap:24px">${'<span class="chip" style="position:static;font-size:34px;color:var(--rose)">\\s+</span>'}<span class="txt" style="font-size:30px">a run of whitespace</span></div>
      <div id="rx_s2" class="abs" style="left:30px;top:220px;display:flex;align-items:center;gap:24px">${'<span class="chip" style="position:static;font-size:34px;color:var(--rose)">\\d:</span>'}<span class="txt" style="font-size:30px">a digit followed by a colon</span></div>
      <div id="rx_s2e" class="abs mono" style="left:300px;top:290px;font-size:28px">"Step <span style="background:rgba(230,57,70,.3);border-radius:4px">1:</span> load"</div>
      <div id="rx_bi" class="abs" style="left:30px;top:370px;display:flex;align-items:center;gap:16px"><div style="width:44px;height:44px">${ICON.check()}</div><span class="txt" style="font-size:28px">built into Python — <b>nothing to install</b></span></div></div>
  `);
  // ---------- IMPORTS : two shapes ----------
  const tiles = (arr, col) => arr.map((s, i) => `<div class="abs mono center" id="${s[0]}" style="left:${24 + (i % 2) * 170}px;top:${70 + Math.floor(i / 2) * 64}px;width:156px;height:50px;border-radius:10px;background:${col};font-size:19px;color:#2a0509;font-weight:700">${s[1]}</div>`).join('');
  board('IMPORTS', ...G(0, 1), `
    ${div('im_t', 110, 60, 0, 0, 'Two shapes of import', 'h1', 'font-size:66px')}
    ${chip('im_c1', 110, 190, '<span class="kc">import</span> <span class="cl">os</span>', 'font-size:40px')}
    ${chip('im_c2', 1000, 190, '<span class="kc">from</span> <span class="cl">pypdf</span> <span class="kc">import</span> <span class="cl">PdfReader</span>', 'font-size:40px')}
    <div class="card" id="im_m1" style="left:110px;top:320px;width:370px;height:300px;border-color:var(--sky)"><div class="abs mono" style="left:24px;top:18px;font-size:28px;color:var(--sky)">os</div>${tiles([['o1', 'path'], ['o2', 'listdir'], ['o3', 'getcwd'], ['o4', 'mkdir'], ['o5', 'remove'], ['o6', 'rename']], '#ffd9a0')}</div>
    <div class="card" id="im_f1" style="left:560px;top:320px;width:340px;height:300px;border-style:dashed"><div class="abs small" style="left:24px;top:18px;letter-spacing:2px">YOUR FILE</div><div id="im_os" class="abs mono center" style="left:30px;top:90px;width:280px;height:150px;border-radius:14px;border:3px solid var(--sky);font-size:40px;color:var(--sky)">os</div></div>
    ${arrow('im_a1', 490, 470, 550, 470, '#ffd9a0', 6)}
    ${chip('im_u1', 110, 680, '<span class="cl">os</span>.path.<span class="fn">join</span>(folder, name)\n<span class="cl">os</span>.<span class="fn">listdir</span>(folder)', 'font-size:30px')}
    ${div('im_u1n', 110, 810, 760, 0, 'everything stays behind the name <b class="mono sky">os.</b>', 'txt')}
    <div class="card" id="im_m2" style="z-index:5;left:1000px;top:320px;width:370px;height:300px;border-color:var(--sun)"><div class="abs mono" style="left:24px;top:18px;font-size:28px;color:var(--sun)">pypdf</div>${tiles([['p1', 'PdfReader'], ['p2', 'PdfWriter'], ['p3', 'PageObject'], ['p4', 'Transform'], ['p5', 'PdfMerger'], ['p6', 'errors']], '#ffe27a')}</div>
    <div class="card" id="im_f2" style="left:1470px;top:320px;width:340px;height:300px;border-style:dashed"><div class="abs small" style="left:24px;top:18px;letter-spacing:2px">YOUR FILE</div></div>
    ${chip('im_u2', 1000, 680, '<span class="cl">PdfReader</span>(path)', 'font-size:32px;border-color:var(--teal)')}
    ${chip('im_u3', 1000, 770, '<span class="cl">pypdf</span>.<span class="cl">PdfReader</span>(path)', 'font-size:32px;color:#cfa999')}
    ${div('im_x', 1000, 800, 470, 5, '', 'strike')}
    ${div('im_u2n', 1500, 690, 340, 0, '✓ the one name lands right in your file', 'txt', 'font-size:24px;color:var(--teal)')}
    ${div('im_both', 610, 920, 700, 90, '<b style="font-size:32px">Both work.</b>&nbsp;<span class="txt" style="font-size:28px">Need one thing? use the short one.</span>', 'card center', 'border-color:var(--teal)')}
  `);
  // ---------- PKG : what a package is ----------
  board('PKG', ...G(1, 1), `
    ${div('pk_t', 110, 60, 0, 0, 'Where did <span class="mono sun">pypdf</span> come from?', 'h1', 'font-size:62px')}
    ${pill('pk_os', 120, 220, '<span class="mono">os</span>', 'bg-sky', 'font-size:38px')}${pill('pk_re', 270, 220, '<span class="mono">re</span>', 'bg-sky', 'font-size:38px')}
    ${div('pk_l1', 120, 300, 0, 0, 'came with Python', 'txt')}
    ${pill('pk_pp', 120, 400, '<span class="mono">pypdf</span>', 'bg-sun', 'font-size:38px')}
    ${div('pk_l2', 120, 480, 0, 0, 'you installed it with pip', 'txt')}
    <div class="card" id="pk_pip" style="left:620px;top:220px;width:260px;height:120px"><div class="center" style="height:120px;font:700 40px var(--mono);color:var(--sun)">pip</div></div>
    ${curve('pk_a', 880, 280, 1050, 200, 1150, 330, '#f5b700', 6)}
    ${div('pk_box', 640, 380, 220, 200, ICON.box('#f5b700'))}
    <div class="card" id="pk_sp" style="left:1150px;top:300px;width:660px;height:640px">
      <div class="abs" style="left:30px;top:26px;display:flex;align-items:center;gap:16px"><div style="width:60px;height:50px">${ICON.folder()}</div><span class="mono" style="font-size:28px">site-packages/pypdf/</span></div>
      ${['__init__.py', '_reader.py', '_page.py', '_writer.py', 'generic/', 'filters.py', 'errors.py'].map((f, i) => `<div class="abs mono" id="pk_f${i}" style="left:70px;top:${120 + i * 62}px;font-size:28px;color:#f6e2cc">📄 ${f}</div>`).join('')}</div>
    ${div('pk_nm', 110, 640, 950, 0, 'A package is just <b class="sun">somebody else\'s Python files</b> on your disk.', 'h2', 'font-size:44px;line-height:1.3')}
    ${div('pk_nm2', 110, 820, 0, 0, 'nothing magic — you can open them and read them', 'hand', 'font-size:48px;color:var(--teal)')}
  `);
  // ---------- CLASS : function vs class ----------
  board('CLASS', ...G(2, 1), `
    ${div('cl_t', 110, 50, 0, 0, 'What is <span class="mono teal">PdfReader</span> ?', 'h1', 'font-size:66px')}
    ${chip('cl_n1', 1150, 50, '<span class="cl">PdfReader</span>', 'font-size:34px')}${div('cl_n1l', 1420, 62, 0, 0, '→ CapWords → <b class="teal">class</b>', 'txt', 'font-size:28px')}
    ${chip('cl_n2', 1150, 130, '<span class="cl">os</span>.<span class="fn">listdir</span>', 'font-size:34px')}${div('cl_n2l', 1420, 142, 0, 0, '→ lowercase → <b class="sun">function</b>', 'txt', 'font-size:28px')}
    <div class="card" id="cl_fn" style="left:110px;top:240px;width:820px;height:380px;border-color:var(--sun)">
      <div class="abs small" style="left:30px;top:22px;letter-spacing:3px;color:var(--sun)">CALL A FUNCTION</div>
      <div id="cl_in" class="abs mono center" style="left:40px;top:150px;width:150px;height:80px;border-radius:14px;background:#4a1018;font-size:26px">input</div>
      <div id="cl_gear" class="abs" style="left:300px;top:110px;width:160px;height:160px">${ICON.gear('#f5b700')}</div>
      <div id="cl_out" class="abs mono center" style="left:580px;top:150px;width:200px;height:80px;border-radius:14px;background:var(--sun);color:#2a2000;font-size:28px;font-weight:700">answer</div>
      ${div('cl_done', 590, 260, 0, 0, 'done ✓', 'hand', 'font-size:44px;color:var(--sun)')}</div>
    <div class="card" id="cl_cls" style="left:990px;top:240px;width:820px;height:380px;border-color:var(--teal)">
      <div class="abs small" style="left:30px;top:22px;letter-spacing:3px;color:var(--teal)">CALL A CLASS</div>
      <div id="cl_bp" class="abs center col" style="left:40px;top:90px;width:220px;height:240px;border-radius:14px;border:3px dashed #ffd9a0;background:repeating-linear-gradient(0deg,#4a1a10 0 22px,#5a2414 22px 23px)"><b class="mono" style="font-size:24px;color:#ffd9a0">PdfReader</b><span class="small">the blueprint</span></div>
      ${arrow('cl_ba', 280, 210, 360, 210, '#2fb872', 6)}
      <div id="cl_obj" class="abs" style="left:380px;top:70px;width:400px;height:290px;border-radius:20px;background:#0f3a24;border:3px solid var(--teal)">
        <div class="abs mono" style="left:20px;top:14px;font-size:24px;color:var(--teal)">reader  (an object)</div>
        ${fileIcon('cl_pdf', 30, 70, 'pdf', '', .75)}
        ${['.pages', '.metadata', 'len(.pages)'].map((s, i) => `<div class="abs mono" id="cl_ab${i}" style="left:180px;top:${70 + i * 66}px;padding:8px 14px;border-radius:10px;background:#155a37;font-size:22px;color:#d9f7e6">${s}</div>`).join('')}</div></div>
    ${chip('cl_code', 110, 690, '<span class="va">reader</span> = <span class="cl">PdfReader</span>(path)', 'font-size:40px')}
    ${div('cl_no', 830, 690, 0, 0, '<span style="font:600 32px var(--sans)">“give me the text”</span>', '', 'background:#3a1426;color:#ff8fa3;padding:16px 26px;border-radius:20px')}
    ${div('cl_nox', 830, 720, 360, 5, '', 'strike')}
    ${div('cl_yes', 110, 810, 0, 0, '<span style="font:600 32px var(--sans)">“open this PDF, and give me something I can <b>ask questions of</b>”</span>', '', 'background:#0f3a24;color:#d9f7e6;padding:16px 26px;border-radius:20px')}
    <div class="card" id="cl_q" style="left:1300px;top:660px;width:510px;height:330px">
      ${['<span class="va">reader</span>.pages', '<span class="fn">len</span>(<span class="va">reader</span>.pages)', '<span class="va">reader</span>.pages[<span class="nu">0</span>]', '….<span class="fn">extract_text</span>()'].map((s, i) => `<div class="abs mono" id="cl_q${i}" style="left:24px;top:${22 + i * 74}px;font-size:26px;color:#fff1dc">${s}</div>`).join('')}
      <div class="abs mono" id="cl_qa0" style="left:330px;top:22px;font-size:24px;color:var(--teal)">→ the pages</div>
      <div class="abs" id="cl_qa1" style="left:400px;top:90px;font:800 52px var(--serif);color:var(--sun)">2</div>
      <div class="abs mono" id="cl_qa2" style="left:320px;top:170px;font-size:24px;color:var(--teal)">→ page 1</div>
      <div class="abs mono" id="cl_qa3" style="left:24px;top:290px;width:470px;font-size:19px;color:#ce9178;white-space:nowrap;overflow:hidden">'Plural Labs — Remote and Hybrid Work…'</div></div>
  `);
  // ---------- LAZY : behaves like a list ----------
  const pg = (i, x) => `<div class="abs" id="lz_p${i}" style="left:${x}px;top:250px;width:170px;height:220px;border-radius:10px;border:3px dashed #8f6a62;background:rgba(255,255,255,.03)"><div id="lz_pf${i}" class="abs" style="inset:0;border-radius:8px;background:#fff8ee">${[30, 55, 80, 105, 130, 155].map((y, k) => `<div class="abs" style="left:18px;top:${y}px;width:${[120, 100, 130, 90, 115, 80][k]}px;height:9px;border-radius:4px;background:#e8d7c4"></div>`).join('')}</div><div class="abs mono center" style="left:0;top:230px;width:170px;font-size:22px;color:#d9b8a6">page ${i + 1}</div></div>`;
  board('LAZY', ...G(3, 1), `
    ${div('lz_t', 110, 60, 0, 0, '<span class="mono">reader.pages</span> <span class="mute">looks like a list…</span>', 'h1', 'font-size:60px')}
    ${div('lz_b1', 120, 215, 0, 0, '[', 'mono', 'font-size:230px;line-height:1;color:var(--sun)')}
    ${pg(0, 230)}${pg(1, 440)}${pg(2, 650)}${pg(3, 860)}
    ${div('lz_b2', 1050, 215, 0, 0, ']', 'mono', 'font-size:230px;line-height:1;color:var(--sun)')}
    ${pill('lz_op1', 1250, 230, 'for page in …', 'bg-dark', 'font-family:var(--mono);font-size:26px')}${pill('lz_op2', 1250, 320, 'len(…)', 'bg-dark', 'font-family:var(--mono);font-size:26px')}${pill('lz_op3', 1250, 410, '…[0]', 'bg-dark', 'font-family:var(--mono);font-size:26px')}
    ${div('lz_hand', 700, 520, 0, 0, '👆', '', 'font-size:70px')}
    ${div('lz_n', 120, 600, 1000, 0, 'Pages are read only <b class="sun">when you reach for them</b>', 'h2', 'font-size:42px')}
    <div class="card" id="lz_big" style="left:120px;top:720px;width:900px;height:270px">
      ${[0, 1, 2, 3, 4, 5, 6, 7].map(i => `<div class="abs" style="left:${40 + i * 14}px;top:${40 + i * 10}px;width:130px;height:170px;border-radius:8px;border:2.5px dashed #8f6a62;background:#300810"></div>`).join('')}
      <div class="abs" style="left:300px;top:40px;font:800 70px var(--serif)"><span id="lz_cnt" data-dec="0">0</span> <span style="font-size:40px">pages</span></div>
      <div class="abs txt" style="left:300px;top:150px;font-size:32px">opened <b class="teal">instantly</b> — nothing read yet</div></div>
    <div class="card" id="lz_v1" style="left:1150px;top:720px;width:660px;height:120px;border-color:var(--teal)"><div class="center" style="height:120px;gap:18px;font:700 34px var(--sans)"><div style="width:52px;height:52px">${ICON.check()}</div>behaves like a list</div></div>
    <div class="card" id="lz_v2" style="left:1150px;top:870px;width:660px;height:120px;border-color:var(--rose)"><div class="center" style="height:120px;gap:18px;font:700 34px var(--sans)"><div style="width:52px;height:52px">${ICON.cross()}</div>is a list</div></div>
  `);
  // ---------- LIMIT : extract_text cannot see ----------
  const page = (id, x, y, photo) => `<div class="abs" id="${id}" style="left:${x}px;top:${y}px;width:330px;height:430px;border-radius:12px;background:${photo ? 'linear-gradient(135deg,#a8a29e,#d6d3d1 40%,#a8a29e)' : '#fff8ee'};box-shadow:0 20px 50px rgba(0,0,0,.5)${photo ? ';transform:rotate(-3deg)' : ''}">
     ${[50, 85, 120, 155, 190, 225, 260, 295, 330].map((yy, k) => `<div class="abs" style="left:30px;top:${yy}px;width:${[260, 220, 250, 200, 240, 180, 255, 210, 160][k]}px;height:12px;border-radius:5px;background:${photo ? '#57534e' : '#e8d7c4'};${photo ? 'filter:blur(1.5px)' : ''}"></div>`).join('')}</div>`;
  board('LIMIT', ...G(3, 0), `
    ${div('li_w', 110, 70, 110, 110, ICON.warn())}
    ${div('li_t', 250, 80, 0, 0, 'The most important limit', 'h1', 'font-size:70px')}
    ${page('li_pg', 140, 300, false)}
    <div class="abs" id="li_layer" style="left:140px;top:300px;width:330px;height:430px;border-radius:12px;border:3px solid var(--sky);background:rgba(255,217,160,.12)">
      ${['Plural Labs — Remote', 'and Hybrid Work Policy', '1. The default', 'arrangement…'].map((s, i) => `<div class="abs mono" style="left:22px;top:${50 + i * 46}px;font-size:21px;color:#fff1dc">${s}</div>`).join('')}
      <div class="abs small" style="left:22px;top:380px;color:var(--sky)">text layer</div></div>
    ${div('li_l1', 140, 770, 520, 0, '<b class="sky">extract_text()</b> pulls out text that is <b>already stored as text</b>', 'txt', 'font-size:28px')}
    ${div('li_eye', 760, 360, 200, 125, ICON.eye('#cfa999'))}
    ${div('li_eyex', 770, 415, 180, 8, '', 'strike')}
    ${div('li_eyel', 700, 520, 330, 0, 'it does not look at the page like your eyes do', 'txt center', 'font-size:26px')}
    ${page('li_ph', 1120, 300, true)}
    ${div('li_phl', 1120, 760, 0, 0, '📷 a photo of a document', 'txt', 'font-size:28px')}
    ${arrow('li_ar', 1470, 520, 1580, 520, '#e63946', 6)}
    ${chip('li_empty', 1600, 470, '<span class="st">""</span>', 'font-size:60px;border-color:var(--rose)')}
    ${div('li_noerr', 1590, 600, 0, 0, 'NO ERROR', 'badge bg-sun')}
    ${div('li_pol', 1580, 660, 300, 0, 'politely empty', 'hand', 'font-size:44px;color:var(--sun)')}
    <div class="card" id="li_pin" style="left:1060px;top:870px;width:760px;height:130px;border-color:var(--teal)"><div class="center" style="height:130px;gap:20px"><span style="font-size:46px">📌</span><span class="txt" style="font-size:30px">our loader <b class="teal">checks for exactly this</b></span></div></div>
  `);

  // ================= animation =================
  // d01 import os
  let t = T('d01');
  panel(t, 0, .8); PANEL_H = 0;
  showTab(t, '25');
  focus(t + .2, '25', 52, 52, { zmax: 2.2, cd: 1.6, dip: .2, minCols: 34 });
  note(W('d01', 'lets us'), '25', 52, 12, '📁 look inside folders', 'var(--sky)');
  // d02 import re
  t = T('d02');
  focus(t, '25', 74, 74, { zmax: 2.4, minCols: 34 });
  note(W('d02', 'new'), '25', 74, 12, 'NEW', 'var(--rose)');
  // d03 regex board
  t = T('d03');
  camB(t, 2.0, 'REGEX', 960, 300, 1.15, { dip: .3 });
  wipe('rx_t', t + .9, .8);
  // d04 replace
  t = T('d04');
  camB(t, 1.0, 'REGEX', 510, 340, 1.75);
  fadeIn('rx_a', t, .4);
  fadeUp('rx_code', W('d04', 'replace'), .4, 20);
  to('rx_cat', W('d04', 'cat'), .3, { s: 1.3 }, 'back');
  ft('rx_res', W('d04', 'dog') , .5, { o: 0, x: -40 }, { o: 1, x: 0 }, 'out');
  // d05
  t = T('d05');
  fadeIn('rx_ok', t + .3, .5); pulse('rx_res', W('d05', 'exactly'), 1.08);
  // d06 messy
  t = T('d06');
  camB(t, 1.0, 'REGEX', 1400, 340, 1.75);
  fadeIn('rx_b', t, .4); typeIn('rx_m', t + .2, 2.4);
  // d07
  t = T('d07');
  fadeUp('rx_m2', W('d07', 'squash'), .6, -40); fadeIn('rx_m3', W('d07', 'one space'), .5);
  // d08 forever
  t = T('d08');
  camB(t, 1.1, 'REGEX', 510, 770, 1.5);
  fadeIn('rx_c', t, .3);
  for (let i = 0; i < 7; i++) ft('rx_r' + i, t + .3 + i * .45, .4, { o: 0, x: -60 }, { o: 1, x: 0 }, 'back');
  popIn('rx_inf', W('d08', 'Forever'), .6);
  // d09-d11 shape
  t = T('d09');
  camB(t, 1.1, 'REGEX', 1400, 770, 1.5);
  fadeIn('rx_d', t, .4);
  slideR('rx_s1', W('d10', 'whitespace'), .5, 60); slideR('rx_s2', W('d10', 'digit'), .5, 60); fadeIn('rx_s2e', W('d10', 'colon'), .4);
  t = T('d11');
  popIn('rx_bi', W('d11', 'built'), .5);
  cam(t, 1.6, { x: G(-1, 1)[0] + 960, y: G(-1, 1)[1] + 560, z: .95 });
  // d12 back to code
  t = T('d12');
  focus(t, '25', 136, 136, { zmax: 2.4, cd: 2.0, dip: .3, minCols: 34 });
  // d13-17 two shapes
  t = T('d13');
  camB(t, 1.8, 'IMPORTS', 960, 300, 1.0, { dip: .3 });
  wipe('im_t', t + .6, .6); slideL('im_c1', W('d13', 'import os'), .5); slideR('im_c2', W('d13', 'Both'), .5);
  t = T('d14');
  camB(t, 1.0, 'IMPORTS', 510, 560, 1.35);
  fadeUp('im_m1', t + .1, .5); fadeUp('im_f1', t + .3, .5); drawIn('im_a1', W('d14', 'whole'), .4);
  ft('im_os', W('d14', 'whole') + .3, .6, { o: 0, x: -400, s: .5 }, { o: 1, x: 0, s: 1 }, 'out');
  fadeUp('im_u1', W('d14', 'keep writing'), .5, 20); fadeIn('im_u1n', W('d14', 'keep writing') + .4, .5);
  t = T('d15');
  camB(t, 1.0, 'IMPORTS', 1400, 480, 1.35);
  fadeUp('im_m2', t + .1, .5); fadeUp('im_f2', t + .3, .5);
  to('p1', W('d15', 'just one'), .4, { y: -20, s: 1.15, gl: .6 }, 'back');
  // d16 lands in file
  t = T('d16');
  to('p1', t + .1, 1.0, { x: 520, y: 80, s: 1.5 }, 'io');
  fadeUp('im_u2', W('d16', 'on its own'), .5, 20); fadeIn('im_u2n', W('d16', 'on its own') + .3, .4);
  fadeUp('im_u3', W('d16', 'instead'), .5, 20); ft('im_x', W('d16', 'instead') + .6, .4, { cw: 0 }, { cw: 1 });
  camB(W('d16', 'on its own'), 1.0, 'IMPORTS', 1400, 640, 1.3);
  t = T('d17');
  camB(t, 1.0, 'IMPORTS', 960, 640, .98);
  popIn('im_both', t + .2, .5);
  // d18-20 packages
  t = T('d18');
  camB(t, 1.4, 'PKG', 500, 380, 1.2, { dip: .2 });
  wipe('pk_t', t + .3, .6);
  popIn('pk_os', W('d18', 'os and'), .4); popIn('pk_re', W('d18', 're came') , .4); fadeIn('pk_l1', W('d18', 'came with'), .4);
  popIn('pk_pp', W('d18', 'did not'), .4); fadeIn('pk_l2', W('d18', 'did not') + .3, .4);
  t = T('d19');
  camB(t, 1.2, 'PKG', 1150, 500, 1.0);
  fadeIn('pk_pip', t, .4); ft('pk_box', W('d19', 'downloaded'), .7, { o: 0, y: -80 }, { o: 1, y: 0 }, 'back');
  drawIn('pk_a', W('d19', 'put it'), .6);
  to('pk_box', W('d19', 'put it'), .9, { x: 560, y: -40, s: .4, o: 0 }, 'in');
  fadeIn('pk_sp', W('d19', 'where Python'), .5);
  for (let i = 0; i < 7; i++) slideR('pk_f' + i, W('d19', 'where Python') + .3 + i * .12, .35, 40);
  t = T('d20');
  fadeUp('pk_nm', t + .2, .6); fadeIn('pk_nm2', W('d20', 'Nothing magic'), .6);
  camB(t, 1.2, 'PKG', 800, 650, 1.05);
  // d21-30 class
  t = T('d21');
  camB(t, 1.6, 'CLASS', 700, 200, 1.4, { dip: .25 });
  wipe('cl_t', t + .5, .7);
  t = T('d22');
  camB(t, 1.0, 'CLASS', 1450, 140, 1.6);
  slideR('cl_n1', W('d22', 'capital'), .4, 60); fadeIn('cl_n1l', W('d22', 'class'), .4);
  slideR('cl_n2', W('d22', 'Compare'), .4, 60); fadeIn('cl_n2l', W('d22', 'lowercase'), .4);
  t = T('d23');
  camB(t, 1.2, 'CLASS', 960, 430, 1.0);
  fadeIn('cl_fn', t + .2, .4); fadeIn('cl_cls', t + .45, .4);
  t = T('d24');
  camB(t, .9, 'CLASS', 520, 430, 1.6);
  ft('cl_in', W('d24', 'Call'), .5, { o: 0, x: -60 }, { o: 1, x: 0 });
  to('cl_in', W('d24', 'function') + .2, .6, { x: 220, o: 0 }, 'in');
  ft('cl_gear', W('d24', 'Call'), 3, { r: 0 }, { r: 360 }, 'io');
  popIn('cl_out', W('d24', 'answer'), .5); fadeIn('cl_done', W('d24', 'Done'), .4);
  t = T('d25');
  camB(t, .9, 'CLASS', 1400, 430, 1.6);
  popIn('cl_bp', W('d25', 'Call'), .45); drawIn('cl_ba', W('d25', 'object') - .3, .4);
  ft('cl_obj', W('d25', 'object'), .6, { o: 0, s: .4, x: -100 }, { o: 1, s: 1, x: 0 }, 'back');
  ['cl_ab0', 'cl_ab1', 'cl_ab2'].forEach((id, i) => popIn(id, W('d25', 'abilities') + i * .2, .35));
  t = T('d26');
  camB(t, 1.0, 'CLASS', 760, 760, 1.35);
  wipe('cl_code', t + .1, .9);
  fadeIn('cl_no', W('d26', 'give me'), .4); ft('cl_nox', END('d26', -.4), .3, { cw: 0 }, { cw: 1 });
  t = T('d27');
  fadeUp('cl_yes', t + .1, .5, 20); glow('cl_obj', W('d27', 'ask'), .4, .6);
  t = T('d28');
  camB(t, 1.0, 'CLASS', 1450, 780, 1.45);
  fadeIn('cl_q', t, .3);
  fadeIn('cl_q0', W('d28', 'reader.pages'), .3); fadeIn('cl_qa0', W('d28', 'gives'), .4); glow('cl_ab0', W('d28', 'gives'), .3, .7);
  t = T('d29');
  fadeIn('cl_q1', t + .1, .3); ft('cl_qa1', W('d29', 'tells'), .5, { o: 0, s: 2 }, { o: 1, s: 1 }, 'back');
  t = T('d30');
  fadeIn('cl_q2', t + .1, .3); fadeIn('cl_qa2', W('d30', 'first page'), .4);
  fadeIn('cl_q3', W('d30', 'extract'), .3); ft('cl_qa3', W('d30', 'extract') + .4, 1.4, { o: 0, cw: 0 }, { o: 1, cw: 1 }, 'lin');
  // d31-34 lazy
  t = T('d31');
  camB(t, 1.6, 'LAZY', 900, 330, 1.05, { dip: .25 });
  wipe('lz_t', t + .5, .6); popIn('lz_b1', t + .8, .4); popIn('lz_b2', t + .9, .4);
  [0, 1, 2, 3].forEach(i => { fadeIn('lz_p' + i, t + .9 + i * .1, .3); });
  popIn('lz_op1', W('d31', 'loop'), .4); popIn('lz_op2', W('d31', 'count'), .4); popIn('lz_op3', W('d31', 'index'), .4);
  [0, 1, 2, 3].forEach(i => init('lz_pf' + i, { o: 1 }));
  t = T('d32');
  [0, 1, 2, 3].forEach(i => to('lz_pf' + i, t + .2, .4, { o: 0 }));
  to('lz_b1', W('d32', 'not actually'), .5, { x: -60, r: -12 }, 'back'); to('lz_b2', W('d32', 'not actually'), .5, { x: 60, r: 12 }, 'back');
  ft('lz_hand', W('d32', 'only read'), .5, { o: 0, y: 80 }, { o: 1, y: 0 }, 'out');
  to('lz_hand', W('d32', 'moment'), .5, { x: 0, y: -170 }, 'io');
  ft('lz_pf2', W('d32', 'reach') , .4, { o: 0, s: .6 }, { o: 1, s: 1 }, 'back');
  to('lz_hand', END('d32'), .4, { o: 0 });
  fadeUp('lz_n', W('d32', 'reach'), .5, 20);
  t = T('d33');
  camB(t, 1.1, 'LAZY', 600, 800, 1.4);
  fadeIn('lz_big', t, .4); count('lz_cnt', t + .2, 1.5, 0, 500, 'out');
  t = T('d34');
  camB(t, 1.1, 'LAZY', 1300, 800, 1.3);
  slideR('lz_v1', W('d34', 'behaves'), .5, 60); slideR('lz_v2', W('d34', 'is a list'), .5, 60);
  pulse('lz_v1', W('d34', 'first one'), 1.06); glow('lz_v1', W('d34', 'first one'), .4, .6);
  // d35-40 limit
  t = T('d35');
  camB(t, 1.6, 'LIMIT', 600, 160, 1.4, { dip: .3 });
  ft('li_w', t + .5, .6, { o: 0, s: 2, r: -30 }, { o: 1, s: 1, r: 0 }, 'back'); wipe('li_t', t + .7, .6);
  shake('li_w', END('d35', -.3), 10);
  t = T('d36');
  camB(t, 1.1, 'LIMIT', 420, 560, 1.35);
  fadeUp('li_pg', t, .5); ft('li_layer', W('d36', 'text that'), 1.0, { o: 0, x: 0, y: 0 }, { o: 1, x: 60, y: -50 }, 'back');
  fadeIn('li_l1', W('d36', 'as text'), .5);
  t = T('d37');
  camB(t, 1.0, 'LIMIT', 870, 480, 1.4);
  popIn('li_eye', t + .2, .5); ft('li_eyex', W('d37', 'does not'), .4, { cw: 0 }, { cw: 1 }); fadeIn('li_eyel', W('d37', 'recognise'), .4);
  t = T('d38');
  camB(t, 1.1, 'LIMIT', 1400, 560, 1.25);
  ft('li_ph', t + .2, .6, { o: 0, r: 10, y: 60 }, { o: 1, r: -3, y: 0 }, 'back'); fadeIn('li_phl', W('d38', 'photograph'), .4);
  drawIn('li_ar', W('d38', 'no text'), .4);
  t = T('d39');
  popIn('li_empty', t + .2, .5); popIn('li_noerr', W('d39', 'Politely'), .4); fadeIn('li_pol', W('d39', 'no error'), .4);
  shake('li_empty', W('d39', 'empty'), 8);
  t = T('d40');
  camB(t, 1.2, 'LIMIT', 1200, 700, 1.0);
  slideR('li_pin', W('d40', 'loader'), .5, 60); glow('li_pin', W('d40', 'exactly'), .4, .7);
});
