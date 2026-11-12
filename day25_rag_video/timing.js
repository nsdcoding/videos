// dump line start times + total to timing.json
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage();
  await p.goto('file://' + path.resolve('src/index.html')); await p.waitForFunction(() => window.READY);
  const d = await p.evaluate(() => ({ total: TOTAL, lines: LINES.map(l => ({ id: l.id, chap: l.chap, start: l.start, dur: l.dur })), cams: (renderAt(0), CAM.segs.map(s => ({ t0: s.t0, t1: s.t1, dip: s.dip }))) }));
  fs.writeFileSync('timing.json', JSON.stringify(d, null, 1)); console.log('total', d.total); await b.close();
})();
