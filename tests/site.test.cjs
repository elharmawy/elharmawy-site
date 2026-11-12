// Site checks: run with `node tests/site.test.js` (serves the folder on a local port, uses Playwright).
const http = require('http'), fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const root = path.join(__dirname, '..');
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.json': 'application/json', '.webmanifest': 'application/json' };
const srv = http.createServer((q, r) => {
  if (q.url.startsWith('/api/track')) { const c = new URL(q.url, 'http://x').searchParams.get('code') || ''; r.writeHead(200, { 'content-type': 'application/json' });
    return r.end(JSON.stringify(/HBC1234TEST/i.test(c.replace(/[^a-z0-9]/gi, '')) ? { ok: true, found: true, service: 'Company setup', step: 3, stepName: 'Submitted', status: 'In progress', updated: '2026-11-12', note: '' } : { ok: true, found: false })); }
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
  ok(/value="Residency application assistance"/.test(html) && /value="Golden visa/.test(html), 'residency help + golden visa in the form');
  ok(/subject to (the )?UAE laws|in accordance with the laws and regulations of the United Arab Emirates/.test(html), 'UAE laws line present');
  const man = JSON.parse(fs.existsSync(path.join(root,'img/watermarked.json')) ? fs.readFileSync(path.join(root,'img/watermarked.json'),'utf8') : '{}');
  const crypto = require('crypto');
  const imgs = [].concat(...['img/res','img/res/t','img/svc','img/ai'].map(d => fs.readdirSync(path.join(root,d)).filter(f=>/\.(jpe?g|png|webp)$/i.test(f)).map(f=>d+'/'+f)), ['founder.jpg','og-image.png']);
  const bad = imgs.filter(f => man[f] !== crypto.createHash('sha1').update(fs.readFileSync(path.join(root,f))).digest('hex'));
  ok(bad.length === 0, 'every site image carries the watermark' + (bad.length ? ' (missing: ' + bad.slice(0,5).join(', ') + ')' : ''));
  { const bad=/إقامة مستثمر (لمدة )?سنتين|إقامتك بإسمك|من غير كفيل|عايز إقامة بإسمي|Investor visa \(2 years\)|2-year residency|إقامتك في الإمارات علينا|Your UAE residency, handled/;
    for (const f of ['index.html','start.html','links.html','pay.html']) ok(!bad.test(fs.readFileSync(path.join(root,f),'utf8')), f+': no residency-selling wording'); }
  const iq = fs.readFileSync(path.join(root,'start.html'),'utf8');
  ok(/wa\.me\/971563469000/.test(iq) && !/555128551/.test(iq), 'start page: WhatsApp goes to 056 346 9000');
  ok(/تخضع لقوانين دولة الإمارات/.test(iq), 'start page: UAE laws line');
  ok(/HBC · ELHARMAWY\.COM/.test(iq), 'start page: watermark');
  ok(/مش بنبيع إقامات/.test(iq), 'start page: says we do not sell work visas');
  const robots = fs.readFileSync(path.join(root,'robots.txt'),'utf8');
  ok(/User-agent: OAI-SearchBot\s+Allow: \//.test(robots) && !/Disallow: \/\s*$/m.test(robots), 'robots.txt lets ChatGPT search (OAI-SearchBot) read the site');
  const sm = fs.readFileSync(path.join(root,'sitemap.xml'),'utf8');
  ok(!/https:\/\/www\.elharmawy\.com/.test(sm + robots) && /https:\/\/elharmawy\.com\/start/.test(sm), 'sitemap + robots use the main address elharmawy.com (no www redirect)');
  ok(/rel="canonical" href="https:\/\/elharmawy\.com\/"/.test(html), 'home canonical is https://elharmawy.com/');
  const b = await chromium.launch();
  for (const vp of [{ n: 'phone', width: 390, height: 844 }, { n: 'desktop', width: 1366, height: 860 }]) {
    const pg = await b.newPage({ viewport: { width: vp.width, height: vp.height } });
    const t0 = Date.now(); await pg.goto(base + '/', { waitUntil: 'domcontentloaded' });
    await pg.waitForFunction(() => !document.getElementById('intro'), null, { timeout: 6000 }).catch(() => {});
    const introGone = Date.now() - t0;
    ok(introGone < 4500, `${vp.n}: intro clears in about 2.5 s (${introGone} ms)`);
    ok(await pg.evaluate(() => document.getElementById('site').getAttribute('dir') === 'rtl'), `${vp.n}: opens in Arabic`);
    const over = await pg.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    ok(over <= 1, `${vp.n}: no sideways scroll (${over}px)`);
    const wa = await pg.evaluate(() => [...document.querySelectorAll('a[href*="wa.me"]')].every(a => /wa\.me\/971563469000/.test(a.href)));
    ok(wa, `${vp.n}: every WhatsApp link goes to 056 346 9000`);
    await pg.close();
  }
  { const pg = await b.newPage({ viewport: { width: 390, height: 844 } }); await pg.goto(base + '/start'); await pg.waitForTimeout(300);
    const over = await pg.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth); ok(over <= 1, 'start page: no sideways scroll on phone (' + over + 'px)');
    ok(await pg.evaluate(() => document.dir === 'rtl' || document.documentElement.dir === 'rtl'), 'start page: Arabic right-to-left'); await pg.close(); }

  const TOOLS = ['track', 'renew', 'book', 'check', 'e-invoicing', 'company-setup-ajman', 'company-setup-sharjah', 'company-setup-dubai', 'zh'];
  for (const t of TOOLS) { const pg = await b.newPage({ viewport: { width: 390, height: 844 } }); const errs = []; pg.on('pageerror', e => errs.push(e.message));
    await pg.goto(base + '/' + t); await pg.waitForTimeout(250);
    const over = await pg.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth); ok(over <= 1, t + ': no sideways scroll on phone (' + over + 'px)');
    ok(errs.length === 0, t + ': no script errors ' + errs.join(' | '));
    const src = fs.readFileSync(path.join(root, t + '.html'), 'utf8');
    ok(/class="tool"/.test(src) && /law-line/.test(src), t + ': watermark layer + UAE laws line');
    ok(!/إقامتك بإسمك|من غير كفيل|إقامة مستثمر (لمدة )?سنتين/.test(src), t + ': no residency-selling wording');
    if (t !== 'zh') ok(await pg.evaluate(() => document.getElementById('site').getAttribute('dir') === 'rtl'), t + ': opens in Arabic');
    await pg.close(); }
  { const pg = await b.newPage({ viewport: { width: 390, height: 844 } }); await pg.goto(base + '/track');
    await pg.fill('#tCode', 'HBC-1234-TEST'); await pg.click('#tBtn'); await pg.waitForSelector('#tOut:not([hidden]) .tl');
    ok(await pg.evaluate(() => document.querySelectorAll('#tOut .tl li.done').length === 2 && !!document.querySelector('#tOut .tl li.now')), 'track: known code shows step 3 of 5');
    await pg.fill('#tCode', 'HBC-0000-NONE'); await pg.click('#tBtn'); await pg.waitForTimeout(300);
    ok(await pg.evaluate(() => !document.querySelector('#tOut .tl')), 'track: unknown code shows not found'); await pg.close(); }
  { const pg = await b.newPage(); await pg.goto(base + '/renew'); await pg.click('#rBtn'); ok(await pg.isVisible('#rErr'), 'renew: empty form shows an error');
    await pg.fill('input[name=name]', 'Test'); await pg.fill('input[name=phone]', '0501234567'); await pg.fill('input[name=lic]', '2027-03-01');
    const dl = pg.waitForEvent('download', { timeout: 4000 }).catch(() => null); await pg.click('#rBtn'); const d = await dl;
    ok(!!d && /\.ics$/.test(d.suggestedFilename()) && await pg.isVisible('#rOk'), 'renew: valid form gives a calendar file and success box'); await pg.close(); }
  { const pg = await b.newPage(); await pg.goto(base + '/book'); ok(await pg.evaluate(() => document.querySelectorAll('#bkDay option').length === 12 && ![...document.querySelectorAll('#bkDay option')].some(o => new Date(o.value).getDay() === 0)), 'book: 12 days offered, no Sundays');
    await pg.fill('input[name=name]', 'Test'); await pg.fill('input[name=phone]', '0501234567'); await pg.click('#bBtn'); await pg.waitForSelector('#bOk:not([hidden])');
    ok(/wa\.me\/971563469000/.test(await pg.getAttribute('#bWa', 'href')), 'book: confirm-on-WhatsApp link after request'); await pg.close(); }
  { const pg = await b.newPage(); await pg.goto(base + '/check'); const names = await pg.evaluate(() => [...new Set([...document.querySelectorAll('#qForm input[type=radio]')].map(i => i.name))]);
    for (const n of names) await pg.check(`#qForm input[name=${n}][value=${n === 'bank' ? 'no' : 'yes'}]`);
    await pg.click('#qForm button[type=submit]'); await pg.waitForSelector('#qRes:not([hidden])');
    ok(names.length === 8 && /88%/.test(await pg.textContent('#qRes .ring')), 'check: 7 of 8 yes gives 88%'); await pg.close(); }
  { const pg = await b.newPage(); await pg.goto(base + '/e-invoicing'); ok(await pg.evaluate(() => document.getElementById('clist').classList.contains('blur')), 'e-invoicing: checklist locked at first');
    await pg.fill('#gForm input[name=name]', 'Test'); await pg.fill('#gForm input[name=phone]', '0501234567'); await pg.click('#gForm button'); await pg.waitForTimeout(200);
    ok(await pg.evaluate(() => !document.getElementById('clist').classList.contains('blur')), 'e-invoicing: checklist opens after details'); await pg.close(); }
  await b.close(); srv.close();
  console.log(fails.length ? `\n${fails.length} failing` : '\nall passing'); process.exit(fails.length ? 1 : 0);
})();
