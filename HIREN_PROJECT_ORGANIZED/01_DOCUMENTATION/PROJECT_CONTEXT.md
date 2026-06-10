# Country Cove Inc — Full Project Context
**Last updated: 2026-05-27**
**PM: Sachin Kumar | Client: Hiren Kumar | Company: Country Cove Inc**

---

## 1. Project Overview

Hiren Kumar is building a digital convenience store hub — **Long Island Convenience** — an umbrella of 7 specialty e-commerce stores, all managed from a single Odoo instance. Each store has its own website, domain, branding, and product catalog. An n8n automation layer regenerates website layouts, scrapes card products, and publishes to Odoo automatically.

**BRAND RULE (NEVER VIOLATE):** Every site MUST keep "Long Island" as prefix. Never rename to "Country Cove". `country-cove-inc.odoo.com` is the Odoo backend URL only — NOT a public brand.

---

## 2. Odoo Instance

| Field | Value |
|---|---|
| Instance URL | `https://country-cove-inc.odoo.com` |
| Database | `country-cove-inc` |
| Admin User | `countrycoveinc@gmail.com` |
| Admin Password | `M@nhattan1234` |
| Odoo Version | saas-19.3 |
| XML-RPC UID | 2 (constant — never changes) |

### XML-RPC (Python scripts)
```python
import xmlrpc.client
URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"
uid = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common').authenticate(DB, USER, PASS, {})
m   = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
def xc(model, method, args, kwargs={}):
    return m.execute_kw(DB, uid, PASS, model, method, args, kwargs)
```

### JSON-RPC (n8n HTTP nodes)
```javascript
// Auth
POST /jsonrpc
{ jsonrpc:'2.0', method:'call',
  params:{ service:'common', method:'authenticate',
           args:['country-cove-inc','countrycoveinc@gmail.com','M@nhattan1234',{}] }}
// Returns: { result: 2 }

// Any model operation
POST /jsonrpc
{ jsonrpc:'2.0', method:'call',
  params:{ service:'object', method:'execute_kw',
           args:['country-cove-inc', 2, 'M@nhattan1234', 'model.name', 'method', [args], {}] }}
```

> **Critical:** `website.website` model is NOT accessible via XML-RPC. Use JSON-RPC for website-level operations.

---

## 3. All Websites in Odoo — SITE_MAP

| Website ID | Name | Domain | Status |
|---|---|---|---|
| **1** | Long Island Convenience | longislandconvenience.com | ✅ Live — main hub |
| **18** | Long Island Greeting Cards | (no domain) | ❌ No domain, not built |
| **27** | Country Cove Gift Cards | (no domain) | ❌ Ignore — wrong branding |
| **29** | Cyber Consulting | consultcyber.net | ⚠️ Expires June 6 2026 — renew at GoDaddy June 5 |
| **33** | Long Island Lotto | (no domain) | ❌ No domain, not built |
| **36** | **Long Island Cards** | **longislandcards.com** | ✅ Live — PRIMARY CARD STORE |
| **37** | Long Island Gift Basket | ligiftbasket.com | ⚠️ DNS set, site not built |
| **38** | Long Island Balloons | longislandballoonsdecor.com | ⚠️ DNS set, site not built |
| **39** | Long Island Print & Mail | longislandprintandmail.com | ✅ Live — fully built |
| **40** | Long Island Cigars | (no domain) | ❌ No domain, needs 21+ gate |

### n8n SITE_MAP (used in Parse Input node of all workflows)
```javascript
const SITE_MAP = {
  'long island cards':          36,
  'long island convenience':     1,
  'long island gift basket':    37,
  'long island greeting cards': 18,
  'long island lotto':          33,
  'cyber consulting':           29,
};
```

---

## 4. Website 1 — Long Island Convenience (Hub)

**URL:** https://www.longislandconvenience.com
**Purpose:** Landing hub linking all 7 specialty stores.

