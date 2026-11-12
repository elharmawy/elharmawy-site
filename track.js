/* Shared analytics + ad pixels for every page. Put real IDs in HBC_INTEGRATIONS below. */
window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}
gtag('js',new Date());
var hbcApp=window.matchMedia('(display-mode: standalone)').matches||navigator.standalone===true;
gtag('config','G-M1BHSYLT4R',{opened_from:hbcApp?'app':'browser'});
window.hbcTrack=function(n,p){try{gtag('event',n,p||{});}catch(e){}};
/* Marketing integration points. Leave empty until real IDs exist; nothing loads while they are empty.
   googleAdsId: 'AW-XXXXXXXXX', googleAdsLeadLabel: 'conversion label', metaPixelId: '15-16 digit id'.
   Google Search Console: verify by DNS TXT record, or paste its <meta name="google-site-verification"> tag in this head. */
window.HBC_INTEGRATIONS={googleAdsId:'',googleAdsLeadLabel:'',metaPixelId:''};
(function(c){
  if(c.googleAdsId){ gtag('config',c.googleAdsId); }
  if(c.metaPixelId){ !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js'); fbq('init',c.metaPixelId); fbq('track','PageView'); }
  var base=window.hbcTrack;
  window.hbcTrack=function(n,p){ base(n,p);
    try{ if(n==='generate_lead'){ if(c.googleAdsId&&c.googleAdsLeadLabel) gtag('event','conversion',{send_to:c.googleAdsId+'/'+c.googleAdsLeadLabel}); if(c.metaPixelId&&window.fbq) fbq('track','Lead',{content_name:(p&&p.service)||''}); }
         if(n==='whatsapp_click'&&c.metaPixelId&&window.fbq) fbq('track','Contact'); }catch(e){} };
})(window.HBC_INTEGRATIONS);
