/* Shared helpers for the client tools pages. */
(function () {
  var site = document.getElementById('site');
  function setLang(l) {
    if (!site || site.dataset.fixed) return;
    site.setAttribute('dir', l === 'ar' ? 'rtl' : 'ltr'); site.setAttribute('lang', l); document.documentElement.lang = l;
    try { localStorage.setItem('hbc-lang', l); } catch (e) {}
    document.dispatchEvent(new CustomEvent('hbc-lang', { detail: l }));
  }
  var s = 'ar';
  try { var v = localStorage.getItem('hbc-lang'); if (v === 'en') s = 'en'; } catch (e) {}
  try { var q = new URLSearchParams(location.search).get('lang'); if (q === 'en' || q === 'ar') s = q; } catch (e) {}
  setLang(s);
  var lb = document.getElementById('langBtn');
  if (lb) lb.addEventListener('click', function () { setLang(site.getAttribute('dir') === 'rtl' ? 'en' : 'ar'); });

  var HBC = window.HBC = {};
  HBC.lang = function () { return site ? site.getAttribute('lang') || 'ar' : 'ar'; };
  HBC.t = function (en, ar) { return HBC.lang() === 'ar' ? ar : en; };
  HBC.track = function (n, p) { try { if (window.hbcTrack) window.hbcTrack(n, p || {}); } catch (e) {} };
  HBC.live = /(netlify\.app|elharmawy\.com)$/.test(location.hostname);

  /* Send to the existing Netlify "leads" form (forwarded to the HBC Website Leads sheet). */
  HBC.lead = function (fields) {
    var d = new URLSearchParams();
    d.append('form-name', 'leads');
    d.append('language', HBC.lang());
    Object.keys(fields).forEach(function (k) { if (fields[k] != null) d.append(k, String(fields[k]).slice(0, 1500)); });
    if (!HBC.live) return Promise.resolve();
    return fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: d.toString() })
      .then(function (r) { if (!r.ok) throw new Error('send'); });
  };

  HBC.wa = function (text) { return 'https://wa.me/971563469000?text=' + encodeURIComponent(text); };

  /* Calendar file (.ics) for reminders and appointments. */
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function stamp(d) { return d.getUTCFullYear() + pad(d.getUTCMonth() + 1) + pad(d.getUTCDate()) + 'T' + pad(d.getUTCHours()) + pad(d.getUTCMinutes()) + '00Z'; }
  function day(d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); }
  function esc(s) { return String(s).replace(/[\\;,]/g, function (c) { return '\\' + c; }).replace(/\n/g, '\\n'); }
  HBC.ics = function (events, filename) {
    var L = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//El Harmawy Business Consultancy//Tools//EN', 'CALSCALE:GREGORIAN', 'METHOD:PUBLISH'];
    events.forEach(function (e, i) {
      L.push('BEGIN:VEVENT', 'UID:' + Date.now() + '-' + i + '@elharmawy.com', 'DTSTAMP:' + stamp(new Date()));
      if (e.allDay) { var n = new Date(e.start); n.setDate(n.getDate() + 1); L.push('DTSTART;VALUE=DATE:' + day(e.start), 'DTEND;VALUE=DATE:' + day(n)); }
      else { L.push('DTSTART:' + stamp(e.start), 'DTEND:' + stamp(e.end || new Date(e.start.getTime() + 30 * 60000))); }
      L.push('SUMMARY:' + esc(e.title), 'DESCRIPTION:' + esc(e.desc || ''));
      (e.alarms || []).forEach(function (a) { L.push('BEGIN:VALARM', 'ACTION:DISPLAY', 'DESCRIPTION:' + esc(e.title), 'TRIGGER:' + a, 'END:VALARM'); });
      L.push('END:VEVENT');
    });
    L.push('END:VCALENDAR');
    var blob = new Blob([L.join('\r\n')], { type: 'text/calendar;charset=utf-8' });
    var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = filename || 'elharmawy-reminder.ics';
    document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  };

  HBC.validPhone = function (p) { return /^[+\d][\d\s-]{6,18}$/.test(String(p || '').trim()); };

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a');
    if (a && /wa\.me/.test(a.href)) HBC.track('whatsapp_click', { place: document.body.dataset.page || 'tool' });
  });
})();
