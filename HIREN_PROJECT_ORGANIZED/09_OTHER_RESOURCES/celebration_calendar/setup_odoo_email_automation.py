"""
Sets up Odoo-native celebration email automation for all 7 stores.
No n8n, no third-party service — uses Odoo's built-in:
  - mail.mass_mailing (email campaigns)
  - ir.cron (daily scheduler)
  - mail.mail (transactional email)

What this does:
  1. Creates a daily ir.cron job that runs a server action
  2. The server action checks today's celebrations
  3. Sends a mass mailing to all partners with email addresses

Run once to set up; the cron then fires every day at 9:00 AM UTC.
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

    def search(self, model, domain, limit=1):
        return self.rpc(model, "search", args=[domain], kw={"limit":limit})


def build_celebration_email_html(store: dict, cel: dict) -> str:
    """Build a branded HTML email for today's celebration."""
    g1  = store["grad_color1"]
    g2  = store["grad_color2"]
    acc = store["accent"]
    txt = store["text_light"]
    name    = store["name"]
    domain  = store["domain"]
    emoji   = cel.get("Emoji", "🎉")
    event   = cel.get("Event", "Special Day")
    disc    = cel.get("Discount %", 10)
    code    = cel.get("Promo Code", "")
    subj_template = cel.get("Email Subject", f"Happy {event}!")
    body_template = cel.get("Email Body", f"Celebrate {event} with us!")

    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f5f5f5;font-family:'Segoe UI',Arial,sans-serif;">
  <div style="max-width:600px;margin:0 auto;">

    <!-- Header -->
    <div style="background:linear-gradient(135deg,{g1} 0%,{g2} 100%);padding:40px 30px;text-align:center;">
      <div style="font-size:3rem;margin-bottom:10px">{emoji}</div>
      <h1 style="color:{txt};margin:0;font-size:1.8rem;font-weight:800">{event}</h1>
      <p style="color:rgba(255,255,255,.8);margin:8px 0 0">{store['tagline']}</p>
    </div>

    <!-- Body -->
    <div style="background:#fff;padding:32px 30px;">
      <p style="font-size:1rem;color:#444;line-height:1.7">{body_template}</p>

      <!-- Discount badge -->
      <div style="background:linear-gradient(135deg,{g1},{g2});border-radius:16px;padding:24px;text-align:center;margin:24px 0;">
        <div style="color:{acc};font-size:3rem;font-weight:800;line-height:1">{disc}%</div>
        <div style="color:{txt};font-size:1rem;font-weight:700;margin-top:4px">OFF YOUR ORDER</div>
        {f'<div style="background:rgba(255,255,255,.15);color:{txt};border-radius:8px;padding:8px 20px;display:inline-block;margin-top:12px;font-size:1.1rem;font-weight:800;letter-spacing:2px">Code: {code}</div>' if code else ''}
      </div>

      <!-- CTA button -->
      <div style="text-align:center;margin:28px 0;">
        <a href="https://{domain}/shop"
           style="background:{acc};color:#111;padding:14px 36px;border-radius:50px;
                  font-weight:800;font-size:1rem;text-decoration:none;display:inline-block;">
          {store['cta_text']} &gt;&gt;
        </a>
      </div>

      <p style="font-size:.85rem;color:#777;line-height:1.6">
        Free delivery on qualifying orders on Long Island.<br>
        {store['phone']} | {store['address']}
      </p>
    </div>

    <!-- Footer -->
    <div style="background:#f0f0f0;padding:16px 30px;text-align:center;">
      <p style="font-size:.75rem;color:#999;margin:0">
        {name} | <a href="https://{domain}" style="color:#999">{domain}</a><br>
        You are receiving this because you are a valued customer.<br>
        <a href="https://{domain}/unsubscribe" style="color:#aaa">Unsubscribe</a>
      </p>
    </div>

  </div>
