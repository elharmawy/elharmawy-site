// HBC app service worker: makes the site installable and opens offline with the last saved copy.
const CACHE = "hbc-v3";
const CORE = ["/", "/site.css", "/logo.png", "/favicon.png", "/founder.jpg", "/icons/icon-192.png", "/manifest.webmanifest"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== "GET" || url.origin !== location.origin) return;           // forms, chat POSTs, fonts, WhatsApp: straight to network
  if (url.pathname.startsWith("/api/") || url.pathname.startsWith("/videos/") || url.pathname.endsWith(".mp3")) return; // never cache chat or videos
  if (req.mode === "navigate") {                                                // pages: fresh first, saved copy when offline
    e.respondWith(fetch(req).then(r => { const c = r.clone(); caches.open(CACHE).then(x => x.put("/", c)); return r; })
      .catch(() => caches.match(req).then(m => m || caches.match("/"))));
    return;
  }
  e.respondWith(fetch(req).then(r => {                                           // static files: fresh first, saved copy when offline
    if (r.ok) { const c = r.clone(); caches.open(CACHE).then(x => x.put(req, c)); }
    return r;
  }).catch(() => caches.match(req)));
});
