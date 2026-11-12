"""Build the client tools and local pages. Usage: python3 tools/build_pages.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pages_common import page, B, P, LAW, faq_schema, faq_html, wa_btn
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = {}

HONEY = '<p class="hp"><label>Leave empty <input name="company_website" tabindex="-1" autocomplete="off"></label></p>'
CONTACT_FIELDS = f'''<div class="two">
  <label>{B('Your name', 'الاسم')}<input name="name" autocomplete="name" required></label>
  <label>{B('Mobile / WhatsApp', 'الموبايل / واتساب')}<input name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="05x xxx xxxx" required></label>
</div>'''

# ---------------------------------------------------------------- track
STEPS = [('Documents received', 'استلمنا الأوراق'), ('File prepared', 'جهّزنا الملف'), ('Submitted to the authority', 'اتقدّم للجهة'),
         ('Awaiting the authority', 'مستني قرار الجهة'), ('Completed', 'خلصت')]
track_body = f'''
<div class="eyebrow">{B('Client tools', 'أدوات العملاء')}</div>
<h1>{B('Track your file', 'تابع معاملتك')}</h1>
<p class="lead">{B('Enter the file code we sent you on WhatsApp to see where your transaction stands. No login needed.', 'اكتب كود الملف اللي بعتناه لك على الواتساب، وشوف معاملتك وصلت لفين. من غير تسجيل دخول.')}</p>
<div class="card2">
  <form class="tform" id="trackForm" novalidate>
    <label>{B('File code', 'كود الملف')}<input name="code" id="tCode" autocomplete="off" autocapitalize="characters" placeholder="HBC-0000-XX" required dir="ltr"></label>
    <div class="tbtns"><button class="btn btn-gold" type="submit" id="tBtn">{B('Show status', 'اعرض الحالة')}</button></div>
    <p class="err" id="tErr" hidden></p>
  </form>
</div>
<div id="tOut" hidden style="margin-top:18px"></div>
<h2>{B('What the steps mean', 'معنى كل خطوة')}</h2>
<ol class="steps2">{''.join(f'<li>{B(e, a)}</li>' for e, a in STEPS)}</ol>
<p class="mini-foot">{B('No code yet? Ask us on WhatsApp and we will send it.', 'ما عندكش كود؟ اطلبه مننا على الواتساب.')} {wa_btn('Ask for my code', 'اطلب الكود', 'السلام عليكم، عايز كود متابعة معاملتي.', 'btn btn-ghost2')}</p>
{LAW}'''
track_js = '''
var STEPS=%s;
var f=document.getElementById('trackForm'),out=document.getElementById('tOut'),err=document.getElementById('tErr'),btn=document.getElementById('tBtn');
try{var c0=new URLSearchParams(location.search).get('code');if(c0)document.getElementById('tCode').value=c0;}catch(e){}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function show(j){var t=HBC.t,h='';
 if(!j.ok){h='<div class="card2"><b>'+t('Tracking is being set up. Please ask us on WhatsApp for now.','خدمة المتابعة بتتجهّز. اسألنا على الواتساب لحد ما تشتغل.')+'</b></div>';}
 else if(!j.found){h='<div class="card2"><b>'+t('We could not find this code.','الكود ده مش موجود عندنا.')+'</b><p>'+t('Check the code in our WhatsApp message, or ask us.','راجع الكود في رسالة الواتساب، أو اسألنا.')+'</p></div>';}
 else{h='<div class="card2"><div class="eyebrow">'+esc(j.service)+'</div><h2 style="margin-top:6px">'+esc(j.status||j.stepName)+'</h2><ol class="tl">';
  STEPS.forEach(function(s,i){var n=i+1,cls=n<j.step?'done':(n===j.step?(j.step===5?'done':'now'):'');h+='<li class="'+cls+'"><span class="dot">'+(n<j.step||(n===5&&j.step===5)?'✓':n)+'</span><div><b>'+(HBC.lang()==='ar'?s[1]:s[0])+'</b>'+(n===j.step&&j.stepName?'<small>'+esc(j.stepName)+'</small>':'')+'</div></li>';});
  h+='</ol>'+(j.note?'<p><b>'+t('Note from our team: ','ملاحظة من الفريق: ')+'</b>'+esc(j.note)+'</p>':'')+(j.updated?'<p><small>'+t('Last update: ','آخر تحديث: ')+esc(j.updated)+'</small></p>':'')+'</div>';}
 out.innerHTML=h;out.hidden=false;}
f.addEventListener('submit',function(e){e.preventDefault();err.hidden=true;var code=document.getElementById('tCode').value.trim();
 if(code.replace(/[^A-Za-z0-9]/g,'').length<6){err.textContent=HBC.t('Please enter the full file code.','اكتب كود الملف كامل.');err.hidden=false;return;}
 btn.disabled=true;HBC.track('track_lookup',{});
 fetch('/api/track?code='+encodeURIComponent(code)).then(function(r){return r.json();}).catch(function(){return {ok:false};}).then(function(j){btn.disabled=false;show(j);});});
''' % (str([[e, a] for e, a in STEPS]).replace("'", '"'))
OUT['track.html'] = page('track', 'Track your file', 'تابع معاملتك', 'Track your El Harmawy file status with your file code.',
                         track_body, script=track_js, desc_ar='اكتب كود ملفك وشوف معاملتك وصلت لفين مع الهرماوي لاستشارات الأعمال.')

# ---------------------------------------------------------------- renew
renew_body = f'''
<div class="eyebrow">{B('Client tools', 'أدوات العملاء')}</div>
<h1>{B('Never miss a renewal', 'فكّرني بالتجديد')}</h1>
<p class="lead">{B('Enter your expiry dates. You get reminders in your own phone calendar right away, and our team reminds you on WhatsApp a month before.', 'اكتب مواعيد الانتهاء. هتنزل لك تذكيرات في تقويم موبايلك على طول، وفريقنا هيفكّرك على الواتساب قبلها بشهر.')}</p>
<div class="answer"><b>{B('WHY IT MATTERS', 'ليه مهم؟')}</b>{B('Late licence renewals can bring fines and can block government transactions, visas and bank operations until the licence is renewed.', 'التأخير في تجديد الرخصة ممكن يجيب غرامات، ويوقّف معاملات الشركة الحكومية والبنكية لحد ما تتجدد.')}</div>
<div class="card2">
<form class="tform" id="renForm" novalidate>
  {HONEY}{CONTACT_FIELDS}
  <label>{B('Company name (optional)', 'اسم الشركة (اختياري)')}<input name="company" autocomplete="organization"></label>
  <div class="two">
    <label>{B('Trade licence expiry', 'انتهاء الرخصة التجارية')}<input type="date" name="lic" required></label>
    <label>{B('Licence issued in', 'الرخصة صادرة من')}<select name="em"><option value="Ajman Free Zone">{'منطقة عجمان الحرة'}</option><option value="Ajman">عجمان</option><option value="Sharjah">الشارقة</option><option value="Dubai">دبي</option><option value="Abu Dhabi">أبوظبي</option><option value="Other free zone">منطقة حرة أخرى</option><option value="Other">أخرى</option></select></label>
  </div>
  <div class="two">
    <label>{B('Establishment card expiry (optional)', 'انتهاء بطاقة المنشأة (اختياري)')}<input type="date" name="est"></label>
    <label>{B('Tenancy contract expiry (optional)', 'انتهاء عقد الإيجار (اختياري)')}<input type="date" name="ten"></label>
  </div>
  <p class="err" id="rErr" hidden></p>
  <div class="tbtns"><button class="btn btn-gold" type="submit" id="rBtn">{B('Set my reminders', 'فعّل التذكيرات')}</button></div>
  <small class="hint">{B('We only use your details to remind you about these dates.', 'بياناتك بنستخدمها بس عشان نفكّرك بالمواعيد دي.')}</small>
</form>
<div id="rOk" class="ok-box" hidden><h3>{B('Done. Reminders are set.', 'تمام، التذكيرات اتفعّلت.')}</h3><p>{B('Your calendar file downloaded. Open it to add the reminders to your phone. Our team will message you on WhatsApp a month before each date.', 'نزل لك ملف تقويم، افتحه عشان التذكيرات تتضاف على موبايلك. وفريقنا هيبعتلك على الواتساب قبل كل ميعاد بشهر.')}</p>
<div class="tbtns"><button class="btn btn-ghost2" type="button" id="rIcs">{B('Download the calendar file again', 'نزّل ملف التقويم تاني')}</button>{wa_btn('Renew with us now', 'جدّد معانا دلوقتي', 'السلام عليكم، عايز أجدّد رخصة شركتي.')}</div></div>
</div>
{LAW}'''
renew_js = '''
var f=document.getElementById('renForm'),err=document.getElementById('rErr'),btn=document.getElementById('rBtn'),evs=[];
function d(v){if(!v)return null;var p=v.split('-');return new Date(+p[0],+p[1]-1,+p[2],9,0,0);}
function ev(dt,en,ar){if(!dt)return;var t=HBC.t(en,ar);evs.push({start:dt,allDay:true,title:t,desc:HBC.t('Renew with El Harmawy: WhatsApp +971 56 346 9000 · elharmawy.com','جدّد مع الهرماوي: واتساب 056 346 9000 · elharmawy.com'),alarms:['-P30D','-P7D','-P1D']});}
f.addEventListener('submit',function(e){e.preventDefault();err.hidden=true;var fd=new FormData(f);
 if(fd.get('company_website'))return;
 if(!fd.get('name')||!HBC.validPhone(fd.get('phone'))||!fd.get('lic')){err.textContent=HBC.t('Please add your name, mobile number and licence expiry date.','اكتب الاسم ورقم الموبايل وميعاد انتهاء الرخصة.');err.hidden=false;return;}
 evs=[];ev(d(fd.get('lic')),'Trade licence expires','انتهاء الرخصة التجارية');ev(d(fd.get('est')),'Establishment card expires','انتهاء بطاقة المنشأة');ev(d(fd.get('ten')),'Tenancy contract expires','انتهاء عقد الإيجار');
 btn.disabled=true;
 HBC.lead({name:fd.get('name'),phone:fd.get('phone'),company:fd.get('company'),service:'Licence renewal reminder',source:'renew_tool',
  message:'Licence expiry: '+fd.get('lic')+' ('+fd.get('em')+')'+(fd.get('est')?' · Establishment card: '+fd.get('est'):'')+(fd.get('ten')?' · Tenancy: '+fd.get('ten'):'')})
 .then(function(){HBC.track('generate_lead',{service:'Licence renewal reminder'});HBC.ics(evs,'elharmawy-renewals.ics');f.hidden=true;document.getElementById('rOk').hidden=false;})
 .catch(function(){btn.disabled=false;err.textContent=HBC.t('Could not send. Please try again or message us on WhatsApp.','ماوصلش. جرّب تاني أو ابعتلنا على الواتساب.');err.hidden=false;});});
document.getElementById('rIcs').addEventListener('click',function(){HBC.ics(evs,'elharmawy-renewals.ics');});
'''
OUT['renew.html'] = page('renew', 'Renewal reminder', 'فكّرني بالتجديد', 'Free reminders before your trade licence, establishment card and tenancy expire.',
                         renew_body, script=renew_js, desc_ar='تذكير مجاني قبل انتهاء الرخصة التجارية وبطاقة المنشأة وعقد الإيجار، في تقويم موبايلك وعلى الواتساب.')

# ---------------------------------------------------------------- book
book_body = f'''
<div class="eyebrow">{B('Client tools', 'أدوات العملاء')}</div>
<h1>{B('Book a free consultation', 'احجز استشارة مجانية')}</h1>
<p class="lead">{B('Pick a day and a time. We confirm the appointment with you on WhatsApp.', 'اختار اليوم والساعة، وإحنا نأكد معاك الميعاد على الواتساب.')}</p>
<div class="card2">
<form class="tform" id="bkForm" novalidate>
  {HONEY}{CONTACT_FIELDS}
  <div class="two">
    <label>{B('Topic', 'الموضوع')}<select name="topic">
      <option value="Company setup">تأسيس شركة</option><option value="Accounting & bookkeeping">المحاسبة ومسك الدفاتر</option>
      <option value="Monthly package">باقة شهرية للشركة</option><option value="Corporate bank account">الحساب البنكي للشركة</option>
      <option value="Licence renewal / amendment">تجديد أو تعديل رخصة</option><option value="Government approvals">موافقات حكومية</option>
      <option value="Legal translation / attestation">ترجمة قانونية أو تصديق</option><option value="Other">موضوع تاني</option></select></label>
    <label>{B('How', 'إزاي')}<select name="mode"><option value="WhatsApp call">مكالمة واتساب</option><option value="Phone call">مكالمة تليفون</option><option value="Office visit (Ajman Free Zone)">زيارة المكتب (منطقة عجمان الحرة)</option></select></label>
  </div>
  <label>{B('Day', 'اليوم')}<select name="day" id="bkDay" required></select></label>
  <fieldset style="border:0;padding:0;margin:0"><legend style="font-weight:600;color:var(--navy);margin-bottom:6px">{B('Time (UAE time)', 'الساعة (بتوقيت الإمارات)')}</legend><div class="slots" id="bkSlots"></div></fieldset>
  <p class="err" id="bErr" hidden></p>
  <div class="tbtns"><button class="btn btn-gold" type="submit" id="bBtn">{B('Request this appointment', 'اطلب الميعاد ده')}</button></div>
</form>
<div id="bOk" class="ok-box" hidden><h3>{B('Request received', 'طلبك وصل')}</h3><p id="bOkTxt"></p>
<div class="tbtns"><button class="btn btn-ghost2" type="button" id="bIcs">{B('Add to my calendar', 'ضيفه على التقويم')}</button><a class="btn btn-wa" id="bWa" target="_blank" rel="noopener">{B('Confirm on WhatsApp', 'أكّد على الواتساب')}</a></div></div>
</div>
<p class="mini-foot">{B('Working days Monday to Saturday, 10 am to 6 pm.', 'أيام العمل من الاتنين للسبت، من 10 الصبح لـ 6 المغرب.')}</p>
{LAW}'''
book_js = '''
var dayS=document.getElementById('bkDay'),slots=document.getElementById('bkSlots'),evt=null;
var DN={en:['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],ar:['الأحد','الاتنين','التلات','الأربع','الخميس','الجمعة','السبت']};
function fillDays(){var cur=dayS.value;dayS.innerHTML='';var d=new Date();d.setHours(0,0,0,0);var n=0;
 while(n<12){d.setDate(d.getDate()+1);if(d.getDay()===0)continue;var v=d.getFullYear()+'-'+('0'+(d.getMonth()+1)).slice(-2)+'-'+('0'+d.getDate()).slice(-2);
  var o=document.createElement('option');o.value=v;o.textContent=DN[HBC.lang()==='ar'?'ar':'en'][d.getDay()]+' '+d.getDate()+'/'+(d.getMonth()+1);dayS.appendChild(o);n++;}
 if(cur)dayS.value=cur;}
function fillSlots(){if(slots.children.length)return;['10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00'].forEach(function(t,i){var l=document.createElement('label');l.innerHTML='<input type="radio" name="time" value="'+t+'"'+(i===1?' checked':'')+'>'+t;slots.appendChild(l);});}
fillDays();fillSlots();document.addEventListener('hbc-lang',fillDays);
var f=document.getElementById('bkForm'),err=document.getElementById('bErr'),btn=document.getElementById('bBtn');
f.addEventListener('submit',function(e){e.preventDefault();err.hidden=true;var fd=new FormData(f);if(fd.get('company_website'))return;
 if(!fd.get('name')||!HBC.validPhone(fd.get('phone'))||!fd.get('day')||!fd.get('time')){err.textContent=HBC.t('Please add your name, mobile, day and time.','اكتب الاسم والموبايل واختار اليوم والساعة.');err.hidden=false;return;}
 var when=fd.get('day')+' '+fd.get('time'),p=fd.get('day').split('-'),h=fd.get('time').split(':');
 var start=new Date(Date.UTC(+p[0],+p[1]-1,+p[2],+h[0]-4,0,0));
 evt={start:start,end:new Date(start.getTime()+30*60000),title:HBC.t('Consultation with El Harmawy (to be confirmed)','استشارة مع الهرماوي (مستنية تأكيد)'),desc:fd.get('topic')+' · '+fd.get('mode')+' · WhatsApp +971 56 346 9000',alarms:['-PT1H']};
 btn.disabled=true;
 HBC.lead({name:fd.get('name'),phone:fd.get('phone'),service:'Consultation booking',call_time:when+' (UAE)',source:'book_tool',message:'Topic: '+fd.get('topic')+' · Mode: '+fd.get('mode')})
 .then(function(){HBC.track('generate_lead',{service:'Consultation booking'});f.hidden=true;document.getElementById('bOk').hidden=false;
  document.getElementById('bOkTxt').textContent=HBC.t('You asked for '+when+' (UAE time). We will confirm it with you on WhatsApp. The time is final only after we confirm.','طلبت ميعاد '+when+' بتوقيت الإمارات. هنأكد معاك على الواتساب، والميعاد بيتثبت بعد تأكيدنا.');
  document.getElementById('bWa').href=HBC.wa('السلام عليكم، طلبت ميعاد استشارة '+when+' بخصوص: '+fd.get('topic')+'. الاسم: '+fd.get('name'));})
 .catch(function(){btn.disabled=false;err.textContent=HBC.t('Could not send. Please try again or message us on WhatsApp.','ماوصلش. جرّب تاني أو ابعتلنا على الواتساب.');err.hidden=false;});});
document.getElementById('bIcs').addEventListener('click',function(){if(evt)HBC.ics([evt],'elharmawy-consultation.ics');});
'''
OUT['book.html'] = page('book', 'Book a consultation', 'احجز استشارة', 'Book a free consultation with El Harmawy Business Consultancy.',
                        book_body, script=book_js, desc_ar='احجز استشارة مجانية مع الهرماوي لاستشارات الأعمال: تأسيس شركة، محاسبة، حساب بنكي، معاملات حكومية.')

# ---------------------------------------------------------------- check
QS = [
    ('lic', 'Is your trade licence valid for at least the next 60 days?', 'رخصتك التجارية سارية لـ 60 يوم قدام على الأقل؟',
     'Renew the licence before it expires to avoid fines and blocked transactions.', 'جدّد الرخصة قبل ما تخلص عشان تتجنب الغرامات ووقف المعاملات.'),
    ('ct', 'Is the company registered for corporate tax with the FTA?', 'الشركة متسجّلة في ضريبة الشركات عند الهيئة الاتحادية للضرائب؟',
     'Corporate tax registration is required for companies; late registration carries a penalty. We register through our accredited partner.', 'التسجيل في ضريبة الشركات مطلوب من الشركات، والتأخير عليه غرامة. بنسجّلك عن طريق شريكنا المعتمد.'),
    ('vat', 'If your sales passed AED 375,000 in 12 months, are you VAT registered?', 'لو مبيعاتك عدّت 375,000 درهم في 12 شهر، إنت متسجّل في ضريبة القيمة المضافة؟',
     'Check whether VAT registration is mandatory for you, and register on time.', 'اتأكد إذا كان تسجيل القيمة المضافة إلزامي عليك، وسجّل في ميعادك.'),
    ('books', 'Are your books (sales, expenses, bank) recorded every month?', 'دفاترك (المبيعات والمصاريف والبنك) متسجّلة كل شهر؟',
     'Monthly bookkeeping keeps you ready for tax returns, the bank and audits.', 'مسك الدفاتر شهريًا بيخليك جاهز للإقرار الضريبي والبنك والمراجعة.'),
    ('bank', 'Does the company have its own corporate bank account?', 'الشركة عندها حساب بنكي باسمها؟',
     'A corporate account separates company money and helps with tax and growth. We help prepare the bank file.', 'حساب الشركة بيفصل فلوس الشركة وبيساعد في الضريبة والتوسع. بنساعدك تجهّز ملف البنك.'),
    ('ten', 'Is your office / tenancy contract (Ejari) valid?', 'عقد إيجار المكتب (إيجاري) ساري؟',
     'Most licence renewals need a valid tenancy contract.', 'أغلب تجديدات الرخص محتاجة عقد إيجار ساري.'),
    ('einv', 'Do you know your e-invoicing deadline and service provider?', 'عارف ميعاد الفوترة الإلكترونية بتاعك ومين مزوّد الخدمة؟',
     'E-invoicing is coming in phases from 2027. Read our guide and plan early.', 'الفوترة الإلكترونية جاية على مراحل من 2027. اقرا دليلنا وجهّز بدري.'),
    ('docs', 'Are the company documents (MOA, licence, ID copies) organised in one place?', 'أوراق الشركة (عقد التأسيس، الرخصة، صور الهويات) متجمّعة في مكان واحد؟',
     'Keep a ready company file; banks and authorities ask for it often.', 'خلّي ملف الشركة جاهز، البنوك والجهات بتطلبه كتير.'),
]
qhtml = ''.join(f'''<div class="quiz-q"><b>{B(qe, qa)}</b><div class="seg">
<label><input type="radio" name="{k}" value="yes" required>{B('Yes', 'أيوه')}</label><label><input type="radio" name="{k}" value="no">{B('No', 'لأ')}</label><label><input type="radio" name="{k}" value="unsure">{B('Not sure', 'مش متأكد')}</label></div></div>''' for k, qe, qa, *_ in QS)
check_body = f'''
<div class="eyebrow">{B('Client tools', 'أدوات العملاء')}</div>
<h1>{B('Is your company in good shape?', 'شركتك سليمة؟')}</h1>
<p class="lead">{B('8 quick questions, one minute. You get a score and a short list of what to fix. Free.', '8 أسئلة سريعة في دقيقة. هيطلعلك تقييم وقايمة قصيرة باللي محتاج يتصلّح. مجانًا.')}</p>
<div class="card2"><form class="tform" id="qForm" novalidate>{qhtml}
<p class="err" id="qErr" hidden></p>
<div class="tbtns"><button class="btn btn-gold" type="submit">{B('Show my result', 'اعرض النتيجة')}</button></div></form>
<div id="qRes" hidden></div></div>
<p class="note mini-foot">{B('General information, not legal or tax advice.', 'معلومات عامة، مش استشارة قانونية أو ضريبية.')}</p>
{LAW}'''
check_js = '''
var QS=%s;
var f=document.getElementById('qForm'),res=document.getElementById('qRes'),err=document.getElementById('qErr'),last=null;
f.addEventListener('submit',function(e){e.preventDefault();err.hidden=true;var fd=new FormData(f),score=0,fix=[],ans=[];
 for(var i=0;i<QS.length;i++){var v=fd.get(QS[i][0]);if(!v){err.textContent=HBC.t('Please answer all 8 questions.','جاوب على الـ 8 أسئلة.');err.hidden=false;return;}
  ans.push(QS[i][0]+':'+v);if(v==='yes')score++;else fix.push(QS[i]);}
 var pct=Math.round(score/QS.length*100),ar=HBC.lang()==='ar';last={pct:pct,ans:ans.join(', ')};
 var lvl=pct>=88?HBC.t('Excellent','ممتاز'):pct>=63?HBC.t('Good, a few gaps','كويس، فيه شوية نواقص'):HBC.t('Needs attention','محتاج اهتمام');
 var h='<div class="score"><div class="ring" style="--p:'+pct+'"><span>'+pct+'%%</span></div><div><h2 style="margin:0">'+lvl+'</h2><p>'+HBC.t(score+' of 8 are in order.',score+' من 8 تمام.')+'</p></div></div>';
 if(fix.length){h+='<h2>'+HBC.t('What to fix','اللي محتاج يتصلّح')+'</h2><ul class="fix-list">'+fix.map(function(q){return '<li>'+(ar?q[4]:q[3])+'</li>';}).join('')+'</ul>';}
 h+='<h2>'+HBC.t('Get help with these','عايز مساعدة فيهم؟')+'</h2><form class="tform" id="qLead" novalidate><p class="hp"><label>Leave empty <input name="company_website" tabindex="-1" autocomplete="off"></label></p><div class="two"><label>'+HBC.t('Your name','الاسم')+'<input name="name" required></label><label>'+HBC.t('Mobile / WhatsApp','الموبايل / واتساب')+'<input name="phone" type="tel" inputmode="tel" required></label></div><p class="err" id="qlErr" hidden></p><div class="tbtns"><button class="btn btn-gold" type="submit">'+HBC.t('Send me a plan','ابعتولي خطة')+'</button><a class="btn btn-wa" target="_blank" rel="noopener" href="'+HBC.wa('السلام عليكم، عملت اختبار شركتك سليمة وطلعت '+pct+'%%. عايز مساعدة.')+'">'+HBC.t('Talk on WhatsApp','كلّمنا واتساب')+'</a></div></form>';
 res.innerHTML=h;res.hidden=false;f.hidden=true;HBC.track('health_check_done',{score:pct});res.scrollIntoView({behavior:'smooth',block:'start'});
 document.getElementById('qLead').addEventListener('submit',function(ev){ev.preventDefault();var g=new FormData(ev.target),le=document.getElementById('qlErr');if(g.get('company_website'))return;
  if(!g.get('name')||!HBC.validPhone(g.get('phone'))){le.textContent=HBC.t('Please add your name and mobile.','اكتب الاسم والموبايل.');le.hidden=false;return;}
  HBC.lead({name:g.get('name'),phone:g.get('phone'),service:'Company health check',source:'check_tool',message:'Score '+last.pct+'%% · '+last.ans}).then(function(){HBC.track('generate_lead',{service:'Company health check'});ev.target.outerHTML='<div class="ok-box"><h3>'+HBC.t('Thank you','شكرًا')+'</h3><p>'+HBC.t('Our team will message you on WhatsApp with a short plan.','فريقنا هيبعتلك على الواتساب خطة قصيرة.')+'</p></div>';}).catch(function(){le.textContent=HBC.t('Could not send. Please message us on WhatsApp.','ماوصلش. ابعتلنا على الواتساب.');le.hidden=false;});});});
''' % (str([list(q) for q in QS]).replace("\\'", "’"))
OUT['check.html'] = page('check', 'Company health check', 'شركتك سليمة؟', 'Free 1-minute company health check for UAE companies.',
                         check_body, script=check_js, desc_ar='اختبار مجاني في دقيقة لشركتك في الإمارات: الرخصة، الضرايب، الدفاتر، الحساب البنكي، والفوترة الإلكترونية.')

if __name__ == '__main__':
    import build_more  # noqa: E402  (e-invoicing, emirate pages, Chinese page)
    OUT.update(build_more.pages())
    for name, html in OUT.items():
        open(os.path.join(ROOT, name), 'w', encoding='utf-8').write(html)
    print('built', len(OUT), 'pages:', ', '.join(OUT))
