"""
Configuration for all 7 Hiren Kumar websites.
Defines niches, search queries, product categories, and output folders.
"""

BASE_OUTPUT = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\ScrappedMaterial"

WEBSITES = {
    "LongIslandConvenience": {
        "domain": "longislandconvenience.com",
        "business_name": "Long Island Convenience",
        "niche": "convenience store",
        "location": "Long Island NY",
        "search_queries": [
            "convenience store Long Island NY",
            "bodega grocery delivery Nassau County NY",
            "convenience store snacks beverages Long Island",
            "24 hour store Long Island NY",
        ],
        "known_competitors": [
            "7-eleven.com",
            "quickchek.com",
        ],
        "product_categories": [
            "Snacks & Chips",
            "Beverages & Drinks",
            "Dairy & Eggs",
            "Frozen Foods",
            "Household Items",
            "Tobacco & Vape",
            "Candy & Sweets",
            "Personal Care",
        ],
        "price_range": {"min": 0.99, "max": 25.00},
        "folder": "01_LongIslandConvenience",
    },

    "LongIslandBalloons": {
        "domain": "longislandballoonsdecor.com",
        "business_name": "Long Island Balloons Decor",
        "niche": "balloon decorations party",
        "location": "Long Island NY",
        "search_queries": [
            "balloon decorations Long Island NY",
            "balloon artist party decorator Nassau Suffolk NY",
            "balloon delivery arrangements Long Island",
            "birthday balloon bouquet Long Island NY",
        ],
        "known_competitors": [],
        "product_categories": [
            "Balloon Bouquets",
            "Birthday Packages",
            "Wedding Decorations",
            "Corporate Events",
            "Baby Shower",
            "Gender Reveal",
            "Arch & Garland",
            "Character Balloons",
        ],
        "price_range": {"min": 25.00, "max": 500.00},
        "folder": "02_LongIslandBalloons",
    },

    "LIGiftBasket": {
        "domain": "ligiftbasket.com",
        "business_name": "LI Gift Basket",
        "niche": "gift basket delivery",
        "location": "Long Island NY",
        "search_queries": [
            "gift basket delivery Long Island NY",
            "custom gift baskets Nassau County NY",
            "gift basket shop Suffolk County NY",
            "corporate gift baskets Long Island",
        ],
        "known_competitors": [
            "1800flowers.com",
            "giftbaskets.com",
        ],
        "product_categories": [
            "Food & Gourmet Baskets",
            "Wine & Cheese Baskets",
            "Spa & Relaxation",
            "Baby & New Mom",
            "Sympathy & Condolence",
            "Corporate Gifts",
            "Holiday Baskets",
            "Get Well Baskets",
        ],
        "price_range": {"min": 35.00, "max": 300.00},
        "folder": "03_LIGiftBasket",
    },

    "LongIslandPrintMail": {
        "domain": "longislandprintandmail.org",
        "business_name": "Long Island Print & Mail",
        "niche": "printing mailing services",
        "location": "Long Island NY",
        "search_queries": [
            "printing services Long Island NY",
            "print shop Nassau County NY",
            "business cards flyers printing Plainview NY",
            "banner sign printing Long Island",
        ],
        "known_competitors": [
            "fedex.com/en-us/office.html",
            "theupsstore.com",
        ],
        "product_categories": [
            "Business Cards",
            "Flyers & Leaflets",
            "Banners & Signs",
            "Postcards",
            "Brochures",
            "T-Shirt Printing",
            "Mailing Services",
            "Copying & Scanning",
        ],
        "price_range": {"min": 9.99, "max": 500.00},
        "folder": "04_LongIslandPrintMail",
    },

    "LongIslandCards": {
        "domain": "longislandcard.com",
        "business_name": "Long Island Card",
        "niche": "sports cards collectibles greeting cards",
        "location": "Long Island NY",
        "search_queries": [
            "sports cards shop Long Island NY",
            "trading cards collectibles Nassau County NY",
            "sports card store near me Long Island",
            "greeting cards gift shop Long Island NY",
        ],
        "known_competitors": [],
        "product_categories": [
            "Graded Sports Cards (PSA/BGS)",
            "Raw Singles",
            "Hobby Boxes",
            "Blaster Boxes",
            "Greeting Cards",
            "Memorabilia",
            "Rookie Cards",
            "Vintage Cards",
        ],
        "price_range": {"min": 1.00, "max": 500.00},
        "folder": "05_LongIslandCards",
    },

    "HirenKumar": {
        "domain": "hirenkumar.us",
        "business_name": "Hiren Kumar Advisory",
        "niche": "financial advisor business consultant",
        "location": "Plainview Long Island NY",
        "search_queries": [
            "financial advisor Plainview NY",
            "business consultant Long Island NY",
            "tax advisor CPA Nassau County NY",
            "investment advisor Long Island",
        ],
        "known_competitors": [],
        "product_categories": [
            "Financial Planning",
            "Tax Preparation",
            "Business Consulting",
            "Investment Advisory",
            "Retirement Planning",
            "Estate Planning",
        ],
        "price_range": {"min": 150.00, "max": 5000.00},
        "folder": "06_HirenKumar",
    },

    "ConsultCyber": {
        "domain": "consultcyber.net",
        "business_name": "Consult Cyber",
        "niche": "cybersecurity IT consulting managed services",
        "location": "Long Island NY",
        "search_queries": [
            "cybersecurity consulting Long Island NY",
            "IT managed services Nassau County NY",
            "cyber security company Plainview NY",
            "IT support small business Long Island",
        ],
        "known_competitors": [],
        "product_categories": [
            "Cybersecurity Assessment",
            "Managed IT Services",
            "Network Security",
            "Cloud Services",
            "Data Backup & Recovery",
            "Compliance (HIPAA/PCI)",
            "IT Support & Helpdesk",
            "VoIP & Communications",
        ],
        "price_range": {"min": 99.00, "max": 10000.00},
        "folder": "07_ConsultCyber",
    },
}

# How many competitors to find per website
TOP_N_COMPETITORS = 10

# Request headers to mimic a real browser
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# Delays between requests (seconds) to avoid rate limiting
DELAY_BETWEEN_REQUESTS = 2.0
DELAY_BETWEEN_SITES = 5.0

# Max products to scrape per competitor
MAX_PRODUCTS_PER_COMPETITOR = 20

# Max images to download per competitor
MAX_IMAGES_PER_COMPETITOR = 15

# Image quality settings
IMAGE_MAX_SIZE = (800, 800)
