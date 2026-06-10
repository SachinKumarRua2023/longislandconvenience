# HirenTask — Scripts Index & Project Map
Last updated: 2026-05-30 | Total scripts: 171

---

## FOLDER STRUCTURE

```
HirenTask/
│
├── SCRIPTS_INDEX.md            ← you are here
├── ODOO_WEBSITE_IDS.md         ← all site IDs + domains
├── BLOG_URLS_GOOGLE_INSPECT.md ← 59 blog URLs, all verified 200 OK
│
├── sites/                      ← one folder per Odoo website
│   ├── 01_long_island_convenience/   (site ID 1)
│   ├── 36_long_island_cards/         (site ID 36)
│   ├── 37_long_island_gift_basket/   (site ID 37)
│   ├── 38_long_island_balloons/      (site ID 38)
│   ├── 39_long_island_print_mail/    (site ID 39)
│   └── 41_jhd_advisor/              (site ID 41)
│
├── _universal/                 ← works across any website
│   ├── full_web_builder/       ← build any site from scratch
│   ├── header_footer/          ← nav, menus, footer, contact
│   ├── real_products/          ← products, images, shop
│   ├── seo_indexing/           ← SEO, GSC, schema markup
│   ├── blog/                   ← blog management
│   └── workflow_tools/         ← n8n patches & automation
│
└── BasicWorkflow/              ← n8n workflow JSON files
    ├── odoo-full-website-automation.json   ← MASTER automation
    ├── jhd-advisor-daily-blog-autoposter.json
    ├── ai-cloner-odoo.json
    ├── website-cloner.json
    ├── printmail-full-automation.json
    └── product-image-scraper.json
```

---

## QUICK START — Build any website

```bash
# 1. Use the master builder (agency, ecommerce, tech, local_business, restaurant, nonprofit)
python _universal/full_web_builder/odoo_website_builder.py \
  --site 41 --category agency \
  --name "JHD Advisor" \
  --domain "https://www.jhdadvisor.com" \
  --phone "+1 (917) 338-7086" \
  --email "info@jhdadvisor.com" \
  --location "Long Island, NY"

# 2. OR trigger via n8n webhook (POST):
curl -X POST https://your-n8n/webhook/build-website \
  -H "Content-Type: application/json" \
  -d '{"site_id":41,"category":"agency","name":"JHD Advisor","domain":"https://www.jhdadvisor.com","phone":"+1 (917) 338-7086","location":"Long Island, NY"}'
```

---

## SITES

### Site 1 — Long Island Convenience
`sites/01_long_island_convenience/` | [README](sites/01_long_island_convenience/README.md)

| Script | Purpose |
|--------|---------|
| `build_all_blogs.py` | All blog posts across LIC categories |
| `redesign_convenience_homepage.py` | Full 2026 homepage |
| `FinalFathersDay.py` | Father's Day campaign |
| `add_celebrations_popup.py` | Event countdown popups |
| `fix_convenience_7stores.py` | 7-store location grid |
| `upload_real_images_lic.py` | Real product images |

---

### Site 36 — Long Island Cards
`sites/36_long_island_cards/` | [README](sites/36_long_island_cards/README.md)

| Script | Purpose |
|--------|---------|
| `build_cards_website.py` | Full ecommerce site build |
| `fix_cards_categories.py` | Product category structure |
| `download_real_card_images.py` | Supplier product images |
| `real_card_images.py` | Upload card images |
| `verify_cards_site.py` | Full audit |

---

### Site 37 — Long Island Gift Basket
`sites/37_long_island_gift_basket/` | [README](sites/37_long_island_gift_basket/README.md)

| Script | Purpose |
|--------|---------|
| `build_giftbasket_website.py` | Full site build |
| `rebuild_gift_basket.py` | Full rebuild from scratch |
| `fix_basket_unique_images.py` | Real product images |
| `redesign_giftbasket_homepage.py` | 2026 homepage |

---

### Site 38 — Long Island Balloons & Decor
`sites/38_long_island_balloons/` | [README](sites/38_long_island_balloons/README.md)

| Script | Purpose |
|--------|---------|
| `build_balloon_website.py` | Full site build |
| `balloons_services_store.py` | Service packages + pricing |
| `balloons_carousel.py` | Image carousel |
| `balloons_popup_countdown.py` | Event countdown popup |

---

### Site 39 — Long Island Print & Mail
`sites/39_long_island_print_mail/` | [README](sites/39_long_island_print_mail/README.md)

| Script | Purpose |
|--------|---------|
| `build_printmail_website.py` | Full site + services build |
| `rebuild_printmail_2026.py` | 2026 full rebuild |
| `setup_printmail_products.py` | All products + pricing |
| `fix_printmail_images_final.py` | Product images |