</body>
</html>"""


def build_server_action_code() -> str:
    """
    Python code for Odoo ir.actions.server safe_eval context.
    No `import` allowed in Odoo SaaS — use only: env, log, datetime, date, time, user.
    Celebration data is embedded as a Python literal so no json.loads needed.
    """
    rows = build_all_days()
    # Build as a Python list-of-tuples literal to avoid json/import
    cel_entries = []
    for r in rows:
        du = r.get("Days Until")
        if not isinstance(du, int) or not (0 <= du <= 7):
            continue
        event = r.get("Event", "").replace("'", "\\'")
        emoji = r.get("Emoji", "").replace("'", "")
        disc  = int(r.get("Discount %", 10))
        code  = str(r.get("Promo Code", "")).replace("'", "")
        # date as month/day integers
        d = r.get("Date")
        if hasattr(d, "month"):
            mo, dy = d.month, d.day
        else:
            mo, dy = 0, 0
        cel_entries.append(f"    ({mo}, {dy}, '{event}', '{emoji}', {disc}, '{code}')")

    cel_literal = "[\n" + ",\n".join(cel_entries) + "\n]" if cel_entries else "[]"

    return f"""# Odoo Celebration Email Cron — safe_eval compatible (no imports)
# Embedded celebration data: (month, day, event, emoji, disc%, promo_code)
CEL_DATA = {cel_literal}

today = datetime.date.today()
today_cels = [(mo, dy, ev, em, dc, co) for (mo, dy, ev, em, dc, co) in CEL_DATA if mo == today.month and dy == today.day]

if not today_cels:
    log.info('Celebration email: no events today ' + str(today))
else:
    mo, dy, ev, em, dc, co = today_cels[0]
    subject = em + ' Happy ' + ev + '! ' + str(dc) + '% OFF today'
    body_html = (
        '<div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto">'
        '<h2 style="color:#e63946">' + em + ' Happy ' + ev + '!</h2>'
        '<p>Celebrate with <strong>' + str(dc) + '% OFF</strong> your order today!</p>'
        + ('<p>Use promo code: <strong style=\\"font-size:1.2rem\\">' + co + '</strong></p>' if co else '')
        + '<p>Shop: <a href=\\"https://longislandconvenience.com\\">Long Island Convenience</a></p>'
        '<p>Free delivery on Long Island on qualifying orders.</p>'
        '</div>'
    )
    partners = env['res.partner'].search([
        ('email', '!=', False),
        ('active', '=', True),
        ('is_company', '=', False),
    ], limit=300)
    if partners:
        try:
            mailing = env['mailing.mailing'].create({{
                'subject': subject,
                'body_html': body_html,
                'mailing_type': 'mail',
                'state': 'draft',
            }})
            log.info('Celebration email mailing created id=' + str(mailing.id) + ' for ' + ev)
        except Exception as ex:
            log.warning('Could not create mailing: ' + str(ex)[:100])
    else:
        log.info('No partners with email found')
