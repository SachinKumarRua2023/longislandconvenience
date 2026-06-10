# Hiren Kumar Digital Transformation — Full Technical Reference

**Last updated:** 2026-05-27  
**PM:** Sachin Kumar (SeekHowItHRua)  
**Odoo backend:** `https://country-cove-inc.odoo.com`  
**n8n Cloud:** `https://newworksatnight.app.n8n.cloud`  
**Odoo UID (admin):** `2` (constant — never changes)

---

## 1. ALL LIVE WEBSITE IDs (Confirmed from Odoo)

| ID | Name | Domain | Notes |
|----|------|--------|-------|
| **1** | Long Island Convenience | longislandconvenience.com | Main hub site |
| **18** | Long Island Greeting Cards | — | Greeting cards store |
| **27** | Country Cove Gift Cards | — | Gift cards store |
| **29** | Cyber Consulting | consultcyber.net | Expires June 6 2026 — renew at GoDaddy |
| **33** | Long Island Lotto | — | Lotto site |
| **36** | **Long Island Cards** | **longislandcards.com** | **PRIMARY CARD STORE — all card automation targets this** |
| **37** | Long Island Gift Basket | — | Gift basket store |

> **RULE (NEVER VIOLATE):** Always keep "Long Island" prefix on ALL website names. Never rename any site to "Country Cove".  
> `country-cove-inc.odoo.com` is the Odoo backend URL only — it is NOT a public brand name.

### SITE_MAP (used in n1 Parse Input — all 3 workflows)
```javascript
const SITE_MAP = {
  'long island cards':         36,
  'long island convenience':    1,
  'long island gift basket':   37,
  'long island greeting cards': 18,
  'long island lotto':         33,
  'cyber consulting':          29,
};
```

---

## 2. ALL PRODUCT CATEGORY IDs (Live from Odoo)

### Card Store Categories (used for website_id=36)

| ID | Parent | Category Name | Use For |
|----|--------|---------------|---------|
| **99** | ROOT | Trading Card Games | TCG parent |
| **100** | Trading Card Games | Pokemon Cards | Pokémon singles/packs |
| **101** | Trading Card Games | Magic: The Gathering | MTG singles/sealed |
| **102** | Trading Card Games | Yu-Gi-Oh! Cards | YGO singles |
| **103** | Trading Card Games | One Piece Cards | One Piece TCG |
| **104** | Trading Card Games | Dragon Ball Super Cards | DBS CCG |
| **105** | Trading Card Games | Disney Lorcana | Lorcana |
| **106** | Trading Card Games | Digimon Cards | Digimon |
| **107** | ROOT | Graded Cards | Graded parent |
| **108** | Graded Cards | PSA Graded | PSA slabs |
| **109** | Graded Cards | BGS Graded | Beckett slabs |
| **110** | Graded Cards | CGC Graded | CGC slabs |
| **111** | ROOT | Sealed Products | Boxes/packs parent |
| **112** | Sealed Products | Booster Boxes | 36-pack boxes |
| **113** | Sealed Products | Booster Packs | Individual packs |
| **114** | Sealed Products | Elite Trainer Boxes | ETBs |
| **115** | ROOT | Card Accessories | Supplies parent |
| **119** | ROOT | Playing Cards | Bicycle etc. |
| **92** | ROOT | Sports Cards | Sports parent |
| **93** | Sports Cards | Baseball Cards | Baseball |
| **94** | Sports Cards | Basketball Cards | Basketball |
| **95** | Sports Cards | Football Cards | Football |
| **96** | Sports Cards | Hockey Cards | Hockey |
| **97** | Sports Cards | Soccer Cards | Soccer |
| **98** | Sports Cards | UFC & Boxing Cards | Combat sports |
| **41** | ROOT | Country Cove Sports & Cards | Alt sports parent |
| **42** | Country Cove Sports & Cards | Baseball Cards | (legacy — also used) |
| **43** | Country Cove Sports & Cards | Basketball Cards | |
| **48** | Country Cove Sports & Cards | Magic: The Gathering | |
| **47** | Country Cove Sports & Cards | Pokémon Cards | |