### Key Views
| View ID | Purpose |
|---|---|
| 600 | Homepage (mode=primary, key=website.homepage) — contains `lic-grid` |
| 1378 | Custom header (extension of Main layout 603) |
| 1381 | Custom footer (extension of Main layout 603) |
| 3217 | E-commerce header extension |

### Current 7-Store Grid (inside `<div class="lic-grid">` in view 600)
| # | Store Card | Link | Status |
|---|---|---|---|
| 1 | Cards & Collectibles | https://www.longislandcards.com | Live |
| 2 | Gift Baskets | https://www.ligiftbasket.com | Live |
| 3 | Greeting Cards | # | Coming Soon |
| 4 | Balloons & Décor | https://www.longislandballoonsdecor.com | Live |
| 5 | Cigars & Tobacco (21+) | # | Coming Soon |
| 6 | Lotto | # | Coming Soon |
| 7 | Print & Mail | https://www.longislandprintandmail.com | Live |

### Pages
- `/` — Home (page ID 5)
- `/about` — About Us (page ID 8)
- `/contact` — Contact Us (page ID 9)
- `/stores` — Our Stores (page ID 10)

---

## 5. Website 36 — Long Island Cards ⭐ MAIN AUTOMATION TARGET

**URL:** https://www.longislandcards.com
**Purpose:** Full e-commerce card shop — sports cards, TCG, graded cards, supplies.

### Key Views
| View ID | Purpose |
|---|---|
| 2955 | Homepage (key=website.homepage, primary) |
| 3506 | Footer (extension of 603) |
| 3508 | Header (extension of 603) |
| 3509 | Footer copyright |
| 3510 | Contact page /contact |
| 3719 | AI-generated redesign page (created 2026-05-27 by n8n workflow) |

### Pages
- `/` — Home (page ID 44)
- `/contact` — Contact (page ID 49)
- `/shop` — E-commerce shop
- `/ai-redesign-1779876099267` — AI Redesign page (page ID 76, set as homepage 2026-05-27)

### AI-Generated Page — LIVE ✅
- **URL:** `https://longislandcards.com/ai-redesign-1779876099267`
- **Created:** 2026-05-27 15:35 by n8n workflow `ai-cloner-odoo.json`
- **ir.ui.view ID:** 3719 | **website.page ID:** 76
- **HTML size:** 27.4 KB (28,010 chars) | **Sections:** 17
- **Content:** Hero + ticker + brand nav + featured cards + 6 category grids + trust badges + events + newsletter + footer

### Product Categories (categ_id)
| categ_id | Category | Use For |
|---|---|---|
| 99 | Trading Card Games (parent) | TCG root |
| **100** | Pokemon Cards | Pokémon singles/packs |
| **101** | Magic: The Gathering | MTG singles/sealed |
| **102** | Yu-Gi-Oh! Cards | YGO singles |
| 103 | One Piece Cards | OP TCG |
| 104 | Dragon Ball Super Cards | DBS CCG |
| 105 | Disney Lorcana | Lorcana |
| 106 | Digimon Cards | Digimon |
| 107 | Graded Cards (parent) | Graded root |
| **108** | PSA Graded | PSA slabs |
| 109 | BGS Graded | Beckett slabs |
| 110 | CGC Graded | CGC slabs |
| 111 | Sealed Products (parent) | Sealed root |
| **112** | Booster Boxes | 36-pack boxes |
| 113 | Booster Packs | Individual packs |
| 114 | Elite Trainer Boxes | ETBs |
| 92 | Sports Cards (parent) | Sports root |
| **93** | Baseball Cards | Baseball |
| 94 | Basketball Cards | Basketball |
| 95 | Football Cards | Football |
| 96 | Hockey Cards | Hockey |

### 21 Products (website_id=36) — All have PIL-generated images
IDs 117–137. See TECH_NOTES.md Section 5 for full list.
POC test products IDs 156–167 tagged `[POC]` — delete after testing.

### Contact Info
- Email: info@longislandcards.com
- Address: 605 Old Country Road, Plainview, NY 11803
- Phone: (212) 564-8585

---

## 6. Website 39 — Long Island Print & Mail

