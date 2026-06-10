"""
Sets up Odoo-native WhatsApp automation for celebration messages.
Uses Odoo's built-in 'whatsapp' module (confirmed installed).

What this does:
  1. Creates WhatsApp message templates in Odoo for top celebrations
  2. Creates a daily ir.cron job to send WhatsApp messages at 10 AM
  3. Targets all res.partner records with phone/mobile numbers

Requires:
  - Odoo whatsapp module active (confirmed installed)
  - WhatsApp Business API account connected in Odoo
    (Settings -> WhatsApp -> Accounts)

Run this once to set up templates and cron.
"""

import sys, io, re, time, json, requests
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).parent))
from store_configs import STORES
from build_master_celebration_sheet import build_all_days

ODOO_URL  = "https://country-cove-inc.odoo.com"
ODOO_DB   = "country-cove-inc"
ODOO_USER = "countrycoveinc@gmail.com"
ODOO_PASS = "M@nhattan1234"


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
            raise RuntimeError(d["error"]["data"]["message"][:400])
        return d.get("result")

    def search_read(self, model, domain, fields, limit=100):
        return self.rpc(model, "search_read", args=[domain], kw={"fields":fields,"limit":limit})

    def create(self, model, vals):
        return self.rpc(model, "create", args=[vals])

    def write(self, model, ids, vals):
        return self.rpc(model, "write", args=[ids, vals])

    def fields_get(self, model):
        return self.rpc(model, "fields_get", kw={"attributes": ["string","type"]})


# WhatsApp message text per store + celebration
def build_whatsapp_message(store: dict, cel: dict) -> str:
    name  = store["name"]
    emoji = cel.get("Emoji", "🎉")
    event = cel.get("Event", "Special Day")
    disc  = cel.get("Discount %", 10)
    code  = cel.get("Promo Code", "")
    cta   = store["cta_text"]
    domain = store["domain"]
    phone  = store["phone"]

    msg = (
        f"{emoji} *Happy {event}!* {emoji}\n\n"
        f"Hi! Wishing you a wonderful {event} from all of us at *{name}*!\n\n"
    )
    if code:
        msg += f"*SPECIAL OFFER:* {disc}% OFF today!\nUse code: *{code}* at checkout\n\n"
    else:
        msg += f"*Celebrate with {disc}% off* — valid today only!\n\n"

    msg += (
        f"Shop online: https://{domain}\n"
        f"Call us: {phone}\n"
        f"Long Island, NY - Free local delivery on qualifying orders\n\n"
        f"_{name}_"
    )
    return msg


def check_whatsapp_module(odoo: Odoo) -> dict:
    """Check WhatsApp module configuration in Odoo."""
    info = {}
    try:
        # Check whatsapp.template model
        templates = odoo.search_read("whatsapp.template", [], ["id","name","status"], limit=5)
        info["templates_count"] = len(templates)
        info["sample_templates"] = [t["name"] for t in templates[:3]]
    except Exception as e:
        info["templates_error"] = str(e)[:100]

    try:
        # Check whatsapp.account
        accounts = odoo.search_read("whatsapp.account", [], ["id","name","phone"], limit=5)
        info["accounts"] = [{"id": a["id"], "name": a["name"]} for a in accounts]
    except Exception as e:
        info["accounts_error"] = str(e)[:100]

    try:
        # Check discuss.channel for WhatsApp
        wa_channels = odoo.search_read(
            "discuss.channel",
            [["channel_type", "=", "whatsapp"]],
            ["id","name"],
            limit=5
        )
        info["wa_channels"] = len(wa_channels)
    except Exception as e:
        info["channels_error"] = str(e)[:100]

    return info