> **Recommended category IDs for n8n automation (use these):**  
> Pokemon = **100**, MTG = **101**, YGO = **102**, Sports Baseball = **93**, Sealed = **112**, Graded = **108**

---

## 3. ODOO CONNECTION — Exact Working Method

### Protocol: XML-RPC vs JSON-RPC

| Context | Protocol | Endpoint | Notes |
|---------|----------|----------|-------|
| Python scripts | **XML-RPC** | `/xmlrpc/2/` | Cannot access `website.website` model |
| n8n HTTP nodes | **JSON-RPC** | `/jsonrpc` | Works for all models including `website.website` |

### XML-RPC (Python scripts)
```python
import xmlrpc.client, base64

URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"

uid = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common').authenticate(DB, USER, PASS, {})
# uid = 2 (always)

m  = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
xc = lambda model, method, args, kwargs={}: m.execute_kw(DB, uid, PASS, model, method, args, kwargs)

# Create product with image (confirmed working 2026-05-27)
pid = xc('product.template', 'create', [{
    'name':             'Card Name',
    'type':             'consu',          # consumable = physical goods
    'sale_ok':          True,
    'list_price':       19.99,
    'standard_price':   9.99,             # cost = 50% of list
    'categ_id':         100,              # Pokemon Cards
    'description_sale': '<p>HTML description</p>',
    'website_id':       36,              # Long Island Cards — always use this
    'is_published':     True,
    'image_1920':       base64_string,   # raw b64, NO "data:image/jpeg;base64," prefix
}])

# Update image on existing product
xc('product.template', 'write', [[pid], {'image_1920': base64_string}])

# Read existing products on site 36
products = xc('product.template', 'search_read',
    [[['website_id', '=', 36]]],
    {'fields': ['id','name','list_price','categ_id'], 'limit': 50})
```

### JSON-RPC (n8n HTTP nodes)
```javascript
// Step 1 — authenticate
POST https://country-cove-inc.odoo.com/jsonrpc
Body: { "jsonrpc":"2.0", "method":"call",
  "params": { "service":"common", "method":"authenticate",
              "args": ["country-cove-inc","countrycoveinc@gmail.com","M@nhattan1234",{}] }}
// Returns: { "result": 2 }  ← uid always = 2

// Step 2 — any model operation
POST /jsonrpc
Body: { "jsonrpc":"2.0", "method":"call",
  "params": { "service":"object", "method":"execute_kw",
              "args": ["country-cove-inc", 2, "M@nhattan1234",
                       "product.template", "create", [{ ...vals }], {}] }}
```

### Creating an Odoo Website Page (two steps — both required)
```javascript
// Step A — create ir.ui.view with HTML content
viewId = odooCall('create', 'ir.ui.view', [{
    name:    'Long Island Cards Redesign',
    type:    'qweb',
    arch_db: '<t t-name="website.page_KEY"><t t-call="website.layout"><div id="wrap" class="oe_structure">YOUR_HTML</div></t></t>',
    key:     'website.page_unique_key_here',
    mode:    'primary'
}])

// Step B — create website.page (URL + routing + publish)
pageId = odooCall('create', 'website.page', [{
    name:            'Long Island Cards — AI Redesign',
    url:             '/ai-cards-redesign-1716800000000',
    view_id:         viewId,
    is_published:    true,
    website_indexed: true,
    website_id:      36   // Long Island Cards ALWAYS
}])
// Live at: https://country-cove-inc.odoo.com/ai-cards-redesign-{timestamp}
// To make it homepage: Odoo → Website → Pages → set as homepage (manual step)
```

---

## 4. CONFIRMED WORKING IMAGE SOURCES

### POC Test Results (2026-05-27 — 10/12 products created with real images on site 36)