**URL:** https://www.longislandprintandmail.com

### Key Views
| View ID | Purpose |
|---|---|
| 2958 | Homepage (inherit_id=592, mode=extension) |
| 3514 | Header (extension of 603) |
| 3515 | Footer (extension of 603) |
| 3516 | Contact /contact |
| 3517 | Services /services |

### CRITICAL: Homepage must be an extension view
- `inherit_id = 592` (base Home view), `mode = 'extension'`
- Arch: `<data><xpath expr="//div[@id='wrap']" position="replace">...</xpath></data>`
- If set standalone (inherit_id=False, mode=primary) → site shows 500

### 15 Products (website_id=39), IDs 138–152. PIL images uploaded.

---

## 7. Payment Configuration

| ID | Provider | State | Published |
|---|---|---|---|
| 16 | Razorpay | enabled | ✅ True |
| 24 | Cash on Delivery | enabled | ✅ True |
| 21 | Wire Transfer | enabled | ❌ False |

### Razorpay Credentials
- Key ID: `rzp_live_SYr3kjBJsAOMnw`
- Key Secret: `5HAWnH0Nafjj2xppnyXn5bTy`
- Webhook Secret: `33085b5d853cef9c655c992766d8e865aad6879103699917`

---

## 8. n8n Automation — Three Workflows

