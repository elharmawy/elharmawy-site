/* HBC live demos (HTML Demo engine, vendor/hd.js): the attestation request
   builder and the "Track your file" page, played step by step.
   Every state is worked out from t. Sample data only (no real client). */
(function () {
  var D = window.HTMLDemo; if (!D) return;
  var ease = D.ease, typed = D.typed, glide = D.glide, held = D.held;
  var site = document.getElementById('site');
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function aim($, sel, fx, fy) {
    var st = $('.lv').getBoundingClientRect(), b = $(sel).getBoundingClientRect(), k = st.width / 1200 || 1;
    return [(b.left - st.left + b.width * (fx || 0.55)) / k, (b.top - st.top + b.height * (fy || 0.6)) / k];
  }
  function shell(ar, title, sub, body) {
    return '<div class="lv" dir="' + (ar ? 'rtl' : 'ltr') + '"><header class="lv-top"><b>El Harmawy</b><span>' + esc(title) + '</span></header>' +
      '<div class="lv-body"><h3>' + esc(title) + '</h3><p class="lv-sub">' + esc(sub) + '</p>' + body + '</div></div>';
  }

  /* ---------- 1. Attestation & translation request ---------- */
  var AT = {
    ar: { tab: 'elharmawy.com/attestation', label: 'عرض طلب التصديق والترجمة', steps: ['اختار الخدمة', 'الأوراق', 'ابعت', 'تابع'],
      title: 'اطلب تصديق أو ترجمة', sub: 'اختار، وإحنا نبعتلك عرض سعر مكتوب على الواتساب.',
      svc: ['تصديق شهادة', 'ترجمة قانونية', 'الاتنين'], doc: 'نوع المستند', docv: 'شهادة جامعية', country: 'بلد الإصدار', countryv: 'مصر',
      need: 'هتحتاج:', list: ['أصل الشهادة', 'صورة الجواز', 'تصديقات بلد الإصدار وسفارة الإمارات هناك', 'سكان واضح للترجمة'],
      send: 'ابعت الطلب على واتساب', wa: 'السلام عليكم، محتاج تصديق شهادة جامعية صادرة من مصر + ترجمة قانونية.',
      track: 'تابع معاملتك', tsub: 'اكتب كود الملف اللي بعتناه لك على الواتساب، وشوف معاملتك وصلت لفين.', code: 'HBC-2611-AT', tl: ['استلمنا الأوراق', 'جهّزنا الملف', 'اتقدّم للجهة', 'مستني قرار الجهة', 'خلصت'], sample: 'مثال توضيحي' },
    en: { tab: 'elharmawy.com/attestation', label: 'Attestation and translation request demo', steps: ['Choose', 'Documents', 'Send', 'Track'],
      title: 'Request attestation or translation', sub: 'Choose, and we send you a written quote on WhatsApp.',
      svc: ['Certificate attestation', 'Legal translation', 'Both'], doc: 'Document type', docv: 'University degree', country: 'Issued in', countryv: 'Egypt',
      need: 'You will need:', list: ['The original certificate', 'Passport copy', 'Attestations from the issuing country and the UAE embassy there', 'A clear scan for translation'],
      send: 'Send request on WhatsApp', wa: 'Hello, I need a university degree issued in Egypt attested, plus legal translation.',
      track: 'Track your file', tsub: 'Enter the file code we sent you on WhatsApp to see where your transaction stands.', code: 'HBC-2611-AT', tl: ['Documents received', 'File prepared', 'Submitted to the authority', 'Awaiting the authority', 'Completed'], sample: 'Sample' }
  };
  function buildAttest(lang) {
    var T = AT[lang], ar = lang === 'ar';
    var form = '<div class="lv-chips">' + T.svc.map(function (s, i) { return '<span class="c' + i + '">' + esc(s) + '</span>'; }).join('') + '</div>' +
      '<div class="lv-row"><label>' + esc(T.doc) + '<i class="f1"></i></label><label>' + esc(T.country) + '<i class="f2"></i></label></div>';
    var s1 = { id: 'choose', name: T.steps[0], dur: 5.4, html: shell(ar, T.title, T.sub, form),
      draw: function (t, $) {
        var C = 2.0; $('.c2').classList.toggle('on', t >= C + 0.08);
        $('.f1').textContent = t >= 3.0 ? T.docv : ''; $('.f2').textContent = typed(T.countryv, t, 3.6, 4.4);
        var c = aim($, '.c2'), f = aim($, '.f2', .3);
        var g = glide(t, [[0, 0, ar ? 300 : 900, 640], [0.6, C - 0.4, c[0], c[1]], [C + 0.5, 3.4, f[0], f[1]]], [C, 3.4]);
        return { cursor: { x: g.x, y: g.y, press: g.press } };
      } };
    var lst = '<div class="lv-need"><b>' + esc(T.need) + '</b><ul>' + T.list.map(function (x, i) { return '<li class="n' + i + '">' + esc(x) + '</li>'; }).join('') + '</ul></div>';
    var s2 = { id: 'docs', name: T.steps[1], dur: 5.2, html: shell(ar, T.title, T.sub, '<div class="lv-chips"><span class="on">' + esc(T.svc[2]) + '</span></div>' + lst),
      draw: function (t, $) { for (var i = 0; i < 4; i++) { var x = ease(t, 0.5 + i * 0.8, 1.0 + i * 0.8); var li = $('.n' + i); li.style.opacity = x; li.classList.toggle('ok', t > 1.2 + i * 0.8); } return null; } };
    var s3 = { id: 'send', name: T.steps[2], dur: 5.2, html: shell(ar, T.title, T.sub, '<div class="lv-wa"><small>WhatsApp · +971 56 346 9000</small><p class="m"></p></div><span class="lv-btn">' + esc(T.send) + '</span>'),
      draw: function (t, $) {
        var B = 1.2; $('.lv-btn').classList.toggle('press', held(t, B));
        var w = $('.lv-wa'); w.style.opacity = ease(t, B + 0.1, B + 0.5); $('.m').textContent = typed(T.wa, t, B + 0.4, 4.2);
        var b = aim($, '.lv-btn'); var g = glide(t, [[0, 0, ar ? 300 : 900, 640], [0.2, B - 0.3, b[0], b[1]], [B + 0.5, B + 1.4, ar ? 200 : 1000, 700]], [B]);
        return { cursor: { x: g.x, y: g.y, press: g.press } };
      } };
    var tl = '<div class="lv-code">' + esc(T.code) + ' <em>' + esc(T.sample) + '</em></div><ol class="lv-tl">' + T.tl.map(function (x, i) { return '<li class="s' + i + '"><span>' + (i + 1) + '</span>' + esc(x) + '</li>'; }).join('') + '</ol>';
    var s4 = { id: 'track', name: T.steps[3], dur: 6.0, html: shell(ar, T.track, T.tsub, tl),
      draw: function (t, $) { var now = t < 1.4 ? 1 : t < 2.8 ? 2 : t < 4.2 ? 3 : 4; for (var i = 0; i < 5; i++) { var li = $('.s' + i); li.className = 's' + i + (i < now ? ' done' : i === now ? ' now' : ''); li.querySelector('span').textContent = i < now ? '✓' : (i + 1); } return null; } };
    return { steps: [s1, s2, s3, s4], tabs: [T.tab], label: T.label };
  }

  /* ---------- 2. Track your file ---------- */
  var TR = {
    ar: { tab: 'elharmawy.com/track', label: 'عرض صفحة تابع معاملتك', steps: ['الكود', 'الحالة', 'خلصت'], title: 'تابع معاملتك',
      sub: 'اكتب كود الملف اللي بعتناه لك على الواتساب، وشوف معاملتك وصلت لفين. من غير تسجيل دخول.', lab: 'كود الملف', btn: 'اعرض الحالة',
      code: 'HBC-2611-AT', svc: 'تصديق شهادة + ترجمة قانونية', sample: 'مثال توضيحي', tl: ['استلمنا الأوراق', 'جهّزنا الملف', 'اتقدّم للجهة', 'مستني قرار الجهة', 'خلصت'],
      note: 'ملاحظة من الفريق: الطلب اتقدّم، وهنبلغك أول ما يتصدّق.', done: 'ملاحظة من الفريق: الشهادة جاهزة للاستلام.' },
    en: { tab: 'elharmawy.com/track', label: 'Track your file demo', steps: ['Code', 'Status', 'Completed'], title: 'Track your file',
      sub: 'Enter the file code we sent you on WhatsApp to see where your transaction stands. No login needed.', lab: 'File code', btn: 'Show status',
      code: 'HBC-2611-AT', svc: 'Certificate attestation + legal translation', sample: 'Sample', tl: ['Documents received', 'File prepared', 'Submitted to the authority', 'Awaiting the authority', 'Completed'],
      note: 'Note from our team: submitted, we will tell you as soon as it is attested.', done: 'Note from our team: your certificate is ready to collect.' }
  };
  function buildTrack(lang) {
    var T = TR[lang], ar = lang === 'ar';
    var form = '<div class="lv-form"><label>' + esc(T.lab) + '<div class="lv-in" dir="ltr"><span class="q"></span><i class="car"></i><span class="ph">HBC-0000-XX</span></div></label><span class="lv-btn">' + esc(T.btn) + '</span></div>';
    var res = function (now, note) {
      return '<div class="lv-res"><small>' + esc(T.svc) + ' · <em>' + esc(T.sample) + '</em></small><b class="st">' + esc(T.tl[now]) + '</b><ol class="lv-tl">' +
        T.tl.map(function (x, i) { return '<li class="' + (i < now || (now === 4) ? 'done' : i === now ? 'now' : '') + '"><span>' + (i < now || now === 4 ? '✓' : (i + 1)) + '</span>' + esc(x) + '</li>'; }).join('') + '</ol><p class="nt">' + esc(note) + '</p></div>';
    };
    var F = 0.8, TF = 1.1, TT = 2.8, B = 3.5;
    var s1 = { id: 'code', name: T.steps[0], dur: 5.0, html: shell(ar, T.title, T.sub, form),
      draw: function (t, $) {
        var q = typed(T.code, t, TF, TT); $('.q').textContent = q; $('.ph').style.display = q ? 'none' : ''; $('.car').style.display = t >= F && t < B ? 'block' : 'none';
        $('.lv-in').classList.toggle('focus', t >= F && t < B); $('.lv-btn').classList.toggle('press', held(t, B));
        var i = aim($, '.lv-in', .4), b = aim($, '.lv-btn');
        var g = glide(t, [[0, 0, ar ? 300 : 900, 650], [0.1, F - 0.1, i[0], i[1]], [TT + 0.05, B - 0.35, b[0], b[1]]], [F, B]);
        return { cursor: { x: g.x, y: g.y, press: g.press } };
      } };
    var s2 = { id: 'status', name: T.steps[1], dur: 6.0, html: shell(ar, T.title, T.sub, '<div class="lv-load">•••</div>' + res(2, T.note)),
      draw: function (t, $) { $('.lv-load').style.display = t < 0.9 ? '' : 'none'; var r = $('.lv-res'); r.style.display = t >= 0.9 ? '' : 'none'; r.style.opacity = ease(t, 0.9, 1.4); return null; } };
    var s3 = { id: 'done', name: T.steps[2], dur: 5.0, html: shell(ar, T.title, T.sub, res(4, T.done)),
      draw: function (t, $) { var r = $('.lv-res'); r.style.opacity = ease(t, 0, 0.5); $('.st').style.color = t > 0.6 ? '#1E9E55' : ''; return null; } };
    return { steps: [s1, s2, s3], tabs: [T.tab], label: T.label };
  }

  function mountAll() {
    var lang = site && site.getAttribute('dir') === 'rtl' ? 'ar' : 'en';
    [['attestDemo', buildAttest], ['trackDemo', buildTrack]].forEach(function (p) {
      var el = document.getElementById(p[0]); if (!el || el.dataset.lang === lang) return;
      if (el.hbcDemo) el.hbcDemo.destroy();
      var b = p[1](lang); el.dataset.lang = lang;
      el.hbcDemo = D.mount(el, { steps: b.steps, tabs: b.tabs, label: b.label, stageClass: 'lv-stage' });
    });
  }
  mountAll();
  if (site) new MutationObserver(mountAll).observe(site, { attributes: true, attributeFilter: ['dir'] });
})();
