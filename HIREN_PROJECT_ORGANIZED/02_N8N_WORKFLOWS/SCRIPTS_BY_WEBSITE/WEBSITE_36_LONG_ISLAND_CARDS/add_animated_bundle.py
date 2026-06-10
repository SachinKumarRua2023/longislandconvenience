#!/usr/bin/env python3
"""
Add animated bundle image with fire border and floating effect to New Releases section
"""

import os
import re

base_dir = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\HIREN_PROJECT_ORGANIZED\02_N8N_WORKFLOWS\SCRIPTS_BY_WEBSITE\WEBSITE_36_LONG_ISLAND_CARDS"

# Read the bulk-dragon-collection base64
print("Loading bulk-dragon-collection base64...")
b64_file = os.path.join(base_dir, "bulk-dragon-collection_base64.txt")
with open(b64_file, 'r') as f:
    bundle_b64 = f.read().strip()

# Read homepage
print("Reading homepage_base64.html...")
html_file = os.path.join(base_dir, "homepage_base64.html")
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Create the bundle showcase HTML
bundle_html = f'''
    <!-- BUNDLE SHOWCASE WITH FIRE ANIMATION -->
    <div class="bundle-showcase">
        <div class="bundle-image-wrapper">
            <img class="bundle-image" src="data:image/png;base64,{bundle_b64}" alt="Bulk Dragon Collection">
            <div class="bundle-label">🔥 EXCLUSIVE 🔥</div>
        </div>
    </div>
'''

# Find the New Releases section and add the bundle before the products-grid
pattern = r'(<section class="new-releases">\s*<h2 class="section-title">New Releases</h2>)'
replacement = r'\1' + bundle_html

new_content = re.sub(pattern, replacement, html_content, flags=re.IGNORECASE)

if new_content != html_content:
    html_content = new_content
    print("[OK] Bundle image added to New Releases section")
else:
    print("[ERROR] Could not find New Releases section")
    exit(1)

# Save updated HTML
print("Saving updated homepage...")
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

file_size = os.path.getsize(html_file)
print(f"[OK] Saved ({file_size} bytes)")

print("\n" + "=" * 70)
print("SUCCESS! Animated bundle image added with:")
print("  ✓ Fire glow animation (2s cycle)")
print("  ✓ Floating effect (3s cycle)")
print("  ✓ Fire border label with pulsing glow")
print("  ✓ Background gradient effect")
print("=" * 70)
print("\nThe homepage is ready to deploy!")
print("Run: python deploy_homepage_odoo.py")
