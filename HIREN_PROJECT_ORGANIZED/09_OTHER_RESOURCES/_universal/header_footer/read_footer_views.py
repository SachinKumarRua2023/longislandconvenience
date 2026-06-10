#!/usr/bin/env python3
"""Read footer view content to understand structure"""
import xmlrpc.client, sys

URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"

def connect():
    uid = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common').authenticate(DB, USER, PASS, {})
    if not uid: sys.exit("Auth failed")
    m = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
    return m, uid

def xc(m, uid, model, method, args, kwargs={}):
    return m.execute_kw(DB, uid, PASS, model, method, args, kwargs)

def main():
    m, uid = connect()
    print("Connected\n")

    # Read global footer_custom view [671]
    print("=== Global footer_custom [671] ===")
    v = xc(m, uid, 'ir.ui.view', 'read', [[671]], {'fields': ['id','name','key','arch_db','website_id','inherit_id']})
    if v:
        print(f"key: {v[0]['key']}")
        print(f"website_id: {v[0]['website_id']}")
        print(f"inherit_id: {v[0]['inherit_id']}")
        print(f"arch_db:\n{v[0]['arch_db'][:3000]}")

    print("\n=== Website-1 footer_custom [1381] ===")
    v2 = xc(m, uid, 'ir.ui.view', 'read', [[1381]], {'fields': ['id','name','key','arch_db','website_id','inherit_id']})
    if v2:
        print(f"key: {v2[0]['key']}")
        print(f"website_id: {v2[0]['website_id']}")
        print(f"inherit_id: {v2[0]['inherit_id']}")
        print(f"arch_db:\n{v2[0]['arch_db'][:3000]}")

    # Also check copyright view
    print("\n=== footer_copyright_company_name [687] ===")
    v3 = xc(m, uid, 'ir.ui.view', 'read', [[687]], {'fields': ['id','name','key','arch_db','website_id']})
    if v3:
        print(f"arch_db:\n{v3[0]['arch_db'][:1000]}")

if __name__ == '__main__':
    main()
