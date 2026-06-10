# How We Build Odoo Websites Through Scripting
## JHD Advisor — Complete Training Guide

---

## Overview: What the Workflow Does

Every time you run the **JHD Advisor AI Website Builder v2**, it executes this exact pipeline:

```
Any Website URL
     ↓
Firecrawl Scrape  ──→  Extracts: colors, layout, sections, CTAs, trust signals
     ↓
Firecrawl Search  ──→  Finds 4 top consulting agency sites for inspiration
     ↓
Claude AI Analyze ──→  Returns JSON: colorPalette, typography, heroPattern, etc.
     ↓
Claude AI Generate──→  Outputs: full production HTML (12,000+ tokens, 15 sections)
     ↓
Odoo Auth         ──→  Gets uid (user ID) via JSONRPC
     ↓
Odoo ir.ui.view   ──→  Creates the QWeb template with the HTML
     ↓
Odoo website.page ──→  Creates a URL-routed page linked to the view
     ↓
Odoo Publish      ──→  (Optional) Sets is_published: true immediately
     ↓
Email Report      ──→  Sends preview link + Odoo admin link to you
```

---

## Part 1: How Firecrawl Scrapes Any Website

Firecrawl is a web scraping API that handles JavaScript-heavy websites (like designrush.com, agency portfolios, etc.). Normal HTTP requests can't render JS — Firecrawl runs a real browser behind the scenes.

### API Call
```
POST https://api.firecrawl.dev/v1/scrape
Authorization: Bearer fc-471db502e79143e0982f3d2638b8ccdb
Content-Type: application/json

{
  "url": "https://www.designrush.com/",
  "formats": ["markdown", "links", "extract"],
  "extract": {
    "prompt": "Extract color palette, navigation items, page sections, headlines, CTAs, trust signals..."
  },
  "onlyMainContent": false,
  "waitFor": 2000,
  "timeout": 45000
}
```

### What It Returns
```json
{
  "success": true,
  "data": {
    "markdown": "## Page Title\n\nAll visible text from the page...",
    "links": ["https://designrush.com/agencies", "..."],
    "extract": {
      "headline": "The text it extracted from H1",
      "colorPalette": "Dark navy with electric blue accents",
      "sections": ["hero", "agency listings", "search filters", "testimonials", "footer"]
    },
    "metadata": {
      "title": "DesignRush — Find Top Agencies",
      "description": "..."
    }
  }
}
```

### Key Points
- `formats: ["markdown"]` — gets clean text content (no HTML noise)
- `extract.prompt` — Firecrawl uses AI to extract specific data points you ask for
- `waitFor: 2000` — waits 2 seconds for JS to render before scraping
- Works on ANY website: designrush.com, competitor sites, inspiration sites

---

## Part 2: How Claude Analyzes the Design

After scraping, we send the markdown + extracted data to Claude with a structured prompt.

### What We Ask Claude
```
You are a senior UI/UX director specializing in consulting and technology agency websites.

== PRIMARY INSPIRATION SOURCE ==
[scraped markdown here]

== ADDITIONAL INSPIRATION SITES ==
[search results here]

Return ONLY valid JSON:
{
  "colorPalette": { "primary": "#hex", ... },
  "typography": { "headingFont": "...", ... },
  "designStyle": "description",
  "heroPattern": "split layout / centered / video bg / etc",
  "trustSignals": ["..."],
  "keyValueProps": ["..."],
  "ctaPrimary": "Book a Free Strategy Call",
  "heroHeadline": "...",
  ...
}
```

### Why This Step Matters
Claude doesn't just copy the site — it **adapts** the best design patterns for JHD Advisor. If designrush.com uses a dark blue with gold accents, Claude might suggest a similar dark scheme but adapted to JHD's purple brand.

---

## Part 3: How Claude Generates the Odoo HTML

This is the core generation step. We send Claude a detailed 200-line prompt that specifies:

1. **Brand data** — name, tagline, headline, CTAs, address, phone
2. **Color rules** — exact hex codes, which elements get which colors
3. **15 sections** — exact layout specs for each section in order
4. **JavaScript** — all interactive behaviors (FAQ accordion, mobile menu, countdown)
5. **Technical requirements** — TailwindCSS CDN, Google Fonts, IDs for each section

### The 15 Sections We Always Build
| # | Section | Description |
|---|---------|-------------|
| S1 | Announcement Bar | Scrolling offer with dismiss button |
| S2 | Sticky Header | Logo + nav + CTA, mobile hamburger |
| S3 | Hero | Headline + sub + dual CTA + floating stat cards |
| S4 | Stats Bar | 4 key numbers across the full width |
| S5 | Services Grid | 6 service cards with icons |
| S6 | How It Works | 4-step process with icons |
| S7 | Case Studies | 3 real client result cards |
| S8 | Tech Stack | Logo pill bar |
| S9 | Testimonials | 3 review cards with avatars |
| S10 | Pricing | 3 tiers with feature lists |
| S11 | FAQ | Accordion with 5 questions |
| S12 | Book a Call CTA | Full-width purple gradient CTA section |
| S13 | Newsletter | Email capture form |
| S14 | Footer | 4-column: brand, services, company, contact |