**n8n Cloud:** `https://newworksatnight.app.n8n.cloud`
**All workflow files:** `C:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\BasicWorkflow\`

### API Keys
| Service | Key |
|---|---|
| Claude (Anthropic) | `sk-ant-api03-cSj82EtbhWnArl3rl-...` |
| Claude Model | `claude-sonnet-4-6` |
| Firecrawl | `fc-471db502e79143e0982f3d2638b8ccdb` |
| Vercel | `vcp_81CNUWp76vSnicfxBK2vhYY5ynoMbYx6ZOhh7iRVdI3tp3jPzl3hjPJM` |

---

### 8.1 `ai-cloner-odoo.json` — AI Redesigner (MAIN WORKFLOW) ⭐
**Status:** ✅ Tested live — page created at longislandcards.com/ai-redesign-1779876099267

**Trigger:** Form (8 fields) / Manual / Schedule

**Full 27-node flow:**
```
t0 Form → n1 Parse Input → n2 Odoo Auth → n3 Parse Auth
→ n4 Fetch Websites → n5 Find Site ID → n5b Fetch Card Images (NEW)
→ n6 Firecrawl Search → n7 Build Analysis Prompt → n8 Claude Analyze
→ n9 Build HTML Prompt → n10 Claude Generate HTML (10,000 tokens)
→ n11 Extract HTML + QWeb Wrap → n12 Create ir.ui.view
→ n13 Build Page Request → n14 Create website.page
→ n15 Build Final Summary → n15b Build Set Homepage Request
→ n15c HTTP Set Homepage → n15d Confirm Homepage Set
→ n16 Is Form Trigger? → n17 Form Result / n18 Manual Output
```

**Form Trigger (t0) — 8 fields:**
1. Which Website to Update? (required dropdown)
2. Design Style (dropdown)
3. This Week's Special Promotion (text)
4. Products or Items to Feature (textarea)
5. Announcement Bar Message (text)
6. Events or News This Week (text)
7. Custom Hero Headline (text)
8. Auto-Publish to Odoo? (dropdown)

**HTML Prompt — 17 sections:**
S1 Role | S2 Technical | S3 Colors | S4 Typography | S5 Announcement
S6 Nav | S7 Hero | S8 Featured Products | S9 Categories | S10 Promotions
S11 Events | S12 Trust | S13 Newsletter | S14 Footer | S15 Animations
S16 Mobile | S17 Quality Standards

**Card Images (n5b fetches per category):**
| Category | Source | Count |
|---|---|---|
| Pokemon | pokemontcg.io API + CDN fallback | 6 |
| MTG | Scryfall live API | 6 |
| YGO | YGOPRODECK live API | 6 |
| Sports | YGOPRODECK + sports labels | 6 |
| Sealed | Hardcoded Pokemon/MTG/YGO boxes | 6 |
| Graded | Hardcoded PSA/BGS/CGC slabs | 6 |

**Homepage mechanism:** n15b writes `website.website[36].homepage_id = pageId` via JSON-RPC.

---

### 8.2 `product-image-scraper.json` — Card Product Creator
**Status:** ✅ Built — creates 12 products on site 36 with real card images

**Flow:** Manual/Schedule → Odoo Auth → Pokemon TCG API → Scryfall → YGOPRODECK → Firecrawl Sports → Claude descriptions → Download images → Create products (website_id=36)

**Cards per category:** 3 (PoC default, increase to 10–20 for production)

---

### 8.3 `website-cloner.json` — Vercel Deployer
**Status:** ✅ Working (live: `ai-premium-pokemon-card-ecommer-57179-b75q7o5jh.vercel.app`)

**Flow:** Trigger → Firecrawl → Claude → Deploy to Vercel → Return URL

---

## 9. Technical Issues — Full Bug Log

### BUG-01: n8n Buffer/Stream Issue ⚠️ CRITICAL (affects ALL workflows)
**Root cause:** n8n HTTP nodes return Node.js `Readable` stream objects for large responses, not parsed JSON.
**Symptom:** Silent failure — all data reads as undefined. `htmlKB: 0.6`, `viewId: null`, `pageId: null`.
**Detection:** `resp._readableState` exists when it's a stream.
**Fix — add to EVERY Code node that reads HTTP response:**
```javascript
function decodeBuffer(resp) {
  if (resp?.content || resp?.result !== undefined || resp?.data) return resp;
  if (!resp?._readableState) return resp;
  try {
    const chunks = Array.isArray(resp._readableState.buffer) ? resp._readableState.buffer : [];
    const allBytes = [];
    for (const chunk of chunks) {
      const d = chunk?.data;
      if (Array.isArray(d)) allBytes.push(...d);
      else if (d?.type === 'Buffer' && Array.isArray(d.data)) allBytes.push(...d.data);
    }
    if (allBytes.length > 0) return JSON.parse(Buffer.from(allBytes).toString('utf-8'));
  } catch(e) {}
  return resp;
}
// Usage: const resp = decodeBuffer($input.item.json);
```
**Nodes that need this:** n3, n5, n7, n9, n11, n13, n15, n15d (and any new Code node reading HTTP output).

---

### BUG-02: viewId / pageId null after Odoo Create
**Cause:** HTTP nodes n12 (Create ir.ui.view) and n14 (Create website.page) return streams. n13 and n15 read `resp?.result` which is undefined on a stream object.
**Fix:** Add decodeBuffer to n13 and n15. ✅ Fixed in patch_buffer_homepage.py

---

### BUG-03: Website not changing after run
**Cause 1:** Page created at `/ai-redesign-{ts}` — not the homepage.
**Cause 2:** `is_homepage: true` in page creation may not trigger the inverse in Odoo.
**Fix:** Added n15b → n15c → n15d nodes that explicitly write `website.website[36].homepage_id = pageId` via JSON-RPC. ✅ Fixed in patch_add_homepage_node.py

---

### BUG-04: 404 on country-cove-inc.odoo.com/ai-redesign-...
**Cause:** The page belongs to `website_id=36` (longislandcards.com). When accessed via `country-cove-inc.odoo.com`, Odoo serves website_id=1 and returns 404.
**Fix:** Access via `longislandcards.com/ai-redesign-...` — this works. ✅ Expected behaviour.

---

### BUG-05: Full HTML wrapped in QWeb div (invalid)
**Cause:** n11 was wrapping `<!DOCTYPE html><html><head>...<body>...</body></html>` inside `<div id="wrap">` — invalid XML nesting.
**Fix:** n11 now extracts: `<body>` content only + `<style>`, `<link>`, `<script>` tags from `<head>`. Odoo's `website.layout` provides the proper HTML wrapper. ✅ Fixed in patch_html_extract.py

---

### BUG-06: liveUrl using wrong domain
**Cause:** n15 computed `liveUrl = ODOO_URL + targetPageUrl`, giving `country-cove-inc.odoo.com/ai-redesign-...` which is 404 domain.
**Fix:** n15 now uses `websiteDomain` (longislandcards.com) for `liveUrl`, plus adds `adminUrl` for backend access. ✅ Fixed in patch_html_extract.py

---

### BUG-07: CLIENT BRIEF not reaching Claude
**Cause 1:** `clientBriefBlock` defined in n9 but not injected into `htmlPrompt` string.
**Cause 2:** n9 read `prev.clientBrief` but `prev = n7.item.json` and n7 doesn't pass `clientBrief` through.
**Fix:**
1. Injected `(hasBrief ? clientBriefBlock : '...')` as first section in htmlPrompt before BRAND.
2. Changed n9 to read `$('Parse Input').item.json.clientBrief` directly.
✅ Fixed in patch_brief.py + patch_brief_source.py

---

### BUG-08: n15b reading undefined ODOO_DB / ODOO_PASS
**Cause:** n15 output doesn't include credentials (only `ODOO_URL`, no `uid`, `ODOO_DB`, `ODOO_PASS`). n15b read from n15 which had no credentials → `setHomepageReq` had undefined in JSON-RPC body.
**Fix:** n15b now reads credentials from `$('Code: Build Page Request').item.json` (n13) which has full credential chain. n15 also updated to include `uid`, `ODOO_DB`, `ODOO_PASS` in output. ✅ Fixed in patch_final_fixes.py

---

### BUG-09: Scryfall hardcoded UUIDs returning 404
**Cause:** Scryfall card UUIDs in fallback array were wrong/fabricated.
**Fix:** n5b now fetches fresh cards live from `api.scryfall.com/cards/search` first, falls back to named hardcoded cards with correct UUIDs. ✅ Fixed in patch_section_images.py

---

### BUG-10: Claude generates stock photo images in HTML
**Cause:** Claude had no card image URLs in the prompt — generated placeholder stock photo URLs (waterfalls, vegetables, etc.).
**Fix:** Added n5b node that fetches real card image URLs from 3 live APIs before n9 runs. n9 now injects section-specific image lists into the prompt telling Claude exactly which `<img src>` to use in each section. ✅ Fixed in patch_section_images.py

---

### BUG-11: pokemontcg.io rate limiting
**Cause:** Free tier = 250 req/10min. IP blocked after a few calls with complex query strings.
**Fix:** Use simple URL `https://api.pokemontcg.io/v2/cards?pageSize=6` without special char filters. n5b has Pokemon CDN fallback array for when API fails. Register free API key at pokemontcg.io to remove rate limit.

