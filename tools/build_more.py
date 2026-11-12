"""E-invoicing guide (gated checklist), emirate company-setup pages and the Chinese page."""
from pages_common import page, B, P, LAW, faq_schema, faq_html, wa_btn

HONEY = '<p class="hp"><label>Leave empty <input name="company_website" tabindex="-1" autocomplete="off"></label></p>'
SRC_NOTE = B('Sources: Ministry of Finance Ministerial Decisions No. 243 and 244 of 2025 and later amendments, as reported up to October 2026. Dates and fines can change; confirm with the Ministry of Finance or the FTA.',
             'المصادر: قرارا وزارة المالية رقم 243 و244 لسنة 2025 والتعديلات اللي بعدهم، زي ما اتنشرت لحد أكتوبر 2026. المواعيد والغرامات ممكن تتغير، فاتأكد من وزارة المالية أو الهيئة الاتحادية للضرائب.')


def einvoicing():
    rows = [('Pilot & voluntary', 'تجريبي واختياري', 'Invited businesses and volunteers', 'شركات مدعوّة ومن يختار يبدأ بدري', '—', 'From 1 July 2026', 'من 1 يوليو 2026'),
            ('Phase 1', 'المرحلة الأولى', 'Revenue AED 50 million or more', 'إيراد 50 مليون درهم أو أكتر', '30 Oct 2026', '1 January 2027', '1 يناير 2027'),
            ('Phase 2', 'المرحلة التانية', 'Revenue below AED 50 million', 'إيراد أقل من 50 مليون درهم', '31 Mar 2027', '1 July 2027', '1 يوليو 2027'),
            ('Phase 3', 'المرحلة التالتة', 'Government entities', 'الجهات الحكومية', '31 Mar 2027', '1 October 2027', '1 أكتوبر 2027')]
    trs = ''.join(f'<tr><td>{B(a, b)}</td><td>{B(c, d)}</td><td class="n" dir="ltr">{e}</td><td class="n">{B(f, g)}</td></tr>' for a, b, c, d, e, f, g in rows)
    checklist = [
        ('Find your phase: check your revenue in the latest accounting period (above or below AED 50 million).', 'اعرف مرحلتك: بص على إيرادك في آخر فترة محاسبية (فوق ولا تحت 50 مليون درهم).'),
        ('List which of your sales are B2B or B2G. Sales to individuals (B2C) are outside the system for now.', 'حدّد أنهي مبيعاتك لشركات أو لجهات حكومية. البيع للأفراد خارج النظام دلوقتي.'),
        ('Choose an Accredited Service Provider (ASP) from the Ministry of Finance list, and sign before your phase deadline.', 'اختار مزوّد خدمة معتمد من قايمة وزارة المالية، ووقّع معاه قبل ميعاد مرحلتك.'),
        ('Clean your customer data: legal names, TRN and addresses must match official records.', 'نظّف بيانات عملائك: الاسم القانوني والرقم الضريبي والعنوان لازم يطابقوا الأوراق الرسمية.'),
        ('Check your invoicing or accounting software can connect to your ASP.', 'اتأكد إن برنامج الفواتير أو الحسابات عندك يقدر يتربط بمزوّد الخدمة.'),
        ('Review credit notes and self-billing; they go through the system too.', 'راجع الإشعارات الدائنة والفوترة الذاتية، دي كمان بتعدّي على النظام.'),
        ('Agree who in the company issues, approves and archives e-invoices.', 'حدّد مين في الشركة بيطلّع الفاتورة ومين بيعتمدها ومين بيحفظها.'),
        ('Keep records for the period required by the Tax Procedures Law and be ready to give them to the FTA.', 'احتفظ بالسجلات للمدة اللي بيحددها قانون الإجراءات الضريبية، وخليها جاهزة لو الهيئة طلبتها.'),
        ('Run test invoices with your ASP before the go-live date.', 'جرّب فواتير تجريبية مع مزوّد الخدمة قبل ميعاد التشغيل.'),
        ('Tell your main customers and suppliers when you switch; recipients must also be ready to receive e-invoices.', 'بلّغ عملاءك وموردينك الأساسيين بميعاد التحويل، لأن المستلم كمان لازم يكون جاهز يستقبل الفاتورة الإلكترونية.'),
        ('Put the ASP deadline and go-live date in your calendar with reminders.', 'حط ميعاد مزوّد الخدمة وميعاد التشغيل في التقويم بتذكير.'),
        ('Keep your bookkeeping monthly so the switch is smooth.', 'خلّي دفاترك متسجلة كل شهر عشان التحويل يمشي بسهولة.'),
    ]
    cl = ''.join(f'<li>{B(e, a)}</li>' for e, a in checklist)
    qas = [('Does e-invoicing apply to my small company?', 'هل الفوترة الإلكترونية هتطبق على شركتي الصغيرة؟',
            'Yes, if you sell to other businesses or government. Companies with revenue below AED 50 million are in Phase 2: appoint an ASP by 31 March 2027 and go live by 1 July 2027.',
            'أيوه، لو بتبيع لشركات أو جهات حكومية. الشركات اللي إيرادها أقل من 50 مليون درهم في المرحلة التانية: تعيّن مزوّد خدمة قبل 31 مارس 2027 وتبدأ التشغيل من 1 يوليو 2027.'),
           ('Are sales to individuals included?', 'البيع للأفراد داخل في النظام؟', 'Business-to-consumer (B2C) sales are excluded for now.', 'البيع للأفراد مستثنى دلوقتي.'),
           ('What are the fines?', 'إيه الغرامات؟',
            'Under the amendments announced in October 2026, a first violation is AED 5,000, plus AED 5,000 for each further month, up to AED 50,000 in 12 months. Confirm the current rules with the Ministry of Finance.',
            'حسب التعديلات المعلنة في أكتوبر 2026: أول مخالفة 5,000 درهم، وبيتزود 5,000 عن كل شهر بعدها، بحد أقصى 50,000 درهم في 12 شهر. اتأكد من القواعد الحالية مع وزارة المالية.')]
    body = f'''
<div class="eyebrow">{B('Free guide', 'دليل مجاني')}</div>
<h1>{B('UAE e-invoicing: what your company must do and when', 'الفوترة الإلكترونية في الإمارات: شركتك هتعمل إيه وإمتى')}</h1>
<div class="answer"><b>{B('SHORT ANSWER', 'الإجابة باختصار')}</b>{B('If your company sells to other businesses or government, e-invoicing applies to you. Revenue below AED 50 million: appoint an Accredited Service Provider by 31 March 2027 and go live by 1 July 2027. AED 50 million or more: provider by 30 October 2026, live from 1 January 2027.',
 'لو شركتك بتبيع لشركات أو جهات حكومية، الفوترة الإلكترونية هتطبق عليك. لو إيرادك أقل من 50 مليون درهم: لازم تعيّن مزوّد خدمة معتمد قبل 31 مارس 2027 وتبدأ التشغيل من 1 يوليو 2027. ولو 50 مليون أو أكتر: مزوّد الخدمة قبل 30 أكتوبر 2026، والتشغيل من 1 يناير 2027.')}</div>
<h2>{B('Timeline', 'المواعيد')}</h2>
<div class="tbl-wrap"><table class="tbl"><thead><tr><th>{B('Phase', 'المرحلة')}</th><th>{B('Who', 'مين')}</th><th>{B('Appoint provider by', 'تعيين المزوّد قبل')}</th><th>{B('Go live', 'بداية التشغيل')}</th></tr></thead><tbody>{trs}</tbody></table></div>
<h2>{B('What changes', 'إيه اللي هيتغير')}</h2>
{P('Invoices and credit notes between businesses are sent in a structured electronic format through an Accredited Service Provider (ASP), not as PDF or paper. Both the sender and the receiver need a provider. Sales to individuals are excluded for now.',
   'الفواتير والإشعارات الدائنة بين الشركات هتتبعت بصيغة إلكترونية منظمة عن طريق مزوّد خدمة معتمد، مش PDF أو ورق. واللي بيبعت واللي بيستقبل الاتنين محتاجين مزوّد خدمة. والبيع للأفراد مستثنى دلوقتي.')}
<h2>{B('Your 12-step readiness checklist', 'قايمة الاستعداد في 12 خطوة')}</h2>
<div id="gate" class="gate-locked"><ol class="steps2 blur" id="clist">{cl}</ol></div>
<div class="card2" id="gateBox"><b>{B('Unlock the full checklist', 'افتح القايمة كاملة')}</b>{P('Leave your name and mobile. The checklist opens right away and our team can send you a reminder before your deadline.', 'اكتب اسمك وموبايلك، والقايمة هتفتح على طول، وفريقنا يقدر يفكّرك قبل ميعادك.')}
<form class="tform" id="gForm" novalidate>{HONEY}<div class="two"><label>{B('Your name', 'الاسم')}<input name="name" required></label><label>{B('Mobile / WhatsApp', 'الموبايل / واتساب')}<input name="phone" type="tel" inputmode="tel" required></label></div>
<div class="two"><label>{B('Company (optional)', 'الشركة (اختياري)')}<input name="company"></label><label>{B('Annual revenue', 'الإيراد السنوي')}<select name="rev"><option value="Below AED 50m">أقل من 50 مليون درهم</option><option value="AED 50m or more">50 مليون درهم أو أكتر</option><option value="Not sure">مش متأكد</option></select></label></div>
<p class="err" id="gErr" hidden></p><div class="tbtns"><button class="btn btn-gold" type="submit">{B('Open the checklist', 'افتح القايمة')}</button></div></form></div>
<h2>{B('Questions', 'أسئلة')}</h2>
{faq_html(qas)}
<div class="g-cta"><h2>{B('Get ready with us', 'جهّز معانا')}</h2><p>{B('We keep your books monthly and help you prepare your data and software for your provider. Tax filings go through our accredited partner.', 'بنمسك دفاترك شهريًا ونساعدك تجهّز بياناتك وبرنامجك لمزوّد الخدمة. والإقرارات الضريبية عن طريق شريكنا المعتمد.')}</p>
<div class="g-btns">{wa_btn('Talk to us on WhatsApp', 'كلّمنا واتساب', 'السلام عليكم، عايز أجهّز شركتي للفوترة الإلكترونية.', 'btn btn-gold')}<a class="btn btn-navy" href="book">{B('Book a consultation', 'احجز استشارة')}</a></div></div>
<p class="note mini-foot">{SRC_NOTE} {B('General information, not tax advice.', 'معلومات عامة، مش استشارة ضريبية.')}</p>
{LAW}'''
    js = '''
var unlocked=false;try{unlocked=localStorage.getItem('hbc-einv')==='1';}catch(e){}
function openList(){document.getElementById('clist').classList.remove('blur');document.getElementById('gate').classList.remove('gate-locked');document.getElementById('gateBox').hidden=true;}
if(unlocked)openList();
document.getElementById('gForm').addEventListener('submit',function(e){e.preventDefault();var g=new FormData(e.target),er=document.getElementById('gErr');er.hidden=true;if(g.get('company_website'))return;
 if(!g.get('name')||!HBC.validPhone(g.get('phone'))){er.textContent=HBC.t('Please add your name and mobile.','اكتب الاسم والموبايل.');er.hidden=false;return;}
 HBC.lead({name:g.get('name'),phone:g.get('phone'),company:g.get('company'),service:'E-invoicing guide',source:'einvoicing_guide',message:'Revenue: '+g.get('rev')})
 .then(function(){HBC.track('generate_lead',{service:'E-invoicing guide'});try{localStorage.setItem('hbc-einv','1');}catch(x){}openList();})
 .catch(function(){er.textContent=HBC.t('Could not send. Please try again.','ماوصلش. جرّب تاني.');er.hidden=false;});});
'''
    schema = [faq_schema([(qe, ae) for qe, qa, ae, aa in qas]),
              {"@context": "https://schema.org", "@type": "Article", "headline": "UAE e-invoicing: what your company must do and when", "inLanguage": ["ar", "en"],
               "author": {"@type": "Person", "name": "Ahmed Saeed El Harmawy"}, "publisher": {"@type": "Organization", "name": "El Harmawy Business Consultancy F.Z.E"}, "dateModified": "2026-11-12"}]
    return page('e-invoicing', 'UAE e-invoicing guide', 'دليل الفوترة الإلكترونية في الإمارات', 'UAE e-invoicing timeline, who is in scope and a readiness checklist.',
                body, schema=schema, script=js, desc_ar='مواعيد الفوترة الإلكترونية في الإمارات لكل مرحلة، ومين داخل فيها، وقايمة استعداد في 12 خطوة.')


