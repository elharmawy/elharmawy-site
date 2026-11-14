/* HBC: the website assistant, played as a live demo on the home page.
   Built on HTMLDemo (vendor/hd.js). Every state is worked out from t. */
(function () {
  var el = document.getElementById('askDemo');
  if (!el || !window.HTMLDemo) return;
  var D = window.HTMLDemo, ease = D.ease, typed = D.typed, glide = D.glide, held = D.held;
  var site = document.getElementById('site');

  var TXT = {
    ar: {
      tab: 'elharmawy.com', label: 'عرض مساعد الهرماوي',
      steps: ['اختار المساعد', 'اسأل', 'الرد', 'كلّم فريقنا'],
      head: 'زتونة', sub: 'مساعد ذكي · والفريق يتابع معاك على واتساب',
      pick: 'أهلاً بيك في الهرماوي 👋 تحب تكلّم مين؟', z: 'زتونة', l: 'ليليا',
      hi: 'أهلاً، أنا زتونة! 😄 اسألني أي حاجة عن تأسيس شركتك أو إدارتها في الإمارات.',
      chips: ['ابدأ شركة', 'حساب بنكي للشركة', 'المحاسبة والضرائب', 'المعاملات الحكومية', 'كلّم فريقنا'],
      ph: 'اكتب سؤالك…', q: 'تصريح العمل لسنتين بكام؟',
      a: 'رسم إصدار تصريح العمل لسنتين بيتحدد حسب فئة منشأتك في وزارة الموارد البشرية:\n• الفئة الأولى: 250 درهم\n• الفئة التانية: 1,200 درهم\n• الفئة التالتة: 3,450 درهم\nدي رسوم الوزارة بالهوية الرقمية، ولو عن طريق مركز تسهيل بيتضاف 83 درهم. وأتعابنا بعرض سعر مكتوب.',
      lead: 'سيب اسمك ورقمك هنا، وفريقنا هيتواصل معاك بعرض سعر مكتوب:',
      n: 'الاسم', p: 'رقم الموبايل / واتساب', send: 'ابعت طلبي', wa: 'كمّل على واتساب',
      foot: 'المساعد ممكن يغلط. الأسعار والمتطلبات بيأكدها فريقنا.'
    },
    en: {
      tab: 'elharmawy.com', label: 'El Harmawy assistant demo',
      steps: ['Pick', 'Ask', 'Answer', 'Our team'],
      head: 'Zatouna', sub: 'AI assistant · our team follows up on WhatsApp',
      pick: 'Welcome to El Harmawy 👋 Who would you like to talk to?', z: 'Zatouna', l: 'Lilia',
      hi: "Hi, I'm Zatouna! 😄 Ask me anything about starting or running your company in the UAE.",
      chips: ['Start a Company', 'Open a Corporate Bank Account', 'Accounting & Tax Services', 'Government Services', 'Speak to Our Team'],
      ph: 'Type your question…', q: 'How much is a 2-year work permit?',
      a: "The MOHRE fee to issue a 2-year work permit depends on your establishment's category:\n• Category 1: AED 250\n• Category 2: AED 1,200\n• Category 3: AED 3,450\nThese are ministry fees with the digital ID; through a Tasheel centre AED 83 is added. Our fee comes in a written quote.",
      lead: 'Leave your name and mobile here and our team will send you a written quote:',
      n: 'Your name', p: 'Mobile / WhatsApp', send: 'Send my request', wa: 'Continue on WhatsApp',
      foot: 'AI can make mistakes. Prices and requirements are confirmed by our team.'
    }
  };

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function build(lang) {
    var T = TXT[lang], rtl = lang === 'ar';
    var X = function (x) { return rtl ? 1200 - x : x; }; // mirror pointer for RTL
    // where an element sits on the 1200 x 750 stage (aim 55% across, 60% down)
    var aim = function ($, sel, fx, fy) {
      var st = $('.ad').getBoundingClientRect(), b = $(sel).getBoundingClientRect(), k = st.width / 1200 || 1;
      return [(b.left - st.left + b.width * (fx || 0.55)) / k, (b.top - st.top + b.height * (fy || 0.6)) / k];
    };
    var shell = function (log) {
      return '<div class="ad" dir="' + (rtl ? 'rtl' : 'ltr') + '">' +
        '<header class="ad-head"><img src="img/ai/zatouna.jpg" alt=""><div><b>' + esc(T.head) + '</b><small>' + esc(T.sub) + '</small></div></header>' +
        '<div class="ad-log">' + log + '</div>' +
        '<div class="ad-form"><div class="ad-in"><span class="ad-q"></span><i class="ad-caret"></i><span class="ad-ph">' + esc(T.ph) + '</span></div><span class="ad-send">➤</span></div>' +
        '<p class="ad-foot">' + esc(T.foot) + '</p></div>';
    };
    var chips = '<div class="ad-chips">' + T.chips.map(function (c, i) { return '<span' + (i === 4 ? ' class="wa"' : '') + '>' + esc(c) + '</span>'; }).join('') + '</div>';
    var hi = '<div class="ad-msg bot">' + esc(T.hi) + '</div>';
    // pointer targets in LTR stage coordinates (mirrored for RTL)
    var IN = [520, 668], SEND = [1110, 668], ZAT = [500, 330];

    // 1: pick Zatouna
    var P_CLICK = 2.6, zc = null;
    var s1 = {
      id: 'pick', name: T.steps[0], dur: 5.2,
      html: shell('<div class="ad-pick"><p>' + esc(T.pick) + '</p><div class="ad-pick-row">' +
        '<span class="z"><img src="img/ai/zatouna.jpg" alt=""><b>' + esc(T.z) + '</b></span><span><img src="img/ai/lilia.jpg" alt=""><b>' + esc(T.l) + '</b></span></div></div>' +
        '<div class="ad-after">' + hi + chips + '</div>'),
      draw: function (t, $) {
        var on = t >= P_CLICK + 0.1;
        $('.ad-pick').style.display = on ? 'none' : '';
        var a = $('.ad-after'); a.style.display = on ? '' : 'none'; a.style.opacity = ease(t, P_CLICK + 0.1, P_CLICK + 0.6);
        $('.ad-pick .z').classList.toggle('hov', t > P_CLICK - 0.5 && !on);
        $('.ad-form').style.opacity = on ? 1 : 0.35;
        if (!on) zc = aim($, '.ad-pick .z');
        var z = zc || [X(ZAT[0]), ZAT[1]];
        var g = glide(t, [[0, 0, X(900), 620], [0.9, P_CLICK - 0.45, z[0], z[1]], [P_CLICK + 0.6, P_CLICK + 1.6, X(980), 560]], [P_CLICK]);
        return { cursor: { x: g.x, y: g.y, press: g.press } };
      }
    };

    // 2: type the question and send
    var FOCUS = 1.0, T_FROM = 1.3, T_TO = 3.4, SEND_AT = 4.1;
    var s2 = {
      id: 'ask', name: T.steps[1], dur: 5.4,
      html: shell(hi + chips + '<div class="ad-msg me"></div>'),
      draw: function (t, $) {
        var sent = t >= SEND_AT + 0.08;
        var q = sent ? '' : typed(T.q, t, T_FROM, T_TO);
        $('.ad-q').textContent = q;
        $('.ad-ph').style.display = q || (t >= FOCUS && !sent) ? 'none' : '';
        $('.ad-caret').style.display = t >= FOCUS && !sent ? 'block' : 'none';
        $('.ad-in').classList.toggle('focus', t >= FOCUS && !sent);
        $('.ad-send').classList.toggle('press', held(t, SEND_AT));
        var me = $('.ad-msg.me'); me.textContent = T.q; me.style.display = sent ? '' : 'none';
        $('.ad-chips').style.display = sent ? 'none' : '';
        var g = glide(t, [[0, 0, 980, 560], [0.2, FOCUS - 0.15, IN[0], IN[1]], [T_TO + 0.05, SEND_AT - 0.4, SEND[0], SEND[1]], [SEND_AT + 0.4, SEND_AT + 1.2, 1000, 520]], [FOCUS, SEND_AT]);
        return { cursor: { x: X(g.x), y: g.y, press: g.press } };
      }
    };

    // 3: the answer
    var WAIT_TO = 1.5, A_FROM = 1.6, A_TO = 5.6;
    var s3 = {
      id: 'answer', name: T.steps[2], dur: 7.6,
      html: shell(hi + '<div class="ad-msg me">' + esc(T.q) + '</div><div class="ad-msg bot wait">•••</div><div class="ad-msg bot ans"></div>'),
      draw: function (t, $) {
        $('.ad-msg.wait').style.display = t < WAIT_TO ? '' : 'none';
        var a = $('.ad-msg.ans'); a.style.display = t >= WAIT_TO ? '' : 'none';
        a.textContent = typed(T.a, t, A_FROM, A_TO);
        $('.ad-ph').style.display = '';
        return null;
      }
    };

    // 4: hand over to the team
    var L_IN = 0.4, HOVER = 2.4;
    var s4 = {
      id: 'team', name: T.steps[3], dur: 5.4,
      html: shell('<div class="ad-msg me">' + esc(T.q) + '</div><div class="ad-msg bot">' + esc(T.a) + '</div>' +
        '<div class="ad-lead"><p>' + esc(T.lead) + '</p><div class="ad-f">' + esc(T.n) + '</div><div class="ad-f" dir="ltr">' + esc(T.p) + '</div>' +
        '<div class="ad-btns"><span class="ad-gold">' + esc(T.send) + '</span><span class="ad-wa">' + esc(T.wa) + '</span></div></div>'),
      draw: function (t, $) {
        var l = $('.ad-lead'); l.style.opacity = ease(t, L_IN, L_IN + 0.6); l.style.transform = 'translateY(' + (1 - ease(t, L_IN, L_IN + 0.6)) * 18 + 'px)';
        $('.ad-wa').classList.toggle('hov', t >= HOVER);
        $('.ad-ph').style.display = '';
        var w = aim($, '.ad-wa');
        var g = glide(t, [[0, 0, X(1000), 520], [1.4, HOVER - 0.1, w[0], w[1]]], []);
        return { cursor: { x: g.x, y: g.y } };
      }
    };
    return { steps: [s1, s2, s3, s4], tabs: [T.tab], label: T.label };
  }

  var ctl = null, cur = '';
  function mount() {
    var lang = site && site.getAttribute('dir') === 'rtl' ? 'ar' : 'en';
    if (lang === cur) return;
    cur = lang;
    if (ctl) ctl.destroy();
    var b = build(lang);
    ctl = D.mount(el, { steps: b.steps, tabs: b.tabs, label: b.label, stageClass: 'ad-stage' });
    el.hbcDemo = ctl;
  }
  mount();
  if (site) new MutationObserver(mount).observe(site, { attributes: true, attributeFilter: ['dir'] });
})();
