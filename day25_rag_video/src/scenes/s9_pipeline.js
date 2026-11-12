// c9 : steps 2 to 8, and the answers
(window.SCENES = window.SCENES || []).push(function () {
  const G = (c, r) => [c * 2400, r * 1500];
  const R = window.RUNS;
  // ---------- CHUNK ----------
  const seg = (n, w, col) => Array.from({ length: n }, (_, i) => `<div class="abs" id="ck_${col}${i}" style="left:${i * w}px;top:0;width:${w - 6}px;height:70px;border-radius:10px;background:${col === 'a' ? 'linear-gradient(90deg,#2dd4bf,#38bdf8)' : 'linear-gradient(90deg,#a78bfa,#ff4d6d)'}"></div>`).join('');
  board('CHUNK', ...G(4, 0), `
    ${div('ck_t', 110, 50, 0, 0, 'Step 2 · chunk <span class="mute" style="font-size:40px">— same 60-word cutting</span>', 'h1', 'font-size:58px')}
    <div class="card" id="ck_pages" style="left:110px;top:170px;width:1700px;height:300px">
      <div class="abs mono" style="left:30px;top:30px;font-size:24px;color:#cfd8ff">remote_work_policy.pdf · page 1</div>
      <div class="abs" style="left:30px;top:70px;width:1640px;height:70px">${seg(7, 234, 'a')}</div>
      <div class="abs mono" style="left:30px;top:170px;font-size:24px;color:#cfd8ff">page 2</div>
      <div class="abs" style="left:30px;top:210px;width:400px;height:70px">${seg(1, 300, 'b')}</div>
      <div class="abs" id="ck_wall" style="left:20px;top:155px;width:1660px;height:5px;border-radius:3px;background:var(--sun);box-shadow:0 0 18px var(--sun)"></div>
      <div class="abs" id="ck_sc" style="left:250px;top:10px;width:60px;height:60px">${ICON.scissors('#ffd23f')}</div>
      ${div('ck_free', 500, 215, 0, 0, '½ the chunking done for free — a chunk never mixes two pages', 'hand', 'font-size:38px;color:var(--sun)')}</div>
    <div class="card" id="ck_lab" style="left:110px;top:510px;width:1000px;height:270px">
      <div class="abs small" style="left:30px;top:20px;letter-spacing:3px">THE LABEL ON EACH CHUNK</div>
      <div class="abs mono" id="ck_l22" style="left:30px;top:70px;font-size:30px;color:#8e9bc4">Day 22: {<span style="color:#ce9178">"source"</span>: <span style="color:#ce9178">"remote_work_policy.pdf"</span>}</div>
      <div class="abs mono" id="ck_l25" style="left:30px;top:150px;font-size:30px">Day 25: {<span style="color:#ce9178">"source"</span>: <span style="color:#ce9178">"remote_work_policy.pdf"</span>, <span id="ck_pg" style="display:inline-block;background:var(--sun);color:#2a2000;border-radius:8px;padding:0 8px">"page": 1</span>}</div></div>
    <div class="card" id="ck_cnt" style="left:1170px;top:510px;width:640px;height:270px">
      <div class="abs small" style="left:30px;top:20px;letter-spacing:3px">PIECES → CHUNKS</div>
      <div class="abs" style="left:30px;top:70px;font:800 130px var(--serif)"><span class="mute">9</span> → <span id="ck_n" class="teal" data-dec="0">9</span></div></div>
    <div class="card" id="ck_emb" style="left:110px;top:820px;width:1700px;height:220px">
      <div class="abs small" style="left:30px;top:20px;letter-spacing:3px">STEPS 3 + 4 · EMBED AND STORE — UNCHANGED</div>
      ${[0, 1, 2, 3].map(i => `<div class="abs" id="ck_e${i}" style="left:${40 + i * 70}px;top:80px;width:56px;height:100px;border-radius:8px;background:linear-gradient(180deg,#2dd4bf,#38bdf8)"></div>`).join('')}
      ${arrow('ck_ea', 340, 130, 450, 130, '#8e9bc4', 6)}
      <div class="abs mono" id="ck_vec" style="left:470px;top:80px;font-size:26px;color:#c4b5fd;line-height:1.6">[0.012, -0.044, 0.031, …]  × 3072<br><span style="color:var(--sun)">+ {"source": …, "page": 1}</span></div>
      ${arrow('ck_eb', 1150, 130, 1260, 130, '#8e9bc4', 6)}
      <div class="abs" id="ck_db" style="left:1290px;top:50px;width:110px;height:130px">${ICON.db('#a78bfa')}</div>
      ${div('ck_dbl', 1420, 100, 0, 0, 'Qdrant', 'h2', 'font-size:40px;color:var(--vio)')}</div>
  `);
  // ---------- QA ----------
  board('QA', ...G(4, -1), `
    ${div('qa_t', 110, 60, 0, 0, 'The question that ended Day 22', 'h1', 'font-size:58px')}
    <div class="abs" id="qa_q" style="left:110px;top:190px;padding:30px 44px;border-radius:30px 30px 6px 30px;background:var(--sky);color:#04223a;font:700 52px var(--sans)">Can I work from home permanently at Plural Labs?</div>
    <div class="abs" id="qa_old" style="left:110px;top:380px;width:900px;padding:26px 34px;border-radius:24px;background:#1b2558;border:2px solid var(--line);font:500 32px var(--sans);filter:grayscale(1)">
      <div class="small" style="letter-spacing:3px;margin-bottom:10px">DAY 22 · 4 TEXT FILES</div>🤖 I could not find this in the Plural Labs documents.</div>
    <div class="card" id="qa_diff" style="left:110px;top:640px;width:1700px;height:380px">
      ${[['retrieval', 'same', 'var(--mute)'], ['prompt', 'same', 'var(--mute)'], ['loader', 'can now open PDFs', 'var(--teal)']].map(([a, b, c], i) => `<div class="abs" id="qa_r${i}" style="left:40px;top:${40 + i * 105}px;display:flex;align-items:center;gap:30px"><span class="mono" style="font-size:40px;width:260px">${a}</span><span style="font:700 40px var(--sans);color:${c}">${b}</span></div>`).join('')}
      <div class="abs" id="qa_wide" style="left:1150px;top:60px;width:440px;height:260px"><svg width="440" height="260"><path d="M0,20 H440 L300,240 H140 Z" fill="rgba(45,212,191,.15)" stroke="#2dd4bf" stroke-width="5"/></svg><div class="abs center" style="left:0;top:60px;width:440px;font:800 34px var(--sans);color:var(--teal)">the loader got wider</div></div></div>
  `);
  // ---------- PROMPT ----------
  const top = R[0].top;
  board('PROMPT', ...G(5, -1), `
    ${div('pr_t', 110, 50, 0, 0, 'Step 7 · augment', 'h1', 'font-size:58px')}
    <div class="lcard" id="pr_doc" style="left:110px;top:160px;width:1700px;height:860px;padding:36px 44px;font:400 23px/1.55 var(--mono);color:#1a1f3d">
      <div id="pr_i0">You are the internal helpdesk assistant for a company called Plural Labs.</div>
      <div id="pr_i1" style="margin-top:10px">Answer the question using ONLY the context given below. … Do not use any outside knowledge.</div>
      <div id="pr_i2" style="margin-top:10px;background:#fff3c4;border-radius:6px;padding:2px 8px;margin-left:-8px">At the end, mention which file your answer came from, <b>and the page number if there is one.</b></div>
      <div style="margin-top:22px;font-weight:700">CONTEXT:</div>
      ${top.map((c, i) => `<div id="pr_c${i}" style="margin-top:10px"><span id="pr_h${i}" style="display:inline-block;background:#d7f5ef;color:#0f6256;font-weight:700;border-radius:6px;padding:0 8px">From ${c[1]}:</span><div style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#4a5175">${c[2].slice(0, 120)}…</div></div>`).join('')}
      <div style="margin-top:22px;font-weight:700">QUESTION:</div><div id="pr_qq">${R[0].q}</div></div>
    ${div('pr_n', 1280, 60, 0, 0, 'the model can only cite a page if we show it one', 'hand', 'font-size:40px;color:var(--sun);width:560px')}
  `);
  // ---------- QTOUR ----------
  const tour = [
    [R[1].q, '₹15,000 · claim within 60 days', 'remote_work_policy.pdf · page 1', 'var(--rose)'],
    [R[2].q, '5 minutes · you cannot raise it', 'it_security_handbook.pdf · page 1', 'var(--sky)'],
    [R[3].q, 'not by default · ₹8,000 yearly top-up', 'insurance_benefits.pdf · page 1', 'var(--vio)'],
    [R[4].q, '24 paid leaves (12 casual + 12 sick)', 'leave_policy.txt', 'var(--teal)'],
  ];
  board('QTOUR', ...G(6, -1), `
    ${div('qt_t', 110, 50, 0, 0, 'Try the other questions', 'h1', 'font-size:58px')}
    ${tour.map(([q, a, s, c], i) => `<div class="card" id="qt_c${i}" style="left:${110 + (i % 2) * 870}px;top:${170 + Math.floor(i / 2) * 430}px;width:830px;height:390px;border-color:${c}">
      <div class="abs" style="left:30px;top:30px;width:770px;font:600 30px/1.35 var(--sans);color:#dfe6ff">“${q}”</div>
      <div class="abs" id="qt_a${i}" style="left:30px;top:160px;width:770px;font:800 44px/1.2 var(--serif);color:${c}">${a}</div>
      <div class="abs mono" id="qt_s${i}" style="left:30px;top:300px;padding:8px 16px;border-radius:10px;background:#0b1130;font-size:24px;color:var(--sun)">📄 ${s}</div></div>`).join('')}
    ${div('qt_ok', 1330, 1000, 0, 0, 'Day 22 still works ✓', 'pill bg-teal', 'position:absolute;font-size:30px')}
  `);
  // ---------- HONEST ----------
  const sc = R[5].top.map(x => x[0]);
  board('HONEST', ...G(6, 0), `
    ${div('ho_t', 110, 50, 0, 0, 'The honesty test', 'h1', 'font-size:58px')}
    <div class="abs" id="ho_q" style="left:110px;top:170px;padding:24px 36px;border-radius:26px 26px 6px 26px;background:var(--sky);color:#04223a;font:700 42px var(--sans)">What is the notice period if I resign from Plural Labs?</div>
    ${div('ho_none', 110, 300, 0, 0, 'in none of our 9 files', 'pill bg-rose', 'position:absolute;font-size:28px')}
    <div class="card" id="ho_sc" style="left:110px;top:400px;width:1100px;height:420px">
      <div class="abs small" style="left:30px;top:20px;letter-spacing:3px">SIMILARITY SCORES OF THE 3 RETURNED CHUNKS</div>
      ${sc.map((v, i) => `<div class="abs mono" style="left:30px;top:${80 + i * 70}px;font-size:24px;color:#cfd8ff">leave_policy.txt</div><div class="abs" id="ho_b${i}" style="left:300px;top:${84 + i * 70}px;width:${(v - .5) * 2400}px;height:34px;border-radius:8px;background:var(--rose)"></div><div class="abs mono" style="left:${320 + (v - .5) * 2400}px;top:${82 + i * 70}px;font-size:26px;color:var(--rose)">${v.toFixed(3)}</div>`).join('')}
      <div class="abs mono" style="left:30px;top:310px;font-size:24px;color:#8e9bc4">real answer (work from home)</div><div class="abs" id="ho_bw" style="left:440px;top:314px;width:${(R[0].top[0][0] - .5) * 2400}px;height:34px;border-radius:8px;background:var(--teal)"></div><div class="abs mono" id="ho_bwn" style="left:${460 + (R[0].top[0][0] - .5) * 2400}px;top:312px;font-size:26px;color:var(--teal)">${R[0].top[0][0].toFixed(3)}</div></div>
    <div class="card" id="ho_k" style="left:1270px;top:400px;width:540px;height:420px;border-color:var(--sun)">
      <div class="abs mono" style="left:30px;top:30px;font-size:40px;color:var(--sun)">k = 3</div>
      <div class="abs txt" style="left:30px;top:110px;width:480px;font-size:32px">always returns <b>three</b> chunks — helpful or not</div>
      <div class="abs h2" id="ho_k2" style="left:30px;top:270px;width:480px;font-size:38px">high score <span class="rose">≠</span> answer is there</div></div>
    <div class="abs" id="ho_ans" style="left:110px;top:870px;width:1700px;padding:30px 40px;border-radius:24px;background:#0c3b3a;border:3px solid var(--teal);display:flex;gap:28px;align-items:center">
      <div style="width:80px;height:80px;flex:none">${ICON.check()}</div><span style="font:600 38px var(--sans);color:#ccfbf1">🤖 “I could not find this in the Plural Labs documents.”</span></div>
  `);

  // ================= animation =================
  let t = T('j01');
  camB(t, 2.6, 'PIPE', 960, 540, .95, { dip: .45 });
  for (let i = 1; i < 8; i++) { to('plk' + i, W('j01', 'move quickly') + i * .12, .3, { o: 0 }); to('pn' + i, W('j01', 'move quickly') + i * .12, .4, { o: 1, gl: .9 }); to('pn' + i, W('j01', 'move quickly') + i * .12 + .5, .4, { gl: 0 }); }
  to('pn0', t, .5, { s: 1, gl: 0 }); to('p_today', t, .4, { o: 0 }); to('p_same', t, .4, { o: 0 });
  glow('pn1', W('j01', 'one new thing'), .4, 1.1);
  // j02 - j07 chunk
  t = T('j02');
  camB(t, 2.2, 'CHUNK', 960, 320, 1.05, { dip: .4 });
  wipe('ck_t', t + .9, .6); fadeIn('ck_pages', t + 1.0, .3);
  for (let i = 0; i < 7; i++) ft('ck_a' + i, t + 1.2 + i * .15, .3, { o: 0, sx: .2 }, { o: 1, sx: 1 }, 'out');
  ft('ck_b0', t + 2.3, .3, { o: 0, sx: .2 }, { o: 1, sx: 1 }, 'out');
  ft('ck_sc', t + 1.1, 1.6, { o: 1, x: 0 }, { o: 1, x: 1300 }, 'lin'); init('ck_sc', { o: 0 }); to('ck_sc', t + 2.7, .3, { o: 0 });
  t = T('j03');
  camB(t, 1.0, 'CHUNK', 610, 640, 1.5);
  fadeIn('ck_lab', t, .3); fadeIn('ck_l22', W('j03', 'Day 22'), .4); fadeIn('ck_l25', W('j03', 'Now it'), .4);
  ft('ck_pg', W('j03', 'page number'), .5, { s: 2.2, o: 0 }, { s: 1, o: 1 }, 'back');
  t = T('j04');
  pulse('ck_pg', W('j04', 'travels'), 1.25); glow('ck_pg', W('j04', 'travels'), .3, .9);
  camB(W('j04', 'database'), 1.4, 'CHUNK', 960, 600, .95);
  t = T('j05');
  camB(t, 1.0, 'CHUNK', 960, 320, 1.1);
  ft('ck_wall', W('j05', 'loaded page'), .7, { cw: 0 }, { cw: 1 });
  t = T('j06');
  fadeIn('ck_free', t + .2, .5);
  t = T('j07');
  camB(t, 1.0, 'CHUNK', 1490, 640, 1.5);
  fadeIn('ck_cnt', t, .3); count('ck_n', W('j07', 'forty'), 1.2, 9, 44);
  t = T('j08');
  camB(t, 1.0, 'CHUNK', 960, 930, 1.05);
  fadeIn('ck_emb', t, .3); [0, 1, 2, 3].forEach(i => popIn('ck_e' + i, t + .3 + i * .1, .3));
  drawIn('ck_ea', W('j08', 'Embed'), .3); wipe('ck_vec', W('j08', 'Embed') + .3, .8);
  t = T('j09');
  drawIn('ck_eb', W('j09', 'stores'), .3); popIn('ck_db', W('j09', 'stores') + .2, .4); fadeIn('ck_dbl', W('j09', 'stores') + .4, .3);
  pulse('ck_db', W('j09', 'Source'), 1.15);
  // j10 - j13 question
  t = T('j10');
  camB(t, 1.8, 'QA', 960, 320, 1.0, { dip: .3 });
  wipe('qa_t', t + .6, .6);
  t = T('j11');
  ft('qa_q', t, .6, { o: 0, s: .7, y: 40 }, { o: 1, s: 1, y: 0 }, 'back');
  t = T('j12');
  fadeUp('qa_old', t + .2, .5); camB(t, 1.0, 'QA', 700, 440, 1.25);
  t = T('j13');
  camB(t, 1.0, 'QA', 960, 830, 1.05);
  fadeIn('qa_diff', t, .3); slideL('qa_r0', W('j13', 'retrieval'), .4, 40); slideL('qa_r1', W('j13', 'prompt'), .4, 40); slideL('qa_r2', W('j13', 'loader'), .4, 40);
  ft('qa_wide', W('j13', 'open a PDF'), .6, { o: 0, sx: .5 }, { o: 1, sx: 1 }, 'back');
  // j14 - j15 retrieval in the terminal
  t = T('j14');
  panel(t, 620); termClear(t);
  camVS(t, 2.0, .93, { dip: .35, dy: 150 });
  const tl = (tt, h) => termLine(tt, h, { dx: -20, d: .2 });
  tl(t + .6, 'STEP 2 - CHUNK : cut into 44 chunks');
  tl(t + .8, 'STEP 3 and 4 - EMBED and STORE : Qdrant ready with 44 vectors');
  tl(t + 1.0, '------------------------------------------------------------');
  tl(t + 1.2, 'QUESTION : ' + R[0].q);
  tl(t + 1.4, '------------------------------------------------------------');
  tl(W('j14', 'three winning') - .3, 'STEP 5 and 6 - RETRIEVE and RANK : the 3 winning chunks are');
  const rl = R[0].top.map((c, i) => tl(W('j14', 'three winning') + .2 + i * .35, `    <span class="ok">${c[0].toFixed(3)}</span> | <span id="rsrc${i}" style="color:#e2c08d">${c[1]}</span> | ${c[2].slice(0, 65).replace(/</g, '&lt;')} ...`));
  cam(W('j14', 'three winning'), 1.2, { x: VS.x + 1050, y: VS.y + 600, z: 1.25 });
  t = T('j15');
  cam(t, 1.0, { x: VS.x + 860, y: VS.y + 625, z: 1.9 });
  [0, 1, 2].forEach(i => { const w = ['page one', 'Page two', 'page one again'][i]; to('rsrc' + i, W('j15', w), .3, { s: 1 }); });
  // j16 - j18 prompt
  t = T('j16');
  camB(t, 1.8, 'PROMPT', 960, 560, .95, { dip: .3 });
  wipe('pr_t', t + .5, .5); fadeIn('pr_doc', t + .6, .4);
  [0, 1, 2].forEach(i => { fadeIn('pr_c' + i, W('j16', 'header line') + i * .4, .4); ft('pr_h' + i, W('j16', 'page number') + i * .3, .4, { s: 1.15 }, { s: 1 }, 'back'); });
  t = T('j17');
  camB(t, 1.0, 'PROMPT', 900, 290, 1.5);
  pulse('pr_i2', W('j17', 'page number'), 1.03); glow('pr_i2', W('j17', 'page number'), .4, .5);
  t = T('j18');
  fadeIn('pr_n', t + .2, .5); camB(t, 1.0, 'PROMPT', 1300, 300, 1.2);
  // j19 - j21 answer in the terminal
  t = T('j19');
  termClear(t + .5);
  camVS(t, 1.8, .93, { dip: .3, dy: 150 });
  tl(t + .7, 'STEP 7 - AUGMENT : prompt built, ' + R[0].plen + ' characters');
  tl(t + .9, '------------------------------------------------------------');
  tl(t + 1.1, 'STEP 8 - GENERATE : grounded answer');
  tl(t + 1.2, '');
  const ans = R[0].ans.split('\n')[0];
  const words = ans.split(' '); const perLine = 14; const chunks = [];
  for (let i = 0; i < words.length; i += perLine) chunks.push(words.slice(i, i + perLine).join(' '));
  const t0 = W('j19', 'here is'), t1 = END('j20', -1.0);
  chunks.forEach((c, i) => tl(t0 + (t1 - t0) * i / chunks.length, `<span style="color:#ffffff">${c}</span>`));
  tl(t1 + .3, '');
  const srcLine = tl(W('j21', 'Source'), '<span style="color:var(--sun);font-weight:700">Source: remote_work_policy.pdf, page 1</span>');
  cam(t0, 1.2, { x: VS.x + 1000, y: VS.y + 580, z: 1.3 });
  cam(W('j21', 'Source'), .9, { x: VS.x + 750, y: VS.y + 690, z: 2.0 });
  t = T('j22');
  camB(t, 1.8, 'QA', 960, 830, 1.05, { dip: .3 });
  [0, 1, 2].forEach(i => pulse('qa_r' + i, W('j22', ['Same question', 'Same retrieval', 'Same prompt'][i]), 1.08));
  glow('qa_wide', W('j22', 'wider'), .4, .7); pulse('qa_wide', W('j22', 'wider'), 1.1);
  // j23 - j26 tour
  [0, 1, 2, 3].forEach((i) => {
    const id = 'j2' + (3 + i); t = T(id);
    camB(t, i === 0 ? 1.8 : 1.0, 'QTOUR', 545 + (i % 2) * 870, 365 + Math.floor(i / 2) * 430, 1.35, { dip: i === 0 ? .3 : 0 });
    fadeUp('qt_c' + i, t + .2, .5, 30); init('qt_a' + i, { o: 0 }); init('qt_s' + i, { o: 0 });
    fadeIn('qt_a' + i, M(id, .45), .5); slideR('qt_s' + i, M(id, .7), .4, 40);
  });
  if (true) { wipe('qt_t', T('j23', .6), .5); popIn('qt_ok', W('j26', 'did not break'), .5); }
  // j27 - j30 honesty
  t = T('j27');
  camB(t, 1.8, 'HONEST', 960, 300, 1.1, { dip: .3 });
  wipe('ho_t', t + .5, .5); fadeUp('ho_q', W('j27', 'notice'), .5, 30);
  t = T('j28');
  popIn('ho_none', W('j28', 'none'), .4);
  camB(W('j28', 'look at the scores'), 1.0, 'HONEST', 660, 610, 1.4);
  fadeIn('ho_sc', W('j28', 'look at the scores') - .2, .3);
  [0, 1, 2].forEach(i => ft('ho_b' + i, W('j28', 'Point') + i * .2, .6, { cw: 0 }, { cw: 1 }));
  ft('ho_bw', W('j28', 'Even higher'), .6, { cw: 0 }, { cw: 1 }); init('ho_bwn', { o: 0 }); fadeIn('ho_bwn', W('j28', 'Even higher') + .5, .3);
  t = T('j29');
  camB(t, 1.0, 'HONEST', 1540, 610, 1.45);
  fadeIn('ho_k', t, .4); fadeUp('ho_k2', W('j29', 'high score'), .5, 20);
  t = T('j30');
  camB(t, 1.0, 'HONEST', 960, 900, 1.05);
  ft('ho_ans', W('j30', 'I could not'), .6, { o: 0, s: .8 }, { o: 1, s: 1 }, 'back'); glow('ho_ans', W('j30', 'Exactly'), .4, .8);
});
