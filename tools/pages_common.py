"""Shared shell for the client tools and local pages. Pages are built by tools/build_pages.py."""
import json, html as H

SITE = 'https://elharmawy.com'
WA = '+971 56 346 9000'


def B(en, ar, tag='span'):
    return f'<{tag} data-l="en">{en}</{tag}><{tag} data-l="ar">{ar}</{tag}>'


def P(en, ar):
    return f'<p data-l="en">{en}</p><p data-l="ar">{ar}</p>'


LAW = ('<p class="law-line">' + B('Prices and any approvals are subject to the laws of the United Arab Emirates and the decision of the competent authority.',
                                   'الأسعار وأي موافقات تخضع لقوانين دولة الإمارات العربية المتحدة وقرار الجهة المختصة.') + '</p>')


def nav():
    links = [('./', 'Home', 'الرئيسية'), ('start', 'Company setup', 'تأسيس الشركات'), ('track', 'Track your file', 'تابع معاملتك'),
             ('book', 'Book a consultation', 'احجز استشارة'), ('guides/', 'Guides', 'أدلة')]
    return ''.join(f'<a href="{h}">{B(e, a)}</a>' for h, e, a in links)


def footer():
    tools = [('track', 'Track your file', 'تابع معاملتك'), ('renew', 'Renewal reminder', 'فكّرني بالتجديد'), ('book', 'Book a consultation', 'احجز استشارة'),
             ('check', 'Company health check', 'شركتك سليمة؟'), ('e-invoicing', 'E-invoicing guide', 'دليل الفوترة الإلكترونية')]
    local = [('company-setup-ajman', 'Company setup in Ajman', 'تأسيس شركة في عجمان'), ('company-setup-sharjah', 'Company setup in Sharjah', 'تأسيس شركة في الشارقة'),
             ('company-setup-dubai', 'Company setup in Dubai', 'تأسيس شركة في دبي'), ('zh', '中文', '中文')]
    li = lambda xs: ''.join(f'<li><a href="{h}">{B(e, a)}</a></li>' for h, e, a in xs)
    return f'''<footer class="legal"><div class="wrap">
  <div class="fcols">
    <div><h3>{B('Client tools', 'أدوات العملاء')}</h3><ul>{li(tools)}</ul></div>
    <div><h3>{B('Company setup', 'تأسيس الشركات')}</h3><ul>{li(local)}</ul></div>
    <div><h3>{B('Contact', 'تواصل معنا')}</h3><ul><li dir="ltr"><a href="https://wa.me/971563469000" target="_blank" rel="noopener">WhatsApp {WA}</a></li><li><a href="mailto:info@elharmawy.com">info@elharmawy.com</a></li><li><a href="pay">{B('Bank transfer details', 'بيانات التحويل البنكي')}</a></li></ul></div>
  </div>
  <p>EL HARMAWY BUSINESS CONSULTANCY - F.Z.E · {B('Ajman Free Zone, UAE', 'منطقة عجمان الحرة، الإمارات')} · <a href="privacy.html">{B('Privacy Policy', 'سياسة الخصوصية')}</a> · <a href="terms.html">{B('Terms', 'الشروط')}</a></p>
</div></footer>'''


def page(slug, title_en, title_ar, desc, body, *, schema=None, script='', page_id=None, desc_ar=None, fixed=None, extra_head=''):
    canon = f'{SITE}/{slug}'
    sch = ''.join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in (schema or []))
    start_dir, start_lang = ('rtl', 'ar') if fixed != 'zh' else ('ltr', 'zh')
    fixed_attr = ' data-fixed="1"' if fixed else ''
    lang_btn = '' if fixed else f'<button class="lang" id="langBtn" type="button" aria-label="Switch language">{B("العربية", "English")}</button>'
    nav_html = '' if fixed else f'<nav class="nav" aria-label="Main">{nav()}</nav>'
    title = H.escape(title_ar + ' | الهرماوي لاستشارات الأعمال') if fixed != 'zh' else H.escape(title_en)
    return f'''<!doctype html>
<html lang="{start_lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{H.escape(desc_ar or desc)}">
<link rel="canonical" href="{canon}">
<link rel="icon" href="favicon.png">
<meta name="theme-color" content="#011F43">
<meta property="og:type" content="website"><meta property="og:title" content="{H.escape(title_ar if fixed != 'zh' else title_en)}"><meta property="og:description" content="{H.escape(desc_ar or desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{SITE}/og-image.png">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-M1BHSYLT4R"></script>
<script src="track.js?v=20261112"></script>
{sch}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@600;700;800&family=Red+Hat+Text:wght@400;500;600&family=Tajawal:wght@400;500;700;800&display=swap">
<link rel="stylesheet" href="site.css?v=20261112b">
<link rel="stylesheet" href="tools.css?v=20261112b">
{extra_head}
</head>
<body data-page="{page_id or slug}">
<div class="site" id="site" dir="{start_dir}" lang="{start_lang}"{fixed_attr}>
<header class="top"><div class="wrap">
  <a class="brand" href="./" aria-label="El Harmawy Business Consultancy"><img src="logo.png" alt="El Harmawy Business Consultancy F.Z.E"></a>
  {nav_html}
  {lang_btn}
</div></header>
<main class="tool"><div class="wrap">
{body}
</div></main>
{footer() if not fixed else ''}
</div>
<script src="tools.js?v=20261112a"></script>
{f"<script>{script}</script>" if script else ''}
</body>
</html>
'''


def faq_schema(qas):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qas]}


def faq_html(qas_bi):
    return '<div class="faq2">' + ''.join(f'<details><summary>{B(qe, qa)}</summary>{P(ae, aa)}</details>' for qe, qa, ae, aa in qas_bi) + '</div>'


def wa_btn(text_en, text_ar, msg, cls='btn btn-wa'):
    import urllib.parse as u
    return f'<a class="{cls}" href="https://wa.me/971563469000?text={u.quote(msg)}" target="_blank" rel="noopener">{B(text_en, text_ar)}</a>'