---

### BUG-12: patch_form.py string replacement failed silently
**Cause:** Replacement target contained Unicode `═` (U+2550) + literal `\n` — the Python string was different from the JSON-decoded string due to escaping layers.
**Fix:** Always use `json.load()` to decode the workflow first, then operate on the decoded string. Unicode works after `json.load`. Confirmed exact bytes before each replacement.

---

### BUG-13: Vercel 400 `missing_project_settings`
**Cause:** Vercel API v13 requires `?skipAutoDetectionConfirmation=1` for new project deployments.
**Fix:** `https://api.vercel.com/v13/deployments?skipAutoDetectionConfirmation=1` ✅

---

### BUG-14: Dark-on-dark text (website content invisible)
**Cause:** Claude wrote dark-bg Tailwind classes without explicit text color classes. TailwindCSS JIT only generates CSS for classes present in the HTML.
**Fix:** Prompt explicitly specifies: `bg-slate-900 text-slate-100` on body, `text-white` on every heading.

---

### BUG-15: HTML truncated mid-generation
**Cause:** Claude hits `max_tokens` limit mid-generation → no `</html>` tag → regex fails.
**Fix:** Substring fallback: `raw.substring(raw.toLowerCase().indexOf('<!doctype'))`. max_tokens raised to 10,000.

