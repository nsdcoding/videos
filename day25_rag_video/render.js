// Parallel renderer: node render.js <outdir> <jobsJson>   jobs: [{name, f0, f1}]
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs'); const { spawn } = require('child_process');
const FPS = 30;
(async () => {
  const [outdir, jobsFile, nw = '4'] = process.argv.slice(2);
  const jobs = JSON.parse(fs.readFileSync(jobsFile)); fs.mkdirSync(outdir, { recursive: true });
  const queue = jobs.filter(j => !fs.existsSync(path.join(outdir, j.name + '.mp4')));
  async function worker(w) {
    const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
    const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
    p.on('pageerror', e => console.log('PAGEERR', e.message));
    await p.goto('file://' + path.resolve('src/index.html'));
    await p.waitForFunction(() => window.READY); await p.evaluate(() => document.fonts.ready);
    const cdp = await p.context().newCDPSession(p);
    while (queue.length) {
      const j = queue.shift(); const tmp = path.join(outdir, j.name + '.tmp.mp4');
      const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-g', '60', '-r', String(FPS), '-f', 'mp4', tmp], { stdio: ['pipe', 'inherit', 'inherit'] });
      const t0 = Date.now();
      for (let f = j.f0; f < j.f1; f++) {
        await p.evaluate(t => renderAt(t), f / FPS);
        const r = await cdp.send('Page.captureScreenshot', { format: 'jpeg', quality: 93 });
        const buf = Buffer.from(r.data, 'base64');
        if (!ff.stdin.write(buf)) await new Promise(res => ff.stdin.once('drain', res));
      }
      ff.stdin.end(); await new Promise(res => ff.on('close', res));
      fs.renameSync(tmp, path.join(outdir, j.name + '.mp4'));
      console.log(`w${w} ${j.name} ${j.f1 - j.f0}f ${((Date.now() - t0) / 1000).toFixed(0)}s  left:${queue.length}`);
    }
    await b.close();
  }
  await Promise.all(Array.from({ length: +nw }, (_, i) => worker(i)));
})();
