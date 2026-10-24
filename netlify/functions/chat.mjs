// El Harmawy website assistant — Netlify Function calling the Claude API.
// Needs env var ANTHROPIC_API_KEY (set in Netlify > Site configuration > Environment variables).
const MODEL = process.env.CHAT_MODEL || "claude-haiku-5-5";
const MAX_TURNS = 12;          // messages kept per conversation
const MAX_CHARS = 1200;        // per user message

const SYSTEM = `You are the website assistant of El Harmawy Business Consultancy F.Z.E (HBC), Ajman Free Zone, UAE. Licence No. 58667.
Slogan: We Handle It, You Grow.
Reply in the visitor's language: Arabic (simple, friendly Gulf/Egyptian-neutral Arabic) or English. Keep answers short: 2–5 sentences or a short list.

What HBC does:
- Business setup / company formation in UAE free zones and mainland (trade name, licence, office, investor visa). Company setup packages start from AED 4,455 (final price depends on free zone, activity and visas).
- PRO & government services: licence renewals and amendments, visas and Emirates ID, labour and immigration transactions, document attestation.
- Business consultancy: business plans, feasibility studies, pricing, growth strategy.
- HR consultancy: structure, job descriptions, policies, contracts, recruitment support.
- Procurement consulting and sourcing from China with shipping to the UAE.
- Marketing & online advertising, public relations.
- E-commerce: Amazon & Noon store set-up and management.
- VAT and corporate tax filings are handled in coordination with FTA-approved tax agents (HBC is not itself a tax agent).

How HBC works: first call to understand the need, written scope and quote before any work, delivery with updates, follow-up.
Contact: WhatsApp/phone +971 56 346 9000 · info@elharmawy.com · www.elharmawy.com · C1 Building, Ajman Free Zone.
Founder: Ahmed Saeed El Harmawy.

Rules:
- Never invent prices, government fees, timelines or legal requirements beyond what is written above. If asked, say the team will send an exact written quote and invite them to the quote form (#register on the site) or WhatsApp.
- Do not give legal or tax advice; explain generally and refer them to the team.
- When the visitor wants to start, ask for their name and WhatsApp number or direct them to WhatsApp +971 56 346 9000.
- Stay on topic (HBC services and doing business in the UAE). Politely decline unrelated requests.`;

const headers = { "Content-Type": "application/json", "Cache-Control": "no-store" };

export default async (req) => {
  if (req.method === "GET") {
    const k = (process.env.ANTHROPIC_API_KEY || "").trim();
    return new Response(JSON.stringify({ ok: !!k }), { headers });
  }
  if (req.method !== "POST") return new Response("Method not allowed", { status: 405 });
  const key = (process.env.ANTHROPIC_API_KEY || "").replace(/\s+/g, "");
  if (!key) return new Response(JSON.stringify({ error: "not_configured" }), { status: 503, headers });
  let body;
  try { body = await req.json(); } catch { return new Response(JSON.stringify({ error: "bad_json" }), { status: 400, headers }); }
  const msgs = (Array.isArray(body.messages) ? body.messages : [])
    .filter(m => m && (m.role === "user" || m.role === "assistant") && typeof m.content === "string")
    .slice(-MAX_TURNS)
    .map(m => ({ role: m.role, content: m.content.slice(0, MAX_CHARS) }));
  if (!msgs.length || msgs[msgs.length - 1].role !== "user") return new Response(JSON.stringify({ error: "no_message" }), { status: 400, headers });
  while (msgs.length && msgs[0].role !== "user") msgs.shift();
  try {
    const payload = JSON.stringify({ model: MODEL, max_tokens: 450, system: SYSTEM, messages: msgs });
    const base = { "anthropic-version": "2023-06-01", "content-type": "application/json" };
    const call = (auth) => fetch("https://api.anthropic.com/v1/messages", { method: "POST", headers: { ...base, ...auth }, body: payload });
    let r = await call({ "x-api-key": key });
    if (r.status === 401) r = await call({ "Authorization": "Bearer " + key });
    const j = await r.json();
    if (!r.ok) return new Response(JSON.stringify({ error: "upstream", detail: j?.error?.type || r.status, msg: (j?.error?.message || "").slice(0, 200) }), { status: 502, headers });
    const text = (j.content || []).filter(c => c.type === "text").map(c => c.text).join("\n").replace(/\*\*(.+?)\*\*/g, "$1").replace(/^#+\s*/gm, "").replace(/^\s*[-*]\s+/gm, "• ").trim();
    return new Response(JSON.stringify({ reply: text }), { headers });
  } catch (e) {
    return new Response(JSON.stringify({ error: "network" }), { status: 502, headers });
  }
};

export const config = { path: "/api/chat" };