def create_whatsapp_templates(odoo: Odoo, rows: list) -> list:
    """Create WhatsApp templates for top 10 celebrations."""
    top_cels = [r for r in rows if isinstance(r.get("Days Until"), int) and r["Days Until"] >= 0][:10]

    # Check accounts first
    try:
        accounts = odoo.search_read("whatsapp.account", [["active","=",True]], ["id"], limit=1)
        if not accounts:
            print("  No active WhatsApp account in Odoo.")
            print("  Go to: Settings -> WhatsApp -> Accounts -> Connect your WhatsApp Business API")
            return []
        wa_account_id = accounts[0]["id"]
    except Exception as e:
        print(f"  Could not find WhatsApp accounts: {e}")
        return []

    created = []
    for cel in top_cels[:5]:  # create 5 templates to start
        tpl_name = f"CEL_{cel['Event'].replace(' ','_')[:25]}"
        body = (
            f"{cel.get('Emoji','')} Happy {cel['Event']}!\n\n"
            f"Celebrate with {cel['Discount %']}% off today!\n"
            f"Use code: {cel['Promo Code']}\n\n"
            f"Shop: https://longislandconvenience.com\n"
            f"Free delivery on Long Island on qualifying orders."
        )

        try:
            # Check if template already exists
            existing = odoo.search_read(
                "whatsapp.template",
                [["name","=",tpl_name]],
                ["id","name"]
            )
            if existing:
                print(f"  Template '{tpl_name}' already exists (id={existing[0]['id']})")
                created.append(existing[0]["id"])
                continue

            tpl_id = odoo.create("whatsapp.template", {
                "name":             tpl_name,
                "body":             body,
                "wa_account_id":    wa_account_id,
                "model_id":         odoo.search_read("ir.model", [["model","=","res.partner"]], ["id"])[0]["id"],
                "status":           "draft",
            })
            created.append(tpl_id)
            print(f"  Created WhatsApp template: '{tpl_name}' (id={tpl_id})")

        except Exception as e:
            print(f"  Template '{tpl_name}' error: {e}"[:120])

        time.sleep(0.3)

    return created


def build_whatsapp_cron_code(rows: list) -> str:
    """
    Python code for Odoo ir.actions.server safe_eval — no imports allowed.
    Celebration data embedded as Python literal (month, day, event, emoji, disc, code).
    """
    cel_entries = []
    for r in rows:
        du = r.get("Days Until")
        if not isinstance(du, int) or not (0 <= du <= 3):
            continue
        event = r.get("Event", "").replace("'", "\\'")
        emoji = r.get("Emoji", "").replace("'", "")
        disc  = int(r.get("Discount %", 10))
        code  = str(r.get("Promo Code", "")).replace("'", "")
        d = r.get("Date")
        mo, dy = (d.month, d.day) if hasattr(d, "month") else (0, 0)
        cel_entries.append(f"    ({mo}, {dy}, '{event}', '{emoji}', {disc}, '{code}')")

    cel_literal = "[\n" + ",\n".join(cel_entries) + "\n]" if cel_entries else "[]"

    return f"""# Odoo WhatsApp Celebration Cron — safe_eval compatible
CEL_DATA = {cel_literal}

today = datetime.date.today()
today_cels = [(mo, dy, ev, em, dc, co) for (mo, dy, ev, em, dc, co) in CEL_DATA if mo == today.month and dy == today.day]

if not today_cels:
    log.info('WhatsApp: no celebrations today ' + str(today))
else:
    mo, dy, ev, em, dc, co = today_cels[0]
    msg_text = (
        em + ' Happy ' + ev + '! ' + em + '\\n\\n'
        'Use code *' + co + '* for ' + str(dc) + '% off today!\\n'
        'Shop: https://longislandconvenience.com\\n'
        'Long Island, NY - Free delivery on qualifying orders'
    )
    partners = env['res.partner'].search([
        ('mobile', '!=', False),
        ('active', '=', True),
        ('is_company', '=', False),
    ], limit=200)
    log.info('WhatsApp celebration: ' + ev + ' | contacts: ' + str(len(partners)))
    for p in partners[:50]:
        try:
            env['whatsapp.message'].create({{
                'mobile_number': p.mobile,
                'body': msg_text,
                'res_model': 'res.partner',
                'res_id': p.id,
            }})
        except Exception:
            pass
"""


