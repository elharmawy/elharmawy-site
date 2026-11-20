# DESIGN.md — El Harmawy Business Consultancy (HBC)

The design system for everything HBC makes: the website (elharmawy.com), social posts and stories, LinkedIn, invoices and quotations, signs and print. Any person or AI producing HBC material reads this first. When this file and a request disagree, the owner's request wins; when this file and a generic design habit disagree, this file wins.

Source of truth: `site.css` tokens (website) and the six approved post styles in Drive folder "00 الستايلات المعتمدة للتصاميم (6 ستايلات - 13-11-2026)".

---

## 1. Visual theme and atmosphere

A UAE corporate-services firm that is calm, exact and approachable. Think of a well-kept government-services counter run by people who answer on WhatsApp: navy authority, gold warmth, light-grey order. Arabic first, English beside it. Numbers are the hero: prices, fees and steps are shown big and plainly, never hidden.

- Mood: trustworthy, direct, Gulf-professional, Egyptian-friendly voice in Arabic copy.
- Never: playful startup gradients, neon, glassmorphism, stock-photo smiles, dark "tech" themes, beige or pink grounds.

## 2. Colour palette and roles

| Token | Hex | Role |
|---|---|---|
| `navy` | `#011F43` | Primary. Headers, dark bands, headings on light, primary panels |
| `navy-2` | `#0A2E5C` | Hover and layered navy surfaces |
| `gold` | `#D3A45F` | Accent. Main buttons, key numbers on navy, rules, highlights |
| `gold-ink` | `#8A6420` | Gold text on white or light grey (passes contrast) |
| `ground` | `#F5F7FA` | Page ground. **Light grey, never beige or pink** |
| `paper` | `#FFFFFF` | Cards, header band, documents |
| `ink` | `#0E1B2C` | Body text on light |
| `muted` | `#4E5D72` | Secondary text on light |
| `line` | `#DCE2EA` | Borders and dividers |
| `on-navy` | `#EEF2F8` | Text on navy |
| `on-navy-muted` | `#B7C3D6` | Secondary text on navy |
| WhatsApp green | `#157347` | Floating WhatsApp button only |
| Verified blue | `#1DA1F2` | The verified tick beside the name in chat-style designs only |

Rules
- One accent: gold. No second accent colour.
- Gold text on light grounds uses `gold-ink`, never `gold`.
- Body text contrast at least 4.5:1; big numbers at least 3:1.
- No gradient text. No coloured glows.

## 3. Typography

| Use | Family | Weights |
|---|---|---|
| Arabic (all Arabic text, headings included) | Tajawal | 400, 500, 700, 800 |
| English display and headings | Red Hat Display | 600, 700, 800 |
| English body | Red Hat Text | 400, 500, 600 |
| Signature on documents | a handwritten script, red | 400 |

Fallbacks: `"Segoe UI", Tahoma, Arial, sans-serif`. Google Fonts is the only font host.

Scale (web)
- H1: clamp(32px, 4vw, 52px), line-height 1.12 (Arabic 1.3), weight 800.
- H2: clamp(28px, 3.2vw, 40px), weight 800.
- H3: 20–22px, weight 700.
- Body: 16–18px, line-height 1.6; running text max about 65 characters wide.
- Small print and footers: at least 12.5px.
- Prices and figures: tabular numbers, weight 800, set big.

Posts (1080×1350): headline 90–150px Tajawal 800; prices 110–200px; body 30–36px.

Rules
- Arabic headings: letter-spacing 0. English uppercase labels may use slight tracking.
- No eyebrow or kicker labels above headings on the website.
- Formal letters (Word/PDF): Arabic in a wide, heavy, large font; one letter per file.

## 4. Brand assets

- Logo: the HBC horizontal logo (HBC mark + "EL HARMAWY / BUSINESS CONSULTANCY F.Z.E / الهرماوي لاستشارات الأعمال"). White version on navy, colour version on light. Never redraw, recolour, stretch or crop it.
- Slogan: **We Handle It, You Grow** — English only, never translated.
- Approved stamp (since 24/10/2026): blue rectangular double-border stamp with logo, "License No. 58667", Ajman Free Zone. Used on documents only, rotated about −4°, about 85% opacity, over the signature.
- Watermark: every new page or design carries a light watermark. Pattern: "HBC · ELHARMAWY.COM" repeated diagonally (−24°), navy at 3.5–4.5% opacity on light, white at about 6% on navy; posts may add a large faint HBC mark in the centre.
- Contacts on designs: WhatsApp **+971 56 346 9000**, info@elharmawy.com, elharmawy.com. Ahmed's personal number appears only on his business card.

## 5. Components

