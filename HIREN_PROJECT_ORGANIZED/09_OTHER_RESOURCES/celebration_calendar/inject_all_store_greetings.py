"""
Injects celebration greeting banners into all 7 Hiren Kumar Odoo websites.

Approach:
  - Creates a standalone page at /celebrations on each Odoo website
  - HTML files are always saved locally for manual paste-in too
  - Run this script any time the calendar is updated

Usage:
  python inject_all_store_greetings.py
"""

import sys, re, time, json, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from pathlib import Path
from datetime import date
import requests

sys.path.insert(0, str(Path(__file__).parent))
from store_configs import STORES
from build_store_greetings import build_store_html, build_all_days

ODOO_URL  = "https://country-cove-inc.odoo.com"
ODOO_DB   = "country-cove-inc"
ODOO_USER = "countrycoveinc@gmail.com"
ODOO_PASS = "M@nhattan1234"

BASE_OUTPUT = Path(r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\ScrappedMaterial")

STORE_FOLDERS = {
    "LongIslandConvenience": "01_LongIslandConvenience",
    "LongIslandBalloons":    "02_LongIslandBalloons",
    "LIGiftBasket":          "03_LIGiftBasket",
    "LongIslandPrintMail":   "04_LongIslandPrintMail",
    "LongIslandCards":       "05_LongIslandCards",
    "HirenKumar":            "06_HirenKumar",
    "ConsultCyber":          "07_ConsultCyber",
}


# ── Odoo RPC client ───────────────────────────────────────────────────────────
class Odoo:
    def __init__(self):
        self.s = requests.Session()
        self.s.headers["Content-Type"] = "application/json"
        self.uid = None
        self._auth()

    def _auth(self):
        r = self.s.post(f"{ODOO_URL}/web/session/authenticate", json={
            "jsonrpc": "2.0", "method": "call", "id": 1,
            "params": {"db": ODOO_DB, "login": ODOO_USER, "password": ODOO_PASS}
        })
        self.uid = r.json().get("result", {}).get("uid")
        print(f"  Odoo auth: uid={self.uid}" if self.uid else "  Odoo auth FAILED")

    def rpc(self, model, method, args=None, kw=None):
        r = self.s.post(f"{ODOO_URL}/web/dataset/call_kw", json={
            "jsonrpc": "2.0", "method": "call", "id": 2,
            "params": {"model": model, "method": method,
                       "args": args or [], "kwargs": kw or {}}
        })
        data = r.json()
        if "error" in data:
            msg = data["error"].get("data", {}).get("message", str(data["error"]))
            raise RuntimeError(msg[:300])
        return data.get("result")

    def search_read(self, model, domain, fields, limit=10):
        return self.rpc(model, "search_read",
                        args=[domain], kw={"fields": fields, "limit": limit})

    def write(self, model, ids, vals):
        return self.rpc(model, "write", args=[ids, vals])

    def create(self, model, vals):
        return self.rpc(model, "create", args=[vals])


# ── XML-safe arch builder ─────────────────────────────────────────────────────
def _html_to_qweb_arch(html: str, view_name: str) -> str:
    """
    Convert raw HTML to a valid Odoo QWeb arch string.
    - Escapes bare & that are not already XML entities
    - Wraps in a minimal QWeb template
    """
    # Escape bare & (not already &amp; &lt; &gt; &quot; &#NN; &#xNN;)
    safe = re.sub(r'&(?!(amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)', '&amp;', html)
    # Remove HTML comments with -- sequences that break XML
    safe = re.sub(r'<!--.*?-->', '', safe, flags=re.DOTALL)
    return (
        f'<t t-name="{view_name}">'
        f'<t t-call="website.layout">'
        f'<div id="wrap" class="oe_structure">'
        f'{safe}'
        f'</div>'
        f'</t>'
        f'</t>'
    )


# ── Per-store page injection ──────────────────────────────────────────────────
def inject_store(odoo: Odoo, store_key: str, store: dict, rows: list) -> dict:
    site_id = store.get("odoo_site_id")
    name    = store["name"]
    domain  = store["domain"]
    result  = {"store": name, "site_id": site_id, "status": "PENDING", "note": ""}

    # Build + save HTML locally (always)
    html = build_store_html(store_key, store, rows)
    folder   = STORE_FOLDERS[store_key]
    out_file = BASE_OUTPUT / folder / "homepage_celebration_banner.html"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")

    if not site_id:
        result.update(status="FILE_ONLY",
                      note=f"No Odoo site ID — HTML saved to {out_file.name}")
        print(f"  [{name}] No site ID -> HTML saved locally")
        return result

    if not odoo.uid:
        result.update(status="NO_AUTH", note="Odoo login failed")
        return result

    url       = "/celebrations"
    page_name = f"{name} Celebrations"
    view_name = f"website.celebrations.{store_key.lower()}"
    arch      = _html_to_qweb_arch(html, view_name)

    try:
        # Does a /celebrations page already exist for this site?
        existing = odoo.search_read(
            "website.page",
            [["website_id", "=", site_id], ["url", "=", url]],
            ["id", "view_id"]
        )

        if existing:
            page_id = existing[0]["id"]
            view_id = existing[0].get("view_id")
            if isinstance(view_id, list):
                view_id = view_id[0]
            if view_id:
                odoo.write("ir.ui.view", [view_id], {"arch_db": arch})
                result.update(status="UPDATED",
                              note=f"https://{domain}{url} refreshed (page {page_id})")
                print(f"  [{name}] Updated: https://{domain}{url}")
            else:
                result.update(status="NO_VIEW", note="Page exists but no view_id found")
        else:
            # Create view first (no website_id — causes constraint issues on some Odoo versions)
            view_id = odoo.create("ir.ui.view", {
                "name":    page_name,
                "type":    "qweb",
                "arch_db": arch,
            })
            # Create page — try with website_id first, fall back to global
            try:
                page_id = odoo.create("website.page", {
                    "name":              page_name,
                    "url":               f"/celebrations-{site_id}",
                    "website_id":        site_id,
                    "view_id":           view_id,
                    "is_published":      True,
                    "website_published": True,
                })
                url = f"/celebrations-{site_id}"
            except Exception:
                page_id = odoo.create("website.page", {
                    "name":              page_name,
                    "url":               f"/celebrations-{site_id}",
                    "view_id":           view_id,
                    "is_published":      True,
                    "website_published": True,
                })
            result.update(status="CREATED",
                          note=f"https://{domain}{url} (page {page_id})")
            print(f"  [{name}] Created: https://{domain}{url}")

    except Exception as e:
        result.update(status="ERROR", note=str(e)[:300])
        print(f"  [{name}] Error: {e}")

    time.sleep(0.8)
    return result


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    today = date.today()
    print(f"\n{'='*65}")
    print(f"  ODOO CELEBRATION BANNER INJECTOR — ALL 7 STORES")
    print(f"  Date: {today}")
    print(f"{'='*65}\n")

    rows = build_all_days()
    upcoming = [r for r in rows if isinstance(r.get("Days Until"), int) and r["Days Until"] >= 0]
    print(f"  Events: {len(rows)} total | {len(upcoming)} upcoming\n")

    odoo    = Odoo()
    results = []

    for store_key, store in STORES.items():
        print(f"\n  Processing: {store['name']} (site_id={store.get('odoo_site_id')})")
        res = inject_store(odoo, store_key, store, rows)
        results.append(res)

    # Summary
    print(f"\n{'='*65}")
    print(f"  INJECTION SUMMARY")
    print(f"{'='*65}")
    icons = {"CREATED":"[+]","UPDATED":"[OK]","FILE_ONLY":"[F]",
             "NO_VIEW":"[?]","ERROR":"[X]","NO_AUTH":"[!]","PENDING":"[-]"}
    for r in results:
        icon = icons.get(r["status"], "[?]")
        print(f"  {icon} {r['store']:35s} {r['status']:12s}  {r['note']}")

    live = sum(1 for r in results if r["status"] in ("CREATED","UPDATED"))
    saved = sum(1 for r in results if r["status"] in ("CREATED","UPDATED","FILE_ONLY"))
    print(f"\n  Live in Odoo: {live}/7  |  HTML files saved: {saved}/7")

    # Save summary JSON
    summary = BASE_OUTPUT / "injection_summary.json"
    with open(summary, "w") as f:
        json.dump({"date": str(today), "results": results}, f, indent=2)
    print(f"\n  Summary: {summary}")

    print(f"\n  MANUAL PASTE GUIDE (for stores without Odoo site IDs):")
    print(f"  1. Odoo -> Website (select site) -> Edit homepage")
    print(f"  2. Click '+' -> Blocks -> HTML")
    print(f"  3. Paste from: ScrappedMaterial/<store>/homepage_celebration_banner.html")
    print(f"{'='*65}")


if __name__ == "__main__":
    main()
