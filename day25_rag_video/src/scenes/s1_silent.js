// c1 : the silent line
(window.SCENES = window.SCENES || []).push(function () {
  const G = (c, r) => [c * 2400, r * 1500];
  // ---------- KNOW : where company knowledge lives ----------
  const bld = `<div class="abs" style="left:0;top:0;width:260px;height:300px">
     <div class="abs" style="left:30px;top:40px;width:200px;height:260px;background:linear-gradient(180deg,#2a3a8f,#1a2463);border-radius:14px 14px 4px 4px;border:2px solid #4053b5"></div>
     ${[0, 1, 2, 3, 4].map(r => [0, 1, 2].map(c => `<div class="abs" style="left:${58 + c * 52}px;top:${70 + r * 42}px;width:32px;height:24px;border-radius:4px;background:${(r + c) % 3 ? '#ffd23f' : '#5a6bd0'}"></div>`).join('')).join('')}
     <div class="abs" style="left:100px;top:255px;width:60px;height:45px;background:#0d1433;border-radius:6px 6px 0 0"></div></div>`;
  board('KNOW', ...G(1, -1), `
    ${div('k_t', 110, 80, 1700, 0, 'Where does a company keep its knowledge?', 'h1', 'font-size:60px')}
    ${div('k_b', 830, 330, 260, 300, bld)}
    ${div('k_bn', 760, 650, 400, 0, 'PLURAL LABS', 'center', 'font:800 30px var(--sans);letter-spacing:6px')}
    ${curve('k_c1', 830, 420, 600, 330, 470, 320, '#ff4d6d', 4)}${curve('k_c2', 1090, 420, 1320, 330, 1450, 320, '#3b82f6', 4)}
    ${curve('k_c3', 830, 560, 600, 660, 470, 700, '#ff9f43', 4)}${curve('k_c4', 1090, 560, 1320, 660, 1450, 700, '#a78bfa', 4)}
    <div class="card" id="k_f1" style="left:110px;top:220px;width:360px;height:250px">${fileIcon('k_i1', 30, 30, 'pdf', '', .9)}<div class="abs h2" style="left:190px;top:70px">PDFs</div><div class="abs small" style="left:190px;top:125px">policies,<br>handbooks</div></div>
    <div class="card" id="k_f2" style="left:1450px;top:220px;width:360px;height:250px">${fileIcon('k_i2', 30, 30, 'docx', '', .9)}<div class="abs h2" style="left:190px;top:70px">Word</div><div class="abs small" style="left:190px;top:125px">contracts,<br>notes</div></div>
    <div class="card" id="k_f3" style="left:110px;top:600px;width:360px;height:250px">${fileIcon('k_i3', 30, 30, 'html', '', .9)}<div class="abs h2" style="left:190px;top:60px">Web<br>pages</div><div class="abs small" style="left:190px;top:165px">the intranet</div></div>
    <div class="card" id="k_f4" style="left:1450px;top:600px;width:360px;height:250px">${fileIcon('k_i4', 30, 30, 'png', '', .9)}<div class="abs h2" style="left:190px;top:60px">Screen-<br>shots</div><div class="abs small" style="left:190px;top:165px">pasted in chat</div></div>
    ${fileIcon('k_txt', 905, 760, 'txt', '', .55)}
    ${div('k_txtl', 690, 900, 540, 0, 'a neat little .txt file? almost never.', 'hand center', 'font-size:40px;color:var(--sun)')}
  `);
  // ---------- FOLDER : 9 files through the Day 22 gate ----------
  const files = [['expense_policy.txt', 'txt'], ['holiday_calendar_2026.png', 'png'], ['insurance_benefits.pdf', 'pdf'], ['it_security_handbook.pdf', 'pdf'], ['leave_policy.txt', 'txt'], ['pluraldesk_release_notes.html', 'html'], ['product_faq.txt', 'txt'], ['remote_work_policy.pdf', 'pdf'], ['support_tickets.txt', 'txt']];
  const fx = i => 95 + i * 197;
  let fh = '';
  files.forEach(([n, ty], i) => { fh += `<div class="abs" id="fd${i}" style="left:${fx(i)}px;top:70px;width:150px;height:250px">${fileIcon('fdi' + i, 0, 0, ty, '', .82)}<div class="abs mono" style="left:-22px;top:162px;width:170px;text-align:center;font-size:15px;color:#cdd6f7;white-space:normal;word-break:break-all;line-height:1.25">${n}</div></div>`; });
  board('FOLDER', ...G(1, 0), `
    ${div('fo_t', 100, -30, 0, 0, '<span class="mono" style="font-size:40px">📁 plural_labs_docs/</span>', 'h2')}
    ${pill('fo_p1', 260, 330, '4 TXT', '', 'background:#5b7bd5;color:#fff')}${pill('fo_p2', 560, 330, '3 PDF', 'bg-rose')}${pill('fo_p3', 860, 330, '1 HTML', '', 'background:#ff9f43;color:#2a1400')}${pill('fo_p4', 1180, 330, '1 PNG', 'bg-vio')}
    ${div('fo_gate', 560, 450, 800, 190, `<svg width="800" height="190"><path d="M0,0 H800 L520,190 H280 Z" fill="#141d4a" stroke="#ff4d6d" stroke-width="4"/></svg>
       <div class="abs center col" style="left:0;top:22px;width:800px"><b style="font:800 24px var(--sans);letter-spacing:4px;color:var(--rose)">DAY 22 LOADER</b><span class="mono" style="font-size:24px;margin-top:8px;color:#dfe6ff">endswith(".txt") ?</span></div>`)}
    ${div('fo_tray', 560, 690, 800, 170, '<div class="mono" style="position:absolute;left:24px;top:14px;font-size:24px;color:var(--teal)">documents = [</div><div class="mono" style="position:absolute;right:24px;bottom:12px;font-size:24px;color:var(--teal)">]</div>', 'card', 'border-color:var(--teal)')}
    ${fh}
    ${div('fo_c1', 1430, 500, 420, 150, '<div class="small" style="font-size:22px;letter-spacing:3px">LOADED</div><div style="font:800 76px var(--serif)"><span id="fo_n1" class="teal">0</span><span class="mute"> / 9</span></div>', 'card', 'padding:16px 28px')}
    ${div('fo_c2', 1430, 680, 420, 150, `<div class="small" style="font-size:22px;letter-spacing:3px">WARNINGS PRINTED</div><div style="display:flex;align-items:center;gap:20px"><span id="fo_n2" style="font:800 76px var(--serif)" class="rose">0</span><div style="width:64px;height:64px">${ICON.mute()}</div></div>`, 'card', 'padding:16px 28px')}
    ${div('fo_c3', 60, 500, 440, 150, '<div class="small" style="font-size:22px;letter-spacing:3px">SKIPPED</div><div style="font:800 76px var(--serif)" class="rose"><span id="fo_n3">0</span> <span style="font-size:34px">files</span></div>', 'card', 'padding:16px 28px')}
  `);
  // ---------- SILENT : loud vs quiet ----------
  board('SILENT', ...G(2, 0), `
    <div class="card" id="si_a" style="left:90px;top:110px;width:600px;height:400px;border-color:var(--sun)"><div class="abs" style="left:40px;top:40px;width:110px;height:110px">${ICON.bell()}</div>
       <div class="abs h1" style="left:40px;top:180px;font-size:58px">A crash</div><div class="abs txt" style="left:40px;top:270px;font-size:34px">→ you <b class="sun">notice</b> it</div></div>
    <div class="card" id="si_b" style="left:760px;top:110px;width:600px;height:400px;border-color:var(--rose)"><div class="abs" style="left:40px;top:40px;width:110px;height:110px">${ICON.mute()}</div>
       <div class="abs h1" style="left:40px;top:180px;font-size:58px">A silent skip</div><div class="abs txt" style="left:40px;top:270px;font-size:34px">→ you <b class="rose">never</b> notice it</div></div>
    ${div('si_q', 90, 600, 0, 0, '<span style="font:600 30px var(--sans)">Can I work from home permanently?</span>', '', 'background:var(--sky);color:#04223a;padding:18px 28px;border-radius:22px 22px 4px 22px')}
    ${div('si_r', 90, 710, 0, 0, '<span style="font:500 28px var(--sans)">🤖 I could not find this in the Plural Labs documents.</span>', '', 'background:#1b2558;padding:18px 28px;border-radius:22px 22px 22px 4px;border:1.5px solid var(--line)')}
    ${icon('si_p', 120, 830, 90, 'person', '#ffd23f')}
    ${div('si_bl', 230, 845, 0, 0, '“the AI is useless!”', 'hand', 'font-size:52px;color:var(--sun)')}
    ${div('si_x', 270, 875, 330, 6, '', 'strike')}
    ${arrow('si_ar', 700, 880, 980, 880, '#2dd4bf', 6)}
    ${div('si_ld', 1000, 840, 0, 0, 'the real culprit: <b class="mono">the loader</b>', 'pill bg-teal', 'position:absolute;font-size:30px')}
    <div class="card" id="si_rm" style="left:1430px;top:110px;width:420px;height:400px">
       <div class="small" style="position:absolute;left:30px;top:26px;letter-spacing:3px">ROADMAP</div>
       <div id="si_r1" class="abs" style="left:30px;top:80px;width:360px;height:130px;border-radius:16px;background:rgba(255,77,109,.15);border:2px solid var(--rose);padding:16px 22px"><b style="font-size:22px;letter-spacing:3px" class="rose">TODAY</b><div class="h2" style="font-size:40px">PDFs</div></div>
       <div id="si_r2" class="abs" style="left:30px;top:235px;width:360px;height:130px;border-radius:16px;border:2px dashed #3a4687;padding:16px 22px"><b style="font-size:22px;letter-spacing:3px" class="mute">NEXT CLASS</b><div class="h2" style="font-size:34px;color:#aab4dd">HTML · screenshot</div></div></div>
  `);

  // ================= animation =================
  // b01
  let t = T('b01');
  focus(t, '22', 92, 96, { cd: 1.2, zmax: 2.0 });
  const m1 = mark(W('b01', 'two lines'), '22', 95, 11, 37, 'var(--rose)');
  // b02
  t = T('b02');
  camTok(t, '22', 95, 8, 50, 2.3, 1.0);
  const m2 = mark(W('b02', 'end with'), '22', 95, 20, 37);
  note(W('b02', 'end with') + .4, '22', 95, 40, 'does the name end with .txt ?');
  const m3 = mark(W('b02', 'continue'), '22', 96, 8, 16, 'var(--teal)');
  note(W('b02', 'skip it'), '22', 96, 19, '→ skip this file, go to the next one', 'var(--teal)');
  camTok(W('b02', 'skip it'), '22', 96, 8, 50, 2.3, .9);
  // b03
  t = T('b03');
  focus(t, '22', 92, 96, { hl: false, cd: 1.0, zmax: 1.7 });
  note(W('b03', 'harmless'), '22', 92, 40, 'Day 22: all 4 files were .txt ✓', 'var(--sky)');
  // b04 : fly to KNOW
  t = T('b04');
  camB(t, 2.0, 'KNOW', 960, 520, .9, { dip: .35 });
  wipe('k_t', t + .7, .8);
  ft('k_b', t + 1.0, .7, { o: 0, y: 80 }, { o: 1, y: 0 }, 'back'); fadeIn('k_bn', t + 1.3, .5);
  ft('k_b', W('b04', 'actually live'), .5, { sy: 1 }, { sy: 1.06 }, 'out'); to('k_b', W('b04', 'actually live') + .5, .5, { sy: 1 });
  // b05
  t = T('b05');
  [['k_f1', 'k_c1', 'PDFs'], ['k_f2', 'k_c2', 'Word'], ['k_f3', 'k_c3', 'web pages'], ['k_f4', 'k_c4', 'screenshots']].forEach(([f, c, w]) => { drawIn(c, W('b05', w) - .3, .5); popIn(f, W('b05', w), .55); });
  cam(W('b05', 'Word'), 3.5, { x: G(1, -1)[0] + 960, y: G(1, -1)[1] + 560, z: .98 });
  // b06
  t = T('b06');
  ft('k_txt', t + .2, .6, { o: 0, s: 1.6 }, { o: 1, s: 1 }, 'back');
  fadeUp('k_txtl', W('b06', 'neat'), .6, 20);
  ['k_f1', 'k_f2', 'k_f3', 'k_f4'].forEach((id, i) => pulse(id, t + .3 + i * .15, 1.05));
  camB(t, 1.3, 'KNOW', 960, 760, 1.35);
  shake('k_txt', W('b06', 'text file'), 8);
  // b07 : back to explorer
  t = T('b07');
  cam(t, 1.8, { x: VS.x + 230, y: VS.y + 250, z: 2.0 }, { dip: .3 });
  sideHL(t + 1.2, 1);
  for (let i = 0; i < 9; i++) sideHL(W('b07', 'Let') + .35 * i, 2 + i);
  // b08 : FOLDER
  t = T('b08');
  camB(t, 1.4, 'FOLDER', 960, 300, 1.0, { dip: .2 });
  fadeIn('fo_t', t + .2, .5);
  for (let i = 0; i < 9; i++) ft('fd' + i, t + .3 + i * .1, .5, { o: 0, y: -60 }, { o: 1, y: 0 }, 'back');
  [['fo_p1', 'Four'], ['fo_p2', 'three'], ['fo_p3', 'HTML'], ['fo_p4', 'screenshot']].forEach(([p, w]) => popIn(p, W('b08', w), .45));
  [[0, 4, 6, 8], [2, 3, 7], [5], [1]].forEach((g, k) => g.forEach(i => pulse('fd' + i, W('b08', ['Four', 'three', 'HTML', 'screenshot'][k]) + .1, 1.08)));
  // b09 : gate
  t = T('b09');
  camB(t, 1.3, 'FOLDER', 960, 470, .92);
  ft('fo_gate', W('b09', 'feed'), .6, { o: 0, y: -40 }, { o: 1, y: 0 }, 'back');
  fadeUp('fo_tray', W('b09', 'watch'), .5);
  ['fo_p1', 'fo_p2', 'fo_p3', 'fo_p4'].forEach(id => to(id, t + .3, .4, { o: .0 }));
  // b10 : through the gate
  t = T('b10');
  const keep = [0, 4, 6, 8];
  keep.forEach((i, k) => {
    const dx = (600 + k * 190) - fx(i), dy = 545;
    to('fd' + i, t + .2 + k * .35, .9, { x: dx * .5, y: 480, s: .75 }, 'in');
    to('fd' + i, t + 1.1 + k * .35, .6, { x: dx, y: dy, s: .58 }, 'out');
  });
  [1, 2, 3, 5, 7].forEach((i, k) => {
    const tt = W('b10', 'Gone') + k * .22;
    to('fd' + i, tt - .4, .35, { y: -30, r: (k % 2 ? 8 : -8) }, 'out');
    to('fd' + i, tt, 1.1, { y: 1100, r: (k % 2 ? 50 : -50), o: 0 }, 'in');
  });
  count('fo_n1', t + .6, 1.8, 0, 4, 'lin');
  fadeIn('fo_c1', t + .2, .4);
  // b11
  t = T('b11');
  fadeIn('fo_c3', t, .4); count('fo_n3', t + .2, 1.2, 0, 5, 'lin');
  popIn('fo_c2', W('b11', 'not print'), .5); pulse('fo_c2', W('b11', 'single'), 1.12); glow('fo_c2', W('b11', 'single'), .4, .8);
  camB(W('b11', 'not print'), 1.2, 'FOLDER', 1400, 660, 1.2);
  // b12 : loud vs silent
  t = T('b12');
  camB(t, 1.6, 'SILENT', 730, 320, 1.15, { dip: .2 });
  slideL('si_a', W('b12', 'A crash'), .6); slideR('si_b', W('b12', 'A silent'), .6);
  pulse('si_a', W('b12', 'notice'), 1.06); glow('si_b', W('b12', 'never notice'), .4, .7);
  // b13 : blame the AI
  t = T('b13');
  camB(t, 1.2, 'SILENT', 700, 780, 1.15);
  fadeUp('si_q', t + .1, .5, 20); fadeUp('si_r', W('b13', 'get'), .5, 20);
  popIn('si_p', W('b13', 'blame'), .5); fadeIn('si_bl', W('b13', 'blame') + .2, .5);
  ft('si_x', END('b13', -.6), .4, { cw: 0 }, { cw: 1 }); drawIn('si_ar', END('b13', -.3), .5); popIn('si_ld', END('b13', .1), .5);
  // b14 : roadmap
  t = T('b14');
  camB(t, 1.3, 'SILENT', 1500, 330, 1.35);
  fadeIn('si_rm', t + .1, .4); slideR('si_r1', W('b14', 'PDFs'), .5, 60); glow('si_r1', W('b14', 'PDFs') + .4, .4, .7);
  slideR('si_r2', W('b14', 'next class'), .5, 60);
});
