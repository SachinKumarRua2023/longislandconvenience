# Universal — Blog Management
Scripts for creating, fixing and auditing blog posts across all sites.

## Scripts

| Script | What It Does |
|--------|-------------|
| `audit_blog_seo.py` | Audit meta title/description on all posts |
| `check_existing_blogs.py` | Count posts per blog |
| `fix_blog_images_author.py` | Bulk-update author photos + cover images |
| `fix_blog_push.py` | Publish all unpublished posts |
| `inspect_blog_push.py` | Inspect blog post push results |
| `test_full_blog_pipeline.py` | End-to-end blog pipeline test |

## Live blog indexes
- https://www.longislandconvenience.com/blog
- https://www.jhdadvisor.com/blog/jhd-advisor-growth-lab-9

## Blog post safety rule
Always set `cover_properties` to `{"background-image":"none",...}`.
External image URLs in cover_properties cause HTTP 500 via Odoo's og:image generator.
Use `<img>` tags inside the post `content` HTML instead — they work fine.
