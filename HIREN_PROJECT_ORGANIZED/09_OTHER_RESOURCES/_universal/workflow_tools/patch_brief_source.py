#!/usr/bin/env python3
"""Fix n9 to read clientBrief from n1 (Parse Input) directly, not from n7."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

WORKFLOW = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\BasicWorkflow\ai-cloner-odoo.json"

with open(WORKFLOW, 'r', encoding='utf-8') as f:
    wf = json.load(f)

n9 = next(n for n in wf['nodes'] if n.get('name','').startswith('Code: Build Cards HTML Prompt'))
js = n9['parameters']['jsCode']

OLD = "const brief = prev.clientBrief || {};"
NEW = "const brief = ($('Parse Input').item?.json?.clientBrief) || prev.clientBrief || {};"

count = js.count(OLD)
print(f"OLD found {count} time(s)")

if count != 1:
    print("ERROR: not found exactly once")
    sys.exit(1)

js_new = js.replace(OLD, NEW, 1)
print("Replacement done")
print("Verify:", repr(js_new[js_new.find('const brief'):js_new.find('const brief')+100]))

n9['parameters']['jsCode'] = js_new

with open(WORKFLOW, 'w', encoding='utf-8') as f:
    json.dump(wf, f, ensure_ascii=False, indent=2)

print("✓ Saved — n9 now reads clientBrief from Parse Input node")
