"""
Odoo Blog Automation Configuration
Manages all e-commerce websites and their product-to-blog mappings
"""

ODOO_CONFIG = {
    "url": "https://country-cove-inc.odoo.com",
    "db": "country-cove-inc",
    "user": "countrycoveinc@gmail.com",
    "password": "M@nhattan1234",
    "api_endpoint": "/jsonrpc"
}

# Website configurations with product categories and blog sections
WEBSITES = {
    1: {
        "name": "Long Island Convenience",
        "domain": "https://www.longislandconvenience.com",
        "description": "Convenience store with balloons, gift baskets, and greeting cards",
        "blog_sections": {
            3: "Balloons & Party Decor",
            5: "Gift Baskets & Gifts",
            7: "Convenience & Grocery"
        },
        "product_categories": {
            "balloons": "Balloons & Party Supplies",
            "gift_baskets": "Gift Baskets & Gifts",
            "greeting_cards": "Greeting Cards & Stationery"
        },
        "geo_keywords": ["Long Island", "Plainview NY", "Nassau County"]
    },
    36: {
        "name": "Long Island Cards",
        "domain": "https://www.longislandcards.com",
        "description": "Trading cards and collectibles",
        "blog_sections": {
            8: "Pokemon Cards",
            9: "Gaming & Sports Cards",
            10: "Card Values & Guides"
        },
        "product_categories": {
            "pokemon": "Pokemon Trading Cards",
            "gaming": "Gaming & TCG Cards",
            "sports": "Sports Cards"
        },
        "geo_keywords": ["Long Island", "Trading Cards", "Collectibles"]
    },
    37: {
        "name": "Long Island Gift Basket",
        "domain": "https://www.ligiftbasket.com",
        "description": "Specialty gift baskets and gifts",
        "blog_sections": {
            11: "Gift Baskets",
            12: "Occasions & Events",
            13: "Same Day Delivery"
        },
        "product_categories": {
            "graduation": "Graduation Gift Baskets",
            "fathers_day": "Father's Day Gifts",
            "occasions": "All Occasion Baskets"
        },
        "geo_keywords": ["Long Island", "Gift Baskets", "Plainview"]
    },
    38: {
        "name": "Long Island Balloons & Decor",
        "domain": "https://www.longislandballoonsdecor.com",
        "description": "Balloon arrangements and party decorations",
        "blog_sections": {
            14: "Graduation Balloons",
            15: "Party Decorations",
            16: "Event Planning"
        },
        "product_categories": {
            "balloons": "Balloon Arrangements",
            "decorations": "Party Decorations",
            "events": "Event Supplies"
        },
        "geo_keywords": ["Long Island", "Balloons", "Nassau County", "Party Decor"]
    },
    39: {
        "name": "Long Island Print & Mail",
        "domain": "https://www.longislandprintandmail.com",
        "description": "Printing and direct mail services",
        "blog_sections": {
            17: "Printing Services",
            18: "Greeting Cards",
            19: "Direct Mail"
        },
        "product_categories": {
            "printing": "Custom Printing",
            "greeting_cards": "Greeting Cards",
            "direct_mail": "Direct Mail Services"
        },
        "geo_keywords": ["Long Island", "Printing", "Custom Services"]
    }
}

# Blog content templates with SEO focus
BLOG_TEMPLATES = {
    "pokemon": {
        "title_template": "Pokemon Cards {location}: Complete Buying & Trading Guide {year}",
        "keywords": ["pokemon cards", "trading cards", "collectibles", "Long Island"],
        "sections": ["Introduction", "Why Pokemon Cards", "Finding Rare Cards", "Storage Tips", "Fair Pricing"]
    },
    "gaming_cards": {
        "title_template": "Gaming & TCG Cards {location}: Magic, Yu-Gi-Oh & More {year}",
        "keywords": ["trading cards", "gaming cards", "TCG", "collectibles"],
        "sections": ["Card Game Overview", "Popular Games", "Investing Tips", "Local Players", "Events"]
    },
    "balloons": {
        "title_template": "Graduation Balloon Decorations {location}: Complete Party Setup {year}",
        "keywords": ["graduation balloons", "party decorations", "balloon arch", "event planning"],
        "sections": ["Balloon Options", "Decoration Ideas", "Setup Guide", "Budget Tips", "DIY vs Professional"]
    },
    "gift_baskets": {
        "title_template": "Graduation Gift Baskets {location}: Thoughtful Presents for Grads {year}",
        "keywords": ["gift baskets", "graduation gifts", "same day delivery"],
        "sections": ["Gift Basket Ideas", "Customization", "Delivery Options", "Budget Ranges", "Last Minute Options"]
    },
    "fathers_day": {
        "title_template": "Father's Day Gifts {location}: From Gift Baskets to Balloons {year}",
        "keywords": ["fathers day", "gift ideas", "dad gifts"],
        "sections": ["Gift Ideas", "Local Options", "Delivery", "Personalization", "Budget Friendly"]
    }
}

# SEO & Geo-targeting rules
SEO_CONFIG = {
    "min_word_count": 750,
    "max_word_count": 1200,
    "min_headings": 4,
    "include_faq": True,
    "include_schema": True,
    "internal_links": True,
    "meta_description_length": 155,
    "focus_keywords": True,
    "include_cta": True  # Call-to-action linking to product website
}

# Image generation config for blog cover images
IMAGE_CONFIG = {
    "width": 1200,
    "height": 630,
    "brand_colors": {
        "primary": "#6b3e4a",  # Burgundy
        "accent": "#d4af37",   # Gold
        "secondary": "#e94b7f" # Pink
    },
    "fonts": {
        "title": "bold 48px",
        "subtitle": "normal 24px"
    }
}

# Email and notifications
NOTIFICATIONS = {
    "email_on_publish": True,
    "email_recipients": ["kahpk1933@gmail.com"],
    "slack_notifications": False,
    "gsc_submission": True,  # Auto-submit to Google Search Console
    "track_indexing": True
}

# Schedule configuration
SCHEDULE = {
    "frequency": "daily",  # daily, weekly, or manual
    "time": "10:00",  # 10 AM ET
    "timezone": "America/New_York",
    "posts_per_website_per_day": 1,
    "batch_size": 5  # Process 5 products at a time
}