---

### Site 41 — JHD Advisor
`sites/41_jhd_advisor/` | [README](sites/41_jhd_advisor/README.md)

| Script | Purpose |
|--------|---------|
| `setup_jhd_advisor.py` | Initial site setup |
| `jhd_advisor_growth_engine.py` | Three.js homepage + 10 blogs |
| `jhd_advisor_blog_builder.py` | 12 SEO+GEO blog posts |
| `jhd_blog_authors_images.py` | Authors + images (posts 55–66) |
| `jhd_fix_old_blog_images.py` | Authors + images (posts 45–54) |

---

## UNIVERSAL TOOLS

### Full Website Builder
`_universal/full_web_builder/` | [README](_universal/full_web_builder/README.md)

| Script | Purpose |
|--------|---------|
| `odoo_website_builder.py` | **MASTER** — any category, full site |
| `create_odoo_websites.py` | Create new website records |
| `discover_odoo_sites.py` | List all sites + domains |
| `configure_new_domains.py` | Domain routing setup |
| `nuclear_fix.py` | Emergency site recovery |

**Categories:** `agency` · `ecommerce` · `tech` · `local_business` · `restaurant` · `nonprofit`

---

### Header, Footer & Navigation
`_universal/header_footer/` | [README](_universal/header_footer/README.md)

| Script | Purpose |
|--------|---------|
| `fix_all_footers_favicons.py` | Footer + favicon across all sites |
| `cleanup_menus.py` | Remove duplicate menus |
| `add_blog_menu.py` | Add Blog to any nav |
| `create_contact_page.py` | Generate contact pages |
| `fix_social_links.py` | Update all social links |

---

### Real Products & Images
`_universal/real_products/` | [README](_universal/real_products/README.md)

| Script | Purpose |
|--------|---------|
| `direct_image_update.py` | Update product images in views |
| `check_products.py` | List products by website |
| `upload_product_images.py` | Bulk image upload |
| `fix_shop_categories.py` | Fix shop category structure |

> ⚠️ **cover_properties rule:** Never put external URLs in `cover_properties`.
> Odoo's `og:image` will crash with 500. Always use `"background-image":"none"`.
> Put `<img>` tags in the post HTML content instead.

---

### SEO & Google Indexing
`_universal/seo_indexing/` | [README](_universal/seo_indexing/README.md)

| Script | Purpose |
|--------|---------|
| `dominate_local_seo.py` | Full local SEO — schema, citations |
| `add_faq_schema.py` | FAQ schema markup |
| `audit_and_fix_indexing.py` | Full crawl audit |
| `check_all_urls.py` | HTTP status check all URLs |
| `gsc_fix_all.py` | Fix all GSC issues |

---

### Blog Management
`_universal/blog/` | [README](_universal/blog/README.md)

| Script | Purpose |
|--------|---------|
| `audit_blog_seo.py` | Audit all post meta tags |
| `fix_blog_push.py` | Publish unpublished posts |
| `fix_blog_images_author.py` | Bulk author + image update |

---

### n8n Workflow Tools
`_universal/workflow_tools/` | [README](_universal/workflow_tools/README.md)

| Script | Purpose |
|--------|---------|
| `cvp.py` | Sync n8n workflow via MCP |
| `patch_prompt.py` | Patch AI prompts in workflows |
| `fix_jsonbody.py` | Fix HTTP Request JSON body |

---

## ODOO CREDENTIALS

| Field | Value |
|-------|-------|
| URL | https://country-cove-inc.odoo.com |
| DB | country-cove-inc |
| UID | 2 |
| Password | M@nhattan1234 |

## WEBSITE IDs

| ID | Website | Domain |
|----|---------|--------|
| 1  | Long Island Convenience | longislandconvenience.com |
| 36 | Long Island Cards | longislandcards.com |
| 37 | Long Island Gift Basket | ligiftbasket.com |
| 38 | Long Island Balloons & Decor | longislandballoonsdecor.com |
| 39 | Long Island Print & Mail | longislandprintandmail.com |
| 41 | JHD Advisor | jhdadvisor.com |

## KEY SAFETY RULES

1. **cover_properties** — NEVER put external URLs (Unsplash, etc.) here.
   Causes `get_website_meta()` → `url_join()` → **500 error** on all post pages.
   Fixed by: `"background-image": "none"` always. Use `<img>` in content HTML.

2. **og:image** — Falls back to site logo when cover_properties has no URL. Fine.

3. **Blog posts** — Must have `website_id` matching the site they belong to.
   Otherwise routing works but cross-site URL generation can crash.
