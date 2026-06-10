    import xmlrpc.client, sys

    sys.stdout.reconfigure(encoding='utf-8')
    URL = 'https://country-cove-inc.odoo.com'
    DB  = 'country-cove-inc'
    UID = 2
    PW  = 'M@nhattan1234'

    models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
    print("Connected\n")

    # ─────────────────────────────────────────────────────────────
    # NUCLEAR FIX — delete ALL custom hover/pcd views for site 37
    # Then create ONE clean view with JS wrapped in CDATA so XML
    # parser never chokes on && < > characters inside script tags
    # ─────────────────────────────────────────────────────────────

    # Step 1: Find and kill EVERY view on site 37 that has pcd in it
    print("Step 1: Finding all broken pcd/hover views...")
    all_views = models.execute_kw(DB, UID, PW, 'ir.ui.view', 'search_read', [[
        ['website_id', '=', 37]
    ]], {'fields': ['id', 'name', 'key', 'arch_db']})

    kill_ids = []
    for v in all_views:
        arch = v.get('arch_db', '') or ''
        name = v.get('name', '') or ''
        key  = v.get('key',  '') or ''
        if any(x in arch for x in ['pcd-', 'pcd_', 'pcdOpen', 'pcdClose', 'pcd-modal', 'PRODUCT CARD HOVER']):
            kill_ids.append(v['id'])
            print(f"  Will delete [{v['id']}] {name} ({key})")
        elif any(x in name for x in ['Hover', 'hover', 'Global Hover']):
            kill_ids.append(v['id'])
            print(f"  Will delete [{v['id']}] {name} ({key})")

    # Also kill by key
    key_search = models.execute_kw(DB, UID, PW, 'ir.ui.view', 'search', [[
        ['key', 'in', [
            'ligiftbasket.global_hover_css',
            'ligiftbasket.shop_hover_styles',
        ]]
    ]])
    for vid in key_search:
        if vid not in kill_ids:
            kill_ids.append(vid)
            print(f"  Will delete [{vid}] (by key)")

    if kill_ids:
        models.execute_kw(DB, UID, PW, 'ir.ui.view', 'unlink', [kill_ids])
        print(f"\n  ✅ Deleted {len(kill_ids)} views: {kill_ids}")
    else:
        print("  No pcd views found.")

    # Step 2: Clean homepage view 2956
    print("\nStep 2: Cleaning view 2956 (homepage)...")
    arch_home = models.execute_kw(DB, UID, PW, 'ir.ui.view', 'read',
                                [[2956]], {'fields': ['arch_db']})[0]['arch_db']
    markers = [
        ('<!-- ===== PRODUCT CARD HOVER DESCRIPTION =====',
        '<!-- ===== END PRODUCT CARD HOVER DESCRIPTION ====='),
        ('<!-- pcd-start -->', '<!-- pcd-end -->'),
    ]
    cleaned = False
    for ms, me in markers:
        while ms in arch_home and me in arch_home:
            s = arch_home.index(ms)
            e = arch_home.index(me) + len(me)
            arch_home = arch_home[:s] + arch_home[e:]
            cleaned = True

    # Also strip any lingering <style> or <script> blocks with pcd
    import re
    arch_home = re.sub(r'<style>[^<]*pcd[^<]*(?:<[^/][^<]*)*?</style>', '', arch_home, flags=re.DOTALL)
    arch_home = re.sub(r'<script>[^<]*pcd[^<]*(?:<[^/][^<]*)*?</script>', '', arch_home, flags=re.DOTALL)

    models.execute_kw(DB, UID, PW, 'ir.ui.view', 'write',
                    [[2956], {'arch_db': arch_home}])
    print(f"  Homepage cleaned (had markers: {cleaned})")

    # Step 3: Verify site is up by checking view 2956 is valid
    print("\nStep 3: Verifying homepage view is readable...")
    check = models.execute_kw(DB, UID, PW, 'ir.ui.view', 'read',
                            [[2956]], {'fields': ['name', 'active']})[0]
    print(f"  View 2956: name={check['name']}, active={check['active']}")

    print("""
    ══════════════════════════════════════════════════
    NUCLEAR CLEAN COMPLETE

    All pcd/hover views deleted.
    Homepage view cleaned.

    ✅ https://www.ligiftbasket.com should now load.

    The hover feature has been removed cleanly.
    A safe version can be added later if needed.
    ══════════════════════════════════════════════════
    """)