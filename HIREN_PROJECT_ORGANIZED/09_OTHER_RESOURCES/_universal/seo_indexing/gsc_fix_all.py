import json, time, requests, re

session = requests.Session()
session.headers.update({"Content-Type": "application/json"})

# Authenticate
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

# Sites to fix: {website_id: (domain, correct_gsc_code)}
SITES = {
    37: ("https://www.ligiftbasket.com",           "QnNFugGoC1bdy5quUZyUUeviVYt5M2xP9xsZcYAjpjs"),
    38: ("https://www.longislandballoonsdecor.com", "1p0KC4ckpO6CwGbJ6a73LfLIW5bQHyo8B2FCsBa9h2E"),
}

# Read current state first
print("\n=== CURRENT STATE ===")
sites = rpc("website", "search_read",
    [[["id","in",[37,38]]]],
    {"fields":["id","name","domain","google_search_console","custom_code_head"]}
)
for s in sites:
    print(f"  id={s['id']} | {s['name']}")
    print(f"    google_search_console: {repr(s['google_search_console'])}")
    print(f"    custom_code_head     : {repr(s['custom_code_head'])}")

# Fix each site
print("\n=== APPLYING FIXES ===")
for site_id, (domain, code) in SITES.items():
    print(f"\n  Site {site_id} ({domain})")
    print(f"  Setting google_search_console = {code}")

    # Set the native Odoo GSC field AND clear custom_code_head to avoid conflicts
    rpc("website", "write", [[site_id], {
        "google_search_console": code,
        "custom_code_head": "",        # clear to prevent conflicts
    }])
    print(f"  Written.")

# Confirm in DB
print("\n=== CONFIRMING IN DATABASE ===")
sites2 = rpc("website", "search_read",
    [[["id","in",[37,38]]]],
    {"fields":["id","name","google_search_console","custom_code_head"]}
)
for s in sites2:
    gsc = s["google_search_console"]
    head = s["custom_code_head"]
    print(f"  id={s['id']} | {s['name']}")
    print(f"    google_search_console: {repr(gsc)}")
    print(f"    custom_code_head     : {repr(head)}")

# Wait for Odoo page cache to clear
print("\nWaiting 6s for Odoo cache to clear...")
time.sleep(6)

# Verify live
print("\n=== LIVE VERIFICATION ===")
for site_id, (domain, code) in SITES.items():
    try:
        r = requests.get(domain + "/", timeout=15,
            headers={"User-Agent":"Googlebot/2.1 (+http://www.google.com/bot.html)"})
        tag = re.findall(r'<meta[^>]+google-site-verification[^>]+>', r.text, re.I)
        match = code in r.text
        status = "LIVE" if match else "MISSING"
        print(f"  {domain}")
        print(f"    HTTP: {r.status_code} | Code match: {match} [{status}]")
        print(f"    Tag found: {tag}")
    except Exception as e:
        print(f"  {domain} ERROR: {e}")

print("\nDone. Now go to GSC > HTML tag method > click VERIFY for each site.")
