"""Split the long homepage into an 8-section home plus three pages that keep every moved section.
Run from the repo root: python3 tools/redesign/split_home.py <original index.html>
Nothing is deleted: each section removed from the home lands verbatim on its page."""
import re, sys

SRC = open(sys.argv[1], encoding='utf-8').read()
# scripts must not stop when a page does not carry a section
SRC = SRC.replace("    var ids = ['c-cost', 'c-ship', 'c-comm', 'c-target'];\n", "    var ids = ['c-cost', 'c-ship', 'c-comm', 'c-target'];\n    if (!document.getElementById('c-cost')) return;\n", 1)
SRC = SRC.replace("document.getElementById('calcCta').addEventListener('click', function () { document.getElementById('f-service').value", "document.getElementById('calcCta').addEventListener('click', function () { var fs = document.getElementById('f-service'); if (fs) fs.value", 1)

SEC = re.compile(r'\n  <section class="block[^"]*" id="([a-z-]+)"[^>]*>.*?\n  </section>', re.S)
sections = {m.group(1): m.group(0) for m in SEC.finditer(SRC)}

PAGES = {
    'visas': dict(ids=['visas'],
        en=('Residency application help', 'We help you prepare and submit residency applications. The competent authority makes the decision.'),
        ar=('المساعدة في معاملات الإقامة', 'بنساعدك تجهّز طلب الإقامة وتقدّمه، والقرار للجهة المختصة.'),
        title='Residency Application Help in the UAE | El Harmawy Business Consultancy'),
    'solutions': dict(ids=['dubai-etrader', 'solutions', 'offers', 'calculator'],
        en=('Licences and growth solutions', 'Dubai e-Trader and Abu Dhabi freelance licences, ways to grow your trade, and the Amazon and Noon profit calculator.'),
        ar=('رخص وحلول لنمو تجارتك', 'رخصة التاجر الإلكتروني في دبي ورخصة أبوظبي للمهن الحرة، وطرق لنمو تجارتك، وحاسبة أرباح أمازون ونون.'),
        title='e-Trader Licence, Growth Solutions & Amazon Calculator | El Harmawy'),
    'how-we-work': dict(ids=['process', 'videos', 'ask-demo', 'tools', 'guides'],
        en=('How we work', 'From the first call to finished work: our steps, short videos, free tools and guides.'),
        ar=('طريقة شغلنا', 'من أول مكالمة لحد تسليم الشغل: خطواتنا، وفيديوهات قصيرة، وأدوات وأدلة مجانية.'),
        title='How We Work, Videos, Tools & Guides | El Harmawy Business Consultancy'),
}
def cut_div(html, div_id):
    a = html.index(f'<div class="gds reveal" id="{div_id}">')
    depth, i = 0, a
    for m in re.finditer(r'<(/?)div\b', html[a:]):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            e = a + m.end() + html[a + m.end():].index('>') + 1
            return html[:a] + html[e:], html[a:e]
    raise ValueError(div_id)


sections['packages'], _gds = cut_div(sections['packages'], 'service-guides')
sections['service-guides-sec'] = ('\n  <section class="block" id="service-guides-sec">\n    <div class="wrap">\n      ' + _gds + '\n    </div>\n  </section>')
PAGES['how-we-work']['ids'].insert(4, 'service-guides-sec')
MOVED = {i: p for p, d in PAGES.items() for i in d['ids']}
HOME_IDS = ['services', 'how-to-start', 'setup-cost', 'packages', 'about', 'faq', 'register', 'contact']
for i in list(MOVED) + HOME_IDS:
    assert i in sections, i

EYEBROW = re.compile(r'\n\s*<div class="eyebrow">.*?</div>')

