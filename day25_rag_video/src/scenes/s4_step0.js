// c4 : step 0 - reading a PDF the Day 22 way crashes
(window.SCENES = window.SCENES || []).push(function () {
  const G = (c, r) => [c * 2400, r * 1500];
  const letters = 'Plural'.split('');
  board('STEP0', ...G(2, -1), `
    ${div('s0_t', 110, 60, 0, 0, 'Step 0 · a beginner\'s idea', 'h1', 'font-size:62px')}
    ${pill('s0_a', 110, 200, '📄 a PDF is a file', 'bg-dark', 'font-size:32px')}
    ${arrow('s0_a1', 470, 232, 560, 232, '#8e9bc4', 5)}
    ${pill('s0_b', 580, 200, '<span class="mono">open()</span>&nbsp;reads files', 'bg-dark', 'font-size:32px')}
    ${arrow('s0_a2', 950, 232, 1040, 232, '#8e9bc4', 5)}
    ${pill('s0_c', 1060, 200, 'so just open it! 🙂', 'bg-sun', 'font-size:32px')}
    <div class="card" id="s0_txt" style="left:110px;top:380px;width:820px;height:600px">
      <div class="abs small" style="left:30px;top:24px;letter-spacing:3px">A .TXT FILE</div>
      <div class="abs h2" style="left:30px;top:70px">just letters, one after another</div>
      ${letters.map((l, i) => `<div class="abs mono center" id="s0_l${i}" style="left:${40 + i * 90}px;top:190px;width:76px;height:90px;border-radius:12px;background:#1c2559;border:2px solid #3a4687;font-size:46px">${l}</div>`).join('')}
      ${arrow('s0_la', 330, 310, 330, 400, '#2dd4bf', 6)}
      ${chip('s0_str', 180, 420, '<span class="st">"Plural Labs - Leave Policy…"</span>', 'font-size:28px;border-color:var(--teal)')}
      ${div('s0_ok', 220, 520, 400, 60, '<div style="width:50px;height:50px">' + ICON.check() + '</div><span class="txt" style="font-size:30px;margin-left:16px">a Python string</span>', '', 'display:flex;align-items:center')}</div>
    <div class="card" id="s0_good" style="left:1000px;top:380px;width:810px;height:280px;border-color:var(--sun)">
      <div class="abs" style="left:34px;top:40px;width:120px;height:120px">${ICON.bell()}</div>
      <div class="abs h1" style="left:190px;top:40px;font-size:50px">the crash is the <span class="sun">good</span> case</div>
      <div class="abs txt" style="left:190px;top:160px;font-size:30px">it is loud — it stops and tells you exactly what went wrong</div></div>
    <div class="card" id="s0_bad" style="left:1000px;top:700px;width:810px;height:280px;border-color:var(--rose)">
      <div class="abs" style="left:34px;top:40px;width:120px;height:120px">${ICON.mute()}</div>
      <div class="abs h1" style="left:190px;top:40px;font-size:50px">the <span class="rose">quiet</span> case</div>
      <div class="abs mono" style="left:190px;top:140px;font-size:30px">open ✓ → <span class="st">""</span> → keeps running</div>
      <div class="abs hand" id="s0_dots" style="left:190px;top:196px;font-size:40px;color:var(--rose)">…and quietly knows nothing</div></div>
  `);
  const hex = ['25', '50', '44', '46', '2D', '31', '2E', '37', '0A', 'F9', '8A', '02', 'E3', 'CF', '9C', '78', 'DA', '5B', 'F9', '11'];
  const drawers = [['Fonts', 'var(--sky)'], ['Images', 'var(--vio)'], ['Page sizes', 'var(--sun)'], ['Text — compressed', 'var(--rose)']];
  board('PDFBOX', ...G(3, -1), `
    ${div('pb_t', 110, 60, 0, 0, 'A PDF is a small, compressed <span class="grad-text">database</span>', 'h1', 'font-size:58px')}
    <div class="abs" id="pb_cab" style="left:110px;top:200px;width:620px;height:780px;border-radius:22px;background:linear-gradient(180deg,#1d2a6e,#121a46);border:3px solid #3a4ba8">
      ${drawers.map(([n, c], i) => `<div class="abs" id="pb_d${i}" style="left:30px;top:${40 + i * 182}px;width:560px;height:160px;border-radius:14px;background:#0d1433;border:3px solid ${c};display:flex;align-items:center;padding-left:40px"><div style="width:90px;height:14px;border-radius:7px;background:${c};margin-right:36px"></div><span style="font:700 36px var(--sans)">${n}</span></div>`).join('')}</div>
    <div class="card" id="pb_bytes" style="left:820px;top:200px;width:990px;height:380px">
      <div class="abs small" style="left:30px;top:24px;letter-spacing:3px">WHAT open() ACTUALLY SEES</div>
      <div class="abs mono" id="pb_hex" style="left:30px;top:80px;width:600px;font-size:34px;line-height:1.5;color:#c4b5fd;word-spacing:8px">${hex.map((h, i) => `<span style="${h === 'F9' ? 'color:var(--rose);font-weight:800' : ''}">${h}</span>`).join(' ')}</div>
      <div class="abs mono center" id="pb_strbox" style="left:700px;top:100px;width:250px;height:160px;border-radius:16px;border:3px dashed var(--teal);font-size:30px;color:var(--teal)">str</div>
      ${div('pb_x', 790, 280, 70, 70, ICON.cross())}
      ${div('pb_note', 30, 300, 640, 0, 'not letters in any alphabet', 'hand', 'font-size:46px;color:var(--rose)')}</div>
    <div class="card" id="pb_key" style="left:820px;top:640px;width:990px;height:340px;border-color:var(--sun)">
      <div class="abs" id="pb_k" style="left:40px;top:120px;width:220px;height:110px">${ICON.key()}</div>
      <div class="abs mono" style="left:60px;top:250px;font-size:30px;color:var(--sun)">pypdf</div>
      ${fileIcon('pb_pdf', 330, 70, 'pdf', '', .95)}
      ${arrow('pb_ka', 520, 175, 600, 175, '#2dd4bf', 6)}
      <div class="abs mono" id="pb_flow" style="left:620px;top:90px;width:340px;font-size:24px;line-height:1.6;color:#ce9178">"Plural Labs — Remote<br>and Hybrid Work Policy<br>People Team · Version 3…"</div></div>
  `);
  // ================= animation =================
  let t = T('e01');
  focus(t, '25', 156, 162, { cd: 1.6, dip: .2, zmax: 1.7 });
  note(W('e01', 'zero'), '25', 149, 52, 'STEP 0', 'var(--rose)');
  t = T('e02');
  camB(t, 1.6, 'STEP0', 900, 200, 1.25, { dip: .25 });
  wipe('s0_t', t + .6, .6);
  popIn('s0_a', W('e02', 'a PDF'), .4); drawIn('s0_a1', W('e02', 'open') - .3, .3); popIn('s0_b', W('e02', 'open'), .4);
  drawIn('s0_a2', W('e02', 'So just') - .3, .3); popIn('s0_c', W('e02', 'So just'), .45);
  t = T('e03');
  focus(t, '25', 158, 162, { cd: 1.6, dip: .2, zmax: 1.7 });
  mark(W('e03', 'remote work'), '25', 159, 36, 58, 'var(--rose)');
  mark(W('e03', 'read it'), '25', 160, 8, 16);
  t = T('e04');
  panel(t - .2, 330);
  let tt = termCmd(t, 'python3 day25_rag.py', .035);
  termLine(tt + .1, 'STEP 0 - what happens if we read a PDF the Day 22 way');
  const errId = termLine(W('e04', 'refuses'), "    Python refused : <span class=\"err\">'utf-8' codec can't decode byte 0xf9 in position 7124: invalid start byte</span>");
  cam(t, 1.2, { x: VS.x + 1000, y: VS.y + 790, z: 1.4 });
  shake('vsc', W('e04', 'refuses') + .1, 16);
  cam(W('e04', 'utf-8'), 1.0, { x: VS.x + 1060, y: VS.y + 860, z: 1.7 });
  t = T('e05');
  camB(t, 1.8, 'STEP0', 520, 680, 1.25, { dip: .3 });
  fadeIn('s0_txt', t + .5, .4);
  letters.forEach((l, i) => ft('s0_l' + i, W('e05', 'letters') + i * .12, .45, { o: 0, y: -60 }, { o: 1, y: 0 }, 'back'));
  drawIn('s0_la', W('e05', 'Python can'), .4); popIn('s0_str', W('e05', 'straight'), .5); fadeIn('s0_ok', W('e05', 'string'), .4);
  t = T('e06');
  camB(t, 1.8, 'PDFBOX', 700, 540, .95, { dip: .3 });
  wipe('pb_t', t + .6, .6); ft('pb_cab', W('e06', 'compressed'), .7, { o: 0, s: .7 }, { o: 1, s: 1 }, 'back');
  t = T('e07');
  camB(t, 1.0, 'PDFBOX', 420, 590, 1.25);
  drawers.forEach((d, i) => ft('pb_d' + i, W('e07', ['fonts', 'images', 'page sizes', 'text itself'][i]), .5, { o: 0, x: -200 }, { o: 1, x: 0 }, 'back'));
  pulse('pb_d3', W('e07', 'binary'), 1.05);
  t = T('e08');
  camB(t, 1.0, 'PDFBOX', 1310, 400, 1.35);
  fadeIn('pb_bytes', t, .3); typeIn('pb_hex', t + .2, 2.0); fadeIn('pb_strbox', t + .5, .4);
  shake('pb_strbox', W('e08', 'cannot'), 12); popIn('pb_x', W('e08', 'cannot') + .2, .4); fadeIn('pb_note', W('e08', 'alphabet'), .4);
  t = T('e09');
  camB(t, 1.8, 'STEP0', 1400, 520, 1.35, { dip: .3 });
  slideR('s0_good', t + .6, .6);
  t = T('e10');
  pulse('s0_good', W('e10', 'loud'), 1.06); glow('s0_good', W('e10', 'loud'), .4, .7); to('s0_good', END('e10'), .4, { gl: 0 });
  t = T('e11');
  camB(t, 1.1, 'STEP0', 1400, 840, 1.35);
  slideR('s0_bad', t + .2, .6); fadeIn('s0_dots', W('e11', 'quietly'), .6); glow('s0_bad', W('e11', 'quietly'), .4, .7);
  t = T('e12');
  camB(t, 1.8, 'PDFBOX', 1310, 810, 1.35, { dip: .3 });
  fadeIn('pb_key', t + .5, .4); slideL('pb_k', W('e12', 'library'), .6, 100); popIn('pb_pdf', W('e12', 'library') + .2, .4);
  drawIn('pb_ka', W('e12', 'unpacks'), .4); ft('pb_flow', W('e12', 'unpacks') + .3, 1.2, { o: 0, cw: 0 }, { o: 1, cw: 1 }, 'lin');
  pulse('pb_k', W('e12', 'That is'), 1.15);
});
