"""
Odoo Blog Automation Engine
Fetches products, generates SEO blogs, creates cover images, and publishes
Usage: python odoo_blog_automation_engine.py [--website-id] [--product-id] [--dry-run]
"""

import requests
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import sys

from odoo_blog_automation_config import (
    ODOO_CONFIG, WEBSITES, BLOG_TEMPLATES, SEO_CONFIG,
    IMAGE_CONFIG, NOTIFICATIONS, SCHEDULE
)


class OdooBlogAutomation:
    """Main automation engine for Odoo blog creation"""

    def __init__(self, odoo_config: Dict = None):
        self.config = odoo_config or ODOO_CONFIG
        self.session = requests.Session()
        self.uid = None
        self.partner_id = None
        self._authenticate()

    def _authenticate(self) -> bool:
        """Authenticate with Odoo using JSON-RPC"""
        try:
            auth_payload = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "service": "common",
                    "method": "authenticate",
                    "args": [
                        self.config["db"],
                        self.config["user"],
                        self.config["password"],
                        {}
                    ]
                },
                "id": 1
            }

            response = self.session.post(
                f"{self.config['url']}/jsonrpc",
                json=auth_payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                if 'result' in result:
                    self.uid = result['result']
                    print(f"✓ Authenticated with Odoo (UID: {self.uid})")
                    return True

            print(f"✗ Authentication failed: {response.text}")
            return False

        except Exception as e:
            print(f"✗ Authentication error: {str(e)}")
            return False

    def fetch_products(self, website_id: int, limit: int = 50) -> List[Dict]:
        """Fetch products for a specific website"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "service": "object",
                    "method": "execute",
                    "args": [
                        self.config["db"],
                        self.uid,
                        self.config["password"],
                        "product.product",
                        "search_read",
                        [[["sale_ok", "=", True], ["website_id", "=", website_id]]],
                        ["id", "name", "description", "list_price", "category_id", "image_1920"]
                    ]
                },
                "id": 2
            }

            response = self.session.post(
                f"{self.config['url']}/jsonrpc",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                if 'result' in result:
                    products = result['result'][:limit]
                    print(f"✓ Fetched {len(products)} products from website {website_id}")
                    return products

            print(f"✗ Failed to fetch products: {response.text}")
            return []

        except Exception as e:
            print(f"✗ Error fetching products: {str(e)}")
            return []

    def generate_seo_blog_content(
        self,
        website_id: int,
        product: Dict,
        blog_category: str = "balloons"
    ) -> Dict:
        """Generate SEO-optimized blog content for a product"""

        website_info = WEBSITES.get(website_id, {})
        template = BLOG_TEMPLATES.get(blog_category, BLOG_TEMPLATES["balloons"])
        geo_keywords = website_info.get("geo_keywords", ["Long Island"])

        # Build blog content structure
        blog_data = {
            "product_id": product.get("id"),
            "product_name": product.get("name", ""),
            "website_id": website_id,
            "website_name": website_info.get("name", ""),
            "website_domain": website_info.get("domain", ""),
            "category": blog_category,
            "publish_date": datetime.now().strftime("%Y-%m-%d"),
            "author": "Hiren Kumar Digital",
        }

        # Generate title
        year = datetime.now().year
        location = geo_keywords[0] if geo_keywords else "Long Island"
        blog_data["title"] = template["title_template"].format(
            location=location,
            year=year,
            product=product.get("name", "Product")
        )

        # Generate SEO meta description
        blog_data["meta_description"] = (
            f"Discover {product.get('name', 'products')} at {website_info.get('name', '')}. "
            f"Expert tips, buying guides, and local {location} service information. "
            f"Same-day delivery available."
        )[:155]

        # Build blog body with SEO sections
        blog_data["body_html"] = self._build_blog_body(
            product,
            website_info,
            blog_category,
            geo_keywords
        )

        # Meta tags for SEO
        blog_data["meta_tags"] = {
            "keywords": ", ".join(template["keywords"] + geo_keywords),
            "robots": "index, follow",
            "og:title": blog_data["title"],
            "og:description": blog_data["meta_description"],
            "og:type": "article",
            "article:author": blog_data["author"],
            "article:published_time": blog_data["publish_date"]
        }

        # Schema.org structured data
        blog_data["schema_org"] = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": blog_data["title"],
            "description": blog_data["meta_description"],
            "author": {
                "@type": "Organization",
                "name": website_info.get("name", "")
            },
            "publisher": {
                "@type": "Organization",
                "name": website_info.get("name", "")
            },
            "datePublished": blog_data["publish_date"],
            "url": f"{website_info.get('domain', '')}/blog/{self._slug_title(blog_data['title'])}"
        }

        return blog_data

    def _build_blog_body(
        self,
        product: Dict,
        website_info: Dict,
        category: str,
        geo_keywords: List[str]
    ) -> str:
        """Build HTML blog body with SEO optimization"""

        location = geo_keywords[0] if geo_keywords else "Long Island"

        html_sections = [
            f"<h2>About {product.get('name', 'Our Product')}</h2>",
            f"<p>When it comes to {category.replace('_', ' ')} in {location}, "
            f"{website_info.get('name', '')} is your trusted source. "
            f"Our curated selection of {product.get('name', 'products')} ensures "
            f"quality and value for every occasion.</p>",

            "<h2>Why Choose Our Products?</h2>",
            "<ul>",
            "<li>✓ Local expertise with nationwide reach</li>",
            "<li>✓ Same-day delivery available</li>",
            "<li>✓ Personalization options</li>",
            "<li>✓ Competitive pricing</li>",
            "<li>✓ Expert customer service</li>",
            "</ul>",

            f"<h2>{product.get('name', 'Product')} Guide</h2>",
            f"<p>Looking for {product.get('name', 'the perfect gift')} in {location}? "
            f"Our {product.get('name', 'products')} are hand-selected for quality and variety. "
            f"Perfect for {', '.join(geo_keywords)}.</p>",

            f"<h2>Local Service Area</h2>",
            f"<p>We proudly serve {', '.join(geo_keywords)} with fast, reliable delivery. "
            f"Order online and pick up same-day, or have it delivered to your door.</p>",

            f"<h2>Why {location} Chooses Us</h2>",
            f"<p>Since opening our doors, we've become the go-to destination for quality "
            f"{category.replace('_', ' ')} and exceptional service. Our commitment to customer "
            f"satisfaction and local community makes us the trusted choice.</p>",

            "<h2>Order Now</h2>",
            f"<p><strong><a href='{website_info.get('domain', '')}/shop' target='_blank' rel='noopener'>"
            f"Browse our {product.get('name', 'complete selection')} and order today!</a></strong></p>",

            "<h2>Frequently Asked Questions</h2>",
            "<dl>",
            f"<dt>Can you deliver to {geo_keywords[0]}?</dt>",
            "<dd>Yes! We offer same-day delivery to most areas. Contact us for details.</dd>",
            "<dt>How do I customize my order?</dt>",
            "<dd>All of our products can be personalized. Ask our team about custom options!</dd>",
            "<dt>What's your price guarantee?</dt>",
            "<dd>We promise the best value in the area. If you find a better price, we'll match it.</dd>",
            "</dl>"
        ]

        return "\n".join(html_sections)

    def create_cover_image_data(
        self,
        product: Dict,
        website_info: Dict,
        blog_title: str
    ) -> Dict:
        """Generate cover image metadata (actual image creation happens in n8n)"""

        return {
            "width": IMAGE_CONFIG["width"],
            "height": IMAGE_CONFIG["height"],
            "title": blog_title[:50],  # Truncate for image
            "subtitle": website_info.get("name", ""),
            "product_image": product.get("image_1920", ""),
            "colors": IMAGE_CONFIG["brand_colors"],
            "logo_url": f"{website_info.get('domain', '')}/logo.png",
            "branding_text": f"www.{website_info.get('domain', '').split('//')[1] if '//' in website_info.get('domain', '') else ''}"
        }

    def publish_blog_to_odoo(
        self,
        website_id: int,
        blog_section_id: int,
        blog_data: Dict
    ) -> Tuple[bool, str]:
        """Publish blog post to Odoo"""

        try:
            # Prepare blog post data
            post_data = {
                "name": blog_data["title"],
                "subtitle": blog_data["meta_description"],
                "content": blog_data["body_html"],
                "blog_id": blog_section_id,
                "website_id": website_id,
                "author_id": 1,  # Admin
                "is_published": True,
                "post_category_ids": [[6, False, []]],  # No category
            }

            # Add SEO meta if Odoo supports it
            if hasattr(blog_data, "meta_tags"):
                post_data["seo_description"] = blog_data.get("meta_description", "")

            # Create via JSON-RPC
            payload = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "service": "object",
                    "method": "execute",
                    "args": [
                        self.config["db"],
                        self.uid,
                        self.config["password"],
                        "blog.post",
                        "create",
                        [post_data]
                    ]
                },
                "id": 3
            }

            response = self.session.post(
                f"{self.config['url']}/jsonrpc",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                if 'result' in result and result['result']:
                    post_id = result['result']
                    post_url = f"{WEBSITES[website_id]['domain']}/blog/{self._slug_title(blog_data['title'])}-{post_id}"
                    print(f"✓ Blog published: {post_url}")
                    return True, post_url

            print(f"✗ Failed to publish blog: {response.text}")
            return False, ""

        except Exception as e:
            print(f"✗ Error publishing blog: {str(e)}")
            return False, ""

    def _slug_title(self, title: str) -> str:
        """Convert title to URL slug"""
        return title.lower().replace(" ", "-")[:50]

    def submit_to_google_search_console(self, blog_url: str) -> bool:
        """Submit blog URL to Google Search Console for indexing"""
        print(f"ℹ GSC Submission queued for: {blog_url}")
        print(f"  → Manual action: Visit https://search.google.com/search-console/")
        print(f"  → Paste URL and click 'Request Indexing'")
        return True

    def log_blog_metrics(self, blog_data: Dict, post_url: str) -> Dict:
        """Log metrics for monitoring"""

        return {
            "timestamp": datetime.now().isoformat(),
            "website": blog_data.get("website_name"),
            "product": blog_data.get("product_name"),
            "title": blog_data.get("title"),
            "url": post_url,
            "seo_score": self._calculate_seo_score(blog_data),
            "word_count": len(blog_data.get("body_html", "").split()),
            "meta_description_length": len(blog_data.get("meta_description", ""))
        }

    def _calculate_seo_score(self, blog_data: Dict) -> int:
        """Calculate simple SEO score (0-100)"""
        score = 50

        # Title length (50-60 chars is optimal)
        title_len = len(blog_data.get("title", ""))
        if 40 <= title_len <= 70:
            score += 10

        # Meta description (155 chars optimal)
        meta_len = len(blog_data.get("meta_description", ""))
        if 150 <= meta_len <= 160:
            score += 10

        # Body content
        word_count = len(blog_data.get("body_html", "").split())
        if SEO_CONFIG["min_word_count"] <= word_count <= SEO_CONFIG["max_word_count"]:
            score += 20

        # Has schema
        if blog_data.get("schema_org"):
            score += 10

        return min(score, 100)


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Odoo Blog Automation - Create SEO blogs for all e-commerce products"
    )
    parser.add_argument(
        "--website-id",
        type=int,
        default=1,
        help="Website ID to process (default: 1)"
    )
    parser.add_argument(
        "--product-id",
        type=int,
        help="Specific product ID (optional)"
    )
    parser.add_argument(
        "--category",
        default="balloons",
        help="Blog category (default: balloons)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Test mode - don't publish"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Max products to process (default: 5)"
    )

    args = parser.parse_args()

    # Initialize automation engine
    print("🚀 Initializing Odoo Blog Automation Engine...")
    engine = OdooBlogAutomation()

    if not engine.uid:
        print("❌ Failed to authenticate with Odoo")
        return 1

    # Fetch products
    website_id = args.website_id
    products = engine.fetch_products(website_id, limit=args.limit)

    if not products:
        print("❌ No products found")
        return 1

    # Process products
    print(f"\n📝 Generating {len(products)} blog posts...")

    published_blogs = []
    for idx, product in enumerate(products, 1):
        print(f"\n[{idx}/{len(products)}] Processing: {product.get('name')}")

        # Generate blog content
        blog_data = engine.generate_seo_blog_content(
            website_id,
            product,
            args.category
        )

        if args.dry_run:
            print(f"  DRY RUN: Would publish '{blog_data['title']}'")
            print(f"  Words: {len(blog_data['body_html'].split())}")
            print(f"  SEO Score: {engine._calculate_seo_score(blog_data)}/100")
        else:
            # Determine blog section
            blog_sections = WEBSITES[website_id]["blog_sections"]
            blog_section_id = list(blog_sections.keys())[idx % len(blog_sections)]

            # Publish blog
            success, post_url = engine.publish_blog_to_odoo(
                website_id,
                blog_section_id,
                blog_data
            )

            if success:
                # Log metrics
                metrics = engine.log_blog_metrics(blog_data, post_url)
                published_blogs.append(metrics)

                # Submit to GSC
                if NOTIFICATIONS.get("gsc_submission"):
                    engine.submit_to_google_search_console(post_url)

    # Summary
    print(f"\n{'='*60}")
    print(f"✓ Blog Automation Complete")
    print(f"  Published: {len(published_blogs)} blogs")
    print(f"  Website: {WEBSITES[website_id]['name']}")
    print(f"  Category: {args.category}")
    if published_blogs:
        print(f"  Latest URL: {published_blogs[-1]['url']}")
    print(f"{'='*60}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
