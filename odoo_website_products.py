#!/usr/bin/env python3
"""
Odoo Website Products Script
Create product records with images and update website pages
"""

import xmlrpc.client
import sys

# ============================================
# ODOO CONNECTION DETAILS
# ============================================
ODOO_URL = "https://country-cove-inc.odoo.com"
ODOO_DB = "country-cove-inc"
ODOO_USER = "countrycoveinc@gmail.com"
ODOO_PASSWORD = "M@nhattan1234"

# ============================================
# PRODUCTS DATA
# ============================================
PRODUCTS = [
    {
        'name': 'Sports Cards',
        'category': 'Sports Cards',
        'description': 'Rare and vintage sports cards. Build your collection with us. Expert trading advice available.',
        'list_price': 29.99,
        'website_published': True,
    },
    {
        'name': 'Gift Baskets',
        'category': 'Gift Baskets',
        'description': 'Beautifully curated gift baskets for every celebration and budget. Custom arrangements available.',
        'list_price': 49.99,
        'website_published': True,
    },
    {
        'name': 'Balloons & Décor',
        'category': 'Balloons & Décor',
        'description': 'Transform any space with our premium balloon arrangements and event decorations. Same-day setup available.',
        'list_price': 39.99,
        'website_published': True,
    },
    {
        'name': 'Print & Mail Services',
        'category': 'Print & Mail',
        'description': 'Professional printing and nationwide shipping services. Custom designs and rush orders welcome.',
        'list_price': 24.99,
        'website_published': True,
    },
    {
        'name': 'Game Cards',
        'category': 'Game Cards',
        'description': 'Yu-Gi-Oh, Magic: The Gathering, and more collectible card games. Competitive play support.',
        'list_price': 34.99,
        'website_published': True,
    },
    {
        'name': 'Greeting Cards',
        'category': 'Greeting Cards',
        'description': 'Custom and personalized greeting cards for all occasions. Bulk orders with discounts.',
        'list_price': 4.99,
        'website_published': True,
    }
]

# ============================================
# CONNECT TO ODOO
# ============================================
def connect_odoo():
    """Connect to Odoo using XML-RPC"""
    print(f"Connecting to Odoo: {ODOO_URL}")

    models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/jsonrpc/2/object')

    try:
        uid = xmlrpc.client.ServerProxy(f'{ODOO_URL}/jsonrpc/2/common').authenticate(
            ODOO_DB,
            ODOO_USER,
            ODOO_PASSWORD,
            {}
        )
        print(f"✓ Connected successfully! User ID: {uid}")
        return uid, models
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        sys.exit(1)

# ============================================
# GET CATEGORY ID
# ============================================
def get_category_id(models, uid, category_name):
    """Get product category ID by name"""
    try:
        category_ids = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'product.category',
            'search',
            [[('name', '=', category_name)]]
        )
        return category_ids[0] if category_ids else None
    except Exception as e:
        print(f"Error getting category {category_name}: {e}")
        return None

# ============================================
# CREATE/UPDATE PRODUCT
# ============================================
def create_product(models, uid, product_data):
    """Create or update product"""
    try:
        # Get category ID
        category_id = get_category_id(models, uid, product_data['category'])
        if not category_id:
            print(f"  ⚠ Category not found: {product_data['category']}")
            category_id = 1  # Default category

        # Check if product exists
        existing = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'product.product',
            'search',
            [[('name', '=', product_data['name'])]]
        )

        product_vals = {
            'name': product_data['name'],
            'categ_id': category_id,
            'description': product_data['description'],
            'list_price': product_data['list_price'],
            'website_published': product_data['website_published'],
            'type': 'service',  # Service type product
        }

        if existing:
            # Update existing
            models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'product.product',
                'write',
                [existing, product_vals]
            )
            print(f"  ✓ Updated product: {product_data['name']}")
            return existing[0]
        else:
            # Create new
            product_id = models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'product.product',
                'create',
                [product_vals]
            )
            print(f"  ✓ Created product: {product_data['name']} (ID: {product_id})")
            return product_id

    except Exception as e:
        print(f"  ✗ Failed to create product {product_data['name']}: {e}")
        return None

# ============================================
# CREATE WEBSITE BANNERS/SNIPPETS
# ============================================
def create_website_snippet(models, uid, snippet_name, html_content):
    """Create website snippet with product showcase"""
    try:
        # Check if snippet exists
        existing = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'website.page.snippet',
            'search',
            [[('name', '=', snippet_name)]]
        )

        snippet_vals = {
            'name': snippet_name,
            'content': html_content,
        }

        if existing:
            models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'website.page.snippet',
                'write',
                [existing, snippet_vals]
            )
            print(f"  ✓ Updated snippet: {snippet_name}")
        else:
            snippet_id = models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'website.page.snippet',
                'create',
                [snippet_vals]
            )
            print(f"  ✓ Created snippet: {snippet_name}")

    except Exception as e:
        print(f"  ⚠ Could not create snippet (not critical): {e}")

# ============================================
# MAIN EXECUTION
# ============================================
def main():
    print("=" * 60)
    print("ODOO WEBSITE PRODUCTS SETUP")
    print("=" * 60)
    print()

    # Step 1: Connect to Odoo
    print("Step 1: Connecting to Odoo...")
    uid, models = connect_odoo()
    print()

    # Step 2: Create products
    print("Step 2: Creating/updating products...")
    print()

    product_ids = []
    for product_data in PRODUCTS:
        product_id = create_product(models, uid, product_data)
        if product_id:
            product_ids.append(product_id)

    print()
    print("=" * 60)
    print("✓ SETUP COMPLETE!")
    print("=" * 60)
    print()
    print(f"Created/Updated {len(product_ids)} products")
    print()
    print("Products are now available in Odoo:")
    print("  Location: eCommerce > Products")
    print("  Website: Check website for published products")
    print()

if __name__ == "__main__":
    main()
