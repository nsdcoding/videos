// node stills.js out_dir t1 t2 ...   (or "id:offset" to use a narration line time)
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const [out, ...ts] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') errs.push(m.text()); });
  await p.goto('file://' + path.resolve('src/index.html'));
  await p.waitForFunction(() => window.READY || window.__err, null, { timeout: 20000 }).catch(() => { });
  await p.evaluate(() => document.fonts.ready);
  if (errs.length) console.log('ERRORS:', errs.join('\n'));
  console.log('TOTAL', await p.evaluate(() => window.TOTAL));
  for (const s of ts) {
    const t = await p.evaluate(s => { if (s.includes(':')) { const [id, o] = s.split(':'); return T(id) + (+o); } return +s; }, s);
    await p.evaluate(t => renderAt(t), t);
    await p.screenshot({ path: `${out}/${s.replace(':', '_')}.jpg`, type: 'jpeg', quality: 80 });
  }
  if (errs.length) console.log('ERRORS:', errs.join('\n'));
  await b.close();
})();
