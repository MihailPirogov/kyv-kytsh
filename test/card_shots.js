// Screenshots of word cards and other text-over-ornament places: TAG=before|after
const { chromium } = require('playwright-core'); const path = require('path'); const http = require('http'); const fs = require('fs');
const ROOT = path.join(__dirname, '..'); const OUT = path.join(ROOT, 'shots', 'cards'); fs.mkdirSync(OUT, { recursive: true });
const TAG = process.env.TAG || 'after';
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.json': 'application/json', '.woff2': 'font/woff2' };
const srv = http.createServer((q, r) => { let p = decodeURIComponent(q.url.split('?')[0].split('#')[0]); if (p.endsWith('/')) p += 'index.html'; const f = path.join(ROOT, p);
  fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); } else { r.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' }); r.end(d); } }); });
(async () => { await new Promise(r => srv.listen(0, r)); const url = 'http://127.0.0.1:' + srv.address().port + '/index.html';
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  for (const [name, vp] of [['phone', { width: 390, height: 844 }], ['wide', { width: 1366, height: 800 }]]) {
    const ctx = await b.newContext({ viewport: vp, deviceScaleFactor: name === 'phone' ? 2 : 1 }); const p = await ctx.newPage();
    for (const w of ['вӧр', 'пельӧс', 'ва']) { await p.goto(url + '#word=' + encodeURIComponent(w)); await p.waitForSelector('#cardModal:not([hidden])', { timeout: 6000 }).catch(() => {}); await p.waitForTimeout(700);
      await p.screenshot({ path: path.join(OUT, `${TAG}_${name}_card_${w}.png`) }); }
    // other modals with text over ornament
    await p.goto(url); await p.waitForTimeout(800); await p.click('text=Пропустить', { timeout: 2000 }).catch(() => {}); await p.waitForTimeout(300);
    for (const id of ['tWotd', 'tColl', 'tAch', 'tMap']) { if (await p.$('#' + id)) { await p.click('#' + id, { timeout: 3000 }).catch(() => {}); await p.waitForTimeout(500);
      await p.screenshot({ path: path.join(OUT, `${TAG}_${name}_${id}.png`) }); await p.evaluate(() => window.kyvKytsh && kyvKytsh.closeModal && kyvKytsh.closeModal()); await p.waitForTimeout(200); } }
    await ctx.close(); }

  await b.close(); srv.close(); console.log('done', fs.readdirSync(OUT).filter(f => f.startsWith(TAG)).length);
})();
