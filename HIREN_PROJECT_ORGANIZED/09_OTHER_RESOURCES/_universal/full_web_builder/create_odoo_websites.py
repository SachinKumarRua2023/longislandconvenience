#!/usr/bin/env python3
"""
Country Cove Inc -- Create/Fix All Odoo Websites
Handles real Odoo state: renames wrong sites, deletes duplicates, creates missing 3
Run: python create_odoo_websites.py
"""

import xmlrpc.client
import sys

URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"

# Final desired state
FINAL_SITES = [
    {"name": "Country Cove LI",                    "domain": "countrycoveli.com"},
    {"name": "Country Cove Balloons & Decorations", "domain": "countrycoveballoons.com"},
    {"name": "Country Cove Sports & Cards",         "domain": "countrycovesportscards.com"},
    {"name": "Country Cove Greeting Cards & Gifts", "domain": "countrycovegreetingcards.com"},
    {"name": "Country Cove Gift Baskets",           "domain": "countrycovegiftbasket.com"},
    {"name": "Country Cove Cigars & Smoke",         "domain": "countrycovecigars.com"},
    {"name": "Country Cove Lotto",                  "domain": "countrycovelotto.com"},
    {"name": "Country Cove Print & Copy",           "domain": "countrycoveprintservices.com"},
]

# Names to delete (wrong/duplicate sites)
# Note: "Country Cove LI" appears twice -- we delete the duplicate (keep the original ID 1 and rename it)
DELETE_NAMES = [
    "Country Cove Gift Cards",
    "Country Cove Game Cards",
    "Cyber Consulting",
    "CyberConsulting",
]

# Sites to rename: old name -> {new name, new domain}
RENAMES = {
    "Long Island Convenience":       {"name": "Country Cove LI",                    "domain": "countrycoveli.com"},
    "Country Cove Sports and Cards": {"name": "Country Cove Sports & Cards",         "domain": "countrycovesportscards.com"},
    "Country Cove Gift Baskets":     {"name": "Country Cove Gift Baskets",           "domain": "countrycovegiftbasket.com"},
    "Country Cove Balloons":         {"name": "Country Cove Balloons & Decorations", "domain": "countrycoveballoons.com"},
    "Country Cove Greeting Cards":   {"name": "Country Cove Greeting Cards & Gifts", "domain": "countrycovegreetingcards.com"},
}


def connect():
    common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
    uid = common.authenticate(DB, USER, PASS, {})
    if not uid:
        print("ERROR: Authentication failed")
        sys.exit(1)
    models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
    print("Connected as UID " + str(uid))
    return models, uid


def list_sites(models, uid, label=""):
    sites = models.execute_kw(DB, uid, PASS, 'website', 'search_read',
        [[]], {'fields': ['id', 'name', 'domain']})
    if label:
        print("\n" + label + " (" + str(len(sites)) + " sites):")
    for s in sites:
        print("  [" + str(s['id']) + "] " + str(s['name']) + "  --  " + str(s.get('domain', '')))
    return sites


def try_delete(models, uid, site_id, site_name):
    try:
        models.execute_kw(DB, uid, PASS, 'website', 'unlink', [[site_id]])
        print("  DELETED: " + site_name + " (ID " + str(site_id) + ")")
        return True
    except Exception as e:
        print("  Cannot delete " + site_name + " -- archiving: " + str(e)[:80])
        try:
            models.execute_kw(DB, uid, PASS, 'website', 'write',
                [[site_id], {'active': False}])
            print("  ARCHIVED: " + site_name)
            return True
        except Exception as e2:
            print("  SKIP: " + str(e2)[:80])
            return False


def step1_delete_wrong_sites(models, uid):
    print("\n[STEP 1] Deleting wrong/duplicate sites...")

    # Delete from DELETE_NAMES list
    for bad_name in DELETE_NAMES:
        found = models.execute_kw(DB, uid, PASS, 'website', 'search_read',
            [[('name', '=', bad_name)]], {'fields': ['id', 'name']})
        for s in found:
            try_delete(models, uid, s['id'], s['name'])

    # Handle duplicate "Country Cove LI": keep the one with domain countrycoveli.com, delete others
    dup = models.execute_kw(DB, uid, PASS, 'website', 'search_read',
        [[('name', '=', 'Country Cove LI')]], {'fields': ['id', 'name', 'domain']})
    if len(dup) > 1:
        # Keep the one with correct domain, delete the rest
        for s in dup[1:]:
            print("  DUPLICATE Country Cove LI (ID " + str(s['id']) + ") -- deleting")
            try_delete(models, uid, s['id'], s['name'])


