#!/usr/bin/env python3
"""
Install and configure Razorpay payment provider for Long Island Cards.
Razorpay credentials from CountryCove_Project/.env:
  KEY_ID  = rzp_live_SYr3kjBJsAOMnw
  SECRET  = 5HAWnH0Nafjj2xppnyXn5bTy
"""
import xmlrpc.client, sys, time
sys.stdout.reconfigure(encoding='utf-8')

URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"

RZP_KEY_ID     = "rzp_live_SYr3kjBJsAOMnw"
RZP_KEY_SECRET = "5HAWnH0Nafjj2xppnyXn5bTy"
RZP_WEBHOOK    = "33085b5d853cef9c655c992766d8e865aad6879103699917"

uid = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common').authenticate(DB, USER, PASS, {})
m   = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')

def xc(model, method, args, kwargs={}):
    return m.execute_kw(DB, uid, PASS, model, method, args, kwargs)

print(f"Connected UID {uid}\n")

# ── Step 1: Install payment_razorpay module ───────────────────
print("[1] Installing payment_razorpay module...")
mod = xc('ir.module.module', 'search_read',
    [[('name','=','payment_razorpay')]],
    {'fields':['id','name','state'],'limit':1})

if mod:
    mod_id = mod[0]['id']
    mod_state = mod[0]['state']
    print(f"    Module ID {mod_id}, current state: {mod_state}")
    if mod_state == 'installed':
        print("    Already installed — skipping install step.")
    else:
        xc('ir.module.module', 'button_immediate_install', [[mod_id]])
        print("    Install triggered. Waiting 15s for server to process...")
        time.sleep(15)
        # Re-check
        mod2 = xc('ir.module.module', 'read', [[mod_id]], {'fields':['state']})[0]
        print(f"    State after install: {mod2['state']}")
else:
    print("    Module 'payment_razorpay' not found in module list.")
    sys.exit(1)

# ── Step 2: Read Razorpay provider record and its fields ──────
print("\n[2] Reading Razorpay provider record (ID 16)...")
rzp = xc('payment.provider', 'read', [[16]], {})[0]
print(f"    Name: {rzp['name']}, State: {rzp['state']}, Code: {rzp['code']}")
print(f"    Module state: {rzp.get('module_state','?')}")

# Find available credential fields
all_fields = xc('payment.provider', 'fields_get', [], {'attributes': ['string','type']})
cred_fields = {k: v for k, v in all_fields.items()
               if any(x in k.lower() for x in ['razorpay','key_id','key_secret','webhook'])}
print(f"    Credential fields found: {list(cred_fields.keys())}")

# ── Step 3: Enable + configure Razorpay ──────────────────────
print("\n[3] Configuring Razorpay...")
vals = {'state': 'enabled'}

if 'razorpay_key_id' in all_fields:
    vals['razorpay_key_id'] = RZP_KEY_ID
if 'razorpay_key_secret' in all_fields:
    vals['razorpay_key_secret'] = RZP_KEY_SECRET
if 'razorpay_webhook_secret' in all_fields:
    vals['razorpay_webhook_secret'] = RZP_WEBHOOK

result = xc('payment.provider', 'write', [[16], vals])
print(f"    Write result: {result}")

# Verify
rzp2 = xc('payment.provider', 'read', [[16]], {'fields': list(vals.keys()) + ['code','name']})
print(f"    Verification: {rzp2[0]}")

# ── Step 4: Also enable Wire Transfer as backup ───────────────
print("\n[4] Enabling Wire Transfer (ID 21) as backup payment...")
# Create a journal for Wire Transfer if needed
journals = xc('account.journal', 'search_read',
    [[('type','=','bank')]],
    {'fields':['id','name'],'limit':1})
if journals:
    j_id = journals[0]['id']
    xc('payment.provider', 'write', [[21], {
        'state': 'enabled',
        'journal_id': j_id,
    }])
    print(f"    Wire Transfer enabled with journal {journals[0]['name']}")
else:
    print("    No bank journal found — Wire Transfer left as-is")

# ── Step 5: Check Cash on Delivery status ────────────────────
print("\n[5] Verifying Cash on Delivery (ID 24)...")
cod = xc('payment.provider', 'read', [[24]], {'fields':['name','state','journal_id']})[0]
print(f"    {cod['name']}: {cod['state']}, Journal: {cod.get('journal_id','none')}")

print("\nDone! Payment gateway setup complete.")
print("Visit: Website > Configuration > Payment Providers to verify in Odoo backend.")