Buttons
- Primary: gold fill `#D3A45F`, navy text, weight 700, radius 10px, padding 14px 22px. Hover: lighter gold and a 1px lift. Press: 1px down.
- Secondary: outline (1.5px on-navy at 35% on dark, `line` on light), same size.
- One main action per screen. On the website the main action is **WhatsApp**.

Cards
- White on light grey, 1px `line` border, radius 14px, soft shadow. Hover: border turns gold.
- No coloured top bars or side stripes on rounded cards.
- Icons sit beside their heading, not stacked in a tile above it.

Price block
- Label small (e.g., "شركة ذ.م.م"), figure huge and bold, "درهم" small beside it. Always say what is included and what is not.

Chat (WhatsApp style)
- Real WhatsApp proportions. HBC name with the **blue verified tick** beside it.
- Client messages on the sender side; HBC replies on the other side. Times small and grey.

Legal line (required)
- "الموافقات تخضع لقوانين دولة الإمارات" / "All services are subject to UAE laws and regulations and the decision of the competent authority." Underlined where space allows (web page heads, posts).

## 6. The six approved post styles

All six: 1080×1350, logo top, WhatsApp number bottom, legal line at the very bottom, watermark, Arabic copy in Egyptian dialect, prices from the official list only.

1. **Magazine (مجلة)** — light grey ground, logo top-right, double navy rule under the header, gold question line, giant navy headline, huge price with "درهم" in gold, three-column fact row with thin dividers, navy pill with the number.
2. **Official paper (ورقة رسمية)** — navy ground with a tilted white price-list sheet: gold top edge, "PRICE LIST · CITY · YEAR", ruled price rows, red circular "الهرماوي HBC" mark and an "El Harmawy" signature line.
3. **Dubai scene (مشهد دبي)** — night-navy Dubai skyline with a warm horizon glow, white headline with a gold question, two glass-outlined price cards, gold pill with the number.
4. **Question and answer (سؤال وجواب)** — navy top with a giant question (the key word in gold), diagonal gold band below with the answer and two navy price cards.
5. **WhatsApp chat (محادثة واتساب)** — phone frame on navy, real chat with the client question and HBC answers including the prices; verified tick beside the name; closing line "كلّمنا زي ما هو كلّمنا".
6. **Road map (خريطة الطريق)** — light ground, headline "طريقك … في N محطات بس", numbered navy-and-gold circles linked by a dotted gold path, step names and one-line details, then price cards.

## 7. Layout

- Website container 1120px, side gutter at least 20px (16px on phones).
- One idea per screen on the home page; the first screen holds the headline, slogan, one-line offer, the WhatsApp button and three true facts.
- Grids of 2–3 columns that stack to one column under 960px.
- Mobile first: check 390px and 340px; no sideways scrolling.
- Section rhythm: light grey sections, white cards, one navy band for emphasis, navy footer.

## 8. Depth and motion

- Shadows: soft and neutral (`0 18px 40px rgba(1,31,67,.10)`), never coloured.
- Motion is short and purposeful: hero entrance once (0.5–0.7s, ease-out), button lift on hover.
- No fade-in on scroll, no marquees, no autoplay carousels.
- Respect reduced-motion: everything still and visible.

## 9. Language rules

- HBC and Smart: Arabic and English. Arabic is shown first (RTL).
- Arabic copy: clear Egyptian dialect for social media; Modern Standard Arabic for legal lines and documents.
- Invoices and quotations: English (Arabic labels optional).
- Check before publishing: spelling, the names "الهرماوي" and "HBC", the logo, prices and every number.

## 10. Do and don't

Do
- Show real prices from the official list, with what they include.
- Keep the logo, colours and slogan exactly as given.
- Put the WhatsApp number on every design.
- Add the watermark and the legal line.

Don't
- Promise or guarantee approvals, visas or bank accounts.
- Describe HBC as a tax agent, or say it sells residencies.
- Use real government or bank logos, or flags carrying religious text.
- Invent reviews, testimonials, client names or numbers.
- Use beige, pink, neon, gradient text or dark "tech" looks.

## 11. Quick prompt for AI tools

> Design for El Harmawy Business Consultancy (HBC), a UAE company-setup and government-services firm in Ajman Free Zone. Navy #011F43, gold #D3A45F (gold text on light: #8A6420), light grey ground #F5F7FA, white cards. Arabic in Tajawal 800 for headlines, English in Red Hat Display. Arabic first, English beside it. Big clear prices with "درهم". Use the HBC logo as given, slogan "We Handle It, You Grow" in English only. WhatsApp +971 56 346 9000. Light diagonal watermark "HBC · ELHARMAWY.COM". Legal line "الموافقات تخضع لقوانين دولة الإمارات". No guarantees, no gradients, no beige, no stock photos. Use one of the six styles: magazine, official paper, Dubai scene, question and answer, WhatsApp chat, road map.
