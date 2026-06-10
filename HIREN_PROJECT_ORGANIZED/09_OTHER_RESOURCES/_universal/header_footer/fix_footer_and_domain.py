#!/usr/bin/env python3
"""
Fix longislandcards.com footer mismatch:
1. Find footer templates with CyberConsulting / Long Island Convenience
2. Create website-36-specific footer override
3. Verify currency is USD
4. Check website domain config
"""
import xmlrpc.client, sys

URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"
SITE_ID = 36

def connect():
    uid = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common').authenticate(DB, USER, PASS, {})
    if not uid: sys.exit("Auth failed")
    m = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
    print(f"Connected UID {uid}")
    return m, uid

def xc(m, uid, model, method, args, kwargs={}):
    return m.execute_kw(DB, uid, PASS, model, method, args, kwargs)

def main():
    m, uid = connect()

    # ── 1. Check website 36 config ────────────────────────────
    print("\n[1] Website 36 config:")
    site = xc(m, uid, 'website', 'search_read', [[('id','=',SITE_ID)]], {
        'fields': ['id','name','domain','company_id']
    })
    for s in site:
        print(f"  ID={s['id']} name={s['name']} domain={s['domain']} company={s['company_id']}")

    # ── 2. List ALL websites to see domain mapping ─────────────
    print("\n[2] All websites:")
    all_sites = xc(m, uid, 'website', 'search_read', [[]], {
        'fields': ['id','name','domain']
    })
    for s in all_sites:
        print(f"  [{s['id']}] {s['name']} => {s.get('domain','')}")

    # ── 3. Search for CyberConsulting in views ─────────────────
    print("\n[3] Views containing 'CyberConsulting':")
    views = xc(m, uid, 'ir.ui.view', 'search_read',
        [[('arch_db','ilike','CyberConsulting')]],
        {'fields': ['id','name','key','website_id','active'], 'limit': 20})
    for v in views:
        print(f"  [{v['id']}] key={v['key']} website={v.get('website_id')} active={v['active']}")

    # ── 4. Search for "Long Island Convenience" in views ──────
    print("\n[4] Views containing 'Long Island Convenience':")
    views2 = xc(m, uid, 'ir.ui.view', 'search_read',
        [[('arch_db','ilike','Long Island Convenience')]],
        {'fields': ['id','name','key','website_id','active'], 'limit': 20})
    for v in views2:
        print(f"  [{v['id']}] key={v['key']} website={v.get('website_id')} active={v['active']}")

    # ── 5. Search for footer-related views on site 36 ─────────
    print("\n[5] Footer views on website 36:")
    footer_views = xc(m, uid, 'ir.ui.view', 'search_read',
        [[('key','ilike','footer'),('website_id','=',SITE_ID)]],
        {'fields': ['id','name','key','website_id','active'], 'limit': 20})
    for v in footer_views:
        print(f"  [{v['id']}] key={v['key']} active={v['active']}")

    # ── 6. Search for global footer views (no website) ────────
    print("\n[6] Global footer views (no website_id):")
    global_footer = xc(m, uid, 'ir.ui.view', 'search_read',
        [[('key','ilike','footer'),('website_id','=',False)]],
        {'fields': ['id','name','key','website_id','active'], 'limit': 20})
    for v in global_footer:
        print(f"  [{v['id']}] key={v['key']} active={v['active']}")

    # ── 7. Verify company currency ─────────────────────────────
    print("\n[7] Company currency:")
    comp = xc(m, uid, 'res.company', 'search_read', [[]], {
        'fields': ['id','name','currency_id']
    })
    for c in comp:
        print(f"  [{c['id']}] {c['name']} currency={c['currency_id']}")

    # ── 8. Check active pricelists ────────────────────────────
    print("\n[8] Active pricelists:")
    pl = xc(m, uid, 'product.pricelist', 'search_read',
        [[('active','in',[True,False])]],
        {'fields': ['id','name','currency_id','active'], 'limit': 10})
    for p in pl:
        print(f"  [{p['id']}] {p['name']} currency={p['currency_id']} active={p['active']}")

if __name__ == '__main__':
    main()
