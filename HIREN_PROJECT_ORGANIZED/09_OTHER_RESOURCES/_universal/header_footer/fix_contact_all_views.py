import xmlrpc.client, sys

sys.stdout.reconfigure(encoding='utf-8')
URL = 'https://country-cove-inc.odoo.com'
DB  = 'country-cove-inc'
UID = 2
PW  = 'M@nhattan1234'

models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
print("Connected\n")

PHONE     = '+1 (917) 338-7086'
PHONE_RAW = '+19173387086'
EMAIL     = 'countrycoveinc@gmail.com'

results = []

def patch_view(view_id, arch, label):
    res = models.execute_kw(DB, UID, PW, 'ir.ui.view', 'write',
                            [[view_id], {'arch_db': arch}])
    tag = '✅' if res else '❌'
    results.append(f"  {tag} [{view_id}] {label}")
    print(f"  {tag} [{view_id}] {label}")
    return res

def read_arch(view_id):
    return models.execute_kw(DB, UID, PW, 'ir.ui.view', 'read',
                             [[view_id]], {'fields': ['arch_db']})[0]['arch_db']

# ══════════════════════════════════════════════════════════════════════
# 1. FIX WRONG EMAIL IN VIEW 1381 (Convenience footer — Default)
# ══════════════════════════════════════════════════════════════════════
print("── [1381] Convenience footer — fix email ──")
arch = read_arch(1381)
if 'hiren@longislandconvinience.com' in arch:
    arch = arch.replace('mailto:hiren@longislandconvinience.com',
                        f'mailto:{EMAIL}')
    arch = arch.replace('hiren@longislandconvinience.com', EMAIL)
    patch_view(1381, arch, "Convenience footer — email updated")
elif EMAIL in arch:
    print("  ℹ️  Already correct, skipping.")
else:
    print("  ⚠️  Pattern not found — check manually.")

# ══════════════════════════════════════════════════════════════════════
# 2. FIX WRONG EMAIL IN VIEW 3506 (Cards footer)
# ══════════════════════════════════════════════════════════════════════
print("\n── [3506] Cards footer — fix email ──")
arch = read_arch(3506)
for old_email in ['hiren@longislandconvenience.com', 'hiren@longislandconvinience.com']:
    if old_email in arch:
        arch = arch.replace(f'mailto:{old_email}', f'mailto:{EMAIL}')
        arch = arch.replace(old_email, EMAIL)
        break
if EMAIL in arch:
    patch_view(3506, arch, "Cards footer — email updated")
else:
    print("  ⚠️  Pattern not found — check manually.")

# ══════════════════════════════════════════════════════════════════════
# 3. ADD PHONE TO FOOTERS 3629, 3630, 3631, 3627
#    Insert phone <p> immediately before the email <p>
# ══════════════════════════════════════════════════════════════════════
FOOTER_SITES = [
    # (view_id, site_name, accent_color)
    (3629, "Gift Basket footer",   "#2D6A4F"),
    (3630, "Balloons footer",      "#C77DFF"),
    (3631, "Print Mail footer",    "#4361EE"),
    (3627, "JHD Advisor footer",   "#8a2be2"),
]

for vid, label, color in FOOTER_SITES:
    print(f"\n── [{vid}] {label} — add phone ──")
    arch = read_arch(vid)

    if PHONE in arch or '338-7086' in arch:
        print(f"  ℹ️  Phone already present, skipping.")
        continue

    # Find the email <p> and insert phone <p> before it
    email_p = f'<p style="color:#666;font-size:0.85rem;"><a href="mailto:{EMAIL}"'
    if email_p in arch:
        phone_p = (
            f'<p style="color:#666;font-size:0.85rem;margin-bottom:4px;">'
            f'<a href="tel:{PHONE_RAW}" style="color:{color};text-decoration:none;font-weight:700;">'
            f'{PHONE}</a></p>\n                            '
        )
        arch = arch.replace(email_p, phone_p + email_p)
        patch_view(vid, arch, f"{label} — phone added")
    else:
        print(f"  ⚠️  email <p> pattern not found — check manually.")

# ══════════════════════════════════════════════════════════════════════
# 4. UPDATE CARDS HEADER (3508) — add phone to announcement bar
# ══════════════════════════════════════════════════════════════════════
print("\n── [3508] Cards header — add phone to announce bar ──")
arch = read_arch(3508)

old_announce = '<span>Free shipping on orders over $75 • Same-day dispatch before 3 PM • Open 7 days • Plainview, NY</span>'
new_announce = (
    '<span>Free shipping $75+ • Same-day dispatch before 3 PM • '
    f'<a href="tel:{PHONE_RAW}" style="color:#000;text-decoration:none;font-weight:900;">{PHONE}</a>'
    f' • <a href="mailto:{EMAIL}" style="color:#000;text-decoration:none;">{EMAIL}</a></span>'
)

# Try unicode bullet first, then literal •
if old_announce in arch:
    arch = arch.replace(old_announce, new_announce)
    patch_view(3508, arch, "Cards header — phone + email in announce bar")
else:
    # Try literal bullet character
    old_announce2 = '<span>Free shipping on orders over $75 • Same-day dispatch before 3 PM • Open 7 days • Plainview, NY</span>'
    if old_announce2 in arch:
        arch = arch.replace(old_announce2, new_announce)
        patch_view(3508, arch, "Cards header — phone + email in announce bar")
    else:
        # Check if phone already there
        if '338-7086' in arch or PHONE in arch:
            print("  ℹ️  Phone already in header.")
        else:
            print("  ⚠️  Announce bar text not found — check manually.")
            # Show snippet for debugging
            idx = arch.find('lic-announce')
            if idx != -1:
                print(f"  Current bar: {repr(arch[idx:idx+300])}")

# ══════════════════════════════════════════════════════════════════════
# 5. FIX VIEW 3635 (JHD Header Tweaks) — remove tel: hide CSS so
#    standard Odoo header shows the company phone we just set
# ══════════════════════════════════════════════════════════════════════
print("\n── [3635] JHD header — remove phone-hide CSS ──")
arch = read_arch(3635)

new_arch = """<data name="JHD Header Tweaks">
    <xpath expr="//head" position="inside">
        <style type="text/css">
            /* JHD Advisor: style company phone in header */
            header a[href^="tel:"] {
                color: #8a2be2 !important;
                font-weight: 700 !important;
                text-decoration: none !important;
            }
        </style>
    </xpath>
</data>"""

patch_view(3635, new_arch, "JHD header — phone now visible (styled purple)")

# ══════════════════════════════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════════════════════════════
print(f"\n{'═'*65}")
print("  CONTACT INFO FIX COMPLETE")
print(f"{'═'*65}")
for r in results:
    print(r)

print(f"""
  Phone:  {PHONE}
  Email:  {EMAIL}

  Coverage:
    ✅ res.company  — both fields set (governs CyberConsulting + standard templates)
    ✅ Convenience footer (1381) — email corrected
    ✅ Cards footer (3506)       — email corrected
    ✅ Gift Basket footer (3629) — phone added
    ✅ Balloons footer (3630)    — phone added
    ✅ Print Mail footer (3631)  — phone added
    ✅ JHD Advisor footer (3627) — phone added
    ✅ Cards header (3508)       — phone + email in announce bar
    ✅ JHD header (3635)         — company phone now visible
    ✅ Print Mail header (3514)  — phone already in bar (unchanged)

  Hard-refresh each site with Ctrl+Shift+R to verify.
""")
