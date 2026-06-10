# SEO + GEO Marketing Strategy — Hiren Kumar Stores
**Updated:** 2026-05-23  
**Websites:** longislandconvenience.com · longislandcards.com · longislandprintandmail.com  
**Location:** Plainview, NY 11803

---

## 1. KEYWORD MAP (per site)

### longislandconvenience.com
| Type | Keywords |
|------|----------|
| Brand | hiren shop, hiren store long island, long island convenience |
| Primary | convenience store plainview ny, long island convenience store |
| GEO | convenience store near me plainview ny, open convenience store nassau county |
| Products | cigars tobacco long island, lottery tickets plainview ny, gift baskets long island, vape shop plainview ny |
| Long-tail | best convenience store plainview new york, hiren convenience store nassau county |

### longislandcards.com
| Type | Keywords |
|------|----------|
| Brand | hiren cards shop, hiren trading cards, long island cards |
| Primary | sports cards long island, trading cards plainview ny, graded cards long island |
| GEO | PSA graded cards near me, pokemon cards long island, sports cards nassau county |
| Products | buy PSA 10 cards long island, pokemon cards plainview ny, MTG cards long island, yu-gi-oh cards ny, one piece cards long island |
| Long-tail | authenticated trading cards long island, rookie cards long island ny, BGS graded cards near me |

### longislandprintandmail.com
| Type | Keywords |
|------|----------|
| Brand | hiren print and mail, long island print shop, hiren printing services |
| Primary | print and mail long island, printing services plainview ny, same day printing long island |
| GEO | business card printing near me plainview, banner printing long island, notary services plainview ny |
| Products | flyers printing long island, shipping services plainview ny, same day banner printing nassau county |
| Long-tail | same day business card printing long island ny, print shop open near me plainview |

---

## 2. COMPETITOR ANALYSIS

### Print & Mail Competitors (from Google screenshots)
1. **GSB Digital** — ranks for "print services long island" — targets: design + print bundle
2. **Graphic Lab Printing** — ranks for "best print services provider long island" — targets: quality printing

**What we do differently (USP):**
- Same-day printing available in Plainview
- Notary + shipping bundled in one visit
- Family-owned local business (trust signal)

### Cards Competitors
- eBay / TCGPlayer (large marketplaces) — compete on LOCAL IN-PERSON buying, PSA authentication
- Local card shops — compete on selection + graded cards

---

## 3. ON-PAGE SEO IMPLEMENTATION (via Odoo script)

### Meta Tags — All 3 Homepages
Implemented via `implement_seo_odoo.py` script:
- `<title>` — keyword-rich, under 60 chars
- `<meta name="description">` — 150-160 chars, includes location + keywords
- `<meta name="keywords">` — 5-10 core terms
- Open Graph tags (`og:title`, `og:description`, `og:url`)
- Twitter Card tags
- Canonical URL

### JSON-LD Structured Data (LocalBusiness schema)
Each site gets a `LocalBusiness` schema block injected into `<head>`:
- `@type`: ConvenienceStore / Store / PrintShop
- name, address (Plainview NY 11803), telephone, url
- openingHours, priceRange, areaServed

### Sitemap
- Odoo generates `/sitemap.xml` automatically
- Verify at: each-domain.com/sitemap.xml
- Submit to Google Search Console

---

## 4. GOOGLE BUSINESS PROFILE (GBP) — CRITICAL

This is the #1 local SEO action. Must be done manually by Hiren.

### Steps:
1. Go to business.google.com
2. Create 3 separate listings:
   - **Long Island Convenience** — Category: Convenience Store
   - **Long Island Cards** — Category: Trading Card Store / Comic Book Store
   - **Long Island Print & Mail** — Category: Print Shop / Shipping and Mailing Service
3. For each listing:
   - Address: [Plainview NY 11803 exact address]
   - Phone: [business phone]
   - Website: respective domain
   - Hours: exact open/close times
   - Add 10+ photos (storefront, products, interior)
   - Write business description using primary keywords
4. Verify via postcard (takes 5-7 days)

### After Verification:
- Enable messaging
- Add products/services with prices
- Get customers to leave Google reviews (5-star reviews = rank boost)
- Post weekly updates (Google Posts feature)

---

## 5. AI SEARCH OPTIMIZATION (ChatGPT/Perplexity/Gemini)

AI search tools (SearchGPT, Perplexity, Gemini) cite pages that have:
1. **Clear factual content** — who you are, what you sell, where you are
2. **Structured data** — JSON-LD helps AI parse your business info
3. **Authority signals** — backlinks from local directories
4. **FAQ sections** — AI loves Q&A format content

