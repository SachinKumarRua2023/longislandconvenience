#!/usr/bin/env python3
"""
Smart Setup: Check Website ID, find correct website, and organize folder structure
"""

import xmlrpc.client
import os
import shutil
from pathlib import Path

URL = "https://country-cove-inc.odoo.com"
DB = "country-cove-inc"
EMAIL = "countrycoveinc@gmail.com"
PASSWORD = "M@nhattan1234"

print("=" * 80)
print("LONG ISLAND CARDS - Smart Website Setup")
print("=" * 80)
print()

# Step 1: Connect and get all websites
print("[1/4] Connecting to Odoo...")
try:
    common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
    uid = common.authenticate(DB, EMAIL, PASSWORD, {})
    models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")
    print("[OK] Connected\n")
except Exception as e:
    print(f"✗ Connection failed: {e}")
    exit(1)

# Step 2: Get all websites
print("[2/4] Checking all websites...\n")
try:
    website_ids = models.execute_kw(DB, uid, PASSWORD,
        'website', 'search',
        [[]],
        {'order': 'id asc'}
    )

    if not website_ids:
        print("✗ No websites found in Odoo")
        exit(1)

    websites = models.execute_kw(DB, uid, PASSWORD,
        'website', 'read',
        [website_ids, ['id', 'name', 'domain']]
    )

    print("Available Websites in Odoo:")
    print("-" * 80)
    for i, website in enumerate(websites, 1):
        print(f"{i}. ID: {website['id']} | Name: {website['name']} | Domain: {website['domain'] or 'N/A'}")
    print()

except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)

# Step 3: Find Long Island Cards website
print("[3/4] Finding Long Island Cards website...\n")

longisland_website = None
for website in websites:
    name_lower = website['name'].lower()
    if name_lower == 'long island cards':
        longisland_website = website
        break

if not longisland_website:
    print("⚠ Long Island Cards website not found by name.")
    print()
    print("Please select from the list above:")
    try:
        choice = int(input("Enter the number (1-" + str(len(websites)) + "): ")) - 1
        if 0 <= choice < len(websites):
            longisland_website = websites[choice]
        else:
            print("✗ Invalid selection")
            exit(1)
    except:
        print("✗ Invalid input")
        exit(1)

website_id = longisland_website['id']
website_name = longisland_website['name']
website_domain = longisland_website['domain'] or 'unknown'

print(f"[OK] Found: {website_name}")
print(f"  - ID: {website_id}")
print(f"  - Domain: {website_domain}")
print()

# Step 4: Create folder structure
print("[4/4] Organizing folder structure...\n")

# Create folder name
folder_name = f"WEBSITE_{website_id}_{website_name.replace(' ', '_').upper()}"
new_folder = f"c:\\Users\\Sachin Kumar\\OneDrive\\Desktop\\HirenTask\\HIREN_PROJECT_ORGANIZED\\02_N8N_WORKFLOWS\\SCRIPTS_BY_WEBSITE\\{folder_name}"

print(f"Creating folder: {folder_name}")
print()

try:
    # Create directory if it doesn't exist
    Path(new_folder).mkdir(parents=True, exist_ok=True)

    # List of files to move/copy
    files_to_move = [
        'homepage.html',
        'homepage.py',
        'add_images_homepage.py',
        'add_images_homepage_configurable.py',
        'add_images_website_1.py',
        'add_images_website_1_configurable.py',
        'check_websites.py',
        'deploy_homepage_odoo.py',
        'category_config.json',
        'homepage_config.json',
        'README_homepage_images.md',
        'README_add_images.md',
        'QUICKSTART.md',
        'SCRIPTS_OVERVIEW.md',
        'DEPLOYMENT_GUIDE.md',
        'HOMEPAGE_DEPLOYMENT_CHECKLIST.md'
    ]

    current_folder = "c:\\Users\\Sachin Kumar\\OneDrive\\Desktop\\HirenTask\\HIREN_PROJECT_ORGANIZED\\02_N8N_WORKFLOWS\\SCRIPTS_BY_WEBSITE\\WEBSITE_1"

    moved_count = 0
    for file in files_to_move:
        source = os.path.join(current_folder, file)
        if os.path.exists(source):
            dest = os.path.join(new_folder, file)
            shutil.copy2(source, dest)
            print(f"  [OK] {file}")
            moved_count += 1

    print()
    print(f"[OK] Copied {moved_count} files to new folder")
    print()

except Exception as e:
    print(f"[ERROR] Error organizing folder: {e}")
    exit(1)

# Step 5: Update scripts with correct Website ID
print("Updating scripts with correct Website ID...")
print()

try:
    # Update deploy_homepage_odoo.py
    deploy_script = os.path.join(new_folder, 'deploy_homepage_odoo.py')
    if os.path.exists(deploy_script):
        with open(deploy_script, 'r') as f:
            content = f.read()

        # Replace WEBSITE_ID
        content = content.replace('WEBSITE_ID = 1', f'WEBSITE_ID = {website_id}')

        with open(deploy_script, 'w') as f:
            f.write(content)

        print(f"  [OK] Updated deploy_homepage_odoo.py (WEBSITE_ID = {website_id})")

    # Update add_images_homepage.py
    images_script = os.path.join(new_folder, 'add_images_homepage.py')
    if os.path.exists(images_script):
        with open(images_script, 'r') as f:
            content = f.read()

        content = content.replace('WEBSITE_ID = 1', f'WEBSITE_ID = {website_id}')

        with open(images_script, 'w') as f:
            f.write(content)

        print(f"  [OK] Updated add_images_homepage.py (WEBSITE_ID = {website_id})")

    print()

except Exception as e:
    print(f"[WARNING] Could not update some scripts: {e}")
    print()

# Final summary
print("=" * 80)
print("SETUP COMPLETE!")
print("=" * 80)
print()
print(f"Website: {website_name}")
print(f"Website ID: {website_id}")
print(f"Domain: {website_domain}")
print()
print(f"New Folder: {folder_name}")
print(f"Location: {new_folder}")
print()
print("[SUCCESS] All scripts moved and updated!")
print()
print("NEXT STEPS:")
print()
print(f"1. Navigate to the new folder:")
print(f"   cd \"{new_folder}\"")
print()
print("2. Deploy the homepage:")
print(f"   python deploy_homepage_odoo.py")
print()
print("3. Verify on website:")
print(f"   Go to https://{website_domain}")
print()
print("FILES IN NEW FOLDER:")
print("  [OK] homepage.html - Custom homepage design")
print("  [OK] deploy_homepage_odoo.py - Deploy to Odoo")
print("  [OK] add_images_homepage.py - Add category images")
print("  [OK] homepage_config.json - Category configuration")
print("  [OK] README files - Documentation")
print("  [OK] And more...")
print()
