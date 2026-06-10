"""
Injects the AI greeting widget into all 7 Odoo homepage views.
Uses the same idempotent marker approach as inject_homepage_banner.py.

Run AFTER build_ai_widget.py has generated the ai_widget.html files.
Run AFTER deploying ai_proxy_server.py on your VPS and updating AI_PROXY_URL.
"""

import sys, io, re, time, json, requests
from pathlib import Path
from datetime import date

# Redirect stdout before any imports that also redirect it
if hasattr(sys.stdout, "buffer") and not isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
elif hasattr(sys.stdout, "buffer"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, str(Path(__file__).parent))
from store_configs import STORES
from build_ai_widget import build_widget_html, AI_PROXY_URL
from build_master_celebration_sheet import build_all_days

ODOO_URL  = "https://country-cove-inc.odoo.com"
ODOO_DB   = "country-cove-inc"
ODOO_USER = "countrycoveinc@gmail.com"
ODOO_PASS = "M@nhattan1234"

BASE = Path(r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\ScrappedMaterial")
STORE_FOLDERS = {
    "LongIslandConvenience": "01_LongIslandConvenience",
    "LongIslandBalloons":    "02_LongIslandBalloons",
    "LIGiftBasket":          "03_LIGiftBasket",
    "LongIslandPrintMail":   "04_LongIslandPrintMail",
    "LongIslandCards":       "05_LongIslandCards",
    "HirenKumar":            "06_HirenKumar",
    "ConsultCyber":          "07_ConsultCyber",
}

WIDGET_START = "<!-- AI-WIDGET-START -->"
WIDGET_END   = "<!-- AI-WIDGET-END -->"


class Odoo:
    def __init__(self):
        self.s = requests.Session()
        self.s.headers["Content-Type"] = "application/json"
        self.uid = None
        r = self.s.post(f"{ODOO_URL}/web/session/authenticate", json={
            "jsonrpc":"2.0","method":"call","id":1,
            "params":{"db":ODOO_DB,"login":ODOO_USER,"password":ODOO_PASS}
        })
        self.uid = r.json().get("result",{}).get("uid")
        print(f"  Odoo auth: uid={self.uid}" if self.uid else "  Odoo auth FAILED")

    def rpc(self, model, method, args=None, kw=None):
        r = self.s.post(f"{ODOO_URL}/web/dataset/call_kw", json={
            "jsonrpc":"2.0","method":"call","id":2,
            "params":{"model":model,"method":method,"args":args or [],"kwargs":kw or {}}
        })
        d = r.json()
        if "error" in d:
            raise RuntimeError(d["error"]["data"]["message"][:300])
        return d.get("result")

    def search_read(self, model, domain, fields, limit=20):
        return self.rpc(model, "search_read", args=[domain], kw={"fields":fields,"limit":limit})

    def read(self, model, ids, fields):
        return self.rpc(model, "read", args=[ids], kw={"fields":fields})

    def write(self, model, ids, vals):
        return self.rpc(model, "write", args=[ids, vals])


def escape_for_arch(html: str) -> str:
    """Escape bare & that aren't already XML entities, and wrap in marker comments."""
    safe = re.sub(r'&(?!(amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)', '&amp;', html)
    return f"{WIDGET_START}\n{safe}\n{WIDGET_END}"


def strip_old_widget(arch: str) -> str:
    return re.sub(
        re.escape(WIDGET_START) + r".*?" + re.escape(WIDGET_END),
        "", arch, flags=re.DOTALL
    )


def inject_widget_before_closing(arch: str, widget_block: str) -> str:
    """Append widget just before the final </t> or at end of arch."""
    arch = strip_old_widget(arch)
    # Inject before last </t>
    m = re.search(r'(</t>\s*)$', arch)
    if m:
        return arch[:m.start()] + "\n" + widget_block + "\n" + arch[m.start():]
    # Inject before closing </div> of wrap
    m2 = re.search(r'(</div>\s*)$', arch)
    if m2:
        return arch[:m2.start()] + "\n" + widget_block + "\n" + arch[m2.start():]
    return arch + "\n" + widget_block


def process_store(odoo: Odoo, store_key: str, store: dict, rows: list) -> dict:
    site_id = store.get("odoo_site_id")
    name    = store["name"]
    result  = {"store": name, "status": "PENDING", "note": ""}

    # Build widget HTML
    raw_widget = build_widget_html(store_key, store, rows, AI_PROXY_URL)
    widget_block = escape_for_arch(raw_widget)

    # Save locally
    folder   = STORE_FOLDERS[store_key]
    out_file = BASE / folder / "ai_widget.html"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(raw_widget, encoding="utf-8")

    if not site_id or not odoo.uid:
        result.update(status="FILE_ONLY", note="No site ID or auth — HTML saved")
        print(f"  [{name}] HTML saved (no site ID)")
        return result

    try:
        pages = odoo.search_read(
            "website.page",
            [["website_id","=",site_id],["url","=","/"]],
            ["id","view_id"]
        )
        if not pages:
            result.update(status="NO_PAGE", note="No homepage found")
            return result

        view_r  = pages[0].get("view_id")
        view_id = view_r[0] if isinstance(view_r, list) else view_r
        if not view_id:
            result.update(status="NO_VIEW", note="No view_id on homepage page")
            return result

        view_data = odoo.read("ir.ui.view", [view_id], ["arch_db"])
        if not view_data:
            result.update(status="NO_ARCH", note="View unreadable")
            return result

        arch     = view_data[0].get("arch_db") or ""
        new_arch = inject_widget_before_closing(arch, widget_block)

        odoo.write("ir.ui.view", [view_id], {"arch_db": new_arch})
        result.update(
            status="INJECTED",
            note=f"view {view_id} updated | https://{store['domain']}/"
        )
        print(f"  [{name}] AI widget injected into view {view_id}")

    except Exception as e:
        result.update(status="ERROR", note=str(e)[:300])
        print(f"  [{name}] Error: {e}")

    time.sleep(0.6)
    return result


def main():
    today = date.today()
    print(f"\n{'='*65}")
    print(f"  AI WIDGET INJECTOR — ALL 7 STORES")
    print(f"  Date: {today}")
    print(f"  Proxy: {AI_PROXY_URL}")
    print(f"{'='*65}\n")

    if "your-vps-domain" in AI_PROXY_URL:
        print("  WARNING: AI_PROXY_URL is still the placeholder.")
        print("  Update AI_PROXY_URL in build_ai_widget.py before injecting.")
        print("  Widgets will still be saved as HTML files.\n")

    rows    = build_all_days()
    odoo    = Odoo()
    results = []

    for store_key, store in STORES.items():
        print(f"\n  [{store['name']}] site_id={store.get('odoo_site_id')}")
        res = process_store(odoo, store_key, store, rows)
        results.append(res)

    print(f"\n{'='*65}")
    print(f"  SUMMARY")
    print(f"{'='*65}")
    icons = {"INJECTED":"[LIVE]","FILE_ONLY":"[FILE]","NO_PAGE":"[WARN]","ERROR":"[ERR]"}
    for r in results:
        print(f"  {icons.get(r['status'],'[?]')} {r['store']:35s}  {r['note']}")

    live = sum(1 for r in results if r["status"] == "INJECTED")
    print(f"\n  AI widget live: {live}/7")
    print(f"  HTML files saved: 7/7  (ScrappedMaterial/<store>/ai_widget.html)")
    print(f"{'='*65}")

    with open(BASE / "widget_injection_summary.json", "w") as f:
        json.dump({"date": str(today), "proxy": AI_PROXY_URL, "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
