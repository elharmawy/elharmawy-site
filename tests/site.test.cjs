// Site checks: run with `node tests/site.test.js` (serves the folder on a local port, uses Playwright).
const http = require('http'), fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const root = path.join(__dirname, '..');
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.json': 'application/json', '.webmanifest': 'application/json' };
const srv = http.createServer((q, r) => {
  let p = decodeURIComponent(q.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html';
  let f = path.join(root, p); if (!fs.existsSync(f) && fs.existsSync(f + '.html')) f += '.html';
  if (!fs.existsSync(f)) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r);
});
const fails = []; const ok = (c, m) => { console.log((c ? 'PASS ' : 'FAIL ') + m); if (!c) fails.push(m); };
(async () => {
  await new Promise(r => srv.listen(0, r)); const base = 'http://127.0.0.1:' + srv.address().port;
  const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
  ok(!/555128551|55 512 8551/.test(html), 'personal number not on the site');
  ok((html.match(/971563469000/g) || []).length >= 5, 'client WhatsApp number used');
  ok(/href="pay"/.test(html), 'payments page linked');
  ok(/1,780/.test(html) && /Abu Dhabi/.test(html), 'Abu Dhabi licence offer (AED 1,780) shown');
  const foot = html.slice(html.indexOf('<footer class="legal">'), html.indexOf('</footer>'));
  ok(!/Amiri Decree|المرسوم الأميري|مرسوم الأميري|Share capital|رأس المال 100|58667/.test(foot), 'footer has no capital, decree or licence number');
  ok(/value="Investor visa/.test(html) && /value="Golden visa/.test(html), 'investor + golden visa in the form');
  ok(/subject to (the )?UAE laws|in accordance with the laws and regulations of the United Arab Emirates/.test(html), 'UAE laws line present');
  const man = JSON.parse(fs.existsSync(path.join(root,'img/watermarked.json')) ? fs.readFileSync(path.join(root,'img/watermarked.json'),'utf8') : '{}');
  const crypto = require('crypto');
  const imgs = [].concat(...['img/res','img/res/t','img/svc','img/ai'].map(d => fs.readdirSync(path.join(root,d)).filter(f=>/\.(jpe?g|png|webp)$/i.test(f)).map(f=>d+'/'+f)), ['founder.jpg','og-image.png']);
  const bad = imgs.filter(f => man[f] !== crypto.createHash('sha1').update(fs.readFileSync(path.join(root,f))).digest('hex'));
  ok(bad.length === 0, 'every site image carries the watermark' + (bad.length ? ' (missing: ' + bad.slice(0,5).join(', ') + ')' : ''));
  const iq = fs.readFileSync(path.join(root,'iqama.html'),'utf8');
  ok(/wa\.me\/971563469000/.test(iq) && !/555128551/.test(iq), 'iqama page: WhatsApp goes to 056 346 9000');
  ok(/تخضع لقوانين دولة الإمارات/.test(iq), 'iqama page: UAE laws line');
  ok(/HBC · ELHARMAWY\.COM/.test(iq), 'iqama page: watermark');
  ok(/مش بنوفّر فيزا عمل/.test(iq), 'iqama page: says we do not sell work visas');
  const robots = fs.readFileSync(path.join(root,'robots.txt'),'utf8');
  ok(/User-agent: OAI-SearchBot\s+Allow: \//.test(robots) && !/Disallow: \/\s*$/m.test(robots), 'robots.txt lets ChatGPT search (OAI-SearchBot) read the site');
  const b = await chromium.launch();
  for (const vp of [{ n: 'phone', width: 390, height: 844 }, { n: 'desktop', width: 1366, height: 860 }]) {
    const pg = await b.newPage({ viewport: { width: vp.width, height: vp.height } });
    const t0 = Date.now(); await pg.goto(base + '/', { waitUntil: 'domcontentloaded' });
    await pg.waitForFunction(() => !document.getElementById('intro'), null, { timeout: 4000 }).catch(() => {});
    const introGone = Date.now() - t0;
    ok(introGone < 2200, `${vp.n}: intro clears quickly (${introGone} ms)`);
    ok(await pg.evaluate(() => document.getElementById('site').getAttribute('dir') === 'rtl'), `${vp.n}: opens in Arabic`);
    const over = await pg.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    ok(over <= 1, `${vp.n}: no sideways scroll (${over}px)`);
    const wa = await pg.evaluate(() => [...document.querySelectorAll('a[href*="wa.me"]')].every(a => /wa\.me\/971563469000/.test(a.href)));
    ok(wa, `${vp.n}: every WhatsApp link goes to 056 346 9000`);
    await pg.close();
  }
  { const pg = await b.newPage({ viewport: { width: 390, height: 844 } }); await pg.goto(base + '/iqama'); await pg.waitForTimeout(300);
    const over = await pg.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth); ok(over <= 1, 'iqama page: no sideways scroll on phone (' + over + 'px)');
    ok(await pg.evaluate(() => document.dir === 'rtl' || document.documentElement.dir === 'rtl'), 'iqama page: Arabic right-to-left'); await pg.close(); }
  await b.close(); srv.close();
  console.log(fails.length ? `\n${fails.length} failing` : '\nall passing'); process.exit(fails.length ? 1 : 0);
})();
