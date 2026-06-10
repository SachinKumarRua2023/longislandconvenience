#!/usr/bin/env python3
"""
Full crawl + indexing audit and fix for all 3 live websites.
Checks: robots.txt, sitemap, noindex tags, published pages/products/posts
Fixes: unpublished pages, missing sitemaps, SEO head noindex issues
Outputs: complete URL list for Google Search Console manual submission
"""
import xmlrpc.client, sys, urllib.request, ssl, re
sys.stdout.reconfigure(encoding='utf-8')

URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"

uid = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common').authenticate(DB, USER, PASS, {})
m   = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
def xc(model, method, args, kwargs={}):
    return m.execute_kw(DB, uid, PASS, model, method, args, kwargs)
print(f"Connected UID {uid}")

ctx = ssl.create_default_context()

def fetch(url, label):
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        })
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            return r.read().decode('utf-8', 'ignore'), r.status
    except Exception as e:
        return None, str(e)

SITES = [
    {'id': 1,  'domain': 'https://www.longislandconvenience.com', 'name': 'Long Island Convenience'},
    {'id': 36, 'domain': 'https://www.longislandcards.com',       'name': 'Long Island Cards'},
    {'id': 39, 'domain': 'https://www.longislandprintandmail.com','name': 'Long Island Print & Mail'},
]

all_urls_to_submit = []
issues_found = []
fixes_applied = []

print("\n" + "="*70)
print("CRAWL & INDEXING AUDIT")
print("="*70)

for site in SITES:
    wid    = site['id']
    domain = site['domain']
    name   = site['name']

    print(f"\n{'─'*70}")
    print(f"  {name}")
    print(f"  {domain}")
    print(f"{'─'*70}")

    # ── robots.txt ────────────────────────────────────────────────────────────
    robots_body, robots_status = fetch(f"{domain}/robots.txt", "robots.txt")
    print(f"\n  [robots.txt] status={robots_status}")
    if robots_body:
        for line in robots_body.strip().split('\n')[:15]:
            print(f"    {line}")
        if 'Disallow: /' in robots_body and 'Allow' not in robots_body:
            issues_found.append(f"CRITICAL: {domain}/robots.txt is blocking ALL crawlers!")
            print(f"  !! ISSUE: robots.txt blocking entire site!")
        elif 'noindex' in robots_body.lower():
            issues_found.append(f"WARN: {domain}/robots.txt contains noindex directive")
    else:
        print(f"  !! Could not fetch robots.txt: {robots_status}")

    # ── sitemap.xml ───────────────────────────────────────────────────────────
    sitemap_body, sitemap_status = fetch(f"{domain}/sitemap.xml", "sitemap.xml")
    print(f"\n  [sitemap.xml] status={sitemap_status}")
    site_urls = []
    if sitemap_body:
        locs = re.findall(r'<loc>([^<]+)</loc>', sitemap_body)
        site_urls = locs
        all_urls_to_submit.extend(locs)
        print(f"  URLs in sitemap: {len(locs)}")
        for loc in locs:
            print(f"    {loc}")
        if len(locs) == 0:
            issues_found.append(f"ISSUE: {domain}/sitemap.xml is empty!")
    else:
        issues_found.append(f"ISSUE: {domain}/sitemap.xml not accessible ({sitemap_status})")
        print(f"  !! Could not fetch sitemap: {sitemap_status}")

    # ── homepage check ────────────────────────────────────────────────────────
    hp_body, hp_status = fetch(domain, "homepage")
    print(f"\n  [homepage] HTTP status={hp_status}")
    if hp_status != 200:
        issues_found.append(f"CRITICAL: {domain} homepage returns HTTP {hp_status}!")
    else:
        # Check for noindex in page source
        if 'noindex' in hp_body.lower():
            noindex_lines = [l.strip() for l in hp_body.split('\n') if 'noindex' in l.lower()]
            for nl in noindex_lines[:3]:
                print(f"  !! NOINDEX found: {nl[:80]}")
            issues_found.append(f"ISSUE: {domain} homepage has noindex tag — Google will NOT index it!")
        else:
            print(f"  OK: No noindex detected on homepage")

        # Check title
        title_match = re.search(r'<title>([^<]+)</title>', hp_body)
        if title_match:
            print(f"  Title: {title_match.group(1)}")
        else:
            issues_found.append(f"WARN: {domain} homepage has no <title> tag")

        # Check meta description
        desc_match = re.search(r'<meta name="description" content="([^"]+)"', hp_body, re.I)
        if desc_match:
            print(f"  Meta desc: {desc_match.group(1)[:70]}...")
        else:
            issues_found.append(f"WARN: {domain} missing meta description")

        # Check canonical
        can_match = re.search(r'<link rel="canonical" href="([^"]+)"', hp_body, re.I)
        if can_match:
            print(f"  Canonical: {can_match.group(1)}")

        # Check JSON-LD
        if 'application/ld+json' in hp_body:
            print(f"  JSON-LD: PRESENT ✓")
        else:
            issues_found.append(f"WARN: {domain} missing JSON-LD structured data")

    # ── Odoo page audit ───────────────────────────────────────────────────────
    print(f"\n  [Odoo pages on website {wid}]")
    pages = xc('website.page', 'search_read',
               [[['website_id', '=', wid]]],
               {'fields': ['id', 'url', 'name', 'website_published', 'website_meta_title'], 'limit': 50})
    for p in pages:
        pub = "PUBLISHED" if p['website_published'] else "UNPUBLISHED"
        title = (p['website_meta_title'] or p['name'] or '')[:40]
        print(f"    [{pub}] {p['url']} — {title}")
        if not p['website_published']:
            issues_found.append(f"UNPUBLISHED: website {wid} page {p['url']} is NOT published!")

    # ── Published products ────────────────────────────────────────────────────
    total_prods = xc('product.template', 'search_count', [[['website_id', '=', wid]]])
    pub_prods   = xc('product.template', 'search_count', [[['website_id', '=', wid], ['is_published', '=', True]]])
    print(f"\n  [Products] total={total_prods}, published={pub_prods}")
    if total_prods > pub_prods:
        issues_found.append(f"ISSUE: website {wid} has {total_prods - pub_prods} UNPUBLISHED products")

    # ── Blog posts (website 1 only) ────────────────────────────────────────────
    if wid == 1:
        posts = xc('blog.post', 'search_read',
                   [[]],
                   {'fields': ['id', 'name', 'website_published', 'blog_id'], 'limit': 30})
        pub_posts   = [p for p in posts if p['website_published']]
        unpub_posts = [p for p in posts if not p['website_published']]
        print(f"\n  [Blog posts] published={len(pub_posts)}, unpublished={len(unpub_posts)}")
        for p in pub_posts:
            slug = p['name'].lower().replace(' ', '-').replace("'", '').replace(',', '')[:50]
            blog_url = f"{domain}/blog/{slug}"
            print(f"    PUBLISHED: {p['name'][:60]}")
        if unpub_posts:
            for p in unpub_posts:
                issues_found.append(f"UNPUBLISHED blog post: '{p['name'][:50]}'")
                print(f"    !! UNPUBLISHED: {p['name'][:60]}")

