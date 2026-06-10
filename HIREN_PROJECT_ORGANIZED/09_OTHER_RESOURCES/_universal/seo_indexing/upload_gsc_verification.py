"""
upload_gsc_verification.py
Uploads the Google Search Console HTML verification file to the Odoo instance
so it becomes publicly accessible at:
  https://www.ligiftbasket.com/google7eab7c6a696479f4.html
"""

import base64
import json
import time
import requests

# ── Config ────────────────────────────────────────────────────────────────────
ODOO_URL       = "https://country-cove-inc.odoo.com"
ODOO_DB        = "country-cove-inc"
ODOO_EMAIL     = "countrycoveinc@gmail.com"
ODOO_PASSWORD  = "M@nhattan1234"

# The file Google wants accessible at the root of the site
VERIFY_FILENAME = "google7eab7c6a696479f4.html"
VERIFY_CONTENT  = "google-site-verification: google7eab7c6a696479f4.html"

# The live domain (Odoo website ID 14)
LIVE_DOMAIN     = "https://www.ligiftbasket.com"

session = requests.Session()
session.headers.update({"Content-Type": "application/json"})


def rpc(endpoint: str, method: str, args: list, kwargs: dict = None) -> dict:
    payload = {
        "jsonrpc": "2.0",
        "method":  "call",
        "id":      1,
        "params": {
            "model":  endpoint,
            "method": method,
            "args":   args,
            "kwargs": kwargs or {},
        },
    }
    resp = session.post(
        f"{ODOO_URL}/web/dataset/call_kw",
        data=json.dumps(payload),
        timeout=30,
    )
    data = resp.json()
    if data.get("error"):
        raise RuntimeError(data["error"]["data"]["message"])
    return data["result"]


# ── Step 1: Authenticate ──────────────────────────────────────────────────────
print("Step 1 — Authenticating with Odoo…")
auth_resp = session.post(
    f"{ODOO_URL}/web/session/authenticate",
    data=json.dumps({
        "jsonrpc": "2.0",
        "method":  "call",
        "params": {
            "db":       ODOO_DB,
            "login":    ODOO_EMAIL,
            "password": ODOO_PASSWORD,
        },
    }),
    timeout=20,
).json()

uid = auth_resp.get("result", {}).get("uid")
if not uid:
    raise SystemExit(f"Auth failed: {auth_resp}")
print(f"  Authenticated as uid={uid}")


# ── Step 2: Delete any existing attachment with this URL (clean slate) ────────
print(f"\nStep 2 — Removing any existing attachment for /{VERIFY_FILENAME}…")
existing = rpc("ir.attachment", "search_read",
    [[["url", "=", f"/{VERIFY_FILENAME}"]]],
    {"fields": ["id", "name"]},
)
if existing:
    ids = [r["id"] for r in existing]
    rpc("ir.attachment", "unlink", [ids])
    print(f"  Removed {len(ids)} old attachment(s): {ids}")
else:
    print("  None found — proceeding fresh.")


# ── Step 3: Create the public static attachment ───────────────────────────────
print(f"\nStep 3 — Creating public attachment for /{VERIFY_FILENAME}…")
file_bytes   = VERIFY_CONTENT.encode("utf-8")
file_b64     = base64.b64encode(file_bytes).decode("ascii")

attachment_id = rpc("ir.attachment", "create", [{
    "name":        VERIFY_FILENAME,
    "type":        "binary",
    "datas":       file_b64,
    "url":         f"/{VERIFY_FILENAME}",
    "public":      True,
    "mimetype":    "text/html",
    "res_model":   "ir.ui.view",   # tie to website view model
}])
print(f"  Created attachment id={attachment_id}")


# ── Step 4: Make it public via sudo write ─────────────────────────────────────
print("\nStep 4 — Ensuring attachment is marked public…")
rpc("ir.attachment", "write", [[attachment_id], {"public": True}])
print("  Done.")


# ── Step 5: Verify it is accessible on the live domain ───────────────────────
print(f"\nStep 5 — Verifying URL is accessible on {LIVE_DOMAIN}…")
time.sleep(3)   # brief pause for Odoo to register the new route

test_url = f"{LIVE_DOMAIN}/{VERIFY_FILENAME}"
try:
    r = requests.get(test_url, timeout=15,
                     headers={"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"})
    print(f"  URL    : {test_url}")
    print(f"  Status : {r.status_code}")
    print(f"  Body   : {r.text.strip()[:120]}")

    if r.status_code == 200 and "google-site-verification" in r.text:
        print("\n  SUCCESS — File is live and accessible!")
        print("  Go back to Google Search Console and click VERIFY now.")
    elif r.status_code == 200:
        print("\n  File returned 200 but content looks wrong.")
        print(f"  Content: {r.text[:200]}")
    else:
        print(f"\n  File not accessible yet (HTTP {r.status_code}).")
        print("  Try the alternative: Odoo Website > Settings > HTML Head (meta tag method).")
except Exception as e:
    print(f"  Request error: {e}")

# ── Also test via Odoo's own /web/content route ───────────────────────────────
print(f"\nAlso checking /web/content/{attachment_id} (Odoo direct route)…")
r2 = requests.get(f"{ODOO_URL}/web/content/{attachment_id}", timeout=10)
print(f"  Status: {r2.status_code} | Body: {r2.text.strip()[:80]}")
