const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const files = fs.readdirSync('.').filter(f => /^cooper-.*\.html$/.test(f)).sort();
  for (const f of files) { const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
    await p.goto('file://' + path.resolve(f), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: f.replace('.html', '.png') }); await p.close(); console.log(f); }
  const prev = await b.newPage({ viewport: { width: 1700, height: 900 } });
  const imgs = files.map(f => `<img src="file://${path.resolve(f.replace('.html','.png'))}" style="width:320px;margin:6px">`).join('');
  await prev.setContent(`<body style="margin:0;background:#888;display:flex;flex-wrap:wrap;width:1700px">${imgs}</body>`);
  await prev.waitForTimeout(500); await prev.screenshot({ path: '_previa.png', fullPage: true }); await b.close();
})();