| Source | Status | Image Size | Notes |
|--------|--------|-----------|-------|
| **Scryfall** (`cards.scryfall.io/normal/...`) | ✅ Works | 79–129KB | Best quality, always reliable |
| **YGOPRODECK** (`images.ygoprodeck.com/images/cards/...`) | ✅ Works | ~193KB | Excellent card art |
| **pokemon.com CDN** (`assets.pokemon.com/.../SM3/SM3_EN_17.png`) | ✅ Works | 195KB | Official art — URL must be exact set+number |
| **pokemon.com CDN** (`...SM35/SM35_EN_33.png`) | ✅ Works | 136KB | Pikachu VMAX |
| **pokemontcg.io API** | ⚠️ Rate limited | 807KB | Works first call, then blocks ~10min on free tier |
| **TCGDex** (`assets.tcgdex.net`) | ❌ 404 | — | URL format is invalid |
| **blowoutcards.com CDN** | ❌ Blocked | 1KB | Returns 1px hotlink-protection placeholder |
| **bulbagarden.net** | ❌ 403 | — | Hotlink protected |
| **Wikipedia CDN** | ❌ 400 | — | Blocked for programmatic access |

### Pokemon CDN URL Pattern
```
https://assets.pokemon.com/assets/cms2/img/cards/web/{SET}/{SET}_EN_{NUMBER}.png

Known working:
  SM3_EN_17    — Charizard GX (Burning Shadows)    195KB
  SM35_EN_33   — Pikachu VMAX                       136KB

Available set codes: Base, Jungle, Fossil, BW1–BW11, XY1–XY12, SM1–SM35, SWSH1–SWSH12
Note: Not all card numbers exist. Test URL before committing.
```

### Scryfall Image URL (always get fresh from API — UUIDs change)
```python
r = requests.get("https://api.scryfall.com/cards/search?q=f:modern+r:rare", timeout=15).json()
img = r['data'][0]['image_uris']['normal']
# Format: https://cards.scryfall.io/normal/front/{hex}/{hex}/{uuid}.jpg
```

### YGOPRODECK Image URL
```python
r = requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php?type=Effect%20Monster&level=7&num=3", timeout=15).json()
img = r['data'][0]['card_images'][0]['image_url']
# Format: https://images.ygoprodeck.com/images/cards/{card_id}.jpg
```

---

## 5. EXISTING PRODUCTS ON SITE 36 (Long Island Cards)

**Total: 21 products — ALL have images (from previous PIL scripts)**

| ID | Name | Category | Price |
|----|------|----------|-------|
| 117 | 2024-25 Panini Prizm Basketball Hobby Box | Country Cove Sports & Cards | $189.99 |
| 118 | 2024 Topps Baseball Series 1 Hobby Box | Country Cove Sports & Cards | $99.99 |
| 119 | 2024-25 Panini Donruss Football Hobby Box | Country Cove Sports & Cards | $119.99 |
| 120 | 2024-25 Upper Deck Hockey Series 1 | Country Cove Sports & Cards | $89.99 |
| 121 | Pokemon Prismatic Evolutions Booster Box | Trading Card Games / Pokemon | $169.99 |
| 122 | Pokemon Elite Trainer Box — Scarlet & Violet | Sealed Products / ETB | $59.99 |
| 123 | Pokemon Single Booster Pack | Trading Card Games / Pokemon | $5.99 |
| 124 | Pokemon Charizard ex PSA 10 | Graded Cards / PSA | $349.99 |
| 125 | MTG Duskmourn Draft Booster Box | Country Cove Sports & Cards | $124.99 |
| 126 | MTG Commander Precon Deck | Country Cove Sports & Cards | $44.99 |
| 127 | Yu-Gi-Oh! Burst Protocol Booster Box | Trading Card Games / Yu-Gi-Oh! | $89.99 |
| 128 | Yu-Gi-Oh! Blue-Eyes White Dragon PSA 9 | Graded Cards / PSA | $199.99 |
| 129 | One Piece Two Legends Booster Box | Trading Card Games / One Piece | $99.99 |
| 130 | Mike Trout 2011 Topps Update Rookie PSA 10 | Graded Cards / PSA | $499.99 |
| 131 | Luka Doncic Panini Prizm Rookie BGS 9.5 | Graded Cards / BGS | $379.99 |
| 132 | Ultra Pro 9-Pocket Binder (360 cards) | Card Accessories / Binders | $19.99 |
| 133 | Top Loaders 3x4 inch — 25 Pack | Card Accessories / Sleeves | $7.99 |
| 134 | Perfect Fit Inner Sleeves — 100 Pack | Card Accessories / Sleeves | $4.99 |
| 135 | Bicycle Playing Cards — 2 Deck Set | Playing Cards | $9.99 |
| 136 | Long Island Cards Sports Starter Pack | Sports Cards | $49.99 |
| 137 | Long Island Cards TCG Starter Bundle | Trading Card Games | $39.99 |

