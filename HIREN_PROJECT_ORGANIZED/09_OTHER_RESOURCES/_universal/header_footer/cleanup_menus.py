#!/usr/bin/env python3
"""Clean duplicate menus and verify blog posts on convenience.com."""
import xmlrpc.client, sys
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

# Remove duplicate menus: keep ID 9 (Blog), remove 138; keep ID 8 or 120 for Shop (remove duplicate)
# Keep the lower IDs (original), delete the duplicates
to_delete = [120, 138]  # duplicate Shop (/shop) and duplicate Blog
result = xc('website.menu', 'unlink', [to_delete])
print(f"Deleted duplicate menus {to_delete}: {result}")

# Set /shop-all -> /shop on menu ID 8
xc('website.menu', 'write', [[8], {'url': '/shop', 'sequence': 20}])
print("Updated Shop menu URL to /shop")

# Show final menu state
menus = xc('website.menu', 'search_read',
           [[['website_id', '=', 1]]],
           {'fields': ['id', 'name', 'url', 'parent_id', 'sequence'], 'limit': 30})
print("\nFinal menu structure:")
for mn in sorted(menus, key=lambda x: x['sequence']):
    if mn['parent_id']:
        print(f"  seq={mn['sequence']} [{mn['id']}] {mn['name']} -> {mn['url']}")

# Verify blog posts
posts = xc('blog.post', 'search_read',
           [[['website_published', '=', True], ['blog_id', 'in', [2,3,4,5,6]]]],
           {'fields': ['id', 'name', 'blog_id'], 'limit': 20})
print(f"\nPublished blog posts ({len(posts)} total):")
for p in posts:
    print(f"  [{p['blog_id'][1]}] {p['name'][:65]}")
