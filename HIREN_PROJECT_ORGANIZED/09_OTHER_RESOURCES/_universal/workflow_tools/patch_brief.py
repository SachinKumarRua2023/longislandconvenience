#!/usr/bin/env python3
"""Inject CLIENT BRIEF section into n9 htmlPrompt string in ai-cloner-odoo.json."""
import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

WORKFLOW = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\BasicWorkflow\ai-cloner-odoo.json"

with open(WORKFLOW, 'r', encoding='utf-8') as f:
    wf = json.load(f)

# Find node n9
n9 = next((n for n in wf['nodes'] if n.get('id') == 'n9' or n.get('name','').startswith('Code: Build Cards HTML Prompt')), None)
if not n9:
    # Try by name substring
    n9 = next((n for n in wf['nodes'] if 'HTML Prompt' in n.get('name', '') or 'Build Cards' in n.get('name', '')), None)

if not n9:
    print("ERROR: Could not find n9 node")
    print("Nodes:", [n.get('name','?') for n in wf['nodes']])
    sys.exit(1)

print(f"Found node: {n9.get('name')} (id={n9.get('id')})")

js = n9['parameters']['jsCode']
print(f"jsCode length: {len(js)}")

# Show context around the BRAND section to confirm the exact string
brand_pos = js.find('══ BRAND ══')
if brand_pos == -1:
    print("ERROR: '══ BRAND ══' not found in jsCode!")
    # Show first 200 chars of jsCode for debugging
    print("First 500 chars:", repr(js[:500]))
    sys.exit(1)

print(f"\n'══ BRAND ══' found at position {brand_pos}")
print("Context (40 chars before):", repr(js[brand_pos-40:brand_pos+60]))

# The target string: two newlines + the brand line start
# Check what's actually before '══ BRAND ══'
snippet = js[brand_pos-60:brand_pos+80]
print("\nFull snippet around BRAND:", repr(snippet))

# Build the OLD string by finding exactly what precedes '══ BRAND ══'
# We need: (some chars)  '══ BRAND ══\n' +
# Find the actual character before it on the same JS-string-concatenation line
idx = brand_pos
# Walk back to find the quote before ══
while idx > 0 and js[idx] != "'":
    idx -= 1
# idx is now at the opening quote of '══ BRAND ══\n'
before_quote = js[max(0, idx-10):idx]
print(f"\nChars before opening quote: {repr(before_quote)}")

# The OLD target is the newlines + single-quote + ══ BRAND ══\n' +
# We'll be precise: find the exact 2-newline prefix
two_nl_pos = js.rfind('\n\n', 0, brand_pos)
print(f"\nLast \\n\\n before BRAND at pos: {two_nl_pos}")
print("Chars from \\n\\n to BRAND+20:", repr(js[two_nl_pos:brand_pos+20]))

OLD = js[two_nl_pos:brand_pos - (brand_pos - idx)]  # from \n\n to opening quote

# More reliable: just use the 2 newlines + everything up to and including '══ BRAND ══\\n' +
# Find the full line: from \n\n to the + at end
line_end = js.find('\n', brand_pos)
OLD = js[two_nl_pos:line_end]
print(f"\nOLD string: {repr(OLD)}")

# Verify OLD exists uniquely
count = js.count(OLD)
print(f"OLD appears {count} time(s) in jsCode")
if count != 1:
    print("WARNING: not unique, need longer context")

# Build NEW — CLIENT BRIEF section prepended before BRAND section
NEW = (
    "\n\n"
    "'══ CLIENT BRIEF — FOLLOW EXACTLY (overrides default AI choices) ══\\n' +\n"
    "(hasBrief\n"
    "  ? clientBriefBlock + '\\n\\n'\n"
    "  : '(No specific brief provided — full AI creative control)\\n\\n') +\n"
    + OLD
)

print(f"\nNEW string: {repr(NEW[:200])}...")

# Perform replacement
js_new = js.replace(OLD, NEW, 1)

if js_new == js:
    print("\nERROR: Replacement had no effect — OLD string not found exactly")
    sys.exit(1)

print(f"\nReplacement successful. New jsCode length: {len(js_new)}")

# Verify the injection
brief_pos = js_new.find('══ CLIENT BRIEF')
print(f"CLIENT BRIEF now at position: {brief_pos}")
print("Context:", repr(js_new[brief_pos-5:brief_pos+120]))

# Save back
n9['parameters']['jsCode'] = js_new
with open(WORKFLOW, 'w', encoding='utf-8') as f:
    json.dump(wf, f, ensure_ascii=False, indent=2)

print("\n✓ Saved ai-cloner-odoo.json with CLIENT BRIEF injection")
print("  Node:", n9.get('name'))
print("  jsCode length:", len(js_new))
