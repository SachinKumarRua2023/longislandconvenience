import json, time, requests, re

CORRECT_CODE = "QnNFugGoC1bdy5quUZyUUeviVYt5M2xP9xsZcYAjpjs"
CORRECT_META = '<meta name="google-site-verification" content="QnNFugGoC1bdy5quUZyUUeviVYt5M2xP9xsZcYAjpjs" />'

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

# Update with correct code
print("Updating google_search_console field ->", CORRECT_CODE)
rpc("website", "write", [[37], {"google_search_console": CORRECT_CODE}])

print("Updating custom_code_head ->", CORRECT_META)
rpc("website", "write", [[37], {"custom_code_head": CORRECT_META}])

print("Waiting 5s for Odoo cache to clear...")
time.sleep(5)

# Confirm live
r = requests.get("https://www.ligiftbasket.com/", timeout=15,
    headers={"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"})

if CORRECT_CODE in r.text:
    print()
    print("=" * 55)
    print("  SUCCESS — Correct meta tag is LIVE on the site!")
    print("  Go to GSC and click VERIFY now.")
    print("=" * 55)
    tag = re.findall(r'<meta[^>]+google-site-verification[^>]+>', r.text, re.I)
    print("  Live tag:", tag)
else:
    print("Not visible yet. Current GSC tags on page:")
    old = re.findall(r'<meta[^>]+google-site-verification[^>]+>', r.text, re.I)
    print(old)