HERO = '''  <section class="hero hero-v2" data-enter>
    <div class="wrap">
      <div class="h-copy">
        <h1><span data-l="ar">نأسّس شركتك في الإمارات، وإنت مركّز في شغلك</span><span data-l="en">Your UAE company, set up while you run your business</span></h1>
        <p class="h-slogan" dir="ltr" lang="en">We Handle It, <em>You Grow.</em></p>
        <p class="lead"><span data-l="ar">تأسيس الشركة في المنطقة الحرة أو البر الرئيسي، والمساعدة في فتح الحساب البنكي، والمحاسبة، والمعاملات الحكومية. وبنبعتلك عرض سعر مكتوب قبل ما نبدأ أي شغل.</span><span data-l="en">Free zone or mainland formation, corporate bank account help, accounting and government transactions. You get a written quote before any work starts.</span></p>
        <div class="cta-row">
          <a class="btn btn-wa" href="https://wa.me/971563469000?text=%D8%A7%D9%84%D8%B3%D9%84%D8%A7%D9%85%20%D8%B9%D9%84%D9%8A%D9%83%D9%85%D8%8C%20%D8%B9%D8%A7%D9%8A%D8%B2%20%D8%A3%D8%A3%D8%B3%D8%B3%20%D8%B4%D8%B1%D9%83%D8%A9%20%D9%81%D9%8A%20%D8%A7%D9%84%D8%A5%D9%85%D8%A7%D8%B1%D8%A7%D8%AA." target="_blank" rel="noopener">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l2.1-5.4A8.4 8.4 0 1 1 21 11.5z"/></svg>
            <span data-l="ar">راسلنا واتساب</span><span data-l="en">Message us on WhatsApp</span></a>
          <a class="btn btn-line" href="#setup-cost"><span data-l="ar">احسب تكلفة التأسيس</span><span data-l="en">Calculate your setup cost</span></a>
        </div>
        <ul class="h-facts">
          <li><b dir="ltr">2013</b><span data-l="ar">بداية خبرتنا في الإمارات</span><span data-l="en">Working in the UAE since</span></li>
          <li><b>58667</b><span data-l="ar">رخصة هيئة المناطق الحرة في عجمان</span><span data-l="en">Ajman Free Zones Authority licence</span></li>
          <li><b dir="ltr">1,000</b><span data-l="ar">درهم للحساب البنكي، تدفعها بعد موافقة البنك</span><span data-l="en">AED for bank account help, paid after approval</span></li>
        </ul>
      </div>
      <figure class="h-chat" aria-label="WhatsApp">
        <div class="hc-top"><img src="favicon.png" alt="" width="36" height="36"><div><b>El Harmawy HBC <svg class="tick" viewBox="0 0 24 24" width="15" height="15" aria-hidden="true"><path fill="#1DA1F2" d="M12 1.5l2.6 1.9 3.2-.1 1 3 2.6 1.9-1 3.1 1 3.1-2.6 1.9-1 3-3.2-.1L12 22.5l-2.6-1.9-3.2.1-1-3-2.6-1.9 1-3.1-1-3.1 2.6-1.9 1-3 3.2.1z"/><path d="m8 12.2 2.6 2.6L16.2 9" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></b><small><span data-l="ar">متصل الآن</span><span data-l="en">online</span></small></div></div>
        <div class="hc-body">
          <p class="m out" style="--d:.25s"><span data-l="ar">السلام عليكم، عايز أأسس شركة تجارة عامة. أبدأ منين؟</span><span data-l="en">Hello, I want to set up a general trading company. Where do I start?</span><time dir="ltr">10:02 <i class="seen">✓✓</i></time></p>
          <p class="m in" style="--d:.9s"><span data-l="ar">وعليكم السلام، أهلاً بيك. هنختار معاك النشاط والمكان المناسب، ونبعتلك عرض سعر مكتوب بالتكلفة كاملة قبل أي خطوة.</span><span data-l="en">Welcome. We choose the activity and the right location with you, then send a written quote with the full cost before any step.</span><time dir="ltr">10:04</time></p>
          <div class="m in card" style="--d:1.6s">
            <ol>
              <li class="ok"><span data-l="ar">اختيار النشاط والمنطقة</span><span data-l="en">Activity and location</span></li>
              <li class="ok"><span data-l="ar">الرخصة والعقد</span><span data-l="en">Licence and contract</span></li>
              <li class="now"><span data-l="ar">الحساب البنكي للشركة</span><span data-l="en">Corporate bank account</span></li>
            </ol>
            <time dir="ltr">10:05</time>
          </div>
        </div>
      </figure>
    </div>
  </section>
'''


def page_head(p):
    d = PAGES[p]
    return f'''  <section class="page-head" data-enter>
    <div class="wrap">
      <h1><span data-l="ar">{d['ar'][0]}</span><span data-l="en">{d['en'][0]}</span></h1>
      <p><span data-l="ar">{d['ar'][1]}</span><span data-l="en">{d['en'][1]}</span></p>
      <p class="law-u"><span data-l="ar">جميع الخدمات تخضع لقوانين وأنظمة دولة الإمارات العربية المتحدة وقرار الجهة المختصة.</span><span data-l="en">All services are subject to UAE laws and regulations and the decision of the competent authority.</span></p>
      <div class="cta-row"><a class="btn btn-wa" href="https://wa.me/971563469000" target="_blank" rel="noopener"><span data-l="ar">راسلنا واتساب</span><span data-l="en">Message us on WhatsApp</span></a><a class="btn btn-line" href="/"><span data-l="ar">الصفحة الرئيسية</span><span data-l="en">Home page</span></a></div>
    </div>
  </section>
'''


