// Runs automatically after every verified (non-spam) Netlify form submission.
// Forwards the lead to the Google Apps Script web app on info@elharmawy.com, which
// (1) adds a row to the "HBC Website Leads" sheet and (2) emails the client a confirmation.
// Needs env vars LEADS_WEBHOOK_URL and LEADS_SECRET (Netlify > Site configuration > Environment variables).
const FIELDS = ["name", "email", "phone", "company", "service", "language", "call_time", "message", "source",
  "offer", "setup_location", "setup_type", "setup_visas", "setup_activity", "setup_budget",
  "bank_emirate", "bank_company_status", "bank_activity",
  "acct_activity", "acct_monthly_transactions", "acct_bookkeeping", "acct_reports", "acct_vat", "acct_corporate_tax"];

export const handler = async (event) => {
  const url = (process.env.LEADS_WEBHOOK_URL || "").trim();
  const secret = (process.env.LEADS_SECRET || "").trim();
  if (!url || !secret) return { statusCode: 200, body: "not configured" };
  let payload;
  try { payload = JSON.parse(event.body).payload; } catch { return { statusCode: 200, body: "bad body" }; }
  if (!payload || payload.form_name !== "leads") return { statusCode: 200, body: "skip" };
  const d = payload.data || {};
  const lead = { secret, id: payload.id || "", created_at: payload.created_at || new Date().toISOString() };
  for (const k of FIELDS) lead[k] = String(d[k] ?? "").slice(0, 1500);
  try {
    await fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(lead), redirect: "manual" });
  } catch (e) { console.log("leads webhook failed", e && e.message); }
  return { statusCode: 200, body: "ok" };
};
