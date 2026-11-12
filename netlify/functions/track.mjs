// "Track your file": looks up one file code in the HBC tracking sheet and returns only that row.
// The sheet holds no names or phone numbers, only: code | service | step (1-5) | step name | status | last update | note to client.
// The sheet's CSV link comes from env var TRACK_CSV_URL (Netlify > Site configuration > Environment variables),
// or from TRACK_CSV below when the env var is not set.
const TRACK_CSV = "https://docs.google.com/spreadsheets/d/1dgCIIW6JwdbMUARhy-W3oLtX3Dd4LphCdl0xwmxKSsQ/gviz/tq?tqx=out:csv&sheet=Track";
let cache = { at: 0, rows: null };

function parseCSV(t) {
  const rows = []; let row = [], cell = "", q = false;
  for (let i = 0; i < t.length; i++) {
    const c = t[i];
    if (q) { if (c === '"') { if (t[i + 1] === '"') { cell += '"'; i++; } else q = false; } else cell += c; }
    else if (c === '"') q = true;
    else if (c === ",") { row.push(cell); cell = ""; }
    else if (c === "\n") { row.push(cell); rows.push(row); row = []; cell = ""; }
    else if (c !== "\r") cell += c;
  }
  if (cell || row.length) { row.push(cell); rows.push(row); }
  return rows;
}
const norm = (s) => String(s || "").toUpperCase().replace(/[^A-Z0-9]/g, "");
const json = (status, body) => new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" } });

export default async (req) => {
  const url = (process.env.TRACK_CSV_URL || TRACK_CSV || "").trim();
  const code = norm(new URL(req.url).searchParams.get("code"));
  if (!url) return json(200, { ok: false, reason: "not_configured" });
  if (code.length < 6 || code.length > 20) return json(400, { ok: false, reason: "bad_code" });
  try {
    if (!cache.rows || Date.now() - cache.at > 60000) {
      const r = await fetch(url, { redirect: "follow" });
      if (!r.ok || /text\/html/.test(r.headers.get("content-type") || "")) throw new Error("sheet not shared " + r.status);
      cache = { at: Date.now(), rows: parseCSV(await r.text()) };
    }
    const hit = cache.rows.slice(1).find((r) => norm(r[0]) === code);
    if (!hit) return json(200, { ok: true, found: false });
    const step = Math.max(1, Math.min(5, parseInt(hit[2], 10) || 1));
    return json(200, { ok: true, found: true, service: hit[1] || "", step, stepName: hit[3] || "", status: hit[4] || "", updated: hit[5] || "", note: (hit[6] || "").slice(0, 400) });
  } catch (e) {
    console.log("track error", e && e.message);
    return json(200, { ok: false, reason: "unavailable" });
  }
};

export const config = { path: "/api/track" };