> **POC test products IDs 156–167 are tagged `[POC]` — delete from Odoo after testing**

---

## 6. THREE n8n WORKFLOWS — Current Status & Architecture

### 6.1 `website-cloner.json` — Vercel Site Deployer
**Status: ✅ Working** (deployed live: `ai-premium-pokemon-card-ecommer-57179-b75q7o5jh.vercel.app`)

**Flow:**
```
Form/Manual/Schedule → Firecrawl search top card stores → Claude Analyze design patterns
→ Claude Generate HTML (8000 tokens, 15-section homepage) → Deploy to Vercel → Return live URL
```

**Key config in Parse Input (n1):**
- `VERCEL_TOKEN`: `vcp_81CNUWp76vSn...`
- Vercel URL must end with: `?skipAutoDetectionConfirmation=1`

**Known issues fixed:** Buffer decoder on all 4 Code nodes, HTML truncation fallback, dark-on-dark Tailwind classes.

---

### 6.2 `ai-cloner-odoo.json` — Long Island Cards Page Publisher ⭐ MAIN WORKFLOW
**Status: ✅ Built, all patches applied, ready to import and test**

**Flow:**
```
Form (8 fields) / Manual / Schedule
→ n1: Parse Input + read client brief
→ n2: Odoo Authenticate
→ n3: Parse Auth
→ n4: Fetch all websites (JSON-RPC)
→ n5: Find site 36 (SITE_MAP shortcut or fuzzy search)
→ n6: Firecrawl search top card stores
→ n7: Build Analysis Prompt
→ n8: Claude Analyze (design patterns from top 5 stores)
→ n9: Build HTML Prompt (17 sections + CLIENT BRIEF injection)
→ n10: Claude Generate HTML (10,000 tokens, 17-section homepage)
→ n11: Extract HTML + wrap in Odoo QWeb layout
→ n12: Create ir.ui.view (Odoo)
→ n13: Build website.page request
→ n14: Create website.page on site 36
→ n15: Build Final Summary
→ n16: Is Form Trigger? (branch)
→ n17: Form: Show Result  OR  n18: Set: Manual Output
```

**Form Trigger (t0) — 8 fields:**
| # | Field | Type | Required |
|---|-------|------|----------|
| 1 | Which Website to Update? | Dropdown | ✅ Yes |
| 2 | Design Style | Dropdown | No |
| 3 | This Week's Special Promotion | Text | No |
| 4 | Products or Items to Feature | Textarea | No |
| 5 | Announcement Bar Message | Text | No |
| 6 | Events or News This Week | Text | No |
| 7 | Custom Hero Headline | Text | No |
| 8 | Auto-Publish to Odoo? | Dropdown | No |

**Client Brief Flow (how form data reaches Claude):**
```
t0 form → n1 reads all 8 fields → builds clientBrief object
→ n9 reads $('Parse Input').item.json.clientBrief
→ builds clientBriefBlock string from non-empty fields
→ hasBrief = clientBriefBlock.length > 0
→ htmlPrompt = '══ CLIENT BRIEF — FOLLOW EXACTLY ══\n' + (hasBrief ? clientBriefBlock : '(No brief — AI control)') + ... (rest of 17-section prompt)
→ Claude honors client brief FIRST before any default choices
```

**n9 HTML Prompt — 17 sections:**
S1 Role | S2 Technical | S3 Color System | S4 Typography | S5 Announcement Bar
S6 Navigation | S7 Hero | S8 Featured Products | S9 Categories | S10 Promotions
S11 Live Events | S12 Trust Signals | S13 Newsletter | S14 Footer | S15 Animations
S16 Mobile | S17 Quality Standards