### Claude Model & Token Settings
```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 12000,
  "messages": [{ "role": "user", "content": "[the 200-line prompt]" }]
}
```

**Why 12,000 tokens?** A full production HTML page with 14 sections, Tailwind classes, and JavaScript is typically 8,000–11,000 tokens. We set 12,000 as the ceiling to ensure nothing gets cut off.

---

## Part 4: How We Push to Odoo via JSONRPC

Odoo exposes a JSON-RPC API at `/jsonrpc`. All operations use this same endpoint — authentication, reading records, creating records, updating records.

### Step 1: Authenticate
```json
POST https://country-cove-inc.odoo.com/jsonrpc
{
  "jsonrpc": "2.0",
  "method": "call",
  "params": {
    "service": "common",
    "method": "authenticate",
    "args": ["country-cove-inc", "countrycoveinc@gmail.com", "M@nhattan1234", {}]
  }
}
```
**Response:** `{ "result": 2 }` — the `2` is the uid (user ID). We use this uid for all subsequent calls.

### Step 2: Create ir.ui.view (The HTML Template)
`ir.ui.view` is Odoo's template engine record. Every Odoo page is backed by a QWeb view.

```json
POST /jsonrpc
{
  "jsonrpc": "2.0",
  "method": "call",
  "params": {
    "service": "object",
    "method": "execute_kw",
    "args": [
      "country-cove-inc",     // database
      2,                       // uid from authenticate
      "M@nhattan1234",         // password
      "ir.ui.view",            // model
      "create",                // method
      [{                       // values
        "name": "JHD Advisor AI Page",
        "type": "qweb",
        "key": "website.jhd_page_1748780000000",
        "mode": "primary",
        "arch_db": "<t t-name='...'><t t-call='website.layout'><div id='wrap' class='oe_structure'>...YOUR HTML...</div></t></t>"
      }]
    ]
  }
}
```

**The `arch_db` field** is the most important — it holds the full QWeb template. Key wrapper:
```xml
<t t-name="website.jhd_page_{timestamp}">
  <t t-call="website.layout">
    <div id="wrap" class="oe_structure">
      <!-- your CSS/Tailwind links go here -->
      <!-- your full HTML body content goes here -->
    </div>
  </t>
</t>
```

- `t-call="website.layout"` — automatically adds the Odoo header, footer, and theme wrapper
- `id="wrap" class="oe_structure"` — marks it as editable in the Odoo visual editor
- We inject Tailwind CDN and Google Fonts inside `div#wrap` so they load within the page

### Step 3: Create website.page (The URL Route)
```json
{
  "args": [
    "country-cove-inc", 2, "M@nhattan1234",
    "website.page",
    "create",
    [{
      "name": "JHD Advisor — Home Page",
      "url": "/jhd-page-1748780000000",
      "website_id": 41,
      "view_id": 1234,          // the ir.ui.view ID from Step 2
      "is_published": false,
      "website_published": false
    }]
  ]
}
```

This creates the URL route. The page is now accessible at:
`https://country-cove-inc.odoo.com/jhd-page-1748780000000`

### Step 4: Publish (Optional)
```json
{
  "args": [
    "country-cove-inc", 2, "M@nhattan1234",
    "website.page",
    "write",
    [[5678], { "is_published": true, "website_published": true }]
  ]
}
```

The `write` method takes `[[record_id], {field: value}]`. Setting both `is_published` and `website_published` to `true` makes the page live.

---

## Part 5: Reading & Searching Odoo Records

To find a website ID, blog ID, or any other record, use `search_read`:

```json
{
  "args": [
    "country-cove-inc", 2, "M@nhattan1234",
    "website.website",     // model
    "search_read",         // method
    [[                     // domain filter
      ["name", "like", "JHD"]
    ]],
    { "fields": ["id", "name", "domain"], "limit": 10 }
  ]
}
```

**Common models used:**
| Model | Description |
|-------|-------------|
| `website.website` | The website itself (id=41 for JHD Advisor) |
| `website.page` | Individual pages with URL routes |
| `ir.ui.view` | QWeb HTML templates |
| `blog.blog` | Blog channels |
| `blog.post` | Individual blog posts |
| `website.menu` | Navigation menu items |
| `product.template` | Products in the shop |
| `res.partner` | Contacts / customers |

---

## Part 6: Making It Work for ANY Website

