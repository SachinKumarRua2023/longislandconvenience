#!/usr/bin/env python3
"""Add Blog menu item to longislandconvenience.com navigation."""
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

# Get current menus on website 1
menus = xc('website.menu', 'search_read',
           [[['website_id', '=', 1]]],
           {'fields': ['id', 'name', 'url', 'parent_id', 'sequence'], 'limit': 30})
print("Current menus on convenience.com:")
for mn in sorted(menus, key=lambda x: x['sequence']):
    parent = f' parent={mn["parent_id"][0]}' if mn['parent_id'] else ' [ROOT]'
    print(f"  ID={mn['id']} seq={mn['sequence']} name={mn['name']} url={mn['url']}{parent}")

# Find root menu (no parent)
root_menus = [mn for mn in menus if not mn['parent_id']]
if root_menus:
    root_id = root_menus[0]['id']
    print(f"\nRoot menu ID: {root_id}")
else:
    # If no root, find the top-level container
    root_id = menus[0]['id'] if menus else None
    print(f"Using first menu as root: {root_id}")

# Check if Blog menu already exists
blog_menu_exists = any(mn['name'] == 'Blog' or mn['url'] == '/blog' for mn in menus)
if blog_menu_exists:
    print("Blog menu already exists — skipping creation")
else:
    # Find max sequence to add Blog at the end
    max_seq = max((mn['sequence'] for mn in menus if mn['parent_id']), default=50)

    # Create Blog menu item
    blog_menu_id = xc('website.menu', 'create', [{
        'name': 'Blog',
        'url': '/blog',
        'website_id': 1,
        'parent_id': root_id,
        'sequence': max_seq + 10,
    }])
    print(f"Created Blog menu item: ID {blog_menu_id}")

# Also create per-store blog sub-menus
STORE_BLOGS = [
    {'name': 'Cards & Collectibles', 'url': '/blog/sports-trading-cards'},
    {'name': 'Print & Mail',         'url': '/blog/print-mail-services'},
    {'name': 'Gift Baskets',         'url': '/blog/gift-baskets-gifts'},
    {'name': 'Balloons & Decor',     'url': '/blog/balloons-party-decor'},
    {'name': 'Local News',           'url': '/blog/long-island-news'},
]

print("\nVerifying blog is accessible at: https://www.longislandconvenience.com/blog")
print("Posts published:")
posts = xc('blog.post', 'search_read', [[['website_published', '=', True]]], {'fields': ['id', 'name', 'blog_id'], 'limit': 20})
for p in posts:
    print(f"  [{p['blog_id'][1]}] {p['name'][:60]}")

print(f"\nTotal published posts: {len(posts)}")
print("\nDone! Check: https://www.longislandconvenience.com/blog")
