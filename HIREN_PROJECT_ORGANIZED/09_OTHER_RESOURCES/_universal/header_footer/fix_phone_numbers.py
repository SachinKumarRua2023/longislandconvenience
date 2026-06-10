#!/usr/bin/env python3
"""
Fix phone numbers across Long Island Convenience (1), Gift Basket (37), Print & Mail (39).
Replace ALL occurrences of wrong numbers with (917) 338-7086.
"""
import xmlrpc.client, sys, re
sys.stdout.reconfigure(encoding='utf-8')

URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"

uid = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common').authenticate(DB, USER, PASS, {})
m   = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
xc  = lambda mo, me, a, k={}: m.execute_kw(DB, uid, PASS, mo, me, a, k)
print(f"Connected UID {uid}")

CORRECT       = "(917) 338-7086"
CORRECT_HREF  = "tel:+19173387086"
CORRECT_PLAIN = "+1 (917) 338-7086"

WRONG_NUMBERS = [
    "(212) 564-8585", "212-564-8585", "212) 564-8585", "2125648585",
    "(516) 555-0100", "516-555-0100", "516) 555-0100", "5165550100",
    "(516) 300-1234", "516-300-1234",
    "(212) 564.8585", "212.564.8585",
]
WRONG_HREFS = [
    "tel:+12125648585", "tel:+15165550100", "tel:+15163001234",
    "tel:+12125648585", "tel:(212)564-8585", "tel:(516)555-0100",
]

def fix_phones(arch):
    changed = False
    # Fix display numbers
    for wrong in WRONG_NUMBERS:
        if wrong in arch:
            arch = arch.replace(wrong, CORRECT)
            changed = True
    # Fix tel: href links
    for wrong_href in WRONG_HREFS:
        if wrong_href in arch:
            arch = arch.replace(wrong_href, CORRECT_HREF)
            changed = True
    # Fix any remaining 212-564 or 516-555 patterns with regex
    new_arch = re.sub(r'\(212\)\s*564[–\-]8585', CORRECT, arch)
    if new_arch != arch: changed = True; arch = new_arch
    new_arch = re.sub(r'212[–\-\.]564[–\-\.]8585', CORRECT, arch)
    if new_arch != arch: changed = True; arch = new_arch
    new_arch = re.sub(r'\(516\)\s*555[–\-]0100', CORRECT, arch)
    if new_arch != arch: changed = True; arch = new_arch
    new_arch = re.sub(r'516[–\-\.]555[–\-\.]0100', CORRECT, arch)
    if new_arch != arch: changed = True; arch = new_arch
    # Fix tel hrefs
    new_arch = re.sub(r'tel:\+?1?2125648585', CORRECT_HREF, arch)
    if new_arch != arch: changed = True; arch = new_arch
    new_arch = re.sub(r'tel:\+?1?5165550100', CORRECT_HREF, arch)
    if new_arch != arch: changed = True; arch = new_arch
    return arch, changed

total_fixed = 0
for site_id, site_name in [(1,'LI Convenience'),(37,'LI Gift Basket'),(39,'LI Print & Mail')]:
    print(f"\n=== {site_name} (site {site_id}) ===")
    views = xc('ir.ui.view','search_read',
        [[['website_id','=',site_id]]],
        {'fields':['id','key','arch_db']})
    for v in views:
        arch, changed = fix_phones(v['arch_db'])
        if changed:
            xc('ir.ui.view','write',[[v['id']],{'arch_db':arch}])
            print(f"  FIXED view {v['id']} {v['key'][:55]}")
            total_fixed += 1
        else:
            # Check if it already has correct number or no phone
            if CORRECT in v['arch_db']:
                print(f"  OK    view {v['id']} {v['key'][:55]} (already correct)")

print(f"\nTotal views fixed: {total_fixed}")
print(f"Correct number now everywhere: {CORRECT}")