The workflow input accepts any URL. Here's how it handles different site types:

| Source URL | What Firecrawl Gets | How Claude Adapts It |
|-----------|--------------------|--------------------|
| `designrush.com` | Agency directory, dark UI, filter layouts | Dark tech design for JHD, filter-style service nav |
| `mckinsey.com` | Corporate navy, authoritative typography | Corporate blue variant, case study heavy layout |
| `webflow.com` | Minimal white, bold typography, grids | Clean minimal variant, grid-heavy services |
| `zapier.com` | Orange CTAs, workflow diagrams, integrations | Highlight automation workflows, integration logos |
| Any competitor | Their actual design patterns | Best elements adapted to JHD brand |

**The AI always locks:**
- JHD Advisor name, address, phone
- Purple primary color (`#7c3aed`) unless overridden
- All 6 services exactly as defined
- Real testimonials and case studies

**The AI adapts:**
- Hero layout (split vs. centered vs. video)
- Section ordering
- Card styles and spacing
- Animation effects
- Color accents from the source site

---

## Part 7: Odoo Website IDs Reference

| Website | Odoo ID | Domain |
|---------|---------|--------|
| Long Island Convenience | 1 | longislandconvenience.com |
| Long Island Balloons | 17 | longislandballoonsdecor.com |
| LI Gift Basket | 14 / 37 | ligiftbasket.com |
| Long Island Cards | 36 | longislandcards.com |
| **JHD Advisor** | **41** | **jhdadvisor.com** |

---

## Part 8: How to Run the Workflow

### Via the Web Form (Easiest)
1. Go to your n8n instance
2. Find "JHD Advisor — Universal Website Scraper + Odoo AI Builder v2"
3. Click the webhook URL: `https://[your-n8n]/form/jhd-website-builder`
4. Fill in:
   - **URL**: paste any website (e.g. `https://www.designrush.com/`)
   - **Page**: Home Page
   - **Style**: Let AI Match Source Website
   - **Promo**: optional (e.g. "Free audit this week")
   - **Publish**: Yes or No
5. Submit — takes 2–4 minutes
6. Check email for the preview link

### Via Manual Trigger (Testing)
1. Open the workflow in n8n
2. Click "Manual Trigger" node
3. Click "Execute"
4. Defaults: designrush.com → Home Page → Dark Tech style → Draft

### Expected Runtime
| Step | Time |
|------|------|
| Firecrawl scrape | 10–30 seconds |
| Firecrawl search | 10–20 seconds |
| Claude analyze | 5–15 seconds |
| Claude generate HTML | 30–90 seconds |
| Odoo push + publish | 5–15 seconds |
| **Total** | **~2–4 minutes** |

---

## Part 9: Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Firecrawl returns empty | URL blocked JS or captcha | Try a different inspiration URL, or use the fallback (Claude uses its own knowledge) |
| Claude returns partial HTML | Token limit hit | The workflow already uses 12,000 tokens — reduce section count in the prompt |
| Odoo auth uid=null | Wrong password or DB name | Check ODOO_DB = "country-cove-inc" (exact), password = M@nhattan1234 |
| Page not visible on site | website_id mismatch | Confirm JHD Advisor is ID 41 in `website.website` |
| Page looks wrong in browser | Tailwind not loading | Check CDN link in head — must be `cdn.tailwindcss.com` |
| HTML injected with dark text | Missing text-white class | Claude missed explicit text colors — re-run or manually add `class="text-white"` in Odoo editor |

---

## Part 10: Quick Reference — Key n8n Patterns

### Pattern 1: Buffer Decoder (always include in Code nodes)
```javascript
function decodeBuffer(resp) {
  if (resp?.content || resp?.result !== undefined || resp?.data !== undefined) return resp;
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
**Why:** n8n's HTTP node sometimes returns a Node.js readable stream instead of parsed JSON, especially for large responses. This decoder handles both cases.

### Pattern 2: Reference Another Node
```javascript
const cfg = $('Parse Input + Config').item.json;
```

### Pattern 3: Cross-node data access
```javascript
// In Claude Generate node, get data from 3 nodes back:
const designData = $('Code: Merge + Build Analysis Prompt').item.json;
const claudeAnalysis = $('Code: Build JHD HTML Prompt').item.json;
```

### Pattern 4: Safe JSON parse from Claude
```javascript
const raw = claudeResp?.content?.[0]?.text || '';
let parsed = {};
try {
  const m = raw.match(/\{[\s\S]*\}/);
  if (m) parsed = JSON.parse(m[0]);
} catch(e) {}
```
The regex `\{[\s\S]*\}` extracts JSON even if Claude accidentally wraps it in markdown fences.

---

*Last updated: June 2026 | JHD Advisor × SeekHowItHRua*