def emirate(slug, en_name, ar_name, answer_en, answer_ar, rows, steps, qas, wa_msg, extra_en='', extra_ar=''):
    trs = ''.join(f'<tr><td>{B(a, b)}</td><td class="n" dir="ltr">{c}</td></tr>' for a, b, c in rows)
    st = ''.join(f'<li>{B(e, a)}</li>' for e, a in steps)
    body = f'''
<div class="eyebrow">{B('Company setup', 'تأسيس الشركات')}</div>
<h1>{B('Company setup in ' + en_name + ': cost and steps', 'تأسيس شركة في ' + ar_name + ': التكلفة والخطوات')}</h1>
<div class="answer"><b>{B('SHORT ANSWER', 'الإجابة باختصار')}</b>{B(answer_en, answer_ar)}</div>
<h2>{B('Government fees (AED)', 'الرسوم الحكومية (درهم)')}</h2>
<div class="tbl-wrap"><table class="tbl"><tbody>{trs}</tbody></table></div>
{('<p>' + B(extra_en, extra_ar) + '</p>') if extra_en else ''}
<p>{B('Our company setup fee: AED 2,000. Government fees are paid at cost with official receipts. You get a written quote before we start.', 'أتعابنا للتأسيس: 2,000 درهم. الرسوم الحكومية بتتدفع بتكلفتها ومعاها الإيصالات الرسمية. وبيوصلك عرض سعر مكتوب قبل ما نبدأ.')}</p>
<h2>{B('Steps', 'الخطوات')}</h2>
<ol class="steps2">{st}</ol>
<h2>{B('After setup', 'بعد التأسيس')}</h2>
<p>{B('We keep your books, renew your licence on time and handle your company government transactions, in monthly packages from AED 1,000.', 'بنمسك حساباتك، ونجدّد رخصتك في ميعادها، ونخلّص معاملات شركتك الحكومية، في باقات شهرية تبدأ من 1,000 درهم.')}</p>
<h2>{B('Questions', 'أسئلة')}</h2>
{faq_html(qas)}
<div class="g-cta"><h2>{B('Get your exact cost', 'اعرف تكلفتك بالظبط')}</h2><p>{B('Tell us your activity and we send a written quote, usually the same working day.', 'قولنا نشاطك ونبعتلك عرض سعر مكتوب، غالبًا في نفس يوم العمل.')}</p>
<div class="g-btns">{wa_btn('Get a quote on WhatsApp', 'اطلب عرض سعر واتساب', wa_msg, 'btn btn-gold')}<a class="btn btn-navy" href="./#setup-cost">{B('Setup cost calculator', 'حاسبة تكلفة التأسيس')}</a></div></div>
<p class="note mini-foot">{B('Fees as published by the authorities and in our 2026 price list; they can change. General information, not legal advice.', 'الرسوم زي ما الجهات نشرتها وحسب قايمة أسعارنا 2026، وممكن تتغير. معلومات عامة، مش استشارة قانونية.')}</p>
{LAW}'''
    schema = [faq_schema([(qe, ae) for qe, qa, ae, aa in qas]),
              {"@context": "https://schema.org", "@type": "Service", "serviceType": "Company formation", "areaServed": en_name,
               "provider": {"@type": "ProfessionalService", "name": "El Harmawy Business Consultancy F.Z.E", "telephone": "+971563469000", "url": "https://elharmawy.com"},
               "offers": {"@type": "Offer", "priceCurrency": "AED", "price": "2000", "description": "Company setup service fee; government fees extra"}}]
    return page(slug, f'Company setup in {en_name}', f'تأسيس شركة في {ar_name}', f'Company setup in {en_name}: government fees, steps and our fixed fee.',
                body, schema=schema, desc_ar=f'تأسيس شركة في {ar_name}: الرسوم الحكومية، الخطوات، وأتعابنا الثابتة 2,000 درهم.')


