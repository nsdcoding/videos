// c8 : the loading loop, and running it
(window.SCENES = window.SCENES || []).push(function () {
  const G = (c, r) => [c * 2400, r * 1500];
  const names = ['support_tickets.txt', 'expense_policy.txt', 'remote_work_policy.pdf', 'holiday_calendar_2026.png', 'leave_policy.txt', 'insurance_benefits.pdf'];
  const sorted = [...names].sort();
  board('LOOPV', ...G(4, 4), `
    ${div('lv_t', 110, 50, 0, 0, 'The loop, one file at a time', 'h1', 'font-size:58px')}
    <div class="card" id="lv_sort" style="left:110px;top:170px;width:820px;height:420px">
      <div class="abs small" style="left:30px;top:18px;letter-spacing:3px">sorted(os.listdir(folder))</div>
      ${names.map((n, i) => `<div class="abs mono" id="lv_n${i}" style="left:40px;top:${70 + i * 56}px;font-size:26px;padding:4px 14px;border-radius:8px;background:#24050a">${n}</div>`).join('')}
      ${div('lv_same', 520, 350, 0, 0, 'same order, every run', 'hand', 'font-size:38px;color:var(--teal)')}</div>
    <div class="card" id="lv_split" style="left:990px;top:170px;width:820px;height:420px">
      <div class="abs small" style="left:30px;top:18px;letter-spacing:3px">os.path.splitext(name)[1].lower()</div>
      <div class="abs mono" style="left:40px;top:80px;font-size:40px"><span id="lv_a">remote_work_policy</span><span id="lv_b" style="display:inline-block;color:var(--rose)">.pdf</span></div>
      <div class="abs" id="lv_sc" style="left:420px;top:40px;width:70px;height:70px">${ICON.scissors()}</div>
      <div class="abs mono" id="lv_tup" style="left:40px;top:170px;font-size:32px">(<span style="color:#ce9178">"remote_work_policy"</span>, <span style="color:#ce9178;background:rgba(230,57,70,.25);border-radius:6px">".pdf"</span>)</div>
      ${div('lv_idx', 470, 225, 0, 0, '↑ [1]', 'mono', 'font-size:30px;color:var(--rose)')}
      <div class="abs mono" id="lv_up" style="left:40px;top:300px;font-size:36px">"NOTES.PDF" → <span id="lv_low" style="color:var(--teal)">".pdf"</span></div></div>
    <div class="card" id="lv_get" style="left:110px;top:630px;width:820px;height:400px">
      <div class="abs mono" style="left:40px;top:40px;font-size:36px">LOADERS[<span style="color:#ce9178">".html"</span>]</div>
      <div class="abs" id="lv_boom" style="left:440px;top:24px;padding:12px 20px;border-radius:12px;background:var(--rose);font:700 30px var(--mono)">💥 KeyError</div>
      <div class="abs mono" style="left:40px;top:180px;font-size:36px">LOADERS.<span style="color:#dcdcaa">get</span>(<span style="color:#ce9178">".html"</span>)</div>
      <div class="abs" id="lv_calm" style="left:520px;top:166px;padding:12px 20px;border-radius:12px;background:#55121c;border:2.5px solid #569cd6;font:700 30px var(--mono);color:#569cd6">None 😌</div>
      ${div('lv_gl', 40, 290, 760, 0, '.get never crashes — we deal with None ourselves', 'txt', 'font-size:28px;color:var(--teal)')}</div>
    <div class="card" id="lv_todo" style="left:990px;top:630px;width:820px;height:400px;border-color:var(--sun)">
      <div class="abs small" style="left:30px;top:20px;letter-spacing:3px;color:var(--sun)">A LOUD SKIP IS A TO-DO LIST</div>
      ${['☐  write a loader for .html', '☐  write a loader for .png'].map((s, i) => `<div class="abs" id="lv_td${i}" style="left:40px;top:${90 + i * 80}px;font:600 34px var(--sans)">${s}</div>`).join('')}
      ${div('lv_hw', 40, 270, 0, 0, '= next class\'s homework, printed on screen', 'hand', 'font-size:40px;color:var(--sun)')}</div>
  `);
  board('LOOPV2', ...G(5, 4), `
    ${div('l2v_t', 110, 60, 0, 0, '<span class="mono">pieces = loader(file_path)</span>', 'h1', 'font-size:56px')}
    <div class="abs center col" id="l2v_var" style="left:700px;top:260px;width:520px;height:340px;border-radius:26px;border:4px solid var(--sun);background:#3a0a12">
      <div class="abs mono" style="left:24px;top:14px;font-size:30px;color:var(--sun)">loader</div>
      <div class="abs center" id="l2v_ft" style="left:110px;top:120px;width:300px;height:100px;border-radius:16px;border:3px solid var(--teal);font:700 32px var(--mono);color:var(--teal)">load_txt</div>
      <div class="abs center" id="l2v_fp" style="left:110px;top:120px;width:300px;height:100px;border-radius:16px;border:3px solid var(--rose);font:700 32px var(--mono);color:var(--rose)">load_pdf</div></div>
    ${[['txt', 'leave_policy.txt'], ['pdf', 'remote_work_policy.pdf'], ['txt', 'support_tickets.txt']].map(([ty, n], i) => fileIcon('l2v_f' + i, 200, 330, ty, n, .9)).join('')}
    <div class="abs" id="l2v_docs" style="left:1350px;top:220px;width:480px;height:640px;border-radius:22px;border:3px solid var(--teal);background:#24050a">
      <div class="abs mono" style="left:24px;top:16px;font-size:28px;color:var(--teal)">documents = [</div>
      ${[['leave_policy.txt', 'None'], ['remote_work_policy.pdf', '1'], ['remote_work_policy.pdf', '2'], ['support_tickets.txt', 'None']].map(([s, p], i) => `<div class="abs mono" id="l2v_d${i}" style="left:24px;top:${80 + i * 125}px;width:430px;padding:12px 16px;border-radius:12px;background:#4a0e17;font-size:19px;line-height:1.5"><span style="color:#ce9178">"source"</span>: <span style="color:var(--sun)">${s}</span><br><span style="color:#ce9178">"page"</span>: ${p}, <span style="color:#ce9178">"text"</span>: …</div>`).join('')}</div>
    ${div('l2v_n', 700, 660, 520, 0, 'the dictionary already chose the function', 'hand center', 'font-size:40px;color:var(--sun)')}
  `);
  // a result card beside the VS Code window
  add(`<div class="card" id="cmp9" style="left:${VS.x + 1830}px;top:${VS.y + 560}px;width:520px;height:340px;border-color:var(--teal)">
     <div class="abs small" style="left:30px;top:22px;letter-spacing:3px">PIECES OF TEXT LOADED</div>
     <div class="abs" style="left:30px;top:70px;font:800 130px var(--serif)" ><span id="cmp_n" class="teal" data-dec="0">0</span></div>
     <div class="abs txt" style="left:220px;top:110px;font-size:34px">Day 25</div>
     <div class="abs" style="left:30px;top:230px;font:700 46px var(--serif);color:#cfa999">4 <span style="font:500 28px var(--sans)">on Day 22</span></div></div>`);

  // ================= animation =================
  let t = T('i01');
  focus(t, '25', 423, 423, { cd: 1.8, dip: .3, zmax: 2.2, minCols: 46 });
  t = T('i02');
  camB(t, 2.0, 'LOOPV', 520, 380, 1.45, { dip: .35 });
  wipe('lv_t', t + .7, .5); fadeIn('lv_sort', t + .8, .3);
  names.forEach((n, i) => { fadeIn('lv_n' + i, t + 1.0 + i * .08, .2); const k = sorted.indexOf(n); to('lv_n' + i, W('i02', 'sorted') + .3, .9, { y: (k - i) * 56 }, 'io'); });
  fadeIn('lv_same', W('i02', 'same order'), .4);
  t = T('i03');
  focus(t, '25', 429, 429, { cd: 1.8, dip: .3, zmax: 2.0, minCols: 56 });
  mark(W('i03', 'splitext'), '25', 429, 16, 32);
  t = T('i04');
  camB(t, 1.8, 'LOOPV', 1400, 380, 1.45, { dip: .3 });
  fadeIn('lv_split', t + .5, .3); init('lv_sc', { o: 0 });
  ft('lv_sc', W('i04', 'becomes') - .5, .6, { o: 0, y: -40 }, { o: 1, y: 30 }, 'out'); to('lv_b', W('i04', 'becomes'), .4, { x: 30 }, 'back');
  fadeUp('lv_tup', W('i04', 'and dot'), .4, 20); fadeIn('lv_idx', W('i04', 'Square'), .4);
  t = T('i05');
  fadeIn('lv_up', W('i05', 'lower'), .4); pulse('lv_low', W('i05', 'capitals'), 1.3);
  t = T('i06');
  focus(t, '25', 434, 434, { cd: 1.8, dip: .3, zmax: 2.3, minCols: 40 });
  mark(W('i06', 'get'), '25', 434, 13, 24);
  t = T('i07');
  camB(t, 1.8, 'LOOPV', 520, 830, 1.45, { dip: .3 });
  fadeIn('lv_get', t + .5, .3); init('lv_boom', { o: 0 }); init('lv_calm', { o: 0 });
  t = T('i08');
  ft('lv_boom', W('i08', 'KeyError'), .4, { o: 0, s: 2 }, { o: 1, s: 1 }, 'back'); shake('lv_get', W('i08', 'crash the whole'), 12);
  t = T('i09');
  popIn('lv_calm', W('i09', 'None'), .45); fadeIn('lv_gl', END('i09', -.5), .4);
  t = T('i10');
  focus(t, '25', 436, 440, { cd: 1.8, dip: .3, zmax: 2.0 });
  note(W('i10', 'skipping'), '25', 439, 70, 'LOUD', 'var(--sun)');
  t = T('i11');
  camB(t, 1.8, 'LOOPV', 1400, 830, 1.45, { dip: .3 });
  fadeIn('lv_todo', t + .5, .3); slideR('lv_td0', W('i11', 'to-do'), .4, 40); slideR('lv_td1', W('i11', 'to-do') + .3, .4, 40); fadeIn('lv_hw', W('i11', 'homework'), .5);
  t = T('i12');
  focus(t, '25', 447, 447, { cd: 1.8, dip: .3, zmax: 2.4, minCols: 40 });
  mark(W('i12', 'magic'), '25', 447, 13, 30, 'var(--sun)'); glow('hl25', W('i12', 'magic'), .4, .5);
  t = T('i13');
  note(W('i13', 'never write'), '25', 447, 34, '<s>load_pdf(file_path)</s>', 'var(--rose)');
  t = T('i14');
  camB(t, 1.8, 'LOOPV2', 960, 450, 1.0, { dip: .35 });
  wipe('l2v_t', t + .6, .5); fadeIn('l2v_var', t + .7, .3); init('l2v_fp', { o: 0 }); init('l2v_ft', { o: 0 });
  [0, 1, 2].forEach(i => {
    const ts = t + 1.2 + i * 1.6;
    ft('l2v_f' + i, ts, .4, { o: 0, x: -200 }, { o: 1, x: 0 }, 'out');
    to('l2v_f' + i, ts + .5, .6, { x: 640, s: .4, o: 0 }, 'in');
    const f = i === 1 ? 'l2v_fp' : 'l2v_ft';
    set(f, ts + .9, { o: 1 }); to(f, ts + 1.5, .1, { o: 0 });
  });
  fadeIn('l2v_n', W('i14', 'already decided'), .4);
  t = T('i15');
  focus(t, '25', 451, 456, { cd: 1.8, dip: .3, zmax: 2.0 });
  mark(W('i15', 'file name'), '25', 453, 12, 38, 'var(--sun)');
  t = T('i16');
  camB(t, 1.8, 'LOOPV2', 1590, 540, 1.25, { dip: .3 });
  fadeIn('l2v_docs', t + .4, .3); [0, 1, 2, 3].forEach(i => slideR('l2v_d' + i, W('i16', 'Source') + i * .35, .4, 40));
  t = T('i17');
  focus(t, '25', 458, 458, { cd: 1.8, dip: .3, zmax: 2.2, minCols: 60 });
  // i18 - i22 : run it
  t = T('i18');
  unfocus(t, '25');
  panel(t, 470); termClear(t);
  camVS(t, 1.2, .93, { dy: 140 });
  const steps = [
    [T('i18', 1.6), null, 'python3 day25_rag.py'],
    [W('i18', 'watch') + .6, 'STEP 0 - what happens if we read a PDF the Day 22 way'],
    [W('i18', 'watch') + .7, "    Python refused : <span class=\"err\">'utf-8' codec can't decode byte 0xf9 in position 7124: invalid start byte</span>"],
    [W('i18', 'watch') + .8, '------------------------------------------------------------'],
    [W('i19', 'Expense'), '    loaded expense_policy.txt -> 1 piece(s)'],
    [W('i19', 'skipping'), '    <span class="warn">skipping holiday_calendar_2026.png - no loader for .png yet</span>'],
    [W('i20', 'Insurance'), '    loaded insurance_benefits.pdf -> 1 piece(s)'],
    [W('i20', 'IT security'), '    loaded it_security_handbook.pdf -> 2 piece(s)'],
    [W('i21', 'Leave'), '    loaded leave_policy.txt -> 1 piece(s)'],
    [W('i21', 'Skipping'), '    <span class="warn">skipping pluraldesk_release_notes.html - no loader for .html yet</span>'],
    [W('i21', 'Product'), '    loaded product_faq.txt -> 1 piece(s)'],
    [W('i21', 'Remote'), '    loaded remote_work_policy.pdf -> 2 piece(s)'],
    [W('i21', 'Support'), '    loaded support_tickets.txt -> 1 piece(s)'],
    [W('i22', 'Total'), '<span class="ok">STEP 1 - LOAD : 9 pieces of text from plural_labs_docs</span>'],
  ];
  termCmd(steps[0][0], steps[0][2], .04);
  steps.slice(1).forEach(([tt, h]) => termLine(tt, h, { dx: -20, d: .2 }));
  cam(W('i19', 'Expense') - .3, 1.2, { x: VS.x + 900, y: VS.y + 800, z: 1.35 });
  t = T('i22');
  cam(t, 1.4, { x: VS.x + 1400, y: VS.y + 720, z: .9 });
  slideR('cmp9', t + .3, .6, 100); count('cmp_n', W('i22', 'nine'), 1.0, 0, 9); pulse('cmp9', W('i22', 'Day 22'), 1.05);
  // i23 - i26 describe_source
  t = T('i23');
  panel(t, 0); PANEL_H = 0; to('cmp9', t, .5, { o: 0 });
  focus(t, '25', 467, 470, { cd: 1.6, zmax: 2.3, minCols: 40 });
  t = T('i24');
  note(W('i24', 'page two'), '25', 470, 42, 'remote_work_policy.pdf page 2', 'var(--rose)');
  note(W('i24', 'None'), '25', 468, 25, 'leave_policy.txt  (page is None)', 'var(--sky)');
  t = T('i25');
  mark(W('i25', 'If the page'), '25', 468, 4, 22); mark(W('i25', 'Otherwise'), '25', 470, 4, 40, 'var(--teal)');
  t = T('i26');
  note(W('i26', 'only place'), '25', 467, 40, 'the ONE place that handles None', 'var(--sun)');
  focus(t, '25', 467, 470, { hl: false, zmax: 1.7, minCols: 70 });
});
