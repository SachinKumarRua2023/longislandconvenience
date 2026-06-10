#!/usr/bin/env python3
"""
Reorganize homepage structure:
- Move Pokemon cards gallery to TOP
- Keep bundle showcase at BOTTOM
"""

import os
import re

base_dir = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\HIREN_PROJECT_ORGANIZED\02_N8N_WORKFLOWS\SCRIPTS_BY_WEBSITE\WEBSITE_36_LONG_ISLAND_CARDS"
html_file = os.path.join(base_dir, "homepage_base64.html")

print("=" * 70)
print("REORGANIZING HOMEPAGE STRUCTURE")
print("=" * 70)

# Read HTML
print("\nReading homepage...")
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Extract Pokemon gallery section
pokemon_gallery_pattern = r'<!-- POKEMON CARDS SHOWCASE GALLERY -->.*?</style>'
pokemon_match = re.search(pokemon_gallery_pattern, html_content, re.DOTALL)

if pokemon_match:
    pokemon_gallery = pokemon_match.group(0)
    # Remove from current location
    html_content = html_content[:pokemon_match.start()] + html_content[pokemon_match.end():]
    print("[OK] Pokemon gallery extracted from bottom")
else:
    pokemon_gallery = ""
    print("[INFO] Pokemon gallery not found")

# Extract bundle showcase section
bundle_pattern = r'<!-- BUNDLE SHOWCASE WITH FIRE ANIMATION -->.*?</div>\s*(?=<!-- CATEGORIES|<!-- EXPLORE|<section class="special)'
bundle_match = re.search(bundle_pattern, html_content, re.DOTALL)

if bundle_match:
    bundle_showcase = bundle_match.group(0)
    print("[OK] Bundle showcase found")
else:
    bundle_showcase = ""
    print("[INFO] Bundle showcase not found")

# Find insertion point for Pokemon gallery (right after header/nav, before hero)
hero_pattern = r'(<!-- HERO SECTION -->)'
if pokemon_gallery and re.search(hero_pattern, html_content):
    print("\nInserting Pokemon gallery at TOP...")
    html_content = re.sub(
        hero_pattern,
        pokemon_gallery + '\n\n' + r'\1',
        html_content
    )
    print("[OK] Pokemon gallery moved to TOP")

# Ensure bundle is at bottom (before footer)
if bundle_showcase:
    # Remove bundle from middle if it exists
    bundle_remove_pattern = r'<!-- BUNDLE SHOWCASE WITH FIRE ANIMATION -->.*?</div>\s*(?=<!-- |<section|</section)\n*'
    html_content = re.sub(bundle_remove_pattern, '', html_content, flags=re.DOTALL)

    # Add bundle before closing body tag or at end
    if '</body>' in html_content:
        print("\nMoving bundle showcase to BOTTOM...")
        html_content = html_content.replace('</body>', bundle_showcase + '\n\n</body>')
        print("[OK] Bundle showcase moved to BOTTOM")
    else:
        html_content += '\n\n' + bundle_showcase
        print("[OK] Bundle showcase appended to BOTTOM")

# Save updated HTML
print("\nSaving reorganized homepage...")
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

file_size = os.path.getsize(html_file)
print(f"[OK] File saved ({file_size / (1024*1024):.2f} MB)")

print("\n" + "=" * 70)
print("HOMEPAGE STRUCTURE REORGANIZED:")
print("=" * 70)
print("\nNew Order:")
print("  1. Header & Navigation")
print("  2. POKEMON CARDS GALLERY (TOP) - New Location")
print("  3. Hero Section")
print("  4. Features")
print("  5. Categories")
print("  6. Special Sections")
print("  7. New Releases")
print("  8. Products")
print("  9. BUNDLE SHOWCASE (BOTTOM) - Kept Here")
print("  10. Footer")
print("\n" + "=" * 70)