def emirates():
    out = {}
    out['company-setup-ajman.html'] = emirate('company-setup-ajman', 'Ajman', 'عجمان',
        'Ajman Free Zone: trade licence from AED 4,445. Ajman mainland (DED): government fees from about AED 11,837 for a commercial licence or AED 5,837 for a professional licence, depending on the activity. Our setup fee is AED 2,000.',
        'منطقة عجمان الحرة: الرخصة التجارية تبدأ من 4,445 درهم. عجمان بر رئيسي (التنمية الاقتصادية): الرسوم الحكومية تبدأ من حوالي 11,837 درهم للرخصة التجارية و5,837 درهم للمهنية حسب النشاط. وأتعابنا للتأسيس 2,000 درهم.',
        [('Ajman Free Zone trade licence (licence only)', 'رخصة تجارية في منطقة عجمان الحرة (رخصة فقط)', 'from 4,445'),
         ('Mainland: trade name', 'بر رئيسي: حجز الاسم التجاري', '870 + 750'), ('Application', 'الطلب', '10'), ('Security approval', 'الموافقة الأمنية', '207'),
         ('Commercial licence (by activity)', 'الرخصة التجارية (حسب النشاط)', '10,000 – 15,000'), ('Professional licence (by activity)', 'الرخصة المهنية (حسب النشاط)', '4,000 – 7,000'),
         ('General trading / contracting', 'التجارة العامة / المقاولات', '+15,000 / +10,000'),
         ('After the licence: establishment card (1 year)', 'بعد الرخصة: بطاقة المنشأة (سنة)', '407'), ('E-channel', 'الإي تشانل', '3,270'), ('MOHRE establishment file', 'ملف وزارة الموارد البشرية', '555')],
        [('Choose free zone or mainland and the activity', 'اختيار منطقة حرة أو بر رئيسي والنشاط'), ('Reserve the trade name and get initial approval', 'حجز الاسم التجاري والموافقة المبدئية'),
         ('Security approval and tenancy contract', 'الموافقة الأمنية وعقد الإيجار'), ('Licence issued', 'إصدار الرخصة'), ('Company government file and bank account', 'ملف الشركة الحكومي والحساب البنكي')],
        [('Free zone or mainland in Ajman?', 'منطقة حرة ولا بر رئيسي في عجمان؟', 'The free zone is cheaper to start and fully online; mainland suits you if you will trade directly in the local market or need a shop.', 'المنطقة الحرة أرخص في البداية وكلها أونلاين، والبر الرئيسي يناسبك لو هتبيع مباشرة في السوق المحلي أو محتاج محل.'),
         ('Do I need an office?', 'لازم يكون عندي مكتب؟', 'Free zone packages include a desk or virtual office; mainland needs a tenancy contract.', 'باقات المنطقة الحرة فيها مكتب أو مكتب افتراضي، والبر الرئيسي محتاج عقد إيجار.'),
         ('Can I set up from outside the UAE?', 'أقدر أأسّس وأنا برّه الإمارات؟', 'Usually yes for the free zone, with documents sent online.', 'غالبًا أيوه في المنطقة الحرة، والأوراق بتتبعت أونلاين.')],
        'السلام عليكم، عايز أأسّس شركة في عجمان. ابعتلي عرض السعر.')
    out['company-setup-sharjah.html'] = emirate('company-setup-sharjah', 'Sharjah', 'الشارقة',
        'Sharjah mainland government fees are roughly the same as Ajman mainland, plus 13% of the annual tenancy value (charged with the licence) and 5% of the tenancy value for attestation. Free zones such as SHAMS start from about AED 5,700 for the licence. Our setup fee is AED 2,000.',
        'الرسوم الحكومية في الشارقة بر رئيسي تقريبًا زي عجمان بر رئيسي، وبيتزود عليها 13% من قيمة الإيجار السنوي (مع رسوم الرخصة) و5% من قيمة العقد لتوثيقه. والمناطق الحرة زي شمس تبدأ من حوالي 5,700 درهم للرخصة. وأتعابنا للتأسيس 2,000 درهم.',
        [('Mainland licence (similar to Ajman, by activity)', 'رخصة بر رئيسي (قريبة من عجمان، حسب النشاط)', '≈ 11,837+'), ('Added: share of annual rent', 'بيتزود: نسبة من الإيجار السنوي', '13%'),
         ('Tenancy contract attestation', 'توثيق عقد الإيجار', '5%'), ('SHAMS free zone licence', 'رخصة منطقة شمس الحرة', 'from 5,700')],
        [('Choose the activity and location', 'اختيار النشاط والمكان'), ('Trade name and initial approval', 'الاسم التجاري والموافقة المبدئية'), ('Tenancy contract and its attestation', 'عقد الإيجار وتوثيقه'),
         ('Licence issued', 'إصدار الرخصة'), ('Company government file and bank account', 'ملف الشركة الحكومي والحساب البنكي')],
        [('Why does rent change the cost in Sharjah?', 'ليه الإيجار بيغيّر التكلفة في الشارقة؟', 'Because 13% of the annual rent is charged with the licence fees and 5% for attesting the contract.', 'لأن 13% من الإيجار السنوي بتتحسب مع رسوم الرخصة، و5% لتوثيق العقد.'),
         ('Is a free zone cheaper?', 'المنطقة الحرة أرخص؟', 'Often yes to start, for example SHAMS from about AED 5,700 for the licence; it depends on your activity and market.', 'غالبًا أيوه في البداية، مثلًا شمس من حوالي 5,700 درهم للرخصة، وده حسب نشاطك والسوق اللي هتشتغل فيه.')],
        'السلام عليكم، عايز أأسّس شركة في الشارقة. ابعتلي عرض السعر.')
    out['company-setup-dubai.html'] = emirate('company-setup-dubai', 'Dubai', 'دبي',
        'Dubai mainland (DET): government fees from about AED 13,904 for the licence depending on the activity, plus a flexi-desk office. Meydan Free Zone: licence AED 12,500 a year. Dubai e-Trader licence to sell online from home: AED 1,790 all-inclusive. Our setup fee is AED 2,000.',
        'دبي بر رئيسي (دائرة الاقتصاد والسياحة): الرسوم الحكومية للرخصة تبدأ من حوالي 13,904 درهم حسب النشاط، ومعاها مكتب فليكسي ديسك. منطقة ميدان الحرة: الرخصة 12,500 درهم في السنة. ورخصة التاجر الإلكتروني للبيع من البيت: 1,790 درهم شاملة. وأتعابنا للتأسيس 2,000 درهم.',
        [('Trade name', 'الاسم التجاري', '620'), ('Initial approval', 'الموافقة المبدئية', '120'), ('Typing (Tasheel)', 'الطباعة (تسهيل)', '464'), ('MOA', 'عقد التأسيس', '1,200 – 1,500'),
         ('Licence (by activity)', 'الرخصة (حسب النشاط)', '11,500 – 13,500'), ('Establishment card', 'بطاقة المنشأة', '750'), ('Flexi-desk office (Ejari)', 'مكتب فليكسي ديسك (إيجاري)', 'quoted'),
         ('Meydan Free Zone licence (per year)', 'رخصة منطقة ميدان الحرة (سنويًا)', '12,500'), ('Dubai e-Trader licence (all-inclusive)', 'رخصة التاجر الإلكتروني (شاملة)', '1,790')],
        [('Choose mainland, free zone or e-Trader', 'اختيار بر رئيسي أو منطقة حرة أو تاجر إلكتروني'), ('Trade name and initial approval', 'الاسم التجاري والموافقة المبدئية'), ('MOA and office (Ejari)', 'عقد التأسيس والمكتب (إيجاري)'),
         ('Licence issued', 'إصدار الرخصة'), ('Company government file and bank account', 'ملف الشركة الحكومي والحساب البنكي')],
        [('What is the cheapest way to start in Dubai?', 'إيه أرخص طريقة أبدأ بيها في دبي؟', 'For selling online from home, the Dubai e-Trader licence at AED 1,790 (UAE residents and nationals, licence only). For a full company, compare mainland and free zones in a written quote.', 'للبيع أونلاين من البيت، رخصة التاجر الإلكتروني بـ 1,790 درهم (للمقيمين والمواطنين، رخصة فقط). ولشركة كاملة، نقارن لك البر الرئيسي والمناطق الحرة في عرض سعر مكتوب.'),
         ('Do I need an office in Dubai mainland?', 'لازم مكتب في دبي بر رئيسي؟', 'Yes, at least a flexi-desk with an Ejari contract; we quote it separately because its price changes.', 'أيوه، على الأقل فليكسي ديسك بعقد إيجاري، وبنسعّره لوحده لأن سعره بيتغير.')],
        'السلام عليكم، عايز أأسّس شركة في دبي. ابعتلي عرض السعر.')
    return out


