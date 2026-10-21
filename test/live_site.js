const { chromium } = require('playwright-core'); const path = require('path');
(async () => { const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] }); const errs = [];
  for (const [n, u, vp] of [['landing_phone', '/kyv-kytsh-igra/', { width: 390, height: 844 }], ['landing_wide', '/kyv-kytsh-igra/', { width: 1366, height: 900 }], ['blog_post', '/blog/2026-10-21-kyv-kytsh/', { width: 1366, height: 900 }], ['home', '/', { width: 1366, height: 900 }]]) {
    const p = await b.newPage({ viewport: vp }); p.on('pageerror', e => errs.push(n + ': ' + e.message));
    await p.goto('https://pirogovlab.ru' + u, { waitUntil: 'networkidle' }); await p.waitForTimeout(800);
    if (n === 'home') { const el = await p.$('a.proj[href="/kyv-kytsh-igra/"]'); if (el) await el.scrollIntoViewIfNeeded(); }
    const broken = await p.evaluate(() => [...document.images].filter(i => i.complete && i.naturalWidth === 0 && i.loading !== 'lazy').map(i => i.src));
    await p.screenshot({ path: path.join(__dirname, '../shots/live', 'site_' + n + '.png') }); console.log(n, 'broken', broken.length); await p.close(); }
  console.log('errors', errs.length ? errs : 'none'); await b.close(); })();
