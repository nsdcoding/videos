// c6 : part B - the loaders
(window.SCENES = window.SCENES || []).push(function () {
  const G = (c, r) => [c * 2400, r * 1500];
  const dict = (id, x, y, page, text, w = 560) => `<div class="abs mono" id="${id}" style="left:${x}px;top:${y}px;width:${w}px;padding:12px 18px;border-radius:12px;background:#24050a;border:2px solid #7a2a33;font-size:22px;white-space:nowrap;overflow:hidden">{<span style="color:#ce9178">"page"</span>: <span style="color:${page === 'None' ? '#569cd6' : '#b5cea8'}">${page}</span>, <span style="color:#ce9178">"text"</span>: <span style="color:#ce9178">${text}</span>}</div>`;
  board('CONTRACT', ...G(-1, 3), `
    ${div('ct_t', 110, 60, 0, 0, '<span class="eyebrow" style="display:block;margin-bottom:12px">Part B</span>One loader per file format', 'h1', 'font-size:62px')}
    ${div('ct_stamp', 1350, 80, 0, 0, 'SAME CONTRACT', 'badge bg-sun', 'font-size:36px;transform:rotate(-5deg);padding:14px 26px')}
    ${chip('ct_in', 110, 290, '<span class="va">path</span>', 'font-size:40px')}
    ${arrow('ct_a1', 290, 325, 400, 325, '#cfa999', 6)}
    <div class="abs center col" id="ct_box" style="left:420px;top:240px;width:300px;height:170px;border-radius:20px;background:#55121c;border:3px solid var(--sun)"><div style="width:70px;height:70px">${ICON.gear('#f5b700')}</div><b class="mono" style="font-size:28px;margin-top:6px">a loader</b></div>
    ${arrow('ct_a2', 740, 325, 850, 325, '#cfa999', 6)}
    <div class="abs mono" id="ct_out" style="left:870px;top:250px;font-size:40px;line-height:1.5;color:var(--sun)">[ {<span style="color:#ce9178">"page"</span>: …, <span style="color:#ce9178">"text"</span>: …}, … ]</div>
    ${div('ct_outl', 880, 360, 0, 0, 'a LIST of dictionaries', 'hand', 'font-size:44px;color:var(--sun)')}
    <div class="card" id="ct_txt" style="left:110px;top:470px;width:820px;height:300px">${fileIcon('ct_ti', 40, 50, 'txt', '', .9)}${arrow('ct_ta', 210, 140, 290, 140, '#2fb872', 5)}
      ${dict('ct_td', 300, 110, 'None', '"Plural Labs - Leave…"', 490)}${div('ct_tn', 300, 190, 0, 0, '1 item', 'small', 'font-size:26px;color:var(--teal)')}</div>
    <div class="card" id="ct_pdf" style="left:990px;top:470px;width:820px;height:300px">${fileIcon('ct_pi', 40, 50, 'pdf', '', .9)}${arrow('ct_pa', 210, 140, 290, 140, '#2fb872', 5)}
      ${dict('ct_pd0', 300, 40, '1', '"Plural Labs — Re…"', 490)}${dict('ct_pd1', 300, 105, '2', '"7. Office access…"', 490)}${dict('ct_pd2', 300, 170, '3', '"…"', 490)}${div('ct_pn', 300, 240, 0, 0, 'one item per page', 'small', 'font-size:26px;color:var(--teal)')}</div>
    <div class="card" id="ct_rule" style="left:110px;top:820px;width:1700px;height:180px;border-color:var(--teal)"><div class="center" style="height:180px;gap:40px">
      <span class="h2" style="font-size:46px">1 file in → 1 list out</span><span class="txt" style="font-size:34px">with <b id="ct_n" class="sun" data-dec="0">1</b> item(s) — the caller never cares</span></div></div>
  `);
  board('SOCKET', ...G(-1, 4) , `
    ${div('so_t', 110, 60, 0, 0, 'Think of a power socket', 'h1', 'font-size:62px')}
    <div class="abs" id="so_wall" style="left:780px;top:220px;width:360px;height:360px;border-radius:40px;background:#fff8ee;box-shadow:0 30px 70px rgba(0,0,0,.5)">
      <div class="abs" style="left:110px;top:120px;width:36px;height:90px;border-radius:12px;background:#3b0a10"></div><div class="abs" style="left:214px;top:120px;width:36px;height:90px;border-radius:12px;background:#3b0a10"></div>
      <div class="abs" style="left:162px;top:240px;width:36px;height:50px;border-radius:12px;background:#3b0a10"></div></div>
    ${[['so_p0', 140, 'load_txt', 'var(--teal)', false], ['so_p1', 520, 'load_pdf', 'var(--rose)', false], ['so_p2', 1190, 'load_html', '#ff9f43', true], ['so_p3', 1530, 'load_image', 'var(--vio)', true]].map(([id, x, n, c, d]) => `<div class="abs center col" id="${id}" style="left:${x}px;top:660px;width:280px;height:300px;border-radius:22px;border:3px ${d ? 'dashed' : 'solid'} ${c};background:#3a0a12">
      <div style="width:90px;height:120px">${ICON.plug(c)}</div><b class="mono" style="font-size:28px;margin-top:20px;color:${c}">${n}</b>${d ? '<span class="small">next class</span>' : ''}</div>`).join('')}
    ${div('so_fan', 160, 250, 260, 0, '🌀 fan', 'h2', 'font-size:50px')}${div('so_ph', 1500, 250, 330, 0, '📱 charger', 'h2', 'font-size:50px')}
    ${div('so_n', 560, 600, 800, 0, 'same plug → the socket never needs to know', 'hand center', 'font-size:44px;color:var(--sun)')}
  `);
  // ---- PDF loop visuals ----
  const pgcard = (id, x, n) => `<div class="abs" id="${id}" style="left:${x}px;top:120px;width:150px;height:190px;border-radius:10px;background:#fff8ee">${[30, 55, 80, 105, 130].map((y, k) => `<div class="abs" style="left:16px;top:${y}px;width:${[110, 90, 115, 80, 100][k]}px;height:8px;border-radius:4px;background:#e8d7c4"></div>`).join('')}<div class="abs center" id="${id}t" style="left:95px;top:-26px;width:70px;height:70px;border-radius:50%;background:var(--sun);color:#2a2000;font:800 34px var(--serif)">${n}</div></div>`;
  board('PDFLOOP', ...G(0, 4), `
    ${div('pl_t', 110, 50, 0, 0, 'Inside <span class="mono rose">load_pdf</span>', 'h1', 'font-size:58px')}
    <div class="card" id="pl_en" style="left:110px;top:170px;width:820px;height:400px">
      <div class="abs small" style="left:30px;top:20px;letter-spacing:3px">enumerate(reader.pages, start=1)</div>
      ${pgcard('pl_g0', 60, 1)}${pgcard('pl_g1', 260, 2)}${pgcard('pl_g2', 460, 3)}
      <div class="abs mono" id="pl_py" style="left:40px;top:340px;font-size:26px;color:#cfa999">Python counts: <b style="color:#fff1dc">0, 1, 2</b></div>
      <div class="abs mono" id="pl_hu" style="left:440px;top:340px;font-size:26px;color:var(--sun)">humans: <b>1, 2, 3</b></div></div>
    <div class="card" id="pl_none" style="left:990px;top:170px;width:820px;height:400px">
      <div class="abs small" style="left:30px;top:20px;letter-spacing:3px">page.extract_text() <span class="sun">or ""</span></div>
      <div class="abs mono center" id="pl_nv" style="left:60px;top:110px;width:180px;height:90px;border-radius:14px;background:#55121c;border:2.5px solid #569cd6;font-size:36px;color:#569cd6">None</div>
      ${div('pl_boom', 300, 90, 0, 0, '💥 crash on the next line', 'txt', 'font-size:30px;color:var(--rose)')}
      <div class="abs" id="pl_net" style="left:60px;top:260px;width:700px;height:16px;border-radius:8px;background:repeating-linear-gradient(90deg,var(--teal) 0 18px,transparent 18px 30px)"></div>
      ${div('pl_netl', 60, 300, 0, 0, 'safety net: nothing? use <span class="mono st" style="color:#ce9178">""</span> instead', 'txt', 'font-size:30px;color:var(--teal)')}</div>
    <div class="card" id="pl_len" style="left:110px;top:610px;width:820px;height:420px">
      <div class="abs small" style="left:30px;top:20px;letter-spacing:3px">if len(text) &lt; 100 → a scan?</div>
      ${[['IT handbook p.1', 2679], ['Remote policy p.2', 341], ['a scanned page', 0]].map(([n, v], i) => `<div class="abs small" style="left:30px;top:${80 + i * 70}px;font-size:22px;color:#f6e2cc;width:230px">${n}</div><div class="abs" id="pl_b${i}" style="left:270px;top:${84 + i * 70}px;width:${Math.max(6, Math.min(500, v / 5.4))}px;height:26px;border-radius:8px;background:${v < 100 ? 'var(--rose)' : 'var(--teal)'}"></div><div class="abs mono" id="pl_bn${i}" style="left:${290 + Math.max(6, Math.min(500, v / 5.4))}px;top:${80 + i * 70}px;font-size:22px">${v}</div>`).join('')}
      <div class="abs" id="pl_thr" style="left:${270 + 100 / 5.4}px;top:70px;width:4px;height:220px;background:var(--sun)"></div>
      ${div('pl_thrl', 230, 290, 0, 0, '100', 'mono', 'color:var(--sun);font-size:22px')}
      <div class="abs mono" id="pl_warn" style="left:30px;top:340px;width:760px;font-size:19px;color:#e2c08d;white-space:nowrap">    WARNING : scan.pdf page 3 gave only 0 characters - is it a scan?</div></div>
    <div class="card" id="pl_slots" style="left:990px;top:610px;width:820px;height:420px">
      <div class="abs small" style="left:30px;top:20px;letter-spacing:3px">SEARCH RETURNS ONLY 3 CHUNKS</div>
      ${[0, 1, 2].map(i => `<div class="abs" id="pl_s${i}" style="left:${40 + i * 250}px;top:80px;width:220px;height:170px;border-radius:16px;border:3px solid ${i === 2 ? '#8f6a62' : 'var(--teal)'};background:${i === 2 ? '#300810' : 'rgba(47,184,114,.12)'}"><div class="center" style="height:170px;font:600 26px var(--sans);color:${i === 2 ? '#8f6a62' : '#d9f7e6'}">${i === 2 ? 'empty chunk' : 'useful chunk'}</div></div>`).join('')}
      ${div('pl_waste', 540, 260, 0, 0, 'a wasted slot', 'hand', 'font-size:40px;color:var(--rose)')}
      <div class="abs" id="pl_eye" style="left:40px;top:300px;display:flex;align-items:center;gap:20px"><div style="width:100px;height:62px">${ICON.eye('#ffd9a0')}</div><span class="txt" style="font-size:28px">later: a <b class="sky">vision model</b> reads these pages</span></div></div>
  `);
  board('LOADOUT', ...G(1, 4), `
    ${div('lo_t', 110, 80, 0, 0, '<span class="mono">load_pdf("remote_work_policy.pdf")</span>', 'h2', 'font-size:44px')}
    ${fileIcon('lo_f', 140, 300, 'pdf', 'remote_work_policy.pdf', 1.2)}
    ${arrow('lo_a', 400, 420, 520, 420, '#2fb872', 7)}
    <div class="abs mono" id="lo_b" style="left:540px;top:250px;font-size:120px;color:var(--sun)">[</div>
    ${dict('lo_d0', 610, 290, '1', '"Plural Labs — Remote and Hybrid Work Policy People Team · Ver…"', 1120)}
    ${dict('lo_d1', 610, 400, '2', '"7. Office access on remote days The office is open on Monday a…"', 1120)}
    <div class="abs mono" id="lo_b2" style="left:1740px;top:250px;font-size:120px;color:var(--sun)">]</div>
    ${div('lo_n', 610, 520, 0, 0, '2 pages → 2 dictionaries', 'hand', 'font-size:52px;color:var(--teal)')}
  `);

  // ================= animation =================
  let t = T('g01');
  camB(t, 2.0, 'CONTRACT', 700, 220, 1.2, { dip: .35 });
  wipe('ct_t', t + .8, .6);
  t = T('g02');
  ft('ct_stamp', W('g02', 'contract'), .5, { o: 0, s: 2.5, r: -20 }, { o: 1, s: 1, r: 0 }, 'back');
  camB(t, 1.0, 'CONTRACT', 1100, 250, 1.2);
  t = T('g03');
  camB(t, 1.0, 'CONTRACT', 960, 330, 1.05);
  popIn('ct_in', W('g03', 'file path'), .4); drawIn('ct_a1', W('g03', 'file path') + .2, .3); popIn('ct_box', W('g03', 'Each loader'), .45);
  ft('ct_box', W('g03', 'returns'), 1.2, { r: 0 }, { r: 0 }); drawIn('ct_a2', W('g03', 'returns'), .3);
  wipe('ct_out', W('g03', 'list'), .8); fadeIn('ct_outl', W('g03', 'page, and'), .4);
  t = T('g04');
  camB(t, 1.0, 'CONTRACT', 520, 620, 1.5);
  fadeIn('ct_txt', t, .3); popIn('ct_ti', t + .2, .4); drawIn('ct_ta', W('g04', 'only one'), .3); slideR('ct_td', W('g04', 'only one') + .2, .4, 40); fadeIn('ct_tn', W('g04', 'only one') + .5, .3);
  t = T('g05');
  camB(t, 1.0, 'CONTRACT', 1400, 620, 1.5);
  fadeIn('ct_pdf', t, .3); popIn('ct_pi', t + .2, .4); drawIn('ct_pa', W('g05', 'many pages'), .3);
  ['ct_pd0', 'ct_pd1', 'ct_pd2'].forEach((id, i) => slideR(id, W('g05', 'many pages') + .2 + i * .2, .4, 40)); fadeIn('ct_pn', W('g05', 'every loader'), .3);
  t = T('g06');
  camB(t, 1.0, 'CONTRACT', 960, 860, 1.1);
  fadeUp('ct_rule', t, .5); count('ct_n', W('g06', 'four hundred') - .4, 1.0, 1, 400, 'in');
  // socket
  t = T('g07');
  camB(t, 1.8, 'SOCKET', 960, 420, 1.0, { dip: .35 });
  wipe('so_t', t + .6, .5); ft('so_wall', W('g07', 'socket'), .6, { o: 0, s: .6 }, { o: 1, s: 1 }, 'back');
  slideL('so_fan', W('g07', 'fan'), .5); slideR('so_ph', W('g07', 'charger'), .5);
  t = T('g08');
  camB(t, 1.0, 'SOCKET', 960, 620, .95);
  ['so_p0', 'so_p1', 'so_p2', 'so_p3'].forEach((id, i) => ft(id, t + .2 + i * .25, .5, { o: 0, y: 150 }, { o: 1, y: 0 }, 'back'));
  fadeIn('so_n', W('g08', 'without touching'), .5);
  // load_txt in code
  t = T('g09');
  focus(t, '25', 342, 349, { cd: 2.0, dip: .35, zmax: 1.9 });
  note(W('g09', 'unchanged'), '25', 342, 23, 'Day 22, unchanged', 'var(--sky)');
  t = T('g10');
  focus(t, '25', 344, 345, { zmax: 2.2, minCols: 50 });
  t = T('g11');
  focus(t, '25', 349, 349, { zmax: 2.2, minCols: 50 });
  mark(W('g11', 'list'), '25', 349, 11, 56); mark(W('g11', 'None'), '25', 349, 21, 25, 'var(--sky)');
  note(W('g11', 'no pages'), '25', 349, 58, 'no pages → None', 'var(--sky)');
  // load_pdf in code
  t = T('g12');
  focus(t, '25', 352, 356, { zmax: 2.0 });
  note(W('g12', 'star'), '25', 352, 23, '★ the star of the show', 'var(--sun)');
  t = T('g13');
  focus(t, '25', 356, 356, { zmax: 2.4, minCols: 40 });
  mark(W('g13', 'opens'), '25', 356, 13, 28, 'var(--teal)');
  t = T('g14');
  focus(t, '25', 358, 358, { zmax: 2.4, minCols: 40 });
  note(W('g14', 'fill'), '25', 358, 18, '🧺 empty basket', 'var(--sun)');
  t = T('g15');
  focus(t, '25', 363, 363, { zmax: 1.9 });
  mark(W('g15', 'enumerate'), '25', 363, 29, 38); mark(W('g15', 'start equals'), '25', 363, 53, 60, 'var(--rose)');
  // enumerate visual
  t = T('g16');
  camB(t, 1.8, 'PDFLOOP', 520, 370, 1.5, { dip: .3 });
  wipe('pl_t', t, .5); fadeIn('pl_en', t + .5, .3);
  [0, 1, 2].forEach(i => { ft('pl_g' + i, W('g16', 'two things') + i * .3, .5, { o: 0, x: -200 }, { o: 1, x: 0 }, 'out'); popIn('pl_g' + i + 't', W('g16', 'counter') + i * .25, .35); });
  t = T('g17');
  fadeIn('pl_py', W('g17', 'zero'), .4); fadeIn('pl_hu', W('g17', 'page one calls'), .4); pulse('pl_hu', W('g17', 'not page zero'), 1.1);
  t = T('g18');
  focus(t, '25', 368, 368, { cd: 1.8, dip: .3, zmax: 2.3, minCols: 46 });
  mark(W('g18', 'pulls'), '25', 368, 19, 38, 'var(--teal)');
  t = T('g19');
  mark(W('g19', 'or empty'), '25', 368, 39, 44, 'var(--rose)'); camTok(W('g19', 'or empty'), '25', 368, 30, 46, 2.8);
  t = T('g20');
  camB(t, 1.8, 'PDFLOOP', 1400, 370, 1.5, { dip: .3 });
  fadeIn('pl_none', t + .5, .3); init('pl_net', { cw: 0 });
  ft('pl_nv', W('g20', 'None'), .6, { o: 0, y: -100 }, { o: 1, y: 0 }, 'back'); fadeIn('pl_boom', W('g20', 'crash'), .3); shake('pl_boom', W('g20', 'crash'), 10);
  t = T('g21');
  ft('pl_net', W('g21', 'Or empty'), .6, { cw: 0 }, { cw: 1 }); to('pl_nv', W('g21', 'use an empty'), .6, { y: 120 }, 'back');
  fadeIn('pl_netl', W('g21', 'use an empty') + .2, .4); to('pl_boom', W('g21', 'safety'), .4, { o: .2 });
  t = T('g22');
  focus(t, '25', 370, 370, { cd: 1.8, dip: .3, zmax: 2.4, minCols: 40 });
  note(W('g22', 'Part A'), '25', 370, 34, 'our Part A function', 'var(--teal)');
  t = T('g23');
  focus(t, '25', 383, 386, { zmax: 1.9 });
  note(W('g23', 'important'), '25', 383, 30, '⚠ the empty page check', 'var(--rose)');
  t = T('g24');
  camB(t, 1.8, 'PDFLOOP', 520, 820, 1.5, { dip: .3 });
  fadeIn('pl_len', t + .5, .3);
  [0, 1, 2].forEach(i => { ft('pl_b' + i, W('g24', 'shorter') + i * .3, .6, { cw: 0 }, { cw: 1 }); fadeIn('pl_bn' + i, W('g24', 'shorter') + i * .3 + .4, .3); });
  ft('pl_thr', W('g24', 'hundred'), .5, { ch: 0 }, { ch: 1 }); fadeIn('pl_thrl', W('g24', 'hundred'), .4);
  t = T('g25');
  glow('pl_b2', W('g25', 'scan'), .4, 1);
  t = T('g26');
  camB(t, 1.0, 'PDFLOOP', 960, 680, .98);
  t = T('g27');
  camB(t, 1.0, 'PDFLOOP', 520, 900, 1.6);
  ft('pl_warn', W('g27', 'loud warning'), 1.0, { o: 0, cw: 0 }, { o: 1, cw: 1 }, 'lin');
  t = T('g28');
  camB(t, 1.0, 'PDFLOOP', 1400, 820, 1.5);
  fadeIn('pl_slots', t, .3);
  t = T('g29');
  [0, 1, 2].forEach(i => popIn('pl_s' + i, W('g29', 'three') + i * .2, .4));
  fadeIn('pl_waste', W('g29', 'waste'), .4); shake('pl_s2', W('g29', 'waste'), 10);
  t = T('g30');
  slideR('pl_eye', W('g30', 'vision'), .5, 60);
  t = T('g31');
  focus(t, '25', 388, 388, { cd: 1.8, dip: .3, zmax: 2.2, minCols: 56 });
  note(W('g31', 'append'), '25', 388, 62, '→ into the basket', 'var(--sun)');
  t = T('g32');
  focus(t, '25', 390, 390, { zmax: 2.4, minCols: 40 });
  note(W('g32', 'return'), '25', 390, 18, 'one entry per good page', 'var(--teal)');
  t = T('g33');
  camB(t, 1.8, 'LOADOUT', 960, 400, 1.0, { dip: .3 });
  wipe('lo_t', t + .5, .6); popIn('lo_f', t + .7, .4); drawIn('lo_a', t + 1.0, .3); popIn('lo_b', t + 1.1, .3); popIn('lo_b2', t + 1.1, .3);
  slideR('lo_d0', W('g33', 'Page one'), .4, 60); slideR('lo_d1', W('g33', 'page two'), .4, 60); fadeIn('lo_n', W('g33', 'two dictionaries'), .4);
});
