// c10 : wrap up
(window.SCENES = window.SCENES || []).push(function () {
  const G = (c, r) => [c * 2400, r * 1500];
  const take = (id, x, n, title, col) => `<div class="card" id="${id}" style="left:${x}px;top:200px;width:540px;height:300px;border-color:${col}">
     <div class="abs" style="left:34px;top:24px;font:800 110px var(--serif);color:${col}">${n}</div>
     <div class="abs h2" style="left:34px;top:170px;width:480px;font-size:38px">${title}</div></div>`;
  const steps = ['open', 'pull out text', 'clean', 'split pages', 'check not empty'];
  board('TAKE', ...G(4, 1), `
    ${div('tk_t', 110, 60, 0, 0, 'Three things to take away', 'h1', 'font-size:62px')}
    ${take('tk_1', 110, '1', 'The loader got wider, not the retrieval', 'var(--teal)')}
    ${take('tk_2', 690, '2', 'A loader is a pipeline', 'var(--sun)')}
    ${take('tk_3', 1270, '3', 'A dict of functions = one-line formats', 'var(--vio)')}
    <div class="card" id="tk_m" style="left:110px;top:560px;width:540px;height:460px">
      <div class="abs small" style="left:30px;top:24px;letter-spacing:3px">QUALITY ≈ WHAT IT CAN OPEN</div>
      <div class="abs" style="left:40px;top:90px;width:460px;height:40px;border-radius:20px;background:#4a1018"></div>
      <div class="abs" id="tk_mb" style="left:40px;top:90px;width:460px;height:40px;border-radius:20px;background:linear-gradient(90deg,#2fb872,#ffd9a0)"></div>
      <div class="abs txt" style="left:40px;top:160px;width:460px;font-size:28px">Day 22: <b>4</b> of 9 files<br>Day 25: <b class="teal">7</b> of 9 files</div>
      <div class="abs hand" style="left:40px;top:300px;width:460px;font-size:38px;color:var(--teal)">usually the cheapest part to improve</div></div>
    <div class="card" id="tk_p" style="left:690px;top:560px;width:540px;height:460px">
      ${steps.map((s, i) => `<div class="abs" id="tk_s${i}" style="left:40px;top:${30 + i * 82}px;display:flex;align-items:center;gap:18px"><span class="center" style="width:54px;height:54px;border-radius:50%;background:var(--sun);color:#2a2000;font:800 28px var(--serif)">${i + 1}</span><span style="font:600 32px var(--sans)">${s}</span></div>`).join('')}</div>
    <div class="card" id="tk_d" style="left:1270px;top:560px;width:540px;height:460px">
      <div class="abs mono" style="left:30px;top:40px;font-size:28px;line-height:1.7">LOADERS = {<br>&nbsp;&nbsp;<span style="color:#ce9178">".txt"</span>: load_txt,<br>&nbsp;&nbsp;<span style="color:#ce9178">".md"</span>:  load_txt,<br>&nbsp;&nbsp;<span style="color:#ce9178">".pdf"</span>: load_pdf,<br><span id="tk_new" style="display:inline-block;color:var(--orange)">&nbsp;&nbsp;".html": load_html,</span><br>}</div>
      ${div('tk_plus', 360, 330, 0, 0, '+1 line', 'pill bg-sun', 'position:absolute;font-size:30px')}</div>
  `);
  const words = ['Home', 'HR Portal', 'IT Desk', 'Finance', 'Accept cookies', 'Menu', 'Login', 'Home', 'Careers'];
  board('BROKEN', ...G(5, 1), `
    ${div('br_t', 110, 60, 0, 0, 'What is still broken?', 'h1', 'font-size:62px')}
    <div class="card" id="br_html" style="left:110px;top:190px;width:820px;height:480px;border-color:var(--orange)">
      ${fileIcon('br_hi', 40, 40, 'html', '', .9)}
      <div class="abs h2" style="left:220px;top:50px">the HTML page</div>
      <div class="abs txt" style="left:220px;top:110px;width:560px;font-size:26px">strip the menu, the cookie banner, the JavaScript…</div>
      ${words.map((w, i) => `<div class="abs" id="br_w${i}" style="left:${40 + (i % 3) * 250}px;top:${250 + Math.floor(i / 3) * 70}px;padding:8px 18px;border-radius:10px;background:#3a2410;color:#ffbf86;font:600 26px var(--sans)">${w}</div>`).join('')}</div>
    <div class="card" id="br_img" style="left:990px;top:190px;width:820px;height:480px;border-color:var(--vio)">
      ${fileIcon('br_ii', 40, 40, 'png', '', .9)}
      <div class="abs h2" style="left:220px;top:50px">the screenshot</div>
      <div class="abs txt" style="left:220px;top:110px;width:560px;font-size:26px">no text inside — only a picture of text</div>
      <div class="abs" id="br_eye" style="left:260px;top:240px;width:300px;height:190px">${ICON.eye('#f7a1b0')}</div>
      ${div('br_eyel', 200, 420, 0, 0, 'needs a model with eyes', 'hand', 'font-size:42px;color:var(--vio)')}</div>
    <div class="card" id="br_ch" style="left:110px;top:720px;width:1700px;height:290px;border-color:var(--rose)">
      <div class="abs" id="br_sc" style="left:50px;top:70px;width:150px;height:150px">${ICON.scissors()}</div>
      <div class="abs h2" style="left:260px;top:70px;font-size:48px">chunking</div>
      <div class="abs txt" style="left:260px;top:150px;font-size:34px">the <b class="rose">single biggest quality win</b> left in this project</div></div>
  `);
  const rungs = ['Load · any file type', 'Chunk · sentences + overlap', 'Embed · batching + cost', 'Store · persistence', 'Retrieve · hybrid search', 'Fix the question', 'Rerank', 'Citations + refusal', 'Evaluate', 'Ship it'];
  board('LADDER', ...G(6, 1), `
    ${div('ld_t', 110, 60, 0, 0, 'The RAG ladder', 'h1', 'font-size:62px')}
    ${rungs.map((r, i) => `<div class="abs" id="ld_r${i}" style="left:${110 + (i % 2) * 860}px;top:${190 + Math.floor(i / 2) * 120}px;width:820px;height:96px;border-radius:16px;background:#3a0a12;border:2.5px solid ${i === 0 ? 'var(--rose)' : '#6e1e29'};display:flex;align-items:center;gap:24px;padding-left:24px">
       <span style="font:800 44px var(--serif);color:${i === 0 ? 'var(--rose)' : '#8f6a62'}">${String(i + 1).padStart(2, '0')}</span><span style="font:600 30px var(--sans);color:${i === 0 ? '#fff' : '#d9b8a6'}">${r}</span>
       ${i === 0 ? '<span class="abs" style="right:20px;top:24px;font:800 20px var(--sans);letter-spacing:2px;padding:8px 14px;border-radius:8px;background:var(--rose)">PDF ✓ · HTML + IMAGE NEXT</span>' : ''}</div>`).join('')}
    <div class="card" id="ld_hw" style="left:110px;top:820px;width:1700px;height:210px;border-color:var(--sun)">
      <div class="abs small" style="left:30px;top:22px;letter-spacing:3px;color:var(--sun)">BEFORE NEXT CLASS</div>
      ${['run the file yourself', 'try every question', 'swap the hyphen + whitespace lines, count the matches'].map((s, i) => `<div class="abs" id="ld_h${i}" style="left:${30 + [0, 420, 820][i]}px;top:90px;display:flex;gap:14px;align-items:center"><div style="width:44px;height:44px">${ICON.check('#f5b700')}</div><span style="font:600 28px var(--sans)">${s}</span></div>`).join('')}</div>
  `);
  board('END', ...G(5, 0), `
    ${div('en_eye', 0, 330, 1920, 0, 'Plural Labs · AI Developer Program', 'eyebrow', 'text-align:center')}
    ${div('en_t', 0, 400, 1920, 0, 'See you in the next class', '', 'font:800 120px var(--serif);text-align:center')}
    ${div('en_s', 0, 560, 1920, 0, 'Day 26 · <span class="sun">HTML pages</span> and <span class="vio">screenshots</span>', 'h2', 'font-size:48px;color:#f6e2cc;text-align:center')}
  `);

  // ================= animation =================
  let t = T('k01');
  camB(t, 2.2, 'TAKE', 960, 330, 1.0, { dip: .4 });
  wipe('tk_t', t + .9, .6);
  t = T('k02');
  camB(t, 1.0, 'TAKE', 380, 600, 1.15);
  slideL('tk_1', t, .5);
  t = T('k03');
  fadeIn('tk_m', t, .3); ft('tk_mb', W('k03', 'actually open'), 1.0, { cw: 0 }, { cw: .78 }, 'out');
  t = T('k04');
  camB(t, 1.0, 'TAKE', 960, 600, 1.15);
  fadeUp('tk_2', t, .5); fadeIn('tk_p', t + .3, .3);
  t = T('k05');
  steps.forEach((s, i) => slideL('tk_s' + i, W('k05', ['Open', 'Pull', 'Clean', 'Split', 'check'][i]), .4, 40));
  t = T('k06');
  pulse('tk_s2', W('k06', 'cleaning'), 1.1); pulse('tk_s4', W('k06', 'checking'), 1.1);
  t = T('k07');
  camB(t, 1.0, 'TAKE', 1540, 600, 1.15);
  slideR('tk_3', t, .5); fadeIn('tk_d', t + .3, .3); init('tk_new', { o: 0 }); fadeIn('tk_new', W('k07', 'one line'), .4); popIn('tk_plus', W('k07', 'one line') + .3, .4);
  t = T('k08');
  panel(t, 470); termClear(t);
  camVS(t, 2.0, .93, { dip: .4, dy: 150 });
  ['    loaded expense_policy.txt -> 1 piece(s)', '    <span class="warn">skipping holiday_calendar_2026.png - no loader for .png yet</span>', '    loaded insurance_benefits.pdf -> 1 piece(s)', '    <span class="warn">skipping pluraldesk_release_notes.html - no loader for .html yet</span>']
    .forEach((h, i) => termLine(t + .8 + i * .15, h));
  cam(W('k08', 'It told'), 1.0, { x: VS.x + 900, y: VS.y + 640, z: 1.5 });
  t = T('k09');
  camB(t, 1.8, 'BROKEN', 520, 430, 1.4, { dip: .3 });
  wipe('br_t', t + .3, .5); fadeIn('br_html', t + .5, .3);
  words.forEach((w, i) => ft('br_w' + i, W('k09', 'menu') + i * .12, .35, { o: 0, s: .5 }, { o: 1, s: 1 }, 'back'));
  words.forEach((w, i) => to('br_w' + i, W('k09', 'Home,') + i * .05, .5, { y: 300, o: 0, r: (i % 2 ? 20 : -20) }, 'in'));
  t = T('k10');
  camB(t, 1.0, 'BROKEN', 1400, 430, 1.4);
  fadeIn('br_img', t, .3); popIn('br_eye', W('k10', 'model with eyes'), .5); fadeIn('br_eyel', W('k10', 'model with eyes') + .3, .4);
  t = T('k11');
  camB(t, 1.0, 'BROKEN', 960, 860, 1.2);
  fadeUp('br_ch', t, .5); ft('br_sc', W('k11', 'chunking'), 1.5, { r: 0 }, { r: 360 }, 'io');
  t = T('k12');
  camB(t, 1.8, 'LADDER', 960, 480, .98, { dip: .3 });
  wipe('ld_t', t + .5, .5); rungs.forEach((r, i) => slideL('ld_r' + i, t + .7 + i * .12, .4, 60)); glow('ld_r0', W('k12', 'One rung'), .4, .8);
  t = T('k13');
  camB(t, 1.0, 'LADDER', 960, 900, 1.2);
  fadeIn('ld_hw', t, .3); [0, 1, 2].forEach(i => popIn('ld_h' + i, W('k13', ['run the file', 'Try every', 'swap'][i]), .4));
  t = T('k14');
  camB(t, 2.0, 'END', 960, 480, 1.0, { dip: .3 });
  wipe('en_eye', t + .5, .6); fadeUp('en_t', t + .7, .7); fadeUp('en_s', t + 1.1, .6);
  // grand finale: pull out to see the whole world we travelled through
  cam(END('k14', 1.2), 4.5, { x: 6960, y: 2790, z: .1 }, { ease: 'io', drift: 0, noCut: true });
});
