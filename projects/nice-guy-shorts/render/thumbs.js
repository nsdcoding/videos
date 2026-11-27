const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (let n = 1; n <= 8; n++) {
    await p.goto(`http://localhost:8125/nice-guy-shorts/render/thumb.html?n=${n}`);
    await p.waitForFunction('window.READY===true');
    await p.locator('#t').screenshot({ path: `../final/thumbnails/short_${n}_thumbnail.jpg`, type: 'jpeg', quality: 92 });
  }
  await b.close();
})();