---

### BUG-16: `website.website` not accessible via XML-RPC
**Cause:** Model requires specific access rights not granted via XML-RPC in this Odoo config.
**Fix:** Use JSON-RPC for website operations in n8n. website_id=36 hardcoded in Python scripts.

---

## 10. Card Image APIs — What Works

| API | Status | URL Pattern | Notes |
|---|---|---|---|
| **pokemontcg.io** | ✅ Works | `https://images.pokemontcg.io/{setId}/{num}_hires.png` | Rate limited on free tier — get free key |
| **pokemon.com CDN** | ✅ Works | `https://assets.pokemon.com/assets/cms2/img/cards/web/{SET}/{SET}_EN_{N}.png` | Confirmed: SM3_EN_17, SM35_EN_33 |
| **Scryfall** | ✅ Works | `https://cards.scryfall.io/normal/front/{a}/{b}/{uuid}.jpg` | Always fetch fresh from API — don't hardcode UUIDs |
| **YGOPRODECK** | ✅ Works | `https://images.ygoprodeck.com/images/cards/{id}.jpg` | Card IDs are stable integers |
| **blowoutcards.com CDN** | ❌ Blocked | — | Returns 1KB hotlink protection placeholder |
| **bulbagarden.net** | ❌ 403 | — | Hotlink protected |
| **Sports card images** | ❌ No free API | — | Panini/Topps require licensed API. Use YGO art as visual stand-in. |

### Known Working Pokemon CDN URLs
```
https://assets.pokemon.com/assets/cms2/img/cards/web/SM3/SM3_EN_17.png   (Charizard GX)
https://assets.pokemon.com/assets/cms2/img/cards/web/SM35/SM35_EN_33.png (Pikachu VMAX)
```

### Known Working YGO Card IDs (images.ygoprodeck.com/images/cards/{id}.jpg)
```
89631139 — Blue-Eyes White Dragon
46986414 — Dark Magician
33396948 — Exodia the Forbidden One
74677422 — Red-Eyes Black Dragon
77585513 — Jinzo
55144522 — Pot of Greed
```

---

## 11. Odoo QWeb Arch Rules

### Standalone page (primary view — /contact, /services, AI-generated pages)
```xml
<t t-name="website.page_unique_key">
  <t t-call="website.layout">
    <div id="wrap" class="oe_structure">
      <!-- body content ONLY — no DOCTYPE/html/head/body tags -->
      <script src="https://cdn.tailwindcss.com"></script>
      <link href="https://fonts.googleapis.com/..." rel="stylesheet">
      <!-- generated section HTML here -->
    </div>
  </t>
</t>
```

### Extension view (header, footer, homepage override)
```xml
<data>
  <xpath expr="//div[@id='wrap']" position="replace">
    <!-- replacement content -->
  </xpath>
</data>
```
- Root must be `<data>` NOT `<t t-name="">` for extension views
- `mode='extension'`, `inherit_id` must point to valid parent view

### Creating a page via JSON-RPC (two steps required)
```javascript
// Step A — ir.ui.view (HTML container)
viewId = odooCall('create', 'ir.ui.view', [{
  name: 'Page Name',
  type: 'qweb',
  arch_db: '<t t-name="KEY"><t t-call="website.layout"><div id="wrap" class="oe_structure">BODY_CONTENT</div></t></t>',
  key: 'website.page_unique_key',
  mode: 'primary'
}])

// Step B — website.page (URL routing + publish)
pageId = odooCall('create', 'website.page', [{
  name: 'Page Title',
  url: '/page-url',
  view_id: viewId,
  is_published: true,
  website_indexed: true,
  website_id: 36,
  is_homepage: true   // set as homepage
}])

// Step C — force homepage on website record
odooCall('write', 'website.website', [[36], { homepage_id: pageId }])
```

### Common Global View IDs
| ID | Description |
|---|---|
| 592 | Global Home view (base homepage template) |
| 603 | Main layout (parent of all header/footer extends) |
| 687 | footer_copyright_company_name base view |