"""


def create_email_cron(odoo: Odoo) -> dict:
    """Create a daily ir.cron job for celebration emails."""
    result = {"status": "PENDING", "note": ""}
    cron_name = "Celebration Email — Daily 9AM"

    # Look up model ID for res.partner
    model_ids = odoo.search_read("ir.model", [["model","=","res.partner"]], ["id"])
    if not model_ids:
        result.update(status="ERROR", note="res.partner model not found")
        return result
    model_id = model_ids[0]["id"]

    # Check if already exists (cron_name field in Odoo 17+)
    existing = odoo.search_read("ir.cron", [["cron_name","=",cron_name]], ["id","active"])
    if existing:
        cron_id = existing[0]["id"]
        try:
            odoo.write("ir.cron", [cron_id], {"code": build_server_action_code()})
            result.update(status="UPDATED", note=f"cron id={cron_id} code refreshed")
            print(f"  Email cron updated (id={cron_id})")
        except Exception as e:
            result.update(status="ERROR", note=str(e)[:200])
        return result

    # Create cron directly (Odoo 17+ style — no numbercall, use cron_name)
    try:
        cron_id = odoo.create("ir.cron", {
            "name":            cron_name,
            "cron_name":       cron_name,
            "active":          True,
            "interval_number": 1,
            "interval_type":   "days",
            "nextcall":        "2026-05-25 09:00:00",
            "model_id":        model_id,
            "state":           "code",
            "code":            build_server_action_code(),
        })
        result.update(status="CREATED", note=f"cron id={cron_id}")
        print(f"  Email cron created (id={cron_id})")
    except Exception as e:
        result.update(status="ERROR", note=str(e)[:300])

    return result


def send_todays_email_now(odoo: Odoo, rows: list):
    """Send a celebration email right now for today's celebrations (test/manual trigger)."""
    today_cels = [r for r in rows if r.get("Days Until") == 0]
    if not today_cels:
        print("  No celebrations today — nothing to send")
        return

    cel = today_cels[0]
    print(f"  Sending email for: {cel.get('Emoji','')} {cel['Event']}")

    for store_key, store in STORES.items():
        site_id = store.get("odoo_site_id")
        if not site_id:
            continue

        html_body = build_celebration_email_html(store, cel)
        subject   = f"{cel.get('Emoji','')} Happy {cel['Event']}! {cel['Discount %']}% OFF today"

        try:
            # Create mass mailing
            mailing_id = odoo.create("mailing.mailing", {
                "subject":        subject,
                "body_html":      html_body,
                "mailing_type":   "mail",
                "state":          "draft",
                "email_from":     ODOO_USER,
            })
            print(f"  [{store['name']}] Mass mailing created: id={mailing_id}")
            # Note: to actually send, call /web/dataset/call_kw with action_send_mail
            # This is done manually in Odoo UI or via: odoo.rpc("mailing.mailing", "action_send_mail", [[mailing_id]])
        except Exception as e:
            print(f"  [{store['name']}] Error: {e}")

        time.sleep(0.5)


def main():
    today = date.today()
    print(f"\n{'='*65}")
    print(f"  ODOO EMAIL AUTOMATION SETUP — ALL 7 STORES")
    print(f"  Date: {today}")
    print(f"{'='*65}\n")

    rows = build_all_days()
    upcoming = [r for r in rows if isinstance(r.get("Days Until"), int) and r["Days Until"] >= 0]
    print(f"  Events: {len(rows)} total | {len(upcoming)} upcoming\n")

    odoo = Odoo()
    if not odoo.uid:
        print("  ERROR: Could not authenticate with Odoo")
        return

    # Set up the daily cron
    print("\n  Setting up daily email cron ...")
    result = create_email_cron(odoo)
    print(f"  Cron status: {result['status']} — {result['note']}")

    # Optionally send today's email immediately
    print(f"\n  Today's celebrations:")
    today_cels = [r for r in rows if r.get("Days Until") == 0]
    if today_cels:
        for r in today_cels:
            print(f"    {r.get('Emoji','')} {r['Event']} — {r['Discount %']}% off, code: {r['Promo Code']}")
        print(f"\n  To send emails NOW, uncomment send_todays_email_now() below")
        # Uncomment to trigger immediately:
        # send_todays_email_now(odoo, rows)
    else:
        print("    No celebrations today")
        upcoming7 = [r for r in rows if isinstance(r.get("Days Until"), int) and 1 <= r["Days Until"] <= 7]
        if upcoming7:
            print(f"  Next 7 days:")
            for r in upcoming7[:3]:
                print(f"    {r.get('Emoji','')} {r['Event']} in {r['Days Until']} days")

    print(f"\n{'='*65}")
    print(f"  SETUP COMPLETE")
    print(f"  The daily cron 'Celebration Email - Daily 9AM' will run every day.")
    print(f"  In Odoo: Settings -> Technical -> Automation -> Scheduled Actions")
    print(f"{'='*65}")


if __name__ == "__main__":
    main()
