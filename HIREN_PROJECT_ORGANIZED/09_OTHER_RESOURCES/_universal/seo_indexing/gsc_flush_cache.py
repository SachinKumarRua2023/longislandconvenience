import json, time, requests, re

session = requests.Session()
session.headers.update({"Content-Type": "application/json"})

auth = session.post(
    "https://country-cove-inc.odoo.com/web/session/authenticate",
    data=json.dumps({"jsonrpc":"2.0","method":"call","params":{
        "db":"country-cove-inc","login":"countrycoveinc@gmail.com","password":"M@nhattan1234"
    }}), timeout=20
).json()
print("Auth uid:", auth["result"]["uid"])

def rpc(model, method, args, kwargs=None):
    r = session.post("https://country-cove-inc.odoo.com/web/dataset/call_kw",
        data=json.dumps({"jsonrpc":"2.0","method":"call","id":1,"params":{
            "model":model,"method":method,"args":args,"kwargs":kwargs or {}
        }}), timeout=30)
    d = r.json()
    if d.get("error"):
        raise RuntimeError(d["error"]["data"]["message"])
    return d["result"]

SITES = {
    37: ("https://www.ligiftbasket.com",           "QnNFugGoC1bdy5quUZyUUeviVYt5M2xP9xsZcYAjpjs"),
    38: ("https://www.longislandballoonsdecor.com", "1p0KC4ckpO6CwGbJ6a73LfLIW5bQHyo8B2FCsBa9h2E"),
}

# Step 1: Clear caches via available methods
print("\nStep 1 — Clearing Odoo caches...")
for model, method in [
    ("ir.http",  "clear_caches"),
    ("website",  "clear_caches"),
    ("ir.rule",  "clear_caches"),
]:
    try:
        rpc(model, method, [])
        print(f"  {model}.{method}() — Done.")
    except Exception as e:
        print(f"  {model}.{method}() — Note: {e}")

# Step 2: Search for and delete cached attachments with the old GSC code
OLD_CODE = "google7eab7c6a696479f4"
print(f"\nStep 2 — Removing cached attachments containing old code '{OLD_CODE}'...")
old_attachments = rpc("ir.attachment", "search_read",
    [["|",
      ["name", "ilike", OLD_CODE],
      ["url",  "ilike", OLD_CODE],
    ]],
    {"fields": ["id","name","url","type"]}
)
print(f"  Found {len(old_attachments)} attachment(s):")
for a in old_attachments:
    print(f"    id={a['id']} | name={a['name']} | url={a.get('url','')}")
if old_attachments:
    ids = [a["id"] for a in old_attachments]
    rpc("ir.attachment", "unlink", [ids])
    print(f"  Deleted {len(ids)} attachment(s).")

# Step 3: Touch both website records to force cache bust (flip a char and flip back)
print("\nStep 3 — Touching website records to bust page cache...")
for site_id, (domain, code) in SITES.items():
    # Read current name
    site = rpc("website","search_read",[[["id","=",site_id]]],{"fields":["name","google_search_console"]})[0]
    current_name = site["name"]
    print(f"  Site {site_id}: {current_name} | gsc={site['google_search_console']}")
    # Touch: write then write back (forces ORM to update write_date → cache bust)
    rpc("website","write",[[site_id],{"name": current_name + " "}])
    time.sleep(0.5)
    rpc("website","write",[[site_id],{"name": current_name}])
    print(f"  Touched.")

# Step 4: Call website._invalidate_routing() equivalent
print("\nStep 4 — Calling ir.http cache clear...")
try:
    rpc("ir.http", "clear_caches", [])
    print("  Done.")
except Exception as e:
    print(f"  Note: {e}")

# Step 5: Wait and verify
print("\nStep 5 — Waiting 8s then checking live pages...")
time.sleep(8)

for site_id, (domain, code) in SITES.items():
    r = requests.get(domain + "/", timeout=15,
        headers={"User-Agent":"Googlebot/2.1 (+http://www.google.com/bot.html)",
                 "Cache-Control":"no-cache, no-store"})
    tags = re.findall(r'<meta[^>]+google-site-verification[^>]+>', r.text, re.I)
    match = code in r.text
    print(f"\n  {domain}")
    print(f"  HTTP: {r.status_code} | Correct code live: {match}")
    print(f"  Tags: {tags}")
    if match:
        print(f"  >>> READY — Go to GSC HTML tag tab and click VERIFY <<<")
    else:
        # Show what's in the page for debugging
        all_gsc = re.findall(r'google[A-Za-z0-9_-]{15,}', r.text)
        print(f"  Codes found in page: {list(set(all_gsc))[:5]}")