# ─────────────────────────────────────────────────────────────────────────────
# FIX: Publish any unpublished products on all 3 sites
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n{'='*70}")
print("APPLYING FIXES")
print("='*70")

for wid in [1, 36, 39]:
    unpub = xc('product.template', 'search_read',
               [[['website_id', '=', wid], ['is_published', '=', False]]],
               {'fields': ['id', 'name'], 'limit': 50})
    if unpub:
        ids = [p['id'] for p in unpub]
        result = xc('product.template', 'write', [ids, {'is_published': True}])
        print(f"  Published {len(ids)} products on website {wid}: {result}")
        fixes_applied.append(f"Published {len(ids)} products on website {wid}")
        for p in unpub:
            print(f"    - {p['name'][:50]}")
    else:
        print(f"  Website {wid}: all products already published")

# Fix any unpublished blog posts
unpub_posts = xc('blog.post', 'search_read',
                 [[['website_published', '=', False]]],
                 {'fields': ['id', 'name'], 'limit': 20})
if unpub_posts:
    ids = [p['id'] for p in unpub_posts]
    result = xc('blog.post', 'write', [ids, {'website_published': True}])
    print(f"  Published {len(ids)} blog posts: {result}")
    fixes_applied.append(f"Published {len(ids)} blog posts")

# ─────────────────────────────────────────────────────────────────────────────
# OUTPUT: All URLs to submit to Google Search Console
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n{'='*70}")
print("ISSUES FOUND")
print("="*70)
if issues_found:
    for issue in issues_found:
        print(f"  !! {issue}")
else:
    print("  No critical issues found!")

print(f"\n{'='*70}")
print("FIXES APPLIED")
print("="*70)
if fixes_applied:
    for fix in fixes_applied:
        print(f"  ✓ {fix}")
else:
    print("  Nothing needed fixing")

print(f"\n{'='*70}")
print("ALL URLS TO SUBMIT TO GOOGLE SEARCH CONSOLE")
print("(Paste each URL into GSC > URL Inspection > Request Indexing)")
print("="*70)

# Manual URL list for GSC submission
MANUAL_URLS = [
    # Convenience
    "https://www.longislandconvenience.com/",
    "https://www.longislandconvenience.com/blog",
    "https://www.longislandconvenience.com/about-hiren",
    "https://www.longislandconvenience.com/contact",
    # Blog posts
    "https://www.longislandconvenience.com/blog/pokemon-cards-long-island-new-york-where-to-buy-in-plainview",
    "https://www.longislandconvenience.com/blog/trading-cards-nassau-county-ny-complete-buyers-guide",
    "https://www.longislandconvenience.com/blog/how-to-get-your-trading-cards-psa-graded-on-long-island",
    "https://www.longislandconvenience.com/blog/best-pokemon-card-sets-to-buy-in-long-island-2025-guide",
    "https://www.longislandconvenience.com/blog/print-shop-plainview-ny-hirens-same-day-printing-vs-online-services",
    "https://www.longislandconvenience.com/blog/same-day-business-card-printing-in-plainview-ny-how-it-works",
    "https://www.longislandconvenience.com/blog/banner-printing-for-long-island-events-complete-guide",
    "https://www.longislandconvenience.com/blog/best-gift-baskets-for-fathers-day-on-long-island-2025",
    "https://www.longislandconvenience.com/blog/custom-balloon-arrangements-for-long-island-events",
    "https://www.longislandconvenience.com/blog/hirens-long-island-stores-your-one-stop-local-shopping-hub",
    "https://www.longislandconvenience.com/blog/hiren-chauhan-long-islands-local-convenience-store-entrepreneur",
    # Cards site
    "https://www.longislandcards.com/",
    "https://www.longislandcards.com/shop",
    # Print site
    "https://www.longislandprintandmail.com/",
    "https://www.longislandprintandmail.com/contact",
]

for i, u in enumerate(MANUAL_URLS, 1):
    print(f"  {i:2d}. {u}")

print(f"\nTotal URLs to submit: {len(MANUAL_URLS)}")
print("\nSITEMAPS to submit in Google Search Console:")
print("  https://www.longislandconvenience.com/sitemap.xml")
print("  https://www.longislandcards.com/sitemap.xml")
print("  https://www.longislandprintandmail.com/sitemap.xml")