### Implemented in each homepage:
- "About" section with store description + location
- FAQ block with 5 common questions per site
- JSON-LD with `speakable` property for voice search

### Directory Listings (builds AI training data):
Submit all 3 stores to:
- Yelp.com (free listing)
- YellowPages.com
- Bing Places (business.bing.com)
- Apple Maps (mapsconnect.apple.com)
- Foursquare (foursquare.com/add-place)
- Chamber of Commerce (nassaucountyny.gov or local chamber)
- BrightLocal / Moz Local citation sweep

---

## 6. BLOG STRATEGY (per site)

### longislandconvenience.com/blog
- "7 Best Lottery Scratch-Off Strategies in New York"
- "Best Cigars Under $20 Near Plainview NY"
- "How to Order Custom Gift Baskets for Same-Day Delivery on Long Island"
- "Why Shop Local? Convenience Stores in Nassau County vs. Big Box"

### longislandcards.com/blog
- "How to Get Your Trading Cards PSA Graded in Long Island"
- "Best Pokemon Card Sets to Buy in 2025 — Plainview NY Store Guide"
- "Mike Trout Rookie Card Value: What Collectors Need to Know"
- "Top 10 Sports Cards to Invest In — Long Island Expert Picks"
- "Yu-Gi-Oh! Tournament Prep Guide — Where to Buy Cards on Long Island"

### longislandprintandmail.com/blog
- "Same-Day Business Card Printing in Plainview NY — How It Works"
- "Best Banner Printing Options for Long Island Events"
- "When Do You Need a Notary? Long Island Small Business Guide"
- "How to Ship Packages Cheaply from Long Island — Carrier Comparison"

---

## 7. BACKLINK STRATEGY

### Easy Wins (get within 30 days):
1. Nassau County Chamber of Commerce listing
2. Plainview local community Facebook group — mention store
3. Nextdoor.com business listing (free)
4. Long Island Press — local business spotlight (pitch them)
5. Google News — write a press release about new store opening

### Medium Term:
- Partner with local Long Island schools/teams for sponsorships (get .edu backlinks)
- Sponsor a local youth sports team — get listed on their site
- Write guest posts for local Long Island blogs

---

## 8. TECHNICAL SEO CHECKLIST

- [x] Meta title + description — implemented via script
- [x] JSON-LD LocalBusiness schema — implemented via script  
- [x] Open Graph tags — implemented via script
- [ ] Google Search Console — submit sitemap manually (business.google.com)
- [ ] Google Analytics — add tracking ID to Odoo settings
- [ ] SSL certificate — longislandprintandmail.com (contact IONOS)
- [ ] Mobile speed — Odoo themes are mobile-responsive by default
- [ ] Core Web Vitals — check at pagespeed.web.dev for each domain
- [ ] robots.txt — verify at domain.com/robots.txt (Odoo handles automatically)
- [ ] Sitemap — verify at domain.com/sitemap.xml

---

## 9. TIMELINE

| Week | Action |
|------|--------|
| Week 1 | Run implement_seo_odoo.py — meta tags + JSON-LD on all 3 sites |
| Week 1 | Create Google Business Profile for all 3 stores |
| Week 1 | Submit to Yelp, YellowPages, Bing Places |
| Week 2 | Add Google Analytics to all 3 Odoo sites |
| Week 2 | Submit sitemaps to Google Search Console |
| Week 2 | Write first blog post for each site |
| Week 3 | Ask existing customers for Google reviews |
| Week 3 | Create Nextdoor business listing |
| Month 2 | 2 blog posts per site per month |
| Month 2 | Google Posts — weekly updates on GBP |
| Month 3 | Check rankings, iterate on content |

---

## 10. EXPECTED RESULTS

- **Brand keywords** ("long island convenience", "hiren shop") — Top 3 Google within 4-6 weeks after GBP verification
- **Local GEO keywords** ("convenience store plainview ny") — Top 5 within 8-12 weeks
- **AI search appearance** — appears in Perplexity/Gemini answers within 4-8 weeks after structured data indexed
- **Competitive keywords** ("print and mail long island") — Top 5 within 3-6 months with consistent blogging

---

## SCRIPTS IN THIS FOLDER

| Script | Purpose |
|--------|---------|
| `implement_seo_odoo.py` | Injects meta tags + JSON-LD into all 3 Odoo websites |
| `fix_convenience_7stores_v3.py` | Fixed 7-store grid (DONE) |
| `upload_pil_images_lic_v2.py` | Product images for Long Island Cards (DONE) |