**Critical fixes applied:**
- Buffer decoder in all Code nodes reading HTTP responses
- `$('Parse Input').item.json.clientBrief` — reads brief from correct node (not n7)
- CLIENT BRIEF section injected FIRST in htmlPrompt (before BRAND section)
- `max_tokens: 10000` (up from 8000) to prevent truncation on 17-section output
- HTML extraction: regex + `doctypeStart` substring fallback
- `website_id: 36` hardcoded in n14 website.page creation

**Output:** New page at `https://country-cove-inc.odoo.com/ai-cards-redesign-{timestamp}`

---

### 6.3 `product-image-scraper.json` — Card Product Creator with Real Images
**Status: ✅ Built, needs first run test**

**Flow:**
```
Manual Trigger / Schedule
→ Odoo Auth
→ Pokemon TCG API (3 cards, categ_id=100)
→ Scryfall MTG API (3 cards, categ_id=101)
→ YGOPRODECK API (3 cards, categ_id=102)
→ Firecrawl Sports search (3 cards, categ_id=93)
→ Aggregate all 12 cards
→ Claude: generate professional descriptions
→ Download images → base64
→ Create products: website_id=36, is_published=True
→ All 12 products live on longislandcards.com/shop
```

**Cards per category:** 3 (PoC default — increase after verification)

**website_id auto-lookup in Process node:**
```javascript
const websites = await odooCall('search_read', 'website.website', [[[]]], { fields: ['id','name','domain'] });
const cardsSite = websites.find(w => {
    const t = ((w.name||'') + ' ' + (w.domain||'')).toLowerCase();
    return t.includes('card') || t.includes('sport') || t.includes('tcg') || t.includes('longisland');
});
targetWebsiteId = cardsSite?.id; // = 36
```

---

## 7. WHAT FAILED AND WHY — Complete List

### F1: n8n Buffer/Stream issue ⚠️ CRITICAL — affects ALL workflows
**Root cause:** n8n HTTP nodes return Node.js `Readable` stream for large responses, not parsed JSON. Stream has `_readableState.buffer` with raw bytes.  
**Symptom:** Silent failure — `htmlKB: 0.6`, `sitesAnalyzed: 0`, all data lost.  
**Fix:** Add `decodeBuffer()` function to EVERY Code node that reads from HTTP nodes.
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
```

### F2: Vercel 400 `missing_project_settings`
**Root cause:** API v13 requires `?skipAutoDetectionConfirmation=1` for new projects.  
**Fix:** `https://api.vercel.com/v13/deployments?skipAutoDetectionConfirmation=1`

### F3: Website content invisible (dark on dark)
**Root cause:** Claude wrote dark-bg Tailwind classes without explicit text color classes. TailwindCSS JIT doesn't generate CSS for classes not in the HTML.  
**Fix:** Prompt specifies exact classes: `bg-slate-900 text-slate-100` on body, `text-white` on every heading.

### F4: HTML truncated — regex fails on incomplete HTML
**Root cause:** Claude hits `max_tokens` mid-generation. No `</html>` tag → regex `/(<!DOCTYPE...\/html>)/i` fails.  
**Fix:** Substring fallback: `raw.substring(raw.toLowerCase().indexOf('<!doctype'))`.

### F5: `Accept-Encoding: identity` did NOT fix Buffer issue
**Root cause:** Buffer is n8n's internal stream wrapping — not compression. This header is useless for this problem.

### F6: `website.website` not accessible via XML-RPC
**Root cause:** Model requires specific access rights not granted via XML-RPC.  
**Fix:** Use JSON-RPC in n8n for website lookup. For Python scripts, website_id=36 is hardcoded.

### F7: pokemontcg.io rate limiting
**Root cause:** Free tier = 250 req/10min. IP blocked after a few calls.  
**Fix:** Use simple URL without special char filters. Get free API key at pokemontcg.io.

### F8: blowoutcards.com CDN blocked
**Root cause:** Added hotlink protection — now returns 1KB placeholder.  
**Fix:** Use Scryfall (confirmed working) or official pokemon.com CDN.

### F9: CLIENT BRIEF not reaching Claude (fixed 2026-05-27)
**Root cause:** Two separate bugs:  
  1. `clientBriefBlock` was defined in n9 but NOT inserted into `htmlPrompt` string  
  2. n9 read `prev.clientBrief` from n7 output, but n7 never passes `clientBrief` through  
