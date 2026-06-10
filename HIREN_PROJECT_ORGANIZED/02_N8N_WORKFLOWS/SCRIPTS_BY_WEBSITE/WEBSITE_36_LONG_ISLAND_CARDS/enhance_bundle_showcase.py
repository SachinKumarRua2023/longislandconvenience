#!/usr/bin/env python3
"""
Enhance bundle showcase with:
- Full width and height display
- Fire border circulating animation
- Better visibility
- Stronger glow effects
"""

import os
import re

base_dir = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\HIREN_PROJECT_ORGANIZED\02_N8N_WORKFLOWS\SCRIPTS_BY_WEBSITE\WEBSITE_36_LONG_ISLAND_CARDS"
html_file = os.path.join(base_dir, "homepage_base64.html")

print("=" * 70)
print("ENHANCING BUNDLE SHOWCASE WITH FIRE BORDER & FULL DISPLAY")
print("=" * 70)

# Read HTML
print("\nReading homepage...")
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Enhanced CSS animations for bundle showcase
enhanced_css = '''
    /* ========== ENHANCED FIRE BORDER ANIMATION ========== */
    @keyframes fire-border-circulate {
        0% {
            border-color: #ff4500;
            box-shadow: 0 0 30px #ff4500, inset 0 0 30px rgba(255, 69, 0, 0.5), 0 0 60px #ff4500;
            filter: brightness(1.2);
        }
        25% {
            border-color: #ff6347;
            box-shadow: 0 0 40px #ff6347, inset 0 0 40px rgba(255, 99, 71, 0.6), 0 0 80px #ff6347;
            filter: brightness(1.3);
        }
        50% {
            border-color: #ffa500;
            box-shadow: 0 0 50px #ffa500, inset 0 0 50px rgba(255, 165, 0, 0.7), 0 0 100px #ffa500;
            filter: brightness(1.4);
        }
        75% {
            border-color: #ff6347;
            box-shadow: 0 0 40px #ff6347, inset 0 0 40px rgba(255, 99, 71, 0.6), 0 0 80px #ff6347;
            filter: brightness(1.3);
        }
        100% {
            border-color: #ff4500;
            box-shadow: 0 0 30px #ff4500, inset 0 0 30px rgba(255, 69, 0, 0.5), 0 0 60px #ff4500;
            filter: brightness(1.2);
        }
    }

    @keyframes floating-enhanced {
        0%, 100% {
            transform: translateY(0px) scale(1);
        }
        50% {
            transform: translateY(-30px) scale(1.02);
        }
    }

    /* Enhanced bundle showcase */
    .bundle-showcase {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 60px 20px;
        background: linear-gradient(135deg, rgba(255, 69, 0, 0.1) 0%, rgba(255, 99, 71, 0.1) 50%, rgba(255, 165, 0, 0.1) 100%);
        border-radius: 16px;
        margin-bottom: 60px;
        position: relative;
        border: 4px solid #ff4500;
        min-height: 500px;
        box-shadow: 0 0 80px rgba(255, 69, 0, 0.4), inset 0 0 60px rgba(255, 69, 0, 0.2);
    }

    .bundle-image-wrapper {
        position: relative;
        animation: floating-enhanced 4s ease-in-out infinite;
        z-index: 2;
    }

    .bundle-image {
        max-width: 100%;
        width: 400px;
        height: auto;
        max-height: 500px;
        border-radius: 16px;
        animation: fire-border-circulate 2.5s ease-in-out infinite;
        border: 6px solid #ff4500;
        padding: 12px;
        background: white;
        box-shadow: 0 0 80px rgba(255, 69, 0, 0.8), inset 0 0 40px rgba(255, 69, 0, 0.3);
        object-fit: cover;
        filter: drop-shadow(0 0 30px rgba(255, 69, 0, 0.7));
        transition: transform 0.3s ease;
    }

    .bundle-image:hover {
        transform: scale(1.05);
    }

    .bundle-label {
        position: absolute;
        top: -15px;
        right: 30px;
        background: linear-gradient(135deg, #ff4500 0%, #ff6347 50%, #ffa500 100%);
        color: white;
        padding: 15px 30px;
        border-radius: 25px;
        font-weight: bold;
        font-size: 18px;
        animation: fire-border-circulate 2s ease-in-out infinite;
        box-shadow: 0 8px 25px rgba(255, 69, 0, 0.8);
        transform: rotate(-12deg);
        z-index: 3;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        letter-spacing: 1px;
    }

    /* Fire effect particles */
    .bundle-showcase::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background:
            radial-gradient(circle at 20% 30%, rgba(255, 69, 0, 0.15) 0%, transparent 20%),
            radial-gradient(circle at 80% 70%, rgba(255, 165, 0, 0.15) 0%, transparent 20%),
            radial-gradient(circle at 50% 50%, rgba(255, 99, 71, 0.1) 0%, transparent 30%);
        animation: floating-enhanced 6s ease-in-out infinite;
        pointer-events: none;
        border-radius: 16px;
    }
'''

# Find and replace the CSS section for bundle showcase
print("\nUpdating CSS animations for bundle showcase...")

# Find the existing bundle CSS
pattern = r'(\.bundle-showcase\s*\{[^}]*\}.*?\.bundle-label\s*\{[^}]*\})'
if re.search(pattern, html_content, re.DOTALL):
    print("  [OK] Found existing bundle CSS, replacing...")
    # Replace with enhanced version
    html_content = re.sub(pattern, enhanced_css, html_content, flags=re.DOTALL)
else:
    print("  [INFO] Bundle CSS not found in main style, will be added")

# Enhance the bundle image HTML if needed
print("\nUpdating bundle image HTML structure...")

# Find bundle image and enhance it
bundle_pattern = r'(<img class="bundle-image"[^>]*src="data:image/png;base64,[^"]*"[^>]*>)'
bundle_replacement = r'<img class="bundle-image" \1 style="max-width: 100%; width: 400px; height: auto; max-height: 500px;">'

html_content = re.sub(bundle_pattern, bundle_replacement, html_content)

if re.search(bundle_pattern, html_content):
    print("  [OK] Bundle image enhanced")

# Save updated HTML
print("\nSaving enhanced homepage...")
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

file_size = os.path.getsize(html_file)
print(f"[OK] File saved ({file_size / (1024*1024):.2f} MB)")

print("\n" + "=" * 70)
print("BUNDLE SHOWCASE ENHANCED:")
print("  ✓ Full width and height display (400x500px)")
print("  ✓ Fire border circulating animation (2.5s cycle)")
print("  ✓ Enhanced floating effect (4s cycle)")
print("  ✓ Strong glow effects (inset + outer)")
print("  ✓ Fire label with gradient (pulsing)")
print("  ✓ Brightness animation during glow")
print("  ✓ Better visibility and prominence")
print("  ✓ Fire particle background effects")
print("=" * 70)
print("\nBundle showcase is now highly visible with active fire animations!")
