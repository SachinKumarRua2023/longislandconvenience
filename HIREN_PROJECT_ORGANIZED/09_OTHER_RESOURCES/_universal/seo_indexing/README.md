# Universal — SEO & Google Indexing
Scripts for SEO optimization, Google Search Console and indexing management.

## Scripts

| Script | What It Does |
|--------|-------------|
| `dominate_local_seo.py` | Full local SEO setup — schema, citations, GBP integration |
| `add_faq_schema.py` | FAQ schema JSON-LD for product categories |
| `audit_and_fix_indexing.py` | Full crawl audit: robots.txt, sitemap, noindex tags |
| `check_all_urls.py` | Live HTTP status check for all blog URLs |
| `debug_verification.py` | Google Search Console meta tag verification test |
| `gsc_fix_all.py` | Fix all Google Search Console issues |
| `gsc_flush_cache.py` | Flush GSC cache and request re-crawl |
| `fix_seo_views.py` | Fix SEO meta tags in Odoo views |
| `seo_all_sites.py` | Apply SEO config across all sites |
| `implement_seo_odoo.py` | Full Odoo SEO implementation |
| `rebuild_seo_safe.py` | Rebuild SEO without breaking live pages |
| `fix_gsc_code.py` | Fix GSC verification code |
| `fix_google_verification.py` | Google site verification fixes |
| `fix_verification_content.py` | Fix verification meta content |
| `serve_google_verification.py` | Serve Google verification file |
| `upload_gsc_metatag.py` | Upload GSC meta tag to Odoo |
| `upload_gsc_verification.py` | Upload GSC verification file |
| `test_seo_audit.py` | Run SEO audit test suite |
| `update_company_contact.py` | Update company contact info for schema |

## Google Search Console — All blog URLs
See `../../BLOG_URLS_GOOGLE_INSPECT.md`

## Schema types implemented
- LocalBusiness (all sites)
- FAQPage (product category pages)
- BlogPosting (all blog posts)
- BreadcrumbList (navigation)

## ⚠️ cover_properties 500-error rule
External Unsplash URLs in `cover_properties` → 500 error via `og:image` crash.
Always set `"background-image": "none"` in cover_properties.