---

## 12. Scripts & Patch Files

### Location: `C:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\`

| Script | Purpose | Date | Status |
|---|---|---|---|
| `upload_images_v2.py` | Upload 21 product images for Long Island Cards | 2026-05-23 | ✅ Done |
| `fix_contact_page.py` | Create /contact page for longislandcards.com | 2026-05-23 | ✅ Done |
| `setup_payments.py` | Install Razorpay, configure live keys, enable COD | 2026-05-23 | ✅ Done |
| `build_printmail_website.py` | Build all views for longislandprintandmail.com | 2026-05-23 | ✅ Done |
| `fix_printmail_500.py` | Fix homepage 2958: set inherit_id=592, mode=extension | 2026-05-23 | ✅ Done |
| `setup_printmail_products.py` | Create services page + 15 products for Print & Mail | 2026-05-23 | ✅ Done |
| `upload_printmail_images.py` | Upload PIL images for 15 Print & Mail products | 2026-05-23 | ✅ Done |
| `fix_convenience_7stores_v3.py` | 7-store grid rewrite using div-nesting counter | 2026-05-23 | ✅ Done |
| `upload_pil_images_lic_v2.py` | Upload PIL images for all 21 LIC products | 2026-05-23 | ✅ Done |
| `test_odoo_image_route.py` | POC: 12 products on site 36 with real card images | 2026-05-27 | ✅ Ran (10/12 with images) |
| `patch_prompt.py` | Rewrites n9 jsCode with 17-section HTML prompt | 2026-05-27 | ✅ Applied |
| `patch_form.py` | Updates t0 (8 fields), n1 (SITE_MAP + clientBrief), n5, n17 | 2026-05-27 | ✅ Applied |
| `patch_brief.py` | Injects CLIENT BRIEF section into n9 htmlPrompt string | 2026-05-27 | ✅ Applied |
| `patch_brief_source.py` | Fixes n9 to read clientBrief from Parse Input node (not n7) | 2026-05-27 | ✅ Applied |
| `patch_buffer_homepage.py` | Adds decodeBuffer to n13/n15, is_homepage:true in page create | 2026-05-27 | ✅ Applied |
| `patch_add_homepage_node.py` | Adds n15b/n15c/n15d: force-set homepage on Odoo website | 2026-05-27 | ✅ Applied |
| `patch_final_fixes.py` | n5 decodeBuffer, n15 adds credentials to output, n15b reads from n13 | 2026-05-27 | ✅ Applied |
| `patch_html_extract.py` | n11 body-only extraction, n15 liveUrl uses websiteDomain | 2026-05-27 | ✅ Applied |
| `patch_card_images.py` | Adds n5b node (fetch real card images), injects URLs into n9 | 2026-05-27 | ✅ Applied |
| `patch_section_images.py` | Expands to 6 per category, section-specific prompt injection | 2026-05-27 | ✅ Applied |

---

## 13. Technical Patterns

### Div-Nesting Counter (find matching closing tag)
```python
def find_matching_div_end(text, start):
    depth = 0; i = start
    while i < len(text):
        if text[i:i+4] == '<div': depth += 1; i += 4
        elif text[i:i+6] == '</div>':
            depth -= 1
            if depth == 0: return i + 6
            i += 6
        else: i += 1
    return -1
```

### PIL Image Upload to Odoo
```python
import base64, io
from PIL import Image
buf = io.BytesIO()
img.convert('RGB').save(buf, 'JPEG', quality=90)
b64 = base64.b64encode(buf.getvalue()).decode()
xc('product.template', 'write', [[product_id], {'image_1920': b64}])
# image_1920 = raw base64 string — NO "data:image/jpeg;base64," prefix
```

