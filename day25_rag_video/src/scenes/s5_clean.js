// c5 : part A - clean_text
(window.SCENES = window.SCENES || []).push(function () {
  const G = (c, r) => [c * 2400, r * 1500];
  const box = (id, x, y, ch, col = '#1c2559', bd = '#3a4687', w = 96) => `<div class="abs mono center" id="${id}" style="left:${x}px;top:${y}px;width:${w}px;height:110px;border-radius:14px;background:${col};border:2.5px solid ${bd};font-size:56px">${ch}</div>`;
  // ---------- PARTS ----------
  const part = (id, x, L, title, sub, ic, col) => `<div class="card" id="${id}" style="left:${x}px;top:330px;width:540px;height:560px;border-color:${col}">
     <div class="abs" style="left:40px;top:30px;font:800 120px var(--serif);color:${col}">${L}</div>
     <div class="abs" style="left:350px;top:50px;width:140px;height:140px">${ic}</div>
     <div class="abs h2" style="left:40px;top:220px;font-size:44px">${title}</div>
     <div class="abs txt" style="left:40px;top:300px;width:470px;font-size:30px">${sub}</div></div>`;
  board('PARTS', ...G(-1, 2), `
    ${div('pa_t', 110, 70, 0, 0, '<span class="eyebrow" style="display:block;margin-bottom:12px">Step 1 · Load</span>The whole lesson, in three parts', 'h1', 'font-size:62px')}
    ${part('pa_a', 110, 'A', 'clean the text', 'one function that fixes what PDFs give us', ICON.broom(), 'var(--teal)')}
    ${part('pa_b', 690, 'B', 'one loader per format', 'small functions that read .txt, .pdf …', ICON.plug('#ffd23f'), 'var(--sun)')}
    ${part('pa_c', 1270, 'C', 'a dictionary that picks', 'the right loader for each file', ICON.key('#a78bfa'), 'var(--vio)')}
  `);
  // ---------- LIG ----------
  const LG = [['ﬀ', 'U+FB00', 'ff'], ['ﬁ', 'U+FB01', 'fi'], ['ﬂ', 'U+FB02', 'fl'], ['ﬃ', 'U+FB03', 'ffi'], ['ﬄ', 'U+FB04', 'ffl']];
  board('LIG', ...G(0, 2), `
    ${div('lg_t', 110, 60, 0, 0, 'Problem 1 · <span class="rose">ligatures</span>', 'h1', 'font-size:64px')}
    ${['E<span class="lgg">ﬀ</span>ective', 'O<span class="lgg">ﬃ</span>ce', 'Con<span class="lgg">ﬁ</span>dential'].map((w, i) => `<div class="abs" id="lg_w${i}" style="left:${110 + i * 560}px;top:190px;font:600 68px var(--serif)">${w}</div>`).join('')}
    <style>.lgg{color:inherit;border-radius:8px;transition:none}.lgon .lgg{color:var(--rose);background:rgba(255,77,109,.18)}</style>
    ${div('lg_look', 1450, 210, 0, 0, 'look normal…', 'hand', 'font-size:48px;color:var(--sun)')}
    <div class="card" id="lg_fuse" style="left:110px;top:350px;width:820px;height:320px">
      <div class="abs small" style="left:30px;top:22px;letter-spacing:3px">THE PRINTER JOINS THEM</div>
      ${box('lg_f', 180, 120, 'f')}${box('lg_i', 520, 120, 'i')}
      <div class="abs mono center" id="lg_fi" style="left:330px;top:105px;width:150px;height:140px;border-radius:16px;background:var(--rose);font-size:90px;color:#fff">ﬁ</div>
      ${pill('lg_500', 560, 250, '500 years of printing', 'bg-sun', 'font-size:22px')}</div>
    <div class="card" id="lg_uni" style="left:990px;top:350px;width:820px;height:320px">
      <div class="abs small" style="left:30px;top:22px;letter-spacing:3px">UNICODE KEPT THEM AS REAL CHARACTERS</div>
      ${LG.map(([g, u], i) => `<div class="abs center col" id="lg_u${i}" style="left:${30 + i * 155}px;top:80px;width:140px;height:200px;border-radius:14px;background:#1c2559;border:2px solid #3a4687"><span style="font:600 70px var(--serif);color:var(--rose)">${g}</span><span class="mono small" style="font-size:20px">${u}</span></div>`).join('')}</div>
    <div class="card" id="lg_cnt" style="left:110px;top:720px;width:1700px;height:300px">
      ${box('lg_c0', 60, 40, 'o')}${box('lg_c1', 170, 40, 'ﬃ', 'rgba(255,77,109,.25)', 'var(--rose)')}${box('lg_c2', 280, 40, 'c')}${box('lg_c3', 390, 40, 'e')}
      <div class="abs" style="left:530px;top:50px;font:800 80px var(--serif)" class="rose"><span id="lg_n1" class="rose" data-dec="0">0</span> <span style="font-size:36px">characters</span></div>
      ${['o', 'f', 'f', 'i', 'c', 'e'].map((c, i) => box('lg_d' + i, 60 + i * 110, 170, c, '#123b39', 'var(--teal)')).join('')}
      <div class="abs" style="left:760px;top:180px;font:800 80px var(--serif)"><span id="lg_n2" class="teal" data-dec="0">0</span> <span style="font-size:36px">characters</span></div>
      ${div('lg_same', 1180, 110, 480, 0, 'same look,<br><b class="rose">different word</b>', 'h2', 'font-size:48px')}</div>
  `);
  board('LIG2', ...G(1, 2), `
    ${div('l2_t', 110, 60, 0, 0, 'Why should we care?', 'h1', 'font-size:64px')}
    <div class="card" id="l2_scan" style="left:110px;top:200px;width:820px;height:380px">
      <div class="abs small" style="left:30px;top:22px;letter-spacing:3px">THE EMBEDDING MODEL READS CHARACTERS</div>
      ${box('l2_c0', 150, 140, 'O')}${box('l2_c1', 260, 140, 'ﬃ', 'rgba(255,77,109,.25)', 'var(--rose)')}${box('l2_c2', 370, 140, 'c')}${box('l2_c3', 480, 140, 'e')}
      <div class="abs" id="l2_beam" style="left:140px;top:120px;width:8px;height:150px;background:var(--sky);box-shadow:0 0 30px var(--sky);border-radius:4px"></div>
      ${div('l2_q', 620, 160, 0, 0, '≠ office', 'mono', 'font-size:48px;color:var(--rose)')}</div>
    <div class="card" id="l2_srch" style="left:990px;top:200px;width:820px;height:380px">
      <div class="abs small" style="left:30px;top:22px;letter-spacing:3px">A STUDENT SEARCHES</div>
      <div class="abs" id="l2_qb" style="left:30px;top:80px;padding:16px 26px;border-radius:20px;background:var(--sky);color:#04223a;font:600 30px var(--sans)">“when is the office open?”</div>
      ${arrow('l2_ar', 300, 170, 300, 240, '#8e9bc4', 5)}
      <div class="abs mono" id="l2_ch" style="left:30px;top:250px;width:760px;padding:16px 22px;border-radius:14px;background:#0b1130;border:2px solid #3a4687;font-size:24px;color:#aab4dd">"…7. O<span class="rose">ﬃ</span>ce access on remote days. The o<span class="rose">ﬃ</span>ce is open…"</div>
      ${div('l2_miss', 560, 90, 0, 0, 'MISSED', 'badge bg-rose', 'font-size:30px;transform:rotate(-8deg)')}</div>
    <div class="card" id="l2_fix" style="left:110px;top:640px;width:1700px;height:360px;border-color:var(--teal)">
      <div class="abs" style="left:80px;top:90px;font:600 120px var(--serif)"><span id="l2_bad">O<span class="rose">ﬃ</span>ce</span></div>
      <div class="abs" id="l2_good" style="left:80px;top:90px;font:600 120px var(--serif)">O<span class="teal">ffi</span>ce</div>
      ${arrow('l2_fa', 520, 170, 680, 170, '#2dd4bf', 7)}
      <div class="abs h2" id="l2_fl" style="left:740px;top:110px;font-size:52px">office is <span class="teal">office</span> again</div>
      <div class="abs" id="l2_ck" style="left:1450px;top:100px;width:120px;height:120px">${ICON.check()}</div></div>
  `);
  // ---------- RESUB ----------
  board('RESUB', ...G(2, 2), `
    ${div('rs_t', 110, 60, 0, 0, 'Meet <span class="mono sky">re.sub</span>', 'h1', 'font-size:64px')}
    <div class="abs mono" id="rs_call" style="left:110px;top:200px;font-size:64px;white-space:pre"><span class="cl" style="color:#4ec9b0">re</span>.<span style="color:#dcdcaa">sub</span>(<span id="rs_a1" style="color:var(--rose)">pattern</span>, <span id="rs_a2" style="color:var(--sun)">replacement</span>, <span id="rs_a3" style="color:var(--sky)">text</span>)</div>
    ${div('rs_l1', 330, 300, 300, 0, 'the SHAPE to look for', 'small center', 'color:var(--rose);font-size:26px')}
    ${div('rs_l2', 700, 300, 380, 0, 'what to put instead', 'small center', 'color:var(--sun);font-size:26px')}
    ${div('rs_l3', 1120, 300, 300, 0, 'the text to work on', 'small center', 'color:var(--sky);font-size:26px')}
    <div class="card" id="rs_all" style="left:110px;top:400px;width:1700px;height:200px">
      <div class="abs mono" id="rs_txt" style="left:40px;top:60px;font-size:40px;white-space:pre">a<span class="ws">··</span>b<span class="ws">···</span>c<span class="ws">↵·</span>d<span class="ws">····</span>e<span class="ws">→</span>f</div>
      <div class="abs mono" id="rs_txt2" style="left:40px;top:60px;font-size:40px;white-space:pre;color:var(--teal)">a b c d e f</div>
      ${div('rs_noloop', 1150, 60, 0, 0, 'EVERY match · no loop', 'badge bg-sky', 'font-size:28px')}</div>
    <div class="card" id="rs_imm" style="left:110px;top:650px;width:820px;height:350px">
      <div class="abs small" style="left:30px;top:22px;letter-spacing:3px">STRINGS NEVER CHANGE</div>
      <div class="abs" id="rs_glass" style="left:40px;top:80px;width:330px;height:150px;border-radius:16px;border:3px solid #7dd3fc;background:rgba(125,211,252,.08)"><div class="center mono" style="height:150px;font-size:30px;color:#ce9178">"Your\\nscreen"</div><div class="abs" style="right:-20px;top:-24px;width:56px;height:56px">${ICON.lock('#7dd3fc')}</div></div>
      <div class="abs" id="rs_new" style="left:440px;top:80px;width:330px;height:150px;border-radius:16px;border:3px solid var(--teal);background:rgba(45,212,191,.12)"><div class="center mono" style="height:150px;font-size:30px;color:#ce9178">"Your screen"</div><div class="abs badge bg-teal" style="left:10px;top:-22px;font-size:18px">NEW</div></div>
      <div class="abs mono" id="rs_lbl" style="left:500px;top:270px;font-size:34px"><span class="va" style="color:#9cdcfe">text</span> = …</div>
      ${curve('rs_arr', 610, 266, 640, 250, 610, 236, '#2dd4bf', 5)}
      <div class="abs" id="rs_trash" style="left:640px;top:250px;width:80px;height:80px">${ICON.trash()}</div></div>
    <div class="card" id="rs_bug" style="left:990px;top:650px;width:820px;height:350px;border-color:var(--rose)">
      <div class="abs small" style="left:30px;top:22px;letter-spacing:3px;color:var(--rose)">THE BUG THAT EATS EVENINGS</div>
      <div class="abs mono" style="left:30px;top:80px;font-size:30px;color:#8e9bc4"><s>text =</s> <span style="color:#4ec9b0">re</span>.<span style="color:#dcdcaa">sub</span>(…)</div>
      ${div('rs_nerr', 30, 150, 0, 0, 'NO ERROR', 'badge bg-sun')}
      <div class="abs" id="rs_moon" style="left:250px;top:140px;font-size:56px">🌙🌙🌙</div>
      <div class="abs txt" id="rs_tip" style="left:30px;top:240px;width:760px;font-size:30px">cleaning does nothing? <b class="sun">look for “text =” first</b></div></div>
  `);
  // ---------- HYPH ----------
  board('HYPH', ...G(0, 3), `
    ${div('hy_t', 110, 60, 0, 0, 'Problem 2 · a <span class="rose">hyphen</span> at the end of a line', 'h1', 'font-size:60px')}
    <div class="lcard" id="hy_doc" style="left:110px;top:190px;width:760px;height:400px;padding:40px 46px;font:400 30px/1.75 var(--serif);text-align:justify">
      All travel claims must be submitted with bills for reim<span id="hy_br" style="color:#ff4d6d;font-weight:700">burse-</span><br><span style="color:#ff4d6d;font-weight:700">ment</span> within thirty days of the travel date, through the finance portal only.</div>
    <div class="card" id="hy_raw" style="left:950px;top:190px;width:860px;height:180px"><div class="abs small" style="left:30px;top:20px;letter-spacing:3px">WHAT PYPDF GIVES US</div>
      <div class="abs mono" style="left:30px;top:80px;font-size:44px">"reimburse<span class="ws">-\\n</span>ment"</div></div>
    <div class="card" id="hy_pat" style="left:950px;top:410px;width:860px;height:180px"><div class="abs small" style="left:30px;top:20px;letter-spacing:3px">THE PATTERN</div>
      <div class="abs mono" style="left:30px;top:70px;font-size:56px">r"<span id="hy_p1" style="color:var(--rose)">-</span><span id="hy_p2" style="color:var(--sky)">\\n</span>"  →  <span id="hy_p3" style="color:var(--sun)">""</span></div>
      ${div('hy_l1', 520, 30, 0, 0, '- : a hyphen', 'small', 'color:var(--rose);font-size:24px')}${div('hy_l2', 520, 75, 0, 0, '\\n : a newline', 'small', 'color:var(--sky);font-size:24px')}${div('hy_l3', 520, 120, 0, 0, '"" : nothing = delete', 'small', 'color:var(--sun);font-size:24px')}</div>
    <div class="card" id="hy_join" style="left:110px;top:640px;width:1100px;height:170px">
      <div class="abs mono" id="hy_orig" style="left:40px;top:50px;font-size:56px;white-space:pre">reimburse<span id="hy_gap" style="display:inline-block;color:var(--rose)">-↵</span>ment</div>
      <div class="abs mono" id="hy_res" style="left:40px;top:50px;font-size:56px;color:var(--teal)">reimbursement ✓</div></div>
    <div class="card" id="hy_zero" style="left:1270px;top:640px;width:540px;height:170px"><div class="abs small" style="left:30px;top:20px;letter-spacing:3px">MATCHES IN OUR 3 PDFS</div>
      <div class="abs" style="left:30px;top:56px;font:800 84px var(--serif)" ><span id="hy_n" class="sun" data-dec="0">9</span></div>
      <div class="abs txt" style="left:150px;top:80px;font-size:26px;width:360px">our PDF tool never hyphenates</div></div>
    ${pill('hy_w', 110, 860, 'from Word → lots of matches', 'bg-dark', 'font-size:28px')}${pill('hy_l', 600, 860, 'from LaTeX → lots of matches', 'bg-dark', 'font-size:28px')}
    ${div('hy_keep', 1110, 862, 0, 0, '🛡 the rule stays — it costs nothing', 'pill bg-teal', 'font-size:28px;position:absolute')}
    ${chip('hy_cnt', 110, 950, '<span style="color:#dcdcaa">print</span>(<span style="color:#dcdcaa">len</span>(<span style="color:#4ec9b0">re</span>.<span style="color:#dcdcaa">findall</span>(<span class="st" style="color:#ce9178">r"-\\n"</span>, raw_text)))', 'font-size:30px')}
    ${div('hy_out', 1050, 958, 0, 0, '→ <b>0</b>', 'mono', 'font-size:38px;color:var(--sun)')}
  `);
  // ---------- WS ----------
  board('WS', ...G(1, 3), `
    ${div('ws_t', 110, 60, 0, 0, 'Problem 3 · ragged <span class="sky">whitespace</span>', 'h1', 'font-size:62px')}
    ${div('ws_star', 1220, 70, 0, 0, '★ the rule that does the real work', 'pill bg-sun', 'font-size:26px;position:absolute')}
    <div class="card" id="ws_ins" style="left:110px;top:190px;width:640px;height:400px">
      <div class="abs small" style="left:30px;top:20px;letter-spacing:3px">A PDF STORES INSTRUCTIONS</div>
      ${['draw "Do not" at (72, 540)', 'draw "turn it" at (131, 540)', 'draw "off. Your" at (190, 540)', 'draw "screen" at (72, 556)', 'draw "must lock" at (130, 556)'].map((s, i) => `<div class="abs mono" id="ws_i${i}" style="left:30px;top:${80 + i * 58}px;font-size:25px;color:#c4b5fd">${s}</div>`).join('')}</div>
    <div class="lcard" id="ws_pg" style="left:800px;top:190px;width:600px;height:400px">
      <div class="abs" style="left:40px;top:50px;width:430px;font:400 32px/1.8 var(--serif)">Do not turn it off. Your<br>screen must lock auto-<br>matically after 5 minutes</div>
      <div class="abs" id="ws_mg" style="left:480px;top:20px;width:4px;height:360px;background:repeating-linear-gradient(180deg,#ff4d6d 0 12px,transparent 12px 22px)"></div>
      ${div('ws_mgl', 400, 330, 0, 0, 'right margin', 'small', 'color:#ff4d6d;font-size:20px')}</div>
    <div class="card" id="ws_real" style="left:1450px;top:190px;width:360px;height:400px;border-color:var(--sky)">
      <div class="abs small" style="left:24px;top:20px;letter-spacing:2px">IT HANDBOOK, PAGE 1</div>
      <div class="abs mono" style="left:24px;top:70px;width:320px;font-size:24px;line-height:1.6;color:#ce9178">"Do not turn it off. Your<span class="ws">\\n</span>screen must lock automatically"</div>
      <div class="abs" style="left:24px;top:270px;font:800 70px var(--serif)"><span id="ws_n" class="sky" data-dec="0">0</span></div>
      <div class="abs small" style="left:130px;top:290px;width:210px;font-size:20px">broken lines in this one handbook</div></div>
    <div class="card" id="ws_pat" style="left:110px;top:640px;width:900px;height:370px">
      <div class="abs mono" style="left:40px;top:30px;font-size:90px">r"<span id="ws_s" style="color:var(--sky)">\\s</span><span id="ws_p" style="color:var(--sun)">+</span>"</div>
      <div class="abs" id="ws_sl" style="left:420px;top:40px"><div class="small" style="color:var(--sky);font-size:24px;letter-spacing:2px">\\s = ONE WHITESPACE CHARACTER</div>
        <div style="display:flex;gap:16px;margin-top:14px">${['space ·', 'tab →', 'newline ↵'].map((s, i) => `<span id="ws_k${i}" class="mono" style="padding:8px 16px;border-radius:10px;background:#0f2a5a;border:2px solid var(--sky);font-size:24px">${s}</span>`).join('')}</div></div>
      <div class="abs" id="ws_pl" style="left:420px;top:170px"><div class="small" style="color:var(--sun);font-size:24px;letter-spacing:2px">+ = ONE OR MORE OF THE THING BEFORE ME</div>
        <div style="display:flex;gap:10px;margin-top:14px;align-items:flex-end">${[1, 2, 3, 4, 5].map(i => `<span id="ws_b${i}" style="width:44px;height:${20 + i * 14}px;border-radius:6px;background:var(--sun);display:inline-block"></span>`).join('')}<span class="mono" style="font-size:30px;margin-left:16px">1 … <span id="ws_cnt" data-dec="0">1</span></span></div></div></div>
    <div class="card" id="ws_col" style="left:1060px;top:640px;width:750px;height:370px">
      <div class="abs small" style="left:30px;top:20px;letter-spacing:3px">EVERY RUN → ONE SPACE</div>
      <div class="abs mono" id="ws_m1" style="left:30px;top:90px;font-size:32px;white-space:pre">it<span class="ws">···</span>off.<span class="ws">→</span>Your<span class="ws">↵</span>screen</div>
      ${arrow('ws_ca', 300, 160, 300, 230, '#2dd4bf', 6)}
      <div class="abs mono" id="ws_m2" style="left:30px;top:250px;font-size:32px;color:var(--teal)">it off. Your screen ✓</div></div>
  `);
  // ---------- RAW ----------
  board('RAWS', ...G(2, 3), `
    ${div('rw_t', 110, 60, 0, 0, 'What is the little <span class="mono sun">r</span> ?', 'h1', 'font-size:64px')}
    <div class="abs mono" id="rw_big" style="left:110px;top:190px;font-size:150px"><span id="rw_r" style="color:var(--sun);display:inline-block">r</span><span style="color:#ce9178">"\\s+"</span></div>
    ${div('rw_rl', 500, 260, 0, 0, '= a RAW string', 'h2', 'font-size:52px')}
    <div class="card" id="rw_esc" style="left:110px;top:420px;width:820px;height:380px">
      <div class="abs small" style="left:30px;top:22px;letter-spacing:3px">INSIDE A NORMAL STRING, \\ STARTS A CODE</div>
      ${[['"\\n"', 'a newline ↵'], ['"\\t"', 'a tab →'], ['"\\s"', '??? not a code']].map(([a, b], i) => `<div class="abs" id="rw_e${i}" style="left:30px;top:${90 + i * 90}px;display:flex;gap:30px;align-items:center"><span class="mono" style="font-size:40px;color:#ce9178;width:130px">${a}</span><span style="font-size:36px">→</span><span class="txt" style="font-size:32px;${i === 2 ? 'color:var(--rose)' : ''}">${b}</span></div>`).join('')}</div>
    <div class="abs" id="rw_warn" style="left:990px;top:420px;width:820px;height:150px;border-radius:16px;background:#3d3000;border:2.5px solid var(--sun);padding:24px 30px;display:flex;gap:22px;align-items:center"><div style="width:70px;height:70px;flex:none">${ICON.warn()}</div><div class="mono" style="font-size:27px;color:#ffe9a8">SyntaxWarning: "\\s" is an<br>invalid escape sequence</div></div>
    <div class="card" id="rw_pipe" style="left:990px;top:610px;width:820px;height:190px">
      <div class="abs mono" style="left:40px;top:55px;font-size:56px;color:var(--sun)">r</div>
      <div class="abs" style="left:110px;top:85px;width:440px;height:16px;border-radius:8px;background:#1c2559"></div>
      <div class="abs mono" id="rw_tok" style="left:120px;top:48px;font-size:56px;color:#ce9178">\\s</div>
      <div class="abs center col" style="left:580px;top:30px;width:210px;height:130px;border-radius:14px;border:3px solid var(--teal)"><b style="font-size:24px">regex</b><span class="small">engine</span></div></div>
    <div class="card" id="rw_habit" style="left:110px;top:850px;width:1700px;height:150px;border-color:var(--teal)"><div class="center" style="height:150px;gap:26px"><div style="width:70px;height:70px">${ICON.check()}</div><span class="h2" style="font-size:44px">If a string is a regex, start it with <span class="mono sun">r</span>. Every time.</span></div></div>
  `);
  // ---------- ORDER ----------
  board('ORDER', ...G(3, 3), `
    ${div('or_t', 110, 60, 0, 0, 'Order <span class="rose">matters</span>', 'h1', 'font-size:66px')}
    <div class="card" id="or_c1" style="left:110px;top:200px;width:560px;height:150px;border-color:var(--rose)"><div class="abs" style="left:30px;top:30px;font:800 80px var(--serif);color:var(--rose)">1</div><div class="abs mono" style="left:120px;top:52px;font-size:34px">hyphen  r"-\\n"</div></div>
    <div class="card" id="or_c2" style="left:110px;top:380px;width:560px;height:150px;border-color:var(--sky)"><div class="abs" style="left:30px;top:30px;font:800 80px var(--serif);color:var(--sky)">2</div><div class="abs mono" style="left:120px;top:52px;font-size:34px">whitespace r"\\s+"</div></div>
    ${div('or_ok', 700, 330, 90, 90, ICON.check())}
    <div class="card" id="or_bad" style="left:850px;top:200px;width:960px;height:560px;border-color:var(--rose)">
      <div class="abs small" style="left:30px;top:22px;letter-spacing:3px;color:var(--rose)">SWAP THEM…</div>
      <div class="abs mono" style="left:30px;top:80px;font-size:28px;color:#8e9bc4">step 1 · whitespace first</div>
      <div class="abs mono" id="or_s1" style="left:30px;top:130px;font-size:46px">"reimburse-<span class="ws">↵</span>ment"</div>
      ${arrow('or_a', 300, 210, 300, 270, '#8e9bc4', 5)}
      <div class="abs mono" id="or_s2" style="left:30px;top:280px;font-size:46px">"reimburse-<span style="background:rgba(56,189,248,.3);border-radius:6px">·</span>ment"</div>
      <div class="abs mono" style="left:30px;top:380px;font-size:28px;color:#8e9bc4">step 2 · look for  r"-\\n"</div>
      <div class="abs" id="or_scan" style="left:30px;top:270px;width:12px;height:90px;background:var(--rose);box-shadow:0 0 30px var(--rose);border-radius:6px"></div>
      ${div('or_x', 30, 440, 0, 0, '0 matches — never again', 'pill bg-rose', 'font-size:30px;position:absolute')}</div>
    ${div('or_sil', 110, 820, 1700, 0, 'The hyphen fix <b class="rose">silently stops working</b>. No error.', 'h2 center', 'font-size:50px')}
  `);

  // ================= animation =================
  let t = T('f01');
  panel(t, 0); PANEL_H = 0;
  camB(t, 2.0, 'PARTS', 960, 520, .98, { dip: .35 });
  wipe('pa_t', t + .8, .6);
  ['pa_a', 'pa_b', 'pa_c'].forEach((id, i) => fadeUp(id, t + 1.3 + i * .25, .5));
  t = T('f02');
  [['pa_a', 'Part A'], ['pa_b', 'Part B'], ['pa_c', 'Part C']].forEach(([id, w], i, arr) => { glow(id, W('f02', w), .3, .8); to(id, W('f02', w), .3, { s: 1.04 }); if (i < 2) to(id, W('f02', arr[i + 1][1]), .3, { gl: 0, s: 1 }); });
  camB(W('f02', 'Part A'), 1.0, 'PARTS', 380, 610, 1.4); camB(W('f02', 'Part B'), 1.0, 'PARTS', 960, 610, 1.4); camB(W('f02', 'Part C'), 1.0, 'PARTS', 1540, 610, 1.4);
  t = T('f03');
  focus(t, '25', 198, 199, { cd: 1.8, dip: .3, zmax: 2.2, minCols: 50 });
  note(W('f03', 'three problems'), '25', 198, 25, '① ligatures  ② hyphens  ③ whitespace', 'var(--teal)');
  // f04 - f09 ligatures
  t = T('f04');
  camB(t, 1.8, 'LIG', 960, 300, 1.1, { dip: .3 });
  wipe('lg_t', t + .7, .6);
  t = T('f05');
  ['Effective', 'Office', 'Confidential'].forEach((w, i) => fadeUp('lg_w' + i, W('f05', w), .5, 30));
  t = T('f06');
  fadeIn('lg_look', t + .1, .4); cls('LIG', W('f06', 'not normal'), 'lgon', true);
  ['lg_w0', 'lg_w1', 'lg_w2'].forEach((id, i) => pulse(id, W('f06', 'not normal') + i * .12, 1.08));
  t = T('f07');
  camB(t, 1.0, 'LIG', 520, 510, 1.55);
  fadeIn('lg_fuse', t, .3); popIn('lg_f', t + .2, .4); popIn('lg_i', t + .4, .4); init('lg_fi', { o: 0 });
  to('lg_f', W('f07', 'joins'), .6, { x: 150 }, 'in'); to('lg_i', W('f07', 'joins'), .6, { x: -150 }, 'in');
  to('lg_f', W('f07', 'joins') + .6, .2, { o: 0 }); to('lg_i', W('f07', 'joins') + .6, .2, { o: 0 });
  ft('lg_fi', W('f07', 'joins') + .55, .5, { o: 0, s: .4 }, { o: 1, s: 1 }, 'back');
  popIn('lg_500', W('f07', 'five hundred'), .4);
  t = T('f08');
  camB(t, 1.0, 'LIG', 1400, 510, 1.55);
  fadeIn('lg_uni', t, .3); LG.forEach((g, i) => popIn('lg_u' + i, W('f08', 'characters') - .6 + i * .15, .4));
  t = T('f09');
  camB(t, 1.0, 'LIG', 960, 870, 1.0);
  fadeIn('lg_cnt', t, .3);
  ['lg_c0', 'lg_c1', 'lg_c2', 'lg_c3'].forEach((id, i) => popIn(id, W('f09', ['o, then', 'one joined', 'then c', 'then e'][i]), .35));
  count('lg_n1', W('f09', 'Four'), .6, 0, 4); [0, 1, 2, 3, 4, 5].forEach(i => popIn('lg_d' + i, W('f09', 'not six') + i * .07, .3)); count('lg_n2', W('f09', 'not six'), .6, 0, 6);
  fadeIn('lg_same', END('f09', -.3), .5);
  // f10 - f11 why care
  t = T('f10');
  camB(t, 1.8, 'LIG2', 520, 400, 1.4, { dip: .3 });
  wipe('l2_t', t + .5, .5); fadeIn('l2_scan', t + .6, .4);
  ['l2_c0', 'l2_c1', 'l2_c2', 'l2_c3'].forEach((id, i) => popIn(id, t + .8 + i * .1, .3));
  ft('l2_beam', W('f10', 'reads'), 1.6, { o: 1, x: 0 }, { o: 1, x: 440 }, 'io'); init('l2_beam', { o: 0 }); set('l2_beam', W('f10', 'reads') - .01, { o: 1 }); to('l2_beam', W('f10', 'reads') + 1.6, .3, { o: 0 });
  t = T('f11');
  popIn('l2_q', W('f11', 'not the same'), .4);
  camB(W('f11', 'A student'), 1.0, 'LIG2', 1400, 400, 1.4);
  fadeIn('l2_srch', W('f11', 'A student') - .2, .3); fadeUp('l2_qb', W('f11', 'A student'), .4, 20); drawIn('l2_ar', W('f11', 'miss'), .3); fadeIn('l2_ch', W('f11', 'miss') + .2, .4);
  ft('l2_miss', W('f11', 'completely'), .4, { o: 0, s: 2 }, { o: 1, s: 1 }, 'back'); to('l2_ch', W('f11', 'completely'), .5, { o: .35 });
  // f12 - f13 the dictionary + loop in code
  t = T('f12');
  focus(t, '25', 216, 222, { cd: 1.8, dip: .3, zmax: 2.0 });
  [216, 217, 218, 219, 220, 221].forEach((L, i) => { });
  mark(W('f12', 'left'), '25', 217, 8, 11, 'var(--rose)'); mark(W('f12', 'left') + .2, '25', 220, 8, 11, 'var(--rose)');
  mark(W('f12', 'right'), '25', 217, 13, 17, 'var(--teal)'); mark(W('f12', 'right') + .2, '25', 220, 13, 18, 'var(--teal)');
  t = T('f13');
  focus(t, '25', 223, 224, { zmax: 2.1, minCols: 60 });
  note(W('f13', 'every pair'), '25', 223, 64, 'ﬀ→ff  ﬁ→fi  ﬂ→fl  ﬃ→ffi  ﬄ→ffl', 'var(--sun)');
  t = T('f14');
  camB(t, 1.8, 'LIG2', 960, 820, 1.05, { dip: .3 });
  fadeIn('l2_fix', t + .6, .4); init('l2_good', { o: 0 });
  ft('l2_bad', W('f14', 'Office is'), .5, { o: 1 }, { o: 0 }); fadeIn('l2_good', W('f14', 'Office is'), .5);
  drawIn('l2_fa', W('f14', 'Office is') + .3, .4); fadeIn('l2_fl', W('f14', 'again'), .4); popIn('l2_ck', W('f14', 'again') + .3, .4);
  // f15 - f22 re.sub
  t = T('f15');
  camB(t, 1.8, 'RESUB', 900, 260, 1.2, { dip: .3 });
  wipe('rs_t', t + .6, .5); ft('rs_call', W('f15', 'tool'), 1.0, { o: 0, cw: 0 }, { o: 1, cw: 1 }, 'out');
  t = T('f16');
  [['rs_a1', 'rs_l1', 'shape'], ['rs_a2', 'rs_l2', 'instead'], ['rs_a3', 'rs_l3', 'text to']].forEach(([a, l, w]) => { pulse(a, W('f16', w), 1.2); fadeUp(l, W('f16', w), .4, -20); });
  t = T('f17');
  camB(t, 1.0, 'RESUB', 960, 500, 1.05);
  fadeIn('rs_all', t, .3); init('rs_txt2', { o: 0 });
  to('rs_txt', W('f17', 'replaces all'), .4, { o: 0 }); ft('rs_txt2', W('f17', 'replaces all') + .2, .5, { o: 0, y: -20 }, { o: 1, y: 0 });
  popIn('rs_noloop', W('f17', 'Every one'), .4);
  t = T('f18');
  focus(t, '25', 278, 278, { cd: 1.8, dip: .3, zmax: 2.4, minCols: 40 });
  mark(W('f18', 'Now look'), '25', 278, 4, 10, 'var(--rose)');
  t = T('f19');
  camB(t, 1.8, 'RESUB', 520, 820, 1.45, { dip: .3 });
  fadeIn('rs_imm', t + .5, .3); popIn('rs_glass', W('f19', 'never be changed'), .5); init('rs_new', { o: 0 }); init('rs_lbl', { o: 0 }); init('rs_arr', { dr: 0 }); init('rs_trash', { o: 0 });
  t = T('f20');
  ft('rs_new', W('f20', 'brand new'), .6, { o: 0, x: -400 }, { o: 1, x: 0 }, 'out');
  fadeIn('rs_lbl', W('f20', 'hands it'), .4);
  t = T('f21');
  to('rs_lbl', W('f21', 'forget'), .4, { o: .25 });
  popIn('rs_trash', W('f21', 'throw'), .4);
  to('rs_new', W('f21', 'throw'), .8, { x: 220, y: 160, s: .2, r: 40, o: 0 }, 'in');
  t = T('f22');
  camB(t, 1.0, 'RESUB', 1400, 820, 1.45);
  fadeIn('rs_bug', t, .3); popIn('rs_nerr', t + .3, .4); ft('rs_moon', W('f22', 'evenings'), .6, { o: 0, x: -60 }, { o: 1, x: 0 }); fadeUp('rs_tip', W('f22', 'look for'), .5, 20);
  // f23 - f31 hyphen
  t = T('f23');
  camB(t, 2.0, 'HYPH', 960, 300, 1.05, { dip: .35 });
  wipe('hy_t', t + .7, .6);
  t = T('f24');
  camB(t, 1.0, 'HYPH', 490, 400, 1.6);
  ft('hy_doc', t, .5, { o: 0, y: 40 }, { o: 1, y: 0 }); pulse('hy_br', W('f24', 'hyphen'), 1.3);
  t = T('f25');
  camB(t, 1.0, 'HYPH', 1380, 290, 1.6);
  fadeUp('hy_raw', t + .1, .5, 30);
  t = T('f26');
  camB(t, 1.0, 'HYPH', 1380, 500, 1.6);
  fadeIn('hy_pat', t, .3); fadeIn('hy_l1', W('f26', 'hyphen'), .3); pulse('hy_p1', W('f26', 'hyphen'), 1.5); fadeIn('hy_l2', W('f26', 'newline'), .3); pulse('hy_p2', W('f26', 'Backslash'), 1.4);
  t = T('f27');
  fadeIn('hy_l3', W('f27', 'empty'), .3); pulse('hy_p3', W('f27', 'empty'), 1.5);
  t = T('f28');
  camB(t, 1.0, 'HYPH', 660, 725, 1.5);
  fadeIn('hy_join', t, .3); init('hy_res', { o: 0 });
  to('hy_gap', W('f28', 'becomes'), .5, { o: 0, sy: 0 }); to('hy_orig', W('f28', 'reimbursement') - .1, .3, { o: 0 }); fadeIn('hy_res', W('f28', 'reimbursement'), .4);
  t = T('f29');
  camB(t, 1.0, 'HYPH', 1540, 725, 1.6);
  fadeIn('hy_zero', t, .3); count('hy_n', W('f29', 'zero'), .8, 9, 0, 'out');
  t = T('f30');
  camB(t, 1.0, 'HYPH', 960, 880, 1.15);
  popIn('hy_w', W('f30', 'Word'), .4); popIn('hy_l', W('f30', 'LaTeX'), .4); slideR('hy_keep', W('f30', 'stays'), .5, 60);
  t = T('f31');
  camB(t, 1.0, 'HYPH', 700, 960, 1.4);
  wipe('hy_cnt', W('f31', 'Count'), .8); fadeIn('hy_out', W('f31', 'how many') + .3, .4);
  // f32 - f42 whitespace
  t = T('f32');
  camB(t, 1.8, 'WS', 960, 300, 1.05, { dip: .3 });
  wipe('ws_t', t + .6, .6); popIn('ws_star', W('f32', 'real work'), .45);
  t = T('f33');
  camB(t, 1.0, 'WS', 430, 400, 1.6);
  fadeIn('ws_ins', t, .3); [0, 1, 2, 3, 4].forEach(i => slideL('ws_i' + i, W('f33', 'instructions') + i * .25, .35, 40));
  t = T('f34');
  camB(t, 1.0, 'WS', 1100, 400, 1.6);
  ft('ws_pg', t, .5, { o: 0, y: 40 }, { o: 1, y: 0 }); ft('ws_mg', W('f34', 'margin'), .6, { ch: 0 }, { ch: 1 }); fadeIn('ws_mgl', W('f34', 'margin') + .3, .3);
  t = T('f35');
  cam(t + .3, 1.0, { x: G(1, 3)[0] + 1140, y: G(1, 3)[1] + 400, z: 1.9 });
  t = T('f36');
  camB(t, 1.0, 'WS', 1630, 390, 1.9);
  fadeIn('ws_real', t, .4);
  t = T('f37');
  count('ws_n', W('f37', 'forty'), 1.0, 0, 45); camB(W('f37', 'Tables'), 1.0, 'WS', 1300, 400, 1.2);
  t = T('f38');
  camB(t, 1.0, 'WS', 560, 825, 1.5);
  fadeIn('ws_pat', t, .3); init('ws_sl', { o: 0 }); init('ws_pl', { o: 0 });
  t = T('f39');
  fadeIn('ws_sl', t, .3); pulse('ws_s', t, 1.3);
  [['ws_k0', 'A space'], ['ws_k1', 'a tab'], ['ws_k2', 'a newline']].forEach(([id, w]) => popIn(id, W('f39', w), .35));
  t = T('f40');
  fadeIn('ws_pl', t, .3); pulse('ws_p', t, 1.4);
  [1, 2, 3, 4, 5].forEach(i => ft('ws_b' + i, W('f40', 'one or more') + i * .15, .3, { o: 0, sy: 0 }, { o: 1, sy: 1 }, 'back'));
  t = T('f41');
  count('ws_cnt', W('f41', 'any length'), 1.6, 1, 1000, 'in');
  t = T('f42');
  camB(t, 1.0, 'WS', 1430, 825, 1.5);
  fadeIn('ws_col', t, .3); fadeIn('ws_m1', t + .2, .3); drawIn('ws_ca', W('f42', 'Watch'), .4); fadeUp('ws_m2', W('f42', 'Every messy'), .5, -30);
  // f43 - f47 raw strings
  t = T('f43');
  camB(t, 1.8, 'RAWS', 560, 280, 1.3, { dip: .3 });
  wipe('rw_t', t + .6, .5); fadeIn('rw_big', t + .8, .4); to('rw_r', W('f43', 'little r'), .5, { s: 1.5 }, 'back'); to('rw_r', END('f43'), .4, { s: 1 });
  t = T('f44');
  fadeIn('rw_rl', t, .4); camB(W('f44', 'Inside'), 1.0, 'RAWS', 520, 610, 1.45);
  fadeIn('rw_esc', W('f44', 'Inside') - .2, .3); slideL('rw_e0', W('f44', 'Backslash n'), .4, 40); slideL('rw_e1', W('f44', 'Backslash t'), .4, 40);
  t = T('f45');
  slideL('rw_e2', t, .4, 40); camB(W('f45', 'newer'), 1.0, 'RAWS', 1400, 500, 1.5);
  ft('rw_warn', W('f45', 'warn'), .5, { o: 0, y: -40 }, { o: 1, y: 0 }, 'back'); shake('rw_warn', W('f45', 'invalid'), 8);
  t = T('f46');
  camB(t, 1.0, 'RAWS', 1400, 700, 1.5);
  fadeIn('rw_pipe', t, .3); ft('rw_tok', W('f46', 'pass through'), 1.4, { x: 0 }, { x: 460 }, 'io');
  t = T('f47');
  camB(t, 1.0, 'RAWS', 960, 700, 1.0);
  ft('rw_habit', t + .1, .5, { o: 0, s: .8 }, { o: 1, s: 1 }, 'back');
  // f48 - f52 order
  t = T('f48');
  camB(t, 1.8, 'ORDER', 960, 400, 1.0, { dip: .3 });
  wipe('or_t', t + .6, .5); slideL('or_c1', W('f48', 'order'), .4); slideL('or_c2', W('f48', 'order') + .2, .4);
  t = T('f49');
  popIn('or_ok', W('f49', 'before'), .45); camB(t, 1.0, 'ORDER', 450, 370, 1.5);
  t = T('f50');
  camB(t, 1.0, 'ORDER', 1330, 330, 1.5);
  fadeIn('or_bad', t, .3); init('or_s2', { o: 0 }); init('or_scan', { o: 0 });
  to('or_c1', t + .2, .6, { y: 180 }); to('or_c2', t + .2, .6, { y: -180 });
  drawIn('or_a', W('f50', 'becomes a space'), .4); fadeIn('or_s2', W('f50', 'Now we have'), .4);
  t = T('f51');
  camB(t, 1.0, 'ORDER', 1330, 480, 1.4);
  set('or_scan', W('f51', 'looking'), { o: 1 }); ft('or_scan', W('f51', 'looking'), 1.8, { x: 0 }, { x: 560 }, 'io'); to('or_scan', W('f51', 'looking') + 1.8, .3, { o: 0 });
  popIn('or_x', W('f51', 'never match'), .45);
  t = T('f52');
  camB(t, 1.0, 'ORDER', 960, 600, .98);
  fadeUp('or_sil', t + .2, .5, 30); pulse('or_sil', W('f52', 'No error'), 1.05);
  // f53 strip
  t = T('f53');
  focus(t, '25', 322, 323, { cd: 1.8, dip: .3, zmax: 2.3, minCols: 46 });
  mark(W('f53', 'strip'), '25', 323, 15, 23);
  note(W('f53', 'start and'), '25', 323, 26, '"␣␣Your screen␣" → "Your screen"', 'var(--teal)');
});
