// Runs automatically after every successful Netlify deploy.
// Tells Bing (which ChatGPT search relies on) and other IndexNow engines about every URL in the sitemap.
const KEY = "58758f66978ad943e3b8cf72ca9cb539";
const HOST = "elharmawy.com";
export default async () => {
  try {
    const xml = await (await fetch("https://" + HOST + "/sitemap.xml")).text();
    const urlList = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]).slice(0, 10000);
    const r = await fetch("https://api.indexnow.org/indexnow", {
      method: "POST",
      headers: { "Content-Type": "application/json; charset=utf-8" },
      body: JSON.stringify({ host: HOST, key: KEY, keyLocation: "https://" + HOST + "/" + KEY + ".txt", urlList }),
    });
    console.log("IndexNow", r.status, urlList.length, "urls");
  } catch (e) {
    console.log("IndexNow failed", e && e.message);
  }
  return new Response("ok");
};