def chinese():
    body = '''
<div class="eyebrow">El Harmawy Business Consultancy · 阿联酋公司服务</div>
<h1>在阿联酋注册公司，我们帮您办好</h1>
<div class="answer"><b>简要回答</b>阿治曼自由区贸易执照起价 4,445 迪拉姆。我们的公司注册服务费为 2,000 迪拉姆，政府费用按实际金额收取并提供官方收据。开始前提供书面报价。</div>
<h2>我们的服务</h2>
<ul>
<li><b>公司注册</b>：自由区与本土（迪拜、阿治曼、沙迦）执照，选择合适的经营范围。</li>
<li><b>公司银行账户协助</b>：准备公司资料与简介，向合适的银行提交并跟进至银行决定。服务费 1,000 迪拉姆，银行批准后才付款。</li>
<li><b>会计与记账</b>：每月记账、发票与报表，月度套餐 1,000 迪拉姆起。税务申报通过我们认证的合作伙伴办理。</li>
<li><b>政府事务</b>：执照续期与变更、政府审批的提交与跟进。</li>
<li><b>法律翻译</b>：法院认证的翻译，中文、阿拉伯语、英语等。</li>
</ul>
<h2>步骤</h2>
<ol class="steps2"><li>通过 WhatsApp 告诉我们您的业务</li><li>收到书面报价</li><li>注册公司并取得执照</li><li>开设银行账户，之后由我们负责记账和政府事务</li></ol>
<div class="g-cta"><h2>联系我们</h2><p>WhatsApp：+971 56 346 9000 · 邮箱：info@elharmawy.com · 地址：阿治曼自由区 C1 楼</p>
<div class="g-btns"><a class="btn btn-gold" href="https://wa.me/971563469000?text=%E6%82%A8%E5%A5%BD%EF%BC%8C%E6%88%91%E6%83%B3%E5%9C%A8%E9%98%BF%E8%81%94%E9%85%8B%E6%B3%A8%E5%86%8C%E5%85%AC%E5%8F%B8%E3%80%82" target="_blank" rel="noopener">WhatsApp 咨询</a><a class="btn btn-navy" href="profile/HBC-Company-Profile-ZH.pdf">下载公司简介（中文）</a></div></div>
<p class="law-line">价格及任何审批均须遵守阿拉伯联合酋长国法律，并以主管机关的决定为准。我们不出售也不担保签证。</p>
<p class="mini-foot"><a href="./?lang=en">English</a> · <a href="./">العربية</a></p>'''
    schema = [{"@context": "https://schema.org", "@type": "ProfessionalService", "name": "El Harmawy Business Consultancy F.Z.E", "inLanguage": "zh",
               "telephone": "+971563469000", "url": "https://elharmawy.com/zh", "areaServed": "AE"}]
    return page('zh', '阿联酋公司注册 | El Harmawy Business Consultancy', '', 'El Harmawy Business Consultancy：阿联酋公司注册、银行账户协助、会计记账与政府事务。',
                body, schema=schema, fixed='zh', desc_ar='El Harmawy Business Consultancy：阿联酋公司注册、银行账户协助、会计记账与政府事务。')


def pages():
    out = {'e-invoicing.html': einvoicing(), 'zh.html': chinese()}
    out.update(emirates())
    return out
