#!/usr/bin/env python3
"""Discover all websites, categories, and products in Odoo."""
import json, sys, requests
sys.stdout.reconfigure(encoding='utf-8')

ODOO_URL  = 'https://country-cove-inc.odoo.com'
ODOO_DB   = 'country-cove-inc'
ODOO_PASS = 'M@nhattan1234'
UID       = 2

def rpc(model, method, args, kwargs={}):
    r = requests.post(ODOO_URL + '/jsonrpc', json={
        'jsonrpc': '2.0', 'method': 'call', 'id': 1,
        'params': {'service': 'object', 'method': 'execute_kw',
                   'args': [ODOO_DB, UID, ODOO_PASS, model, method, args, kwargs]}
    }, timeout=30)
    result = r.json()
    if result.get('error'):
        print(f'RPC ERROR: {result["error"]}')
        return None
    return result.get('result')

# ── Websites ──────────────────────────────────────────────────────────────────
print('=== WEBSITES ===')
websites = rpc('website.website', 'search_read', [[[]]], {'fields': ['id','name','domain'], 'limit': 30})
for w in (websites or []):
    print(f"  id={w['id']:3} | {w['name']:40} | {w['domain']}")

# ── Product Categories ────────────────────────────────────────────────────────
print('\n=== PRODUCT CATEGORIES ===')
cats = rpc('product.category', 'search_read', [[[]]], {'fields': ['id','name','parent_id'], 'limit': 100})
for c in sorted(cats or [], key=lambda x: x['id']):
    parent = c['parent_id'][1] if c['parent_id'] else ''
    print(f"  id={c['id']:4} | {c['name']:35} | parent: {parent}")

# ── Products per Website ──────────────────────────────────────────────────────
print('\n=== PRODUCTS PER WEBSITE ===')
for w in (websites or []):
    wid = w['id']
    prods = rpc('product.template', 'search_read',
                [[['website_id', '=', wid]]],
                {'fields': ['id','name','categ_id','list_price','is_published','image_1920'], 'limit': 50})
    has_img = sum(1 for p in (prods or []) if p.get('image_1920'))
    print(f"\n  [{w['name']}] (website_id={wid}) — {len(prods or [])} products, {has_img} with images")
    for p in (prods or []):
        cat = p['categ_id'][1] if p['categ_id'] else 'No Category'
        img = '✓' if p.get('image_1920') else '✗'
        print(f"    id={p['id']:5} img={img} ${p['list_price']:7.2f} | {p['name'][:50]:50} | {cat}")

# ── All published products (any website) ─────────────────────────────────────
print('\n=== ALL PRODUCTS WITHOUT IMAGES ===')
no_img = rpc('product.template', 'search_read',
             [[['image_1920', '=', False], ['is_published', '=', True]]],
             {'fields': ['id','name','website_id','categ_id'], 'limit': 100})
print(f"  {len(no_img or [])} published products have no image")