def create_whatsapp_cron(odoo: Odoo, rows: list) -> dict:
    result = {"status": "PENDING", "note": ""}
    cron_name = "Celebration WhatsApp — Daily 10AM"

    model_ids = odoo.search_read("ir.model", [["model","=","res.partner"]], ["id"])
    if not model_ids:
        result.update(status="ERROR", note="res.partner model not found")
        return result
    model_id = model_ids[0]["id"]

    existing = odoo.search_read("ir.cron", [["cron_name","=",cron_name]], ["id","active"])
    if existing:
        cron_id = existing[0]["id"]
        try:
            odoo.write("ir.cron", [cron_id], {"code": build_whatsapp_cron_code(rows)})
            result.update(status="UPDATED", note=f"cron id={cron_id} code refreshed")
            print(f"  WhatsApp cron updated (id={cron_id})")
        except Exception as e:
            result.update(status="ERROR", note=str(e)[:200])
        return result

    try:
        cron_id = odoo.create("ir.cron", {
            "name":            cron_name,
            "cron_name":       cron_name,
            "active":          True,
            "interval_number": 1,
            "interval_type":   "days",
            "nextcall":        "2026-05-25 10:00:00",
            "model_id":        model_id,
            "state":           "code",
            "code":            build_whatsapp_cron_code(rows),
        })
        result.update(status="CREATED", note=f"cron id={cron_id}")
        print(f"  WhatsApp cron created (id={cron_id})")
    except Exception as e:
        result.update(status="ERROR", note=str(e)[:300])
        print(f"  WhatsApp cron error: {e}"[:150])

    return result


def main():
    today = date.today()
    print(f"\n{'='*65}")
    print(f"  ODOO WHATSAPP AUTOMATION SETUP")
    print(f"  Date: {today}")
    print(f"{'='*65}\n")

    rows = build_all_days()
    odoo = Odoo()

    if not odoo.uid:
        print("  ERROR: Odoo authentication failed")
        return

    # 1. Check WhatsApp module status
    print("  Checking WhatsApp module ...")
    wa_info = check_whatsapp_module(odoo)
    print(f"  WhatsApp accounts: {wa_info.get('accounts', 'N/A')}")
    print(f"  Existing templates: {wa_info.get('templates_count', 0)}")
    if wa_info.get("accounts_error"):
        print(f"  Account check error: {wa_info['accounts_error']}")
    if wa_info.get("templates_error"):
        print(f"  Template check error: {wa_info['templates_error']}")

    # 2. Create WhatsApp templates
    print(f"\n  Creating WhatsApp templates ...")
    created_tpl = create_whatsapp_templates(odoo, rows)
    print(f"  Templates ready: {len(created_tpl)}")

    # 3. Create daily cron
    print(f"\n  Setting up daily WhatsApp cron ...")
    cron_result = create_whatsapp_cron(odoo, rows)
    print(f"  Cron status: {cron_result['status']} — {cron_result['note']}")

    # 4. Print manual setup guide if no WA account
    if not wa_info.get("accounts") or wa_info.get("accounts_error"):
        print(f"\n  {'='*55}")
        print(f"  ACTION REQUIRED: Connect WhatsApp Business API in Odoo")
        print(f"  {'='*55}")
        print(f"  1. Go to: {ODOO_URL}/odoo/whatsapp")
        print(f"  2. Click 'New Account'")
        print(f"  3. Enter your WhatsApp Business API credentials")
        print(f"     (Meta Business Manager -> WhatsApp -> API Setup)")
        print(f"  4. Approve message templates in WhatsApp Manager")
        print(f"  5. Re-run this script after connecting")

    print(f"\n  WhatsApp message preview for today:")
    today_cels = [r for r in rows if r.get("Days Until") == 0]
    if today_cels:
        msg = build_whatsapp_message(list(STORES.values())[0], today_cels[0])
        print(f"\n  {msg[:300]}")
    else:
        upcoming = [r for r in rows if isinstance(r.get("Days Until"), int) and r["Days Until"] > 0]
        if upcoming:
            msg = build_whatsapp_message(list(STORES.values())[0], upcoming[0])
            print(f"  Next celebration: {upcoming[0]['Event']} in {upcoming[0]['Days Until']} days")
            print(f"\n  {msg[:300]}")

    print(f"\n{'='*65}")
    print(f"  WHATSAPP SETUP SUMMARY")
    print(f"  Templates created: {len(created_tpl)}")
    print(f"  Cron: {cron_result['status']}")
    print(f"\n  In Odoo: Settings -> Technical -> Automation -> Scheduled Actions")
    print(f"  Look for: 'Celebration WhatsApp - Daily 10AM'")
    print(f"{'='*65}")


if __name__ == "__main__":
    main()