NAV = '''    <nav class="nav" aria-label="Main">
      <a href="{h}#services"><span data-l="en">Services</span><span data-l="ar">خدماتنا</span></a>
      <a href="{h}#setup-cost"><span data-l="en">Setup cost</span><span data-l="ar">تكلفة التأسيس</span></a>
      <a href="{h}#packages"><span data-l="en">Packages</span><span data-l="ar">الباقات</span></a>
      <a href="visas"><span data-l="en">Residency help</span><span data-l="ar">معاملات الإقامة</span></a>
      <a href="solutions"><span data-l="en">Solutions</span><span data-l="ar">حلولنا</span></a>
      <a href="{h}#faq"><span data-l="en">FAQ</span><span data-l="ar">الأسئلة</span></a>
      <a href="{h}#contact"><span data-l="en">Contact</span><span data-l="ar">تواصل معنا</span></a>
      <details class="nav-more"><summary><span data-l="en">More</span><span data-l="ar">المزيد</span></summary><div class="nav-more-list"><a data-more href="how-we-work"><span data-l="en">How we work</span><span data-l="ar">طريقة شغلنا</span></a><a data-more href="how-we-work#videos"><span data-l="en">Videos</span><span data-l="ar">فيديوهات</span></a><a data-more href="{h}#about"><span data-l="en">About</span><span data-l="ar">من نحن</span></a><a data-more href="guides/"><span data-l="en">Guides</span><span data-l="ar">أدلة</span></a><a data-more href="pay"><span data-l="en">Pay</span><span data-l="ar">الدفع والتحويل</span></a><a data-more href="track"><span data-l="en">Track your file</span><span data-l="ar">تابع معاملتك</span></a></div></details>
    </nav>'''

NAV_RE = re.compile(r'    <nav class="nav" aria-label="Main">.*?\n    </nav>', re.S)
assert NAV_RE.search(SRC)
MAIN_RE = re.compile(r'(<main id="home">\n)(.*?)(\n</main>)', re.S)


ID_PAGE = {}
for _sid, _pg in MOVED.items():
    for _x in re.findall(r'id="([A-Za-z][\w-]*)"', sections[_sid]):
        ID_PAGE[_x] = _pg


def fix_links(html, here_ids, home):
    here_ids = set(here_ids) | set(re.findall(r'id="([A-Za-z][\w-]*)"', html))
    def rep(m):
        i = m.group(1)
        if i in here_ids or i in ('home', 'top'):
            return m.group(0)
        if i in ID_PAGE:
            return f'href="{ID_PAGE[i]}#{i}"'
        return f'href="/#{i}"' if not home else m.group(0)
    return re.sub(r'href="#([A-Za-z][\w-]*)"', rep, html)


def build(main_html, here_ids, home, page=None):
    h = SRC
    h = NAV_RE.sub(lambda m: NAV.format(h='' if home else '/'), h, count=1)
    h = MAIN_RE.sub(lambda m: m.group(1) + main_html + m.group(3), h, count=1)
    h = EYEBROW.sub('', h.replace(main_html, main_html)) if False else h
    # eyebrows (kicker labels) out of every section on these pages
    a, b = h.index('<main id="home">'), h.index('</main>')
    h = h[:a] + EYEBROW.sub('', h[a:b]) + h[b:]
    h = fix_links(h, set(here_ids) | {'aiBox'}, home)
    h = h.replace('<main id="home">', '<main id="home" class="wm">', 1)  # site watermark on the new design
    if not home:
        d = PAGES[page]
        h = h.replace('<a class="brand" href="#home"', '<a class="brand" href="/"')
        h = re.sub(r'<div class="intro" id="intro".*?\n</div>\n', '', h, count=1, flags=re.S)
        h = re.sub(r'<title>.*?</title>', f'<title>{d["title"].replace("&", "&amp;")}</title>', h, count=1)
        url = f'https://elharmawy.com/{page}'
        h = h.replace('<link rel="canonical" href="https://elharmawy.com/">', f'<link rel="canonical" href="{url}">')
        h = h.replace('<meta property="og:url" content="https://elharmawy.com/">', f'<meta property="og:url" content="{url}">')
        h = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="https://elharmawy\.com/[^"]*">\n', '', h)
        h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{d["title"].replace("&", "&amp;")}">', h, count=1)
        h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{d["en"][1]}">', h, count=1)
        h = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "FAQPage".*?</script>\n?', '', h, count=1, flags=re.S)
    return h


# home: hero + 8 sections; contact folded into the register section
contact_inner = re.search(r'<div class="cgrid">.*?\n      </div>', sections['contact'], re.S).group(0)
register = sections['register']
register = register[:register.rindex('\n  </section>')] + '\n    <div class="wrap contact-in" id="contact">\n      <h3><span data-l="ar">أو كلّمنا مباشرة</span><span data-l="en">Or reach us directly</span></h3>\n      ' + contact_inner + '\n    </div>\n  </section>'
home_main = HERO + ''.join(sections[i] if i != 'register' else register for i in HOME_IDS if i != 'contact')
home = build(home_main, HOME_IDS, True)
open('index.html', 'w', encoding='utf-8').write(home.replace('site.css?v=20261114d', 'site.css?v=20261120a'))

for p, d in PAGES.items():
    # every page ends with the same quote form and contacts, so its buttons stay on the page
    main = page_head(p) + ''.join(sections[i] for i in d['ids']) + register
    open(p + '.html', 'w', encoding='utf-8').write(build(main, d['ids'] + ['register', 'contact'], False, p).replace('site.css?v=20261114d', 'site.css?v=20261120a'))

print('home sections:', len(re.findall(r'<section class="block', home)), 'size', len(home))
for p in PAGES:
    print(p, len(open(p + '.html').read()))
