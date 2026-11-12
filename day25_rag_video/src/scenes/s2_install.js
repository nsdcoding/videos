// c2 : install pypdf
(window.SCENES = window.SCENES || []).push(function () {
  const G = (c, r) => [c * 2400, r * 1500];
  const bar = (id, w, c) => `<div class="abs" style="left:0;top:0;width:260px;height:16px;border-radius:8px;background:#1c2559"></div><div class="abs" id="${id}" style="left:0;top:0;width:${w}px;height:16px;border-radius:8px;background:${c}"></div>`;
  const cmpCard = (id, x, name, sp, la, extra, col) => `<div class="card" id="${id}" style="left:${x}px;top:600px;width:520px;height:400px;border-color:${col}">
     <div class="abs mono" style="left:36px;top:30px;font-size:44px;font-weight:700;color:${col}">${name}</div>
     <div class="abs small" style="left:36px;top:120px;letter-spacing:2px">SPEED</div><div class="abs" style="left:200px;top:128px">${bar(id + 'b1', sp, col)}</div>
     <div class="abs small" style="left:36px;top:170px;letter-spacing:2px">LAYOUT</div><div class="abs" style="left:200px;top:178px">${bar(id + 'b2', la, col)}</div>
     <div class="abs txt" id="${id}x" style="left:36px;top:240px;width:450px;font-size:27px">${extra}</div></div>`;
  board('INSTALL', ...G(-1, 0), `
    <div class="card" id="in_pk" style="left:110px;top:110px;width:360px;height:420px;border-color:var(--sun)">
       <div class="abs" style="left:90px;top:40px;width:180px;height:180px">${ICON.box('#ffd23f')}</div>
       <div class="abs mono center" style="left:0;top:250px;width:360px;font-size:56px;font-weight:700" >pypdf</div>
       <div class="abs small center" style="left:0;top:335px;width:360px;font-size:26px">reads text out of PDFs</div></div>
    <div class="card" id="in_py" style="left:540px;top:110px;width:640px;height:420px">
       <div class="abs small" style="left:30px;top:22px;letter-spacing:3px">TWO PYTHONS ON ONE LAPTOP</div>
       <div id="in_p1" class="abs center col" style="left:40px;top:220px;width:240px;height:160px;border-radius:18px;border:3px solid var(--teal);background:rgba(45,212,191,.1)"><b style="font-size:30px">Python 3.14</b><span class="small">runs your file</span></div>
       <div id="in_p2" class="abs center col" style="left:360px;top:220px;width:240px;height:160px;border-radius:18px;border:3px solid #56628c;background:#0b1130"><b style="font-size:30px;color:#9aa5cf">Python 3.9</b><span class="small">some other one</span></div>
       <div id="in_pip" class="abs mono center" style="left:200px;top:80px;width:240px;height:64px;border-radius:14px;background:var(--sun);color:#2a2000;font-size:30px;font-weight:700">pip</div>
       ${curve('in_a1', 320, 150, 470, 170, 480, 214, '#ff4d6d', 5)}
       ${div('in_x', 470, 150, 50, 50, ICON.cross())}
       ${curve('in_a2', 320, 150, 170, 170, 160, 214, '#2dd4bf', 6)}
       ${div('in_m', 30, 395, 600, 0, '<span class="mono" style="font-size:24px;color:var(--teal)">python3 -m pip</span><span class="small"> → always the right one</span>')}</div>
    <div class="card" id="in_pure" style="left:1250px;top:110px;width:560px;height:420px">
       <div class="abs h2" style="left:36px;top:30px">Why <span class="mono sun">pypdf</span>?</div>
       ${['written in pure Python', 'no compiler needed', 'installs on every machine'].map((s, i) => `<div class="abs" id="in_c${i}" style="left:36px;top:${120 + i * 90}px;display:flex;align-items:center;gap:20px"><div style="width:52px;height:52px">${ICON.check()}</div><span class="txt" style="font-size:31px">${s}</span></div>`).join('')}</div>
    ${cmpCard('in_k1', 110, 'pypdf', 120, 110, '✓ plain text from normal PDFs<br><b class="sun">simplest thing that works</b>', 'var(--sun)')}
    ${cmpCard('in_k2', 700, 'PyMuPDF', 240, 220, 'fast, layout-aware<br><b class="sky">can turn a page into an image</b>', 'var(--sky)')}
    ${cmpCard('in_k3', 1290, 'pdfplumber', 150, 240, 'great with tables<br><span class="mute">and page layout</span>', 'var(--vio)')}
    ${div('in_later', 760, 1020, 420, 0, '→ we meet it in the screenshot class', 'hand', 'font-size:38px;color:var(--sky)')}
  `);
  // floating OS cards over the VS Code window
  add(`<div class="card" id="os_mac" style="left:${VS.x + 1180}px;top:${VS.y + 360}px;width:520px;height:130px;padding:20px 28px">
        <div class="small" style="letter-spacing:3px">MAC · TERMINAL</div><div class="mono" style="font-size:30px;margin-top:10px">pip3 install pypdf</div></div>
       <div class="card" id="os_win" style="left:${VS.x + 1180}px;top:${VS.y + 510}px;width:520px;height:130px;padding:20px 28px;border-color:var(--sky)">
        <div class="small" style="letter-spacing:3px">WINDOWS · COMMAND PROMPT</div><div class="mono" style="font-size:30px;margin-top:10px">pip install pypdf</div></div>`);

  // ================= animation =================
  let t = T('c01');
  camB(t, 2.2, 'INSTALL', 290, 330, 1.45, { dip: .35 });
  ft('in_pk', t + 1.3, .8, { o: 0, y: -300, r: -10 }, { o: 1, y: 0, r: 0 }, 'back');
  pulse('in_pk', W('c01', 'pypdf'), 1.08);

  t = T('c02');
  camVS(t, 1.8, .93, { dip: .3, dy: 120 });
  panel(t + 1.0, 400);
  let tt = termCmd(W('c02', 'type'), 'pip3 install pypdf', .06);
  slideR('os_mac', W('c02', 'Mac'), .6, 80);
  cam(W("c02", "type"), 1.2, { x: VS.x + 1000, y: VS.y + 700, z: 1.2 });
  termLine(tt + .2, 'Collecting pypdf');
  termLine(tt + .6, '  Downloading pypdf-py3-none-any.whl <span class="ok">━━━━━━━━━━━━━━━━━━━━</span> 100%');
  termLine(tt + 1.2, 'Installing collected packages: pypdf');
  termLine(tt + 1.8, '<span class="ok">Successfully installed pypdf</span>');

  t = T('c03');
  slideR('os_win', W('c03', 'Windows'), .6, 80);
  cam(t, 1.0, { x: VS.x + 1350, y: VS.y + 520, z: 1.45 });
  glow('os_win', W('c03', 'pip install'), .4, .6); to('os_win', END('c03'), .4, { gl: 0 });

  t = T('c04');
  cam(t, 1.0, { x: VS.x + 1000, y: VS.y + 700, z: 1.2 });
  tt = termCmd(W('c04', 'use'), 'python3 -m pip install pypdf', .045);
  termLine(tt + .2, 'Requirement already satisfied: pypdf');
  camB(W('c04', 'always'), 1.6, 'INSTALL', 860, 330, 1.45, { dip: .3 });
  fadeIn('in_py', W('c04', 'always') + .6, .4);
  popIn('in_p1', W('c04', 'always') + .8, .4); popIn('in_p2', W('c04', 'always') + .95, .4); popIn('in_pip', W('c04', 'always') + 1.1, .4);
  drawIn('in_a1', W('c04', 'always') + 1.4, .5); popIn('in_x', W('c04', 'always') + 1.9, .4);
  drawIn('in_a2', W('c04', 'Python you') - .3, .5); glow('in_p1', W('c04', 'Python you'), .4, .7); fadeIn('in_m', W('c04', 'Python you'), .5);

  t = T('c05');
  camB(t, 1.2, 'INSTALL', 1530, 330, 1.45);
  fadeIn('in_pure', t + .2, .4);
  popIn('in_c0', W('c05', 'pure Python'), .45); popIn('in_c1', W('c05', 'No compiler'), .45); popIn('in_c2', W('c05', 'every student'), .45);

  t = T('c06');
  camB(t, 1.4, 'INSTALL', 960, 790, .98);
  slideL('in_k1', t + .2, .5); slideR('in_k2', W('c06', 'PyMuPDF'), .5); slideR('in_k3', W('c06', 'pdfplumber'), .5);
  ['in_k1', 'in_k2', 'in_k3'].forEach((k, i) => { ft(k + 'b1', W('c06', 'faster') + i * .15, .7, { cw: 0 }, { cw: 1 }); ft(k + 'b2', W('c06', 'layout') + i * .15, .7, { cw: 0 }, { cw: 1 }); });
  init('in_k1x', { o: 0 }); init('in_k2x', { o: 0 }); init('in_k3x', { o: 0 });
  fadeIn('in_k2x', W('c06', 'layout') + .3, .4); fadeIn('in_k3x', W('c06', 'layout') + .5, .4);

  t = T('c07');
  camB(t, 1.2, 'INSTALL', 960, 820, 1.18);
  glow('in_k2', t + .2, .4, .7); fadeIn('in_later', W('c07', 'later'), .5);
  to('in_k2', W('c07', 'But for'), .4, { gl: 0 });
  fadeIn('in_k1x', W('c07', 'But for'), .4); glow('in_k1', W('c07', 'simplest'), .4, .9); pulse('in_k1', W('c07', 'simplest'), 1.06);
  camB(W('c07', 'But for'), 1.0, 'INSTALL', 400, 800, 1.5);
  out('os_mac', END('c07'), .3); out('os_win', END('c07'), .3);
});