**Fix:**  
  1. Injected `(hasBrief ? clientBriefBlock : '...')` into htmlPrompt as FIRST section before BRAND  
  2. Changed n9 to read `$('Parse Input').item.json.clientBrief` directly from n1

### F10: Scryfall hardcoded UUIDs returning 404
**Root cause:** Scryfall card UUIDs change when cards are reprinted or re-indexed.  
**Fix:** Always get fresh UUIDs from the Scryfall search API — never hardcode them.

### F11: patch_form.py replacement failed silently
**Root cause:** Replacement string contained Unicode `═` (U+2550) characters and literal `\n` — escaped differently in Python vs JSON-decoded string.  
**Fix:** Used `json.load()` (which decodes Unicode properly) and confirmed exact byte pattern before replacing.

---

## 8. AUTOMATION VISION — Full Flow

```
TIER 1: Website UI Redesign (ai-cloner-odoo.json)
──────────────────────────────────────────────────
Trigger: Form (client fills brief) OR Schedule (every Monday 9am)
→ Client specifies: promotion, featured products, events, headline, style
→ Firecrawl scrapes TCGPlayer, TrollAndToad, StarCityGames, ChannelFireball, Dave & Adams
→ Claude analyzes competitor design patterns (S1–S5 analysis)
→ Claude generates 17-section homepage HTML (10,000 tokens, Tailwind + Rajdhani font)
  Sections: Announcement bar → Nav → Hero → Featured → Categories → Promotions
            → Events → Trust → Newsletter → Footer + full mobile + animations
→ ir.ui.view + website.page created on site 36
→ Live at longislandcards.com/ai-cards-redesign-{timestamp}
→ Admin sets as homepage when satisfied

TIER 2: Product Catalog (product-image-scraper.json)
──────────────────────────────────────────────────────
Trigger: Daily or on-demand
→ Pokemon TCG API: 3 Scarlet & Violet Rare cards (official images)
→ Scryfall MTG API: 3 Modern-legal Rare creatures (80–130KB images)
→ YGOPRODECK: 3 Level 8 Effect Monsters (~190KB images)
→ Firecrawl: searches custom URL for sports card listings
→ Claude: writes professional product descriptions per card
→ All 12 products → website_id=36, is_published=True
→ Visible immediately on longislandcards.com/shop

TIER 3: External Benchmark (website-cloner.json)
──────────────────────────────────────────────────
Trigger: On-demand
→ Any card store URL → Firecrawl → Claude → Vercel deploy
→ Returns live preview URL for design comparison
→ Use to benchmark quality vs TCGPlayer etc.
```

---

## 9. API KEYS — All Credentials

| Service | Value |
|---------|-------|
| **Anthropic Claude API Key** | `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` |
| **Claude Model** | `claude-sonnet-4-6` |
| **Firecrawl API Key** | `fc-471db502e79143e0982f3d2638b8ccdb` |
| **Vercel Token** | `vcp_81CNUWp76vSnicfxBK2vhYY5ynoMbYx6ZOhh7iRVdI3tp3jPzl3hjPJM` |
| **Odoo URL** | `https://country-cove-inc.odoo.com` |
| **Odoo DB** | `country-cove-inc` |
| **Odoo User** | `countrycoveinc@gmail.com` |
| **Odoo Password** | `M@nhattan1234` |
| **Odoo UID** | `2` (constant) |

---

## 10. n8n IMPORT GUIDE

**Steps — must delete old before importing new:**

1. Open n8n Cloud → find old workflow → click `⋮` → Delete
2. `+ New Workflow` → `⋮` → `Import from file`
3. Import in this order:
   - `BasicWorkflow/ai-cloner-odoo.json` ← most important
   - `BasicWorkflow/product-image-scraper.json`
   - `BasicWorkflow/website-cloner.json`
4. Toggle each workflow to **Active**
5. Test with Manual Trigger first — confirm no Buffer errors in execution log

