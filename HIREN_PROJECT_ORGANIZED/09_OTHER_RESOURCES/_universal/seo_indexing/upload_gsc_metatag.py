"""
upload_gsc_metatag.py
Sets Google Search Console verification on the ligiftbasket.com Odoo website
by injecting the meta tag into the website's custom <head> code.
Also tries the dedicated google_search_console field if available.
"""

import json
import time
import requests

ODOO_URL      = "https://country-cove-inc.odoo.com"
ODOO_DB       = "country-cove-inc"
ODOO_EMAIL    = "countrycoveinc@gmail.com"
ODOO_PASSWORD = "M@nhattan1234"

GSC_CODE      = "google7eab7c6a696479f4"
GSC_META_TAG  = f'<meta name="google-site-verification" content="{GSC_CODE}" />'
LIVE_DOMAIN   = "https://www.ligiftbasket.com"

# Website ID discovered from the 404 HTML: data-website-id="37"
WEBSITE_ID    = 37

session = requests.Session()
session.headers.update({"Content-Type": "application/json"})


def rpc(model: str, method: str, args: list, kwargs: dict = None) -> any:
    payload = {
        "jsonrpc": "2.0", "method": "call", "id": 1,
        "params": {
            "model": model, "method": method,
            "args": args, "kwargs": kwargs or {},
        },
    }
    resp = session.post(
        f"{ODOO_URL}/web/dataset/call_kw",
        data=json.dumps(payload), timeout=30,
    )
    data = resp.json()
    if data.get("error"):
        raise RuntimeError(data["error"]["data"]["message"])
    return data["result"]


# ── Authenticate ──────────────────────────────────────────────────────────────
print("Step 1 — Authenticating…")
auth = session.post(
    f"{ODOO_URL}/web/session/authenticate",
    data=json.dumps({"jsonrpc": "2.0", "method": "call",
                     "params": {"db": ODOO_DB, "login": ODOO_EMAIL,
                                "password": ODOO_PASSWORD}}),
    timeout=20,
).json()
uid = auth.get("result", {}).get("uid")
if not uid:
    raise SystemExit(f"Auth failed: {auth}")
print(f"  uid={uid}")


# ── Read current website record ───────────────────────────────────────────────
print(f"\nStep 2 — Reading website id={WEBSITE_ID}…")
sites = rpc("website", "search_read",
    [[["id", "=", WEBSITE_ID]]],
    {"fields": ["name", "domain", "custom_code_head",
                "google_analytics_key", "google_search_console"]},
)
if not sites:
    # Fallback: find by domain
    print("  Not found by ID — searching by domain…")
    sites = rpc("website", "search_read",
        [[["domain", "ilike", "ligiftbasket"]]],
        {"fields": ["id","name","domain","custom_code_head","google_search_console"]},
    )

if not sites:
    raise SystemExit("Could not find ligiftbasket website record in Odoo.")

site = sites[0]
actual_id = site["id"]
print(f"  Found: id={actual_id} | name={site['name']} | domain={site.get('domain','')}")
print(f"  Existing custom_code_head: {repr(site.get('custom_code_head') or '')[:120]}")
print(f"  Existing google_search_console: {repr(site.get('google_search_console') or '')}")


# ── Method A: dedicated google_search_console field (Odoo 16/17) ──────────────
print(f"\nStep 3A — Setting google_search_console field…")
try:
    rpc("website", "write", [[actual_id], {"google_search_console": GSC_CODE}])
    print(f"  Set google_search_console = '{GSC_CODE}'")
    gsc_field_ok = True
except Exception as e:
    print(f"  Field not available ({e}) — will use custom_code_head instead.")
    gsc_field_ok = False


# ── Method B: inject meta tag into custom_code_head ───────────────────────────
print(f"\nStep 3B — Injecting meta tag into custom_code_head…")
current_head = (site.get("custom_code_head") or "").strip()

# Remove any previous GSC tag to avoid duplicates
import re
current_head_clean = re.sub(
    r'<meta[^>]+google-site-verification[^>]+/?>', "", current_head, flags=re.I
).strip()

new_head = f"{GSC_META_TAG}\n{current_head_clean}".strip()
rpc("website", "write", [[actual_id], {"custom_code_head": new_head}])
print(f"  Updated custom_code_head:")
print(f"  {new_head[:200]}")


# ── Verify the meta tag is now live ──────────────────────────────────────────
print(f"\nStep 4 — Waiting 5 s then checking {LIVE_DOMAIN} for meta tag…")
time.sleep(5)

r = requests.get(LIVE_DOMAIN, timeout=15,
    headers={"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"})
print(f"  HTTP status: {r.status_code}")

found = re.findall(r'google-site-verification["\s:=]+([A-Za-z0-9_-]+)', r.text, re.I)
if found:
    print(f"\n  SUCCESS — Meta tag found in live HTML: {found[0]}")
    print("\n  Next steps:")
    print("  1. Go back to Google Search Console")
    print("  2. Click the VERIFY button")
    print("  3. After verification, go to Sitemaps and submit:")
    print(f"     {LIVE_DOMAIN}/sitemap.xml")
else:
    print("\n  Meta tag NOT yet visible in live HTML.")
    print("  Odoo may need a minute to clear its page cache.")
    print(f"  Try manually: curl {LIVE_DOMAIN} | grep google-site-verification")
    print("  OR: In Odoo backend — Settings > Activate Developer Mode")
    print("        then Website > Configuration > Settings > scroll to 'Head Code'")
    print(f"        and paste: {GSC_META_TAG}")

# ── Print full head for debugging ─────────────────────────────────────────────
head_match = re.search(r'<head[^>]*>(.*?)</head>', r.text, re.S | re.I)
if head_match:
    print(f"\n  Full <head> (first 1200 chars):")
    print(head_match.group(1)[:1200])