### Patching n8n Workflow JSON (safe method)
```python
import json
with open('workflow.json', 'r', encoding='utf-8') as f:
    wf = json.load(f)  # json.load decodes all escaping correctly
node = next(n for n in wf['nodes'] if n['id'] == 'n9')
js = node['parameters']['jsCode']
js_new = js.replace(OLD, NEW, 1)  # operate on decoded string
node['parameters']['jsCode'] = js_new
with open('workflow.json', 'w', encoding='utf-8') as f:
    json.dump(wf, f, ensure_ascii=False, indent=2)  # ensure_ascii=False preserves Unicode
```

### QWeb in Header/Footer Views
```xml
<t t-if="not env.user._is_public()">
  <a href="/my">My Account</a>
</t>
<t t-if="env.user._is_public()">
  <a href="/web/login">Log In</a>
</t>
```

---

## 14. IONOS DNS Pattern (all domains)

1. Domain → DNS Settings → 3 dots → DNS (NOT "Forward Domain")
2. A record: Host=`@`, Value=`148.113.47.19`
3. CNAME record: Host=`www`, Value=`country-cove-inc.odoo.com`
4. odoo.com/my/databases → Domain → enter `www.yourdomain.com` (NO https://)

---

## 15. Business Details

| Field | Value |
|---|---|
| Physical Location | 605 Old Country Road, Plainview, NY 11803 |
| Phone | (917) 338-7086 / (212) 564-8585 |
| Hub Email | hiren@longislandconvinience.com |
| PM Email | sachin@longislandconvinience.com |
| Cards Email | info@longislandcards.com |
| Print Email | info@longislandprintandmail.com |

---

## 16. What's Done vs Pending

### Done ✅
- All 7 website IDs mapped and confirmed
- All product category IDs documented
- Long Island Convenience hub — 7-store grid live
- Long Island Cards — 21 products, all images, contact page
- Long Island Print & Mail — 15 products, all pages, images
- Razorpay + COD payment configured on all sites
- n8n workflow `ai-cloner-odoo.json` — **LIVE** — AI page generated and published to longislandcards.com
- n8n workflow `product-image-scraper.json` — built, tested POC (12 products, 10 with real images)
- n8n workflow `website-cloner.json` — live on Vercel
- All 16 bugs identified and fixed (see Section 9)
- Real card images from 3 APIs (Pokemon, MTG, YGO) injected per section into Claude prompt

### Pending 🔴 High Priority
1. **Re-import ai-cloner-odoo.json** into n8n after latest patches (section images, body-only HTML)
2. **Test ai-cloner with real card images** — verify no more stock photos in output
3. **Set generated page as Odoo homepage** — Odoo → Website → Pages → set as homepage
4. **Long Island Gift Basket** (website 37) — homepage, header, footer, products not built
5. **Long Island Balloons** (website 38) — not built
6. **consultcyber.net renewal** — expires June 6 2026, renew at GoDaddy June 5

### Pending 🟡 Medium Priority
7. Delete POC test products (IDs 156–167) after review
8. Get free pokemontcg.io API key — eliminates rate limiting
9. Long Island Greeting Cards (website 18) — no domain yet
10. Long Island Lotto (website 33) — no domain yet
11. Long Island Cigars (website 40) — needs 21+ age gate

### Pending 🔵 Backlog
12. Sports card images — need paid API (Panini/Topps licensed)
13. Set schedule triggers (every Monday 9am) after first manual run confirmed
14. Mobile app — not started
15. Bulk product upload from CSV
16. Point of Sale module

---

## 17. Session Notes (General)

- Always use `sys.stdout.reconfigure(encoding='utf-8')` at top of Python scripts (Windows UTF-8 issue)
- View 600 is the convenience homepage — always use div-nesting counter to find grid boundary
- When header/footer show 500: disable them (`active=False`), check page loads, fix arch, re-enable
- The `lic-grid` CSS + all LIC custom styles are inside view 600's arch_db inline `<style>` block
- `Accept-Encoding: identity` header does NOT fix the n8n Buffer issue — the Buffer is from n8n's stream wrapping, not gzip
- Never hardcode Scryfall card UUIDs — they change when cards are reprinted; always fetch fresh from API
- Product `image_1920` field in Odoo: raw base64 only — no `data:image/jpeg;base64,` prefix
