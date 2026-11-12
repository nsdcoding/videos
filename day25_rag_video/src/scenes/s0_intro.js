// c0 : title, the Day 22 machine, what changes today
(window.SCENES = window.SCENES || []).push(function () {
  const G = (c, r) => [c * 2400, r * 1500];

  // ---------- VS Code lives at the centre of the world ----------
  buildVSCode(60, 34);
  board('VSB', 0, 0);

  // ---------- TITLE ----------
  board('TITLE', ...G(-1, -1), `
    ${div('t_eye', 170, 250, 0, 0, 'Plural Labs · AI Developer Program', 'eyebrow')}
    ${div('t_day', 160, 300, 0, 0, '<span style="font:800 230px/1 var(--serif)" class="grad-text">DAY <span id="t_num" data-dec="0">22</span></span>')}
    ${div('t_title', 170, 560, 1300, 0, 'RAG with real files', 'h1', 'font-size:110px;line-height:1.05')}
    ${div('t_sub', 175, 700, 0, 0, 'Part 1 &nbsp;—&nbsp; <span class="rose">the PDF</span>', 'h2', 'font-size:54px;color:#f6e2cc')}
    ${div('t_rule', 175, 800, 260, 7, '', '', 'background:var(--rose);border-radius:4px')}
    ${div('t_tags', 175, 850, 1200, 0, '<span class="small" style="font-size:26px">pypdf · regular expressions · dispatch tables · page numbers in answers</span>')}
    ${fileIcon('t_f1', 1330, 200, 'txt', '', 1.1)}${fileIcon('t_f2', 1560, 330, 'pdf', '', 1.25)}
    ${fileIcon('t_f3', 1360, 560, 'html', '', 1.0)}${fileIcon('t_f4', 1610, 640, 'png', '', 1.1)}
  `);
  // ---------- PIPE : the Day 22 machine ----------
  const names = ['LOAD', 'CHUNK', 'EMBED', 'STORE', 'RETRIEVE', 'RANK', 'AUGMENT', 'GENERATE'];
  const nx = i => 190 + i * 220;
  let nodes = '';
  names.forEach((n, i) => {
    const c = i < 4 ? 'var(--teal)' : 'var(--rose)';
    nodes += `<div class="abs center" id="pn${i}" style="left:${nx(i) - 75}px;top:445px;width:150px;height:150px;border-radius:50%;background:#2c060c;border:4px solid ${c};--glow:${i < 4 ? 'rgba(47,184,114,.6)' : 'rgba(230,57,70,.6)'}">
       <span style="font:800 64px var(--serif);color:${c}">${i + 1}</span></div>
       <div class="abs center" id="pl${i}" style="left:${nx(i) - 100}px;top:612px;width:200px;font:800 22px var(--sans);letter-spacing:3px;color:#fff1dc">${n}</div>
       ${icon('plk' + i, nx(i) + 30, 430, 44, 'lock', '#cfa999')}`;
  });
  board('PIPE', ...G(0, -1), `
    ${div('p_title', 110, 90, 0, 0, 'The Day 22 machine', 'h1', 'font-size:64px')}
    ${div('p_eye', 114, 60, 0, 0, 'Recap', 'eyebrow')}
    ${path('p_line', `M${nx(0)},520 L${nx(7)},520`, '#7a2a33', 8)}
    ${path('p_br1', `M${nx(0) - 70},380 L${nx(0) - 70},350 L${nx(3) + 70},350 L${nx(3) + 70},380`, '#2fb872', 5)}
    ${path('p_br2', `M${nx(4) - 70},380 L${nx(4) - 70},350 L${nx(7) + 70},350 L${nx(7) + 70},380`, '#e63946', 5)}
    ${div('p_l1', nx(0) - 70, 255, 680, 0, '<b class="teal">PIPELINE 1 · INDEXING</b><br><span class="small">runs once, in advance</span>', 'h3', 'font-size:28px')}
    ${div('p_l2', nx(4) - 70, 255, 680, 0, '<b class="rose">PIPELINE 2 · ANSWERING</b><br><span class="small">runs for every question</span>', 'h3', 'font-size:28px')}
    ${nodes}
    ${div('p_doc', nx(0) - 30, 500, 60, 40, '', '', 'background:#fff8ee;border-radius:6px;box-shadow:0 0 20px #2fb872')}
    ${icon('p_db', nx(3) - 40, 690, 80, 'db', '#2fb872')}
    ${div('p_q', nx(4) - 60, 490, 120, 60, '<span style="font:700 26px var(--sans)">Q ?</span>', 'center', 'background:var(--sky);color:#3b0a10;border-radius:16px')}
    ${div('p_ans', nx(7) - 140, 690, 280, 80, '<span style="font:700 26px var(--sans)">answer ✓</span>', 'center', 'background:var(--rose);border-radius:18px')}
    ${div('p_worked', 1480, 70, 330, 0, 'IT WORKED ✓', 'badge bg-teal', 'font-size:34px;transform:rotate(-6deg)')}
    ${chip('p_chip', 90, 770, '<span class="kc">if not</span> file_name.<span class="fn">endswith</span>(<span class="st">".txt"</span>):\n    <span class="kc">continue</span>', 'font-size:28px;border-color:var(--rose)')}
    ${div('p_ul', 340, 816, 320, 6, '', '', 'background:var(--rose);border-radius:3px')}
    ${div('p_note', 190, 905, 600, 0, 'one tiny line… today\'s whole class', 'hand', 'font-size:44px;color:var(--sun)')}
    ${div('p_pr1', 790, 760, 330, 200, `<div style="width:64px;height:64px">${ICON.box('#e63946')}</div><b style="font-size:30px;margin-top:14px">Reads PDFs</b>`, 'card center col', 'padding:20px')}
    ${div('p_pr2', 1150, 760, 330, 200, `<div style="font:800 54px var(--serif)" class="sun">p. 2</div><b style="font-size:30px;margin-top:8px">Cites the page</b>`, 'card center col', 'padding:20px')}
    ${div('p_pr3', 1510, 760, 330, 200, `<div style="width:64px;height:64px">${ICON.bell('#f5b700')}</div><b style="font-size:30px;margin-top:14px">No silent skips</b>`, 'card center col', 'padding:20px')}
    ${div('p_today', nx(0) - 105, 690, 210, 0, 'CHANGES TODAY', 'badge bg-rose', 'text-align:center;font-size:20px')}
    ${div('p_same', nx(1) - 60, 690, 1500, 0, '<span class="small" style="font-size:30px">steps 2 → 8 : <b style="color:#fff1dc">same as Day 22</b></span>')}
  `);

  // ================= animation =================
  camStart({ x: G(-1, -1)[0] + 960, y: G(-1, -1)[1] + 540, z: .82 });
  // a01
  let t = T('a01');
  cam(.2, 4.5, { x: G(-1, -1)[0] + 900, y: G(-1, -1)[1] + 540, z: 1 });
  wipe('t_eye', .4, .8);
  fadeUp('t_day', .7, .8);
  count('t_num', W('a01', 'Day 25') - .3, 1.2, 22, 25, 'io');
  pulse('t_day', W('a01', 'Day 25') + .9, 1.08);
  fadeUp('t_title', W('a01', 'today our'), .7);
  fadeUp('t_sub', W('a01', 'grows up'), .7);
  ft('t_rule', W('a01', 'grows'), .8, { cw: 0 }, { cw: 1 });
  fadeIn('t_tags', END('a01', -.6), .8);
  ['t_f1', 't_f2', 't_f3', 't_f4'].forEach((id, i) => { ft(id, .6 + i * .35, .8, { o: 0, y: 120, r: -20 }, { o: 1, y: 0, r: [8, -6, 5, -10][i] }, 'back'); bob(id, 1.5 + i * .3, T('a03'), 14, 2.4 + i * .3); });

  // a02 : fly to the machine
  t = T('a02');
  camB(t + .2, 1.8, 'PIPE', 960, 520, .95, { dip: .25 });
  fadeIn('p_eye', W('a02', 'complete'), .5); wipe('p_title', W('a02', 'complete'), .7);
  drawIn('p_line', W('a02', 'Eight') - .2, 1.6);
  names.forEach((n, i) => { popIn('pn' + i, W('a02', 'Eight') + i * .17, .5); fadeUp('pl' + i, W('a02', 'Eight') + i * .17 + .1, .4, 20); init('plk' + i, { o: 0 }); });

  // a03 : pipeline 1
  t = T('a03');
  camB(t, 1.2, 'PIPE', 600, 470, 1.25);
  drawIn('p_br1', t + .1, .8); fadeUp('p_l1', t + .4, .5, 20);
  [0, 1, 2, 3].forEach(i => { glow('pn' + i, W('a03', 'Load') + i * .45, .3, .9); to('pn' + i, W('a03', 'Load') + i * .45 + .5, .5, { gl: .25 }); });
  ft('p_doc', W('a03', 'Load'), 2.2, { o: 0, x: 0 }, { o: 1, x: 660 }, 'io');
  to('p_doc', W('a03', 'Load') + 2.2, .3, { o: 0 });
  popIn('p_db', W('a03', 'runs once'), .5);

  // a04 : pipeline 2
  t = T('a04');
  camB(t, 1.2, 'PIPE', 1320, 470, 1.25);
  drawIn('p_br2', t + .1, .8); fadeUp('p_l2', t + .4, .5, 20);
  [4, 5, 6, 7].forEach((i, k) => { glow('pn' + i, W('a04', 'retrieve') + k * .45, .3, .9); to('pn' + i, W('a04', 'retrieve') + k * .45 + .5, .5, { gl: .25 }); });
  ft('p_q', W('a04', 'retrieve') - .2, 2.2, { o: 0, x: 0 }, { o: 1, x: 660 }, 'io');
  to('p_q', W('a04', 'retrieve') + 2, .3, { o: 0 });
  popIn('p_ans', W('a04', 'every time'), .5);

  // a05 : it worked ... but
  t = T('a05');
  camB(t, 1.2, 'PIPE', 960, 540, .92);
  ft('p_worked', t + .2, .5, { o: 0, s: 2.2 }, { o: 1, s: 1 }, 'back');
  to('pn0', W('a05', 'But'), .4, { gl: 1, s: 1.12 }, 'out');
  camB(W('a05', 'one tiny'), 1.2, 'PIPE', 480, 760, 1.35);
  ft('p_chip', W('a05', 'one tiny'), .7, { o: 0, y: -260, s: .3 }, { o: 1, y: 0, s: 1 }, 'back');

  // a06 : the subject of the class
  t = T('a06');
  camB(t, 1.0, 'PIPE', 450, 830, 1.9);
  ft('p_ul', t + .5, .6, { cw: 0 }, { cw: 1 }, 'out');
  fadeIn('p_note', W('a06', 'subject'), .6);
  pulse('p_chip', W('a06', 'entire'), 1.06);

  // a07 : three promises
  t = T('a07');
  camB(t, 1.2, 'PIPE', 1240, 830, 1.35);
  popIn('p_pr1', W('a07', 'read PDFs'), .55); popIn('p_pr2', W('a07', 'exact page'), .55); popIn('p_pr3', W('a07', 'never again'), .55);
  glow('p_pr1', W('a07', 'read PDFs') + .3, .3, .6); to('p_pr1', W('a07', 'exact page'), .4, { gl: 0 });
  glow('p_pr2', W('a07', 'exact page') + .3, .3, .6); to('p_pr2', W('a07', 'never again'), .4, { gl: 0 });
  glow('p_pr3', W('a07', 'never again') + .3, .3, .6);

  // a08 : only step 1 changes
  t = T('a08');
  camB(t, 1.2, 'PIPE', 960, 560, 1.0);
  to('p_chip', t, .5, { o: .25 }); to('p_note', t, .5, { o: .25 }); to('p_ul', t, .5, { o: .25 });
  ['p_pr1', 'p_pr2', 'p_pr3'].forEach(id => to(id, t, .5, { o: .25, gl: 0 }));
  to('pn0', W('a08', 'step one'), .5, { gl: 1.2, s: 1.18 }, 'back');
  popIn('p_today', W('a08', 'step one') + .2, .5);
  for (let i = 1; i < 8; i++) { to('pn' + i, W('a08', 'Steps two') + i * .08, .5, { o: .45, gl: 0 }); popIn('plk' + i, W('a08', 'Steps two') + i * .1, .4); }
  fadeIn('p_same', W('a08', 'exactly'), .6);
  pulse('p_today', W('a08', 'One change'), 1.15);

  // a09 : to VS Code
  t = T('a09');
  showTab(0, '25');
  camVS(t + .1, 2.0, .93, { dip: .35 });
  showTab(T('a09', 1.4), '22');
});