def step2_clear_conflicting_domains(models, uid):
    """Before renaming, clear any domain that would conflict with our target domains."""
    print("\n[STEP 2] Clearing domain conflicts...")
    target_domains = {fix['domain'] for fix in RENAMES.values()}

    for domain in target_domains:
        found = models.execute_kw(DB, uid, PASS, 'website', 'search_read',
            [[('domain', '=', domain)]], {'fields': ['id', 'name', 'domain']})
        for s in found:
            # Only clear if this site is NOT already named correctly for this domain
            correct_name = next((f['name'] for f in RENAMES.values() if f['domain'] == domain), None)
            if s['name'] != correct_name and s['name'] not in RENAMES:
                # This site is squatting the domain -- clear it
                print("  Clearing domain from [" + str(s['id']) + "] " + s['name'])
                models.execute_kw(DB, uid, PASS, 'website', 'write',
                    [[s['id']], {'domain': ''}])


def step3_rename_existing(models, uid):
    print("\n[STEP 3] Renaming/fixing existing sites...")
    for old_name, fix in RENAMES.items():
        found = models.execute_kw(DB, uid, PASS, 'website', 'search_read',
            [[('name', '=', old_name)]], {'fields': ['id', 'name', 'domain']})
        if found:
            s = found[0]
            try:
                models.execute_kw(DB, uid, PASS, 'website', 'write',
                    [[s['id']], {'name': fix['name'], 'domain': fix['domain']}])
                print("  RENAMED [" + str(s['id']) + "]: " + old_name + " -> " + fix['name'])
            except Exception as e:
                print("  FAILED rename " + old_name + ": " + str(e)[:100])
        else:
            print("  NOT FOUND (skip): " + old_name)


def step4_create_missing(models, uid):
    print("\n[STEP 4] Creating missing sites...")
    for site in FINAL_SITES:
        exists = models.execute_kw(DB, uid, PASS, 'website', 'search_read',
            [[('name', '=', site['name'])]], {'fields': ['id']})
        if exists:
            # Also make sure domain is correct
            models.execute_kw(DB, uid, PASS, 'website', 'write',
                [[exists[0]['id']], {'domain': site['domain']}])
            print("  EXISTS  : " + site['name'] + " (domain confirmed)")
        else:
            try:
                wid = models.execute_kw(DB, uid, PASS, 'website', 'create',
                    [{'name': site['name'], 'domain': site['domain']}])
                print("  CREATED : [" + str(wid) + "] " + site['name'] + " (" + site['domain'] + ")")
            except Exception as e:
                print("  FAILED  : " + site['name'] + " -- " + str(e)[:80])


def step5_update_company(models, uid):
    print("\n[STEP 5] Updating company info...")
    company = models.execute_kw(DB, uid, PASS, 'res.company', 'search_read',
        [[]], {'fields': ['id', 'name']})
    if not company:
        print("  No company found")
        return
    cid = company[0]['id']
    try:
        models.execute_kw(DB, uid, PASS, 'res.company', 'write', [[cid], {
            'name':    'Country Cove Inc',
            'street':  '605 Old Country Road',
            'city':    'Plainview',
            'zip':     '11803',
            'phone':   '+1 (917) 338-7086',
            'email':   'countrycoveinc@gmail.com',
            'website': 'https://countrycoveli.com',
        }])
        print("  Company updated: Country Cove Inc -- Plainview NY 11803")
    except Exception as e:
        print("  Company update: " + str(e)[:80])


def main():
    print("\n" + "="*60)
    print("  Country Cove Inc -- Odoo Website Cleanup & Setup")
    print("="*60)

    models, uid = connect()
    list_sites(models, uid, "BEFORE")

    step1_delete_wrong_sites(models, uid)
    step2_clear_conflicting_domains(models, uid)
    step3_rename_existing(models, uid)
    step4_create_missing(models, uid)
    step5_update_company(models, uid)

    print()
    final = list_sites(models, uid, "AFTER -- Final State")

    print("\n" + "="*60)
    print("  DONE. " + str(len(final)) + " websites in Odoo.")
    print("\n  HUB:    countrycoveli.com")
    print("  STORE1: countrycoveballoons.com")
    print("  STORE2: countrycovesportscards.com")
    print("  STORE3: countrycovegreetingcards.com")
    print("  STORE4: countrycovegiftbasket.com")
    print("  STORE5: countrycovecigars.com  [21+ AGE GATE NEEDED]")
    print("  STORE6: countrycovelotto.com")
    print("  STORE7: countrycoveprintservices.com")
    print("\n  Next: python setup_odoo_stores.py  (adds all products)")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