**After importing ai-cloner-odoo.json, test the form:**
- Fill "This Week's Special Promotion" with something like: `Buy any booster box, get FREE sleeves`
- Fill "Products or Items to Feature" with: `Pokemon Prismatic Evolutions, MTG Duskmourn, YGO Burst Protocol`
- Fill "Events or News This Week" with: `Saturday Draft Tournament 2pm`
- Check that Claude's output contains those exact items

**Critical check after import:**  
- `HTTP: Deploy to Vercel` in website-cloner → URL must end with `?skipAutoDetectionConfirmation=1`
- `HTTP: Claude — Generate Cards Website HTML` in ai-cloner-odoo → `max_tokens: 10000`

**Form trigger URLs (once active in n8n):**
```
ai-cloner-odoo:         /form/redesign-cards
product-image-scraper:  /form/scrape-card-products
```

---

## 11. PATCH SCRIPTS (in HirenTask folder)

These Python scripts are used to safely edit n8n workflow JSON without breaking escaping.

| File | Purpose | Status |
|------|---------|--------|
| `patch_prompt.py` | Rewrites n9 jsCode with 17-section HTML prompt | ✅ Applied |
| `patch_form.py` | Updates t0 (8 fields), n1 (SITE_MAP + clientBrief), n5, n17 | ✅ Applied |
| `patch_brief.py` | Injects CLIENT BRIEF section into n9 htmlPrompt string | ✅ Applied |
| `patch_brief_source.py` | Fixes n9 to read clientBrief from Parse Input node (not n7) | ✅ Applied |
| `test_odoo_image_route.py` | POC: creates 12 products on site 36 with real card images | ✅ Ran — 10/12 with images |

---

## 12. WHAT'S NOT DONE YET

| Item | Priority | Notes |
|------|----------|-------|
| **Import updated workflows into n8n** | 🔴 High | Delete old → import all 3 from BasicWorkflow/ |
| **Test ai-cloner-odoo with Form Trigger** | 🔴 High | Fill all 8 fields, confirm brief appears in Claude output |
| **Set generated page as Odoo homepage** | 🔴 High | Manual: Odoo → Website → Pages → set as homepage |
| **Test product-image-scraper with Manual Trigger** | 🟡 Medium | Verify 12 products appear on site 36 |
| **Delete POC test products (IDs 156–167)** | 🟡 Medium | Tagged `[POC]` — delete via Odoo UI after review |
| **Pokemon TCG API key (free)** | 🟡 Medium | Register at pokemontcg.io — eliminates rate limit |
| **Sports card real images** | 🟡 Medium | Need Firecrawl `scrape` on product pages for `og:image` |
| **consultcyber.net domain renewal** | 🟡 Medium | Expires June 6 2026 — Hiren renewing June 5 at GoDaddy |
| **Set schedule triggers (Monday 9am)** | 🟢 Low | After first manual test confirms everything works |
| **Mobile app integration** | 🔵 Backlog | Not started |
| **Bulk product upload from CSV** | 🔵 Backlog | Could add CSV-read node to product-image-scraper |

---

## 13. DESIGN QUALITY STANDARD — Top 5 Card Stores

The ai-cloner-odoo prompt is benchmarked against these sites. Generated HTML must match their quality:

| Site | URL | Key Features |
|------|-----|-------------|
| **TCGPlayer** | tcgplayer.com | Live price charts, condition grading, search |
| **TrollAndToad** | trollandtoad.com | Mass listings, advanced filters, buylist |
| **StarCityGames** | starcitygames.com | Premium articles, tournament coverage, card grades |
| **ChannelFireball** | channelfireball.com | Content-first, expert picks, format guides |
| **Dave & Adams** | dacardworld.com | Sealed products, wax breaks, hobby box focus |

**HTML generation prompt guarantees:**
- Rajdhani Google Font for all headings
- TailwindCSS JIT with explicit text color classes on every element
- Dark Navy (`#0B1426`) + Gold (`#D4AF37`) + Electric Blue accent color system
- 17 sections: announcement bar → hero → featured → categories → promotions → events → trust → newsletter → footer
- Fully mobile-responsive, card hover animations, filter sidebar, trust badges
- No dark-on-dark failures (explicit `text-white` / `text-slate-100` everywhere)
