#!/usr/bin/env python3
"""
Country Cove Inc — Odoo Multi-Store Full Setup
7 websites + Hub | All correct Country Cove branding and domains
Run: python setup_odoo_stores.py
"""

import xmlrpc.client
import base64
import requests
import sys
import time

# ─── CONFIG ─────────────────────────────────────────────────────────
URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"

# ─── STORE DATA ──────────────────────────────────────────────────────
# Exactly 7 Country Cove websites matching Fiverr deliverables
# Hub (countrycoveli.com) is handled separately at bottom

STORES = {

  # ═══════════════════════════════════════════════════════════════════
  # SITE 1: Sports & Trading Cards
  # countrycovesportscards.com | ships nationwide
  # ═══════════════════════════════════════════════════════════════════
  "sports_and_cards": {
    "website_name": "Country Cove Sports & Cards",
    "domain": "countrycovesportscards.com",
    "categories": {

      "Baseball Cards": [
        {"name": "2011 Topps Update Mike Trout RC #US175",          "price": 299.99, "img": "baseball card rookie"},
        {"name": "1952 Topps Mickey Mantle Reprint #311",           "price": 149.99, "img": "vintage baseball card"},
        {"name": "2001 Topps Ichiro Suzuki Rookie Card",            "price": 89.99,  "img": "baseball trading card"},
        {"name": "2018 Topps Chrome Derek Jeter Refractor",         "price": 59.99,  "img": "baseball card chrome"},
        {"name": "2020 Bowman Chrome Jasson Dominguez Auto",        "price": 199.99, "img": "baseball autograph card"},
        {"name": "1989 Upper Deck Ken Griffey Jr. Rookie #1",       "price": 79.99,  "img": "ken griffey baseball card"},
        {"name": "2022 Topps Gold Label Aaron Judge Class 1",       "price": 45.99,  "img": "gold baseball card"},
        {"name": "2023 Topps Heritage Ronald Acuna Jr.",            "price": 34.99,  "img": "baseball card heritage"},
        {"name": "PSA 9 2016 Topps Corey Seager Rookie",           "price": 119.99, "img": "PSA graded baseball card"},
        {"name": "1987 Topps Barry Bonds Rookie Card #320",         "price": 39.99,  "img": "1980s baseball card"},
        {"name": "2019 Topps Chrome Vladimir Guerrero Jr. RC",      "price": 49.99,  "img": "baseball rookie card"},
        {"name": "1993 SP Derek Jeter Foil Rookie Card",            "price": 189.99, "img": "derek jeter rookie card"},
        {"name": "2021 Topps Finest Shohei Ohtani Refractor",      "price": 74.99,  "img": "ohtani baseball card"},
        {"name": "1969 Topps Reggie Jackson Rookie #260",           "price": 299.99, "img": "vintage 1960s baseball card"},
      ],

      "Basketball Cards": [
        {"name": "2003-04 Topps Chrome LeBron James Rookie RC",    "price": 849.99, "img": "lebron james basketball card"},
        {"name": "2019-20 Panini Prizm Zion Williamson RC",        "price": 249.99, "img": "zion williamson rookie card"},
        {"name": "1986-87 Fleer Michael Jordan Sticker #8",        "price": 599.99, "img": "michael jordan fleer card"},
        {"name": "2009-10 Topps Gold Stephen Curry Rookie",        "price": 399.99, "img": "stephen curry rookie card"},
        {"name": "2012-13 Panini Prizm Anthony Davis RC",          "price": 99.99,  "img": "basketball prizm card"},
        {"name": "2021-22 Panini Select Evan Mobley RC Concourse", "price": 39.99,  "img": "basketball select card"},
        {"name": "2018-19 Panini Prizm Trae Young Silver RC",      "price": 89.99,  "img": "trae young basketball card"},
        {"name": "2020-21 Panini Mosaic LaMelo Ball RC",           "price": 149.99, "img": "basketball mosaic card"},
        {"name": "1992-93 Topps Shaquille O'Neal Rookie #362",     "price": 79.99,  "img": "shaquille oneal rookie"},
        {"name": "1996-97 Topps Chrome Kobe Bryant Rookie",        "price": 799.99, "img": "kobe bryant rookie card"},
        {"name": "2013-14 Panini Prizm Giannis Antetokounmpo RC",  "price": 499.99, "img": "giannis antetokounmpo card"},
        {"name": "2007-08 Topps Kevin Durant Rookie Card",         "price": 299.99, "img": "kevin durant rookie card"},
      ],

      "Football Cards": [
        {"name": "2000 Playoff Contenders Tom Brady Auto RC /100",  "price": 2499.99,"img": "tom brady rookie card"},
        {"name": "2018 Panini Prizm Lamar Jackson Silver RC",       "price": 199.99, "img": "lamar jackson football card"},
        {"name": "2022 Panini Prizm Patrick Mahomes Silver",        "price": 89.99,  "img": "patrick mahomes card"},
        {"name": "2021 Panini Prizm Trevor Lawrence RC Silver",     "price": 79.99,  "img": "football prizm rookie"},
        {"name": "1986 Topps Jerry Rice Rookie Card #161",          "price": 249.99, "img": "jerry rice rookie card"},
        {"name": "2020 Panini Prizm Justin Herbert RC Silver",      "price": 149.99, "img": "justin herbert rookie card"},
        {"name": "2017 Panini Prizm Patrick Mahomes II RC",         "price": 599.99, "img": "mahomes prizm card"},
        {"name": "2023 Panini Prizm CJ Stroud RC Silver",           "price": 89.99,  "img": "nfl rookie card 2023"},
        {"name": "1984 Topps Dan Marino Rookie Card #123",          "price": 199.99, "img": "vintage football card"},
        {"name": "1981 Topps Joe Montana Rookie Card #216",         "price": 349.99, "img": "joe montana card"},
      ],

      "Hockey Cards": [
        {"name": "2005-06 Upper Deck Sidney Crosby Young Guns RC",  "price": 899.99, "img": "sidney crosby rookie card"},
        {"name": "2015-16 Upper Deck Connor McDavid Young Guns",    "price": 499.99, "img": "connor mcdavid rookie"},
        {"name": "1979-80 O-Pee-Chee Wayne Gretzky Rookie #18",    "price": 3999.99,"img": "wayne gretzky rookie card"},
        {"name": "2016-17 Upper Deck Auston Matthews Young Guns",   "price": 299.99, "img": "auston matthews rookie"},
        {"name": "2023-24 Upper Deck Connor Bedard Young Guns",     "price": 199.99, "img": "nhl 2024 rookie card"},
        {"name": "2020-21 Upper Deck Alexis Lafreniere YG RC",      "price": 89.99,  "img": "hockey rookie card 2020"},
        {"name": "2018-19 Upper Deck Rasmus Dahlin Young Guns",     "price": 79.99,  "img": "hockey card upper deck"},
        {"name": "1990-91 Score Jaromir Jagr Rookie #428",          "price": 49.99,  "img": "jaromir jagr rookie"},
      ],

      "Soccer Cards": [
        {"name": "2004 Panini Lionel Messi RC Card",                "price": 1999.99,"img": "lionel messi card"},
        {"name": "2003 Panini Stickers Cristiano Ronaldo RC",       "price": 999.99, "img": "cristiano ronaldo card"},
        {"name": "2022 Topps Chrome Kylian Mbappe Refractor",       "price": 149.99, "img": "kylian mbappe card"},
        {"name": "2020 Panini Prizm Euro Erling Haaland RC",        "price": 199.99, "img": "erling haaland rookie"},
        {"name": "2022 Topps Chrome Jude Bellingham Refractor",     "price": 129.99, "img": "jude bellingham card"},
        {"name": "2022 Panini World Cup Sticker Complete Set",      "price": 299.99, "img": "world cup sticker album"},
      ],

      "Pokémon Cards": [
        {"name": "Pokémon Scarlet & Violet Base Booster Pack",     "price": 4.99,   "img": "pokemon booster pack"},
        {"name": "Pokémon Paldea Evolved Booster Box (36 Packs)",  "price": 139.99, "img": "pokemon booster box"},
        {"name": "Charizard ex Double Rare SV3 #228",              "price": 49.99,  "img": "charizard pokemon card"},
        {"name": "Pikachu VMAX Rainbow Rare #044/185",             "price": 89.99,  "img": "pikachu vmax rainbow"},
        {"name": "Mewtwo V Alt Art #030/189",                      "price": 74.99,  "img": "mewtwo pokemon card"},
        {"name": "Pokémon Elite Trainer Box — Scarlet & Violet",   "price": 49.99,  "img": "pokemon elite trainer box"},
        {"name": "PSA 10 Charizard Base Set Holo 1st Edition",     "price": 9999.99,"img": "charizard 1st edition psa"},
        {"name": "Umbreon VMAX Alternate Art #215/203",            "price": 399.99, "img": "umbreon vmax alt art"},
        {"name": "Tera Charizard ex Special Illustration Rare",    "price": 199.99, "img": "tera charizard illustration"},
        {"name": "Rayquaza VMAX Alternate Art Secret Rare",        "price": 299.99, "img": "rayquaza vmax card"},
        {"name": "Pokémon 151 Booster Bundle (6 Packs)",           "price": 29.99,  "img": "pokemon 151 cards"},
        {"name": "Lugia V Alt Art Alternate Full Art",             "price": 149.99, "img": "lugia pokemon alt art"},
      ],

      "Magic: The Gathering": [
        {"name": "MTG March of the Machine Draft Booster Pack",    "price": 4.99,   "img": "magic the gathering booster"},
        {"name": "MTG Wilds of Eldraine Draft Booster Box",        "price": 109.99, "img": "magic the gathering booster box"},
        {"name": "MTG The Lord of the Rings Collector Booster",    "price": 29.99,  "img": "lord of the rings mtg"},
        {"name": "MTG Bloomburrow Draft Booster Box",              "price": 109.99, "img": "bloomburrow magic card"},
        {"name": "MTG Commander Precon Deck — Eldrazi Unbound",    "price": 44.99,  "img": "magic commander deck"},
        {"name": "Force of Will Alliances #60 (Near Mint)",        "price": 89.99,  "img": "force of will magic card"},
        {"name": "1996-97 Topps Chrome Kobe Bryant Rookie Clone",  "price": 799.99, "img": "magic foil rare card"},
        {"name": "MTG Murders at Karlov Manor Bundle",             "price": 44.99,  "img": "magic bundle cards"},
        {"name": "Sol Ring Commander Legends Foil",                "price": 14.99,  "img": "sol ring magic"},
        {"name": "MTG Arena Starter Kit 2024",                     "price": 9.99,   "img": "magic arena starter"},
      ],

      "Yu-Gi-Oh!": [
        {"name": "Yu-Gi-Oh! Phantom Nightmare Booster Pack",       "price": 4.99,   "img": "yugioh booster pack"},
        {"name": "Blue-Eyes White Dragon LOB 1st Edition",         "price": 299.99, "img": "blue eyes white dragon"},
        {"name": "Dark Magician MRD 1st Edition Holo",             "price": 149.99, "img": "dark magician yugioh"},
        {"name": "Exodia the Forbidden One LOB 1st Edition",       "price": 499.99, "img": "exodia yugioh card"},
        {"name": "Ash Blossom & Joyous Spring MACR Ultra Rare",    "price": 19.99,  "img": "ash blossom yugioh"},
        {"name": "Yu-Gi-Oh! 25th Anniversary Duelist Pack Set",    "price": 34.99,  "img": "yugioh 25th anniversary"},
        {"name": "Red-Eyes Black Dragon 1st Edition LOB",          "price": 189.99, "img": "red eyes black dragon"},
        {"name": "Yu-Gi-Oh! Tin of the Ancient Battles 2023",      "price": 24.99,  "img": "yugioh tin box"},
        {"name": "Yu-Gi-Oh! Structure Deck: Legend of Blue-Eyes",  "price": 19.99,  "img": "yugioh structure deck"},
      ],

      "Dragon Ball & One Piece TCG": [
        {"name": "DBS Fusion World Booster Pack FB01",             "price": 4.99,   "img": "dragon ball super card game"},
        {"name": "Son Goku Ultra Instinct God Rare FB01-001",      "price": 49.99,  "img": "goku ultra instinct card"},
        {"name": "DBS Fusion World Season 2 Booster Box",          "price": 89.99,  "img": "dragon ball fusion world"},
        {"name": "Gohan Beast Awakening Secret Rare",              "price": 59.99,  "img": "gohan beast card"},
        {"name": "DBS Premium Anniversary Box 2024",               "price": 149.99, "img": "dragon ball anniversary box"},
        {"name": "One Piece TCG Romance Dawn Booster Pack OP01",   "price": 4.99,   "img": "one piece card game"},
        {"name": "Monkey D. Luffy Gear 5 Secret Rare OP06",        "price": 149.99, "img": "luffy gear 5 card"},
        {"name": "Shanks Special Parallel Super Rare",             "price": 89.99,  "img": "shanks one piece card"},
        {"name": "Roronoa Zoro Secret Rare OP01-001",              "price": 199.99, "img": "zoro one piece card"},
        {"name": "One Piece TCG Pillars of Strength Booster Box",  "price": 89.99,  "img": "one piece pillars"},
      ],

    }
  },

  # ═══════════════════════════════════════════════════════════════════
  # SITE 2: Gift Baskets
  # countrycovegiftbasket.com | local delivery + shipping
  # ═══════════════════════════════════════════════════════════════════
  "gift_baskets": {
    "website_name": "Country Cove Gift Baskets",
    "domain": "countrycovegiftbasket.com",
    "categories": {

      "Birthday Baskets": [
        {"name": "Birthday Celebration Deluxe Basket",             "price": 79.99,  "img": "birthday gift basket"},
        {"name": "Sweet 16 Birthday Treat Basket",                 "price": 59.99,  "img": "sweet sixteen birthday basket"},
        {"name": "Chocolate Lover's Birthday Basket",              "price": 69.99,  "img": "chocolate gift basket"},
        {"name": "Spa & Pampering Birthday Basket",                "price": 89.99,  "img": "spa gift basket"},
        {"name": "Wine & Cheese Birthday Gourmet Basket",          "price": 99.99,  "img": "wine cheese gift basket"},
        {"name": "Milestone 30th Birthday Gift Basket",            "price": 89.99,  "img": "30th birthday gift"},
        {"name": "Tropical Fruit & Snack Birthday Basket",         "price": 64.99,  "img": "fruit snack basket"},
        {"name": "Birthday Brunch Basket with Pancake Mix & Syrup","price": 54.99,  "img": "brunch gift basket"},
        {"name": "Kids Birthday Fun Basket with Candy & Toys",     "price": 44.99,  "img": "kids birthday gift basket"},
        {"name": "Coffee & Tea Birthday Lover's Basket",           "price": 59.99,  "img": "coffee tea gift basket"},
        {"name": "Party & Celebration Balloon Gift Basket",        "price": 74.99,  "img": "balloon birthday basket"},
        {"name": "Birthday Glow — Self Care & Skincare Basket",    "price": 94.99,  "img": "skincare gift basket"},
        {"name": "Movie Night Birthday Basket with Snacks",        "price": 49.99,  "img": "movie night gift basket"},
        {"name": "Baked Goods & Cookies Birthday Basket",          "price": 54.99,  "img": "cookies baked goods basket"},
        {"name": "Premium 50th Birthday Luxury Gift Basket",       "price": 149.99, "img": "luxury birthday gift"},
      ],

      "Holiday Baskets": [
        {"name": "Christmas Classic Holiday Cookie Basket",        "price": 69.99,  "img": "christmas gift basket"},
        {"name": "Holiday Gourmet Cheese & Charcuterie Basket",    "price": 109.99, "img": "charcuterie gift basket"},
        {"name": "New Year Celebration Champagne & Treats Basket", "price": 129.99, "img": "new year gift basket"},
        {"name": "Thanksgiving Harvest Gourmet Basket",            "price": 89.99,  "img": "thanksgiving gift basket"},
        {"name": "Hanukkah Traditional Gift Basket",               "price": 79.99,  "img": "hanukkah gift basket"},
        {"name": "Christmas Morning Cozy Breakfast Basket",        "price": 74.99,  "img": "christmas morning basket"},
        {"name": "Valentine's Day Chocolate & Rose Basket",        "price": 69.99,  "img": "valentines day gift basket"},
        {"name": "Easter Spring Celebration Basket",               "price": 54.99,  "img": "easter gift basket"},
        {"name": "Mother's Day Spa & Floral Luxury Basket",        "price": 99.99,  "img": "mothers day gift basket"},
        {"name": "Father's Day Beer & Snacks Basket",              "price": 79.99,  "img": "fathers day gift basket"},
        {"name": "St. Patrick's Day Irish Treats Basket",          "price": 54.99,  "img": "st patricks day basket"},
      ],

      "Corporate Baskets": [
        {"name": "Executive Premium Corporate Gift Basket",        "price": 149.99, "img": "corporate gift basket"},
        {"name": "Team Appreciation Snack & Coffee Basket",        "price": 89.99,  "img": "office snack basket"},
        {"name": "Client Thank You Gourmet Food Basket",           "price": 119.99, "img": "gourmet corporate basket"},
        {"name": "Closing the Deal Champagne Celebration Basket",  "price": 179.99, "img": "champagne corporate gift"},
        {"name": "New Office Grand Opening Gift Basket",           "price": 99.99,  "img": "office grand opening gift"},
        {"name": "Employee of the Month Recognition Basket",       "price": 79.99,  "img": "employee recognition gift"},
        {"name": "Holiday Corporate Logo Gift Basket (Branded)",   "price": 199.99, "img": "branded corporate basket"},
        {"name": "Real Estate Agent Closing Gift Basket",          "price": 109.99, "img": "real estate closing gift"},
        {"name": "Work From Home Comfort Essentials Basket",       "price": 94.99,  "img": "work from home gift basket"},
      ],

      "Baby & Newborn Baskets": [
        {"name": "Welcome Baby Boy Newborn Gift Basket",           "price": 79.99,  "img": "baby boy gift basket"},
        {"name": "Welcome Baby Girl Newborn Gift Basket",          "price": 79.99,  "img": "baby girl gift basket"},
        {"name": "Gender Neutral Yellow Duck Baby Basket",         "price": 74.99,  "img": "newborn baby gift basket"},
        {"name": "New Mom Spa & Pampering Basket",                 "price": 99.99,  "img": "new mom gift basket"},
        {"name": "Twin Baby Welcome Gift Basket Set",              "price": 139.99, "img": "twins baby gift"},
        {"name": "Baby Shower Luxury Keepsake Basket",             "price": 119.99, "img": "baby shower gift basket"},
        {"name": "Organic Baby Essentials Gift Basket",            "price": 89.99,  "img": "organic baby gift"},
        {"name": "Baby's First Year Milestone Basket",             "price": 94.99,  "img": "baby milestone gift"},
      ],

      "Get Well & Sympathy": [
        {"name": "Get Well Soon Comfort Care Basket",              "price": 69.99,  "img": "get well gift basket"},
        {"name": "Healing & Recovery Herbal Tea Basket",           "price": 59.99,  "img": "herbal tea gift basket"},
        {"name": "Hospital Stay Comfort & Entertainment Basket",   "price": 79.99,  "img": "hospital gift basket"},
        {"name": "Sympathy Flower & Gourmet Food Basket",          "price": 89.99,  "img": "sympathy gift basket"},
        {"name": "Thinking of You Sweet Treats Basket",            "price": 54.99,  "img": "thinking of you basket"},
        {"name": "Soup & Wellness Recovery Basket",                "price": 64.99,  "img": "soup wellness gift basket"},
        {"name": "Comfort & Warmth Blanket Gift Basket",           "price": 74.99,  "img": "comfort blanket gift basket"},
        {"name": "Grief & Bereavement Sympathy Basket",            "price": 94.99,  "img": "bereavement gift basket"},
        {"name": "Chemo Care Package — Support & Comfort Basket",  "price": 99.99,  "img": "care package basket"},
      ],

    }
  },

  # ═══════════════════════════════════════════════════════════════════
  # SITE 3: Greeting Cards & Gifts (includes digital gift cards)
  # countrycovegreetingcards.com | membership model
  # ═══════════════════════════════════════════════════════════════════
  "greeting_cards": {
    "website_name": "Country Cove Greeting Cards & Gifts",
    "domain": "countrycovegreetingcards.com",
    "categories": {

      "Birthday Cards": [
        {"name": "Funny Birthday Card — 'Age is Just a Number'",   "price": 5.99,   "img": "funny birthday card"},
        {"name": "Luxury Foil Happy Birthday Card",                "price": 7.99,   "img": "luxury birthday greeting card"},
        {"name": "Kids Birthday Card with Activity Page",          "price": 4.99,   "img": "kids birthday card"},
        {"name": "Milestone 40th Birthday Card Gold Foil",         "price": 6.99,   "img": "40th birthday card"},
        {"name": "From the Whole Group Giant Birthday Card",       "price": 8.99,   "img": "giant group birthday card"},
        {"name": "Personalized Photo Birthday Card",               "price": 9.99,   "img": "photo birthday card"},
        {"name": "Floral Watercolor Birthday Card for Her",        "price": 5.99,   "img": "floral birthday card"},
        {"name": "Handmade Pop-Up Cake Birthday Card",             "price": 8.99,   "img": "popup birthday card"},
        {"name": "Musical Birthday Card — Plays Happy Birthday",   "price": 9.99,   "img": "musical birthday card"},
        {"name": "Birthday Card 5-Pack Assortment",                "price": 14.99,  "img": "birthday card multipack"},
      ],

      "Holiday Cards": [
        {"name": "Christmas Family Photo Card 25-Pack",            "price": 29.99,  "img": "christmas photo card"},
        {"name": "Happy Holidays Foil Boxed Card Set 20-Pack",     "price": 24.99,  "img": "holiday card set"},
        {"name": "Funny Christmas Card — Santa Humor",             "price": 5.99,   "img": "funny christmas card"},
        {"name": "Elegant Gold Embossed Christmas Card Set",       "price": 22.99,  "img": "elegant christmas card"},
        {"name": "Happy New Year Greeting Card Gold Foil",         "price": 5.99,   "img": "new year card"},
        {"name": "Valentine's Day Card — Romantic",                "price": 5.99,   "img": "valentines day card"},
        {"name": "Easter Spring Card with Envelope",               "price": 4.99,   "img": "easter greeting card"},
        {"name": "Thanksgiving Card for Family",                   "price": 5.99,   "img": "thanksgiving card"},
        {"name": "Hanukkah Greeting Card Set 10-Pack",             "price": 14.99,  "img": "hanukkah card"},
        {"name": "Halloween Card Set 8-Pack",                      "price": 11.99,  "img": "halloween greeting card"},
      ],

      "Wedding & Anniversary Cards": [
        {"name": "Wedding Congratulations Luxury Card",            "price": 7.99,   "img": "wedding congratulations card"},
        {"name": "Mr. & Mrs. Pop-Up Wedding Card",                 "price": 9.99,   "img": "wedding popup card"},
        {"name": "25th Silver Anniversary Card",                   "price": 6.99,   "img": "silver anniversary card"},
        {"name": "50th Golden Anniversary Card Luxury Foil",       "price": 7.99,   "img": "golden anniversary card"},
        {"name": "Engagement Congratulations Card",                "price": 5.99,   "img": "engagement card"},
        {"name": "Bridal Shower Card Floral",                      "price": 5.99,   "img": "bridal shower card"},
        {"name": "Happy Anniversary Card Romantic",                "price": 5.99,   "img": "anniversary card"},
        {"name": "Personalized Wedding Couple Photo Card",         "price": 9.99,   "img": "wedding photo card"},
      ],

      "Baby & New Parent Cards": [
        {"name": "It's a Boy New Baby Card Blue",                  "price": 5.99,   "img": "baby boy card"},
        {"name": "It's a Girl New Baby Card Pink",                 "price": 5.99,   "img": "baby girl card"},
        {"name": "Gender Neutral Welcome Baby Card",               "price": 5.99,   "img": "new baby greeting card"},
        {"name": "New Mom Congratulations Card",                   "price": 5.99,   "img": "new mom card"},
        {"name": "Baby Shower Luxury Foil Card",                   "price": 6.99,   "img": "baby shower card"},
        {"name": "Twins New Baby Card",                            "price": 6.99,   "img": "twins baby card"},
        {"name": "Welcome to the World Baby Card",                 "price": 5.99,   "img": "welcome baby world card"},
        {"name": "Baby Shower Card 10-Pack",                       "price": 14.99,  "img": "baby shower card pack"},
      ],

      "Sympathy & Get Well Cards": [
        {"name": "With Sympathy Elegant White Lily Card",          "price": 5.99,   "img": "sympathy card white lily"},
        {"name": "Thinking of You Sympathy Card",                  "price": 5.99,   "img": "thinking of you card"},
        {"name": "Get Well Soon Funny Card",                       "price": 5.99,   "img": "get well soon funny card"},
        {"name": "Deepest Condolences Card Gold Foil",             "price": 6.99,   "img": "condolences card"},
        {"name": "In Loving Memory Memorial Card",                 "price": 6.99,   "img": "memorial card"},
        {"name": "Feel Better Soon — Fun Recovery Card",           "price": 5.99,   "img": "feel better card"},
        {"name": "Sympathy Card 8-Pack Assortment",                "price": 12.99,  "img": "sympathy card pack"},
      ],

      "Thank You & Occasion Cards": [
        {"name": "Elegant Gold Foil Thank You Card Set 20-Pack",   "price": 18.99,  "img": "thank you card gold"},
        {"name": "Funny Thank You Card — Humorous",                "price": 5.99,   "img": "funny thank you card"},
        {"name": "Teacher Thank You Card Appreciation",            "price": 5.99,   "img": "teacher thank you card"},
        {"name": "Business Thank You Note Card Set 50-Pack",       "price": 24.99,  "img": "business thank you cards"},
        {"name": "Congratulations General Card Gold Foil",         "price": 5.99,   "img": "congratulations card"},
        {"name": "Good Luck New Job Card",                         "price": 5.99,   "img": "good luck card"},
        {"name": "Retirement Congratulations Funny Card",          "price": 5.99,   "img": "retirement card funny"},
        {"name": "Promotion Congratulations Card",                 "price": 5.99,   "img": "promotion congratulations card"},
      ],

      "Gift Cards — Restaurant": [
        {"name": "Olive Garden $25 Gift Card",                     "price": 25.00,  "img": "restaurant gift card"},
        {"name": "Olive Garden $50 Gift Card",                     "price": 50.00,  "img": "restaurant gift card"},
        {"name": "Applebee's $25 Gift Card",                       "price": 25.00,  "img": "applebees gift card"},
        {"name": "Cheesecake Factory $50 Gift Card",               "price": 50.00,  "img": "cheesecake factory gift card"},
        {"name": "Starbucks $25 Gift Card",                        "price": 25.00,  "img": "starbucks gift card"},
        {"name": "Starbucks $50 Gift Card",                        "price": 50.00,  "img": "starbucks gift card"},
        {"name": "DoorDash $50 Digital Gift Card",                 "price": 50.00,  "img": "food delivery gift card"},
        {"name": "Uber Eats $25 Digital Gift Card",                "price": 25.00,  "img": "uber eats gift card"},
        {"name": "Texas Roadhouse $50 Gift Card",                  "price": 50.00,  "img": "texas roadhouse gift"},
      ],

      "Gift Cards — Shopping & Entertainment": [
        {"name": "Amazon $25 Gift Card",                           "price": 25.00,  "img": "amazon gift card"},
        {"name": "Amazon $50 Gift Card",                           "price": 50.00,  "img": "amazon gift card"},
        {"name": "Amazon $100 Gift Card",                          "price": 100.00, "img": "amazon gift card"},
        {"name": "Target $50 Gift Card",                           "price": 50.00,  "img": "target gift card"},
        {"name": "Visa $50 Prepaid Gift Card",                     "price": 55.95,  "img": "visa prepaid gift card"},
        {"name": "Visa $100 Prepaid Gift Card",                    "price": 105.95, "img": "visa gift card"},
        {"name": "Netflix $25 Digital Gift Card",                  "price": 25.00,  "img": "netflix gift card"},
        {"name": "AMC Theaters $25 Gift Card",                     "price": 25.00,  "img": "movie theater gift card"},
        {"name": "Best Buy $50 Gift Card",                         "price": 50.00,  "img": "best buy gift card"},
        {"name": "Apple iTunes $50 Gift Card",                     "price": 50.00,  "img": "apple gift card"},
      ],

      "Gift Cards — Gaming": [
        {"name": "PlayStation Store $25 Gift Card",                "price": 25.00,  "img": "playstation gift card"},
        {"name": "PlayStation Store $50 Gift Card",                "price": 50.00,  "img": "playstation gift card"},
        {"name": "Xbox $25 Gift Card",                             "price": 25.00,  "img": "xbox gift card"},
        {"name": "Xbox $50 Gift Card",                             "price": 50.00,  "img": "xbox gift card"},
        {"name": "Nintendo eShop $50 Gift Card",                   "price": 50.00,  "img": "nintendo eshop gift card"},
        {"name": "Steam $50 Wallet Gift Card",                     "price": 50.00,  "img": "steam wallet gift card"},
        {"name": "Roblox $25 Gift Card",                           "price": 25.00,  "img": "roblox gift card"},
        {"name": "Fortnite V-Bucks $25 Gift Card",                 "price": 25.00,  "img": "fortnite gift card"},
      ],

    }
  },

  # ═══════════════════════════════════════════════════════════════════
  # SITE 4: Balloons & Decorations
  # countrycoveballoons.com | local delivery Long Island
  # ═══════════════════════════════════════════════════════════════════
  "balloons": {
    "website_name": "Country Cove Balloons & Decorations",
    "domain": "countrycoveballoons.com",
    "categories": {

      "Birthday Balloons": [
        {"name": "Happy Birthday Gold Foil Balloon Bouquet",       "price": 24.99,  "img": "birthday balloon bouquet"},
        {"name": "Rainbow Birthday Balloon Arch Kit",              "price": 39.99,  "img": "birthday balloon arch"},
        {"name": "Giant 36\" Happy Birthday Mylar Balloon",        "price": 14.99,  "img": "giant birthday balloon"},
        {"name": "Number Foil Birthday Balloon Set",               "price": 19.99,  "img": "number birthday balloon"},
        {"name": "Birthday Princess Balloon Bouquet Pink",         "price": 29.99,  "img": "princess birthday balloon"},
        {"name": "Superhero Birthday Balloon Party Pack",          "price": 34.99,  "img": "superhero balloon party"},
        {"name": "Confetti Balloon Pack 50 Birthday Balloons",     "price": 12.99,  "img": "confetti birthday balloon"},
        {"name": "Pastel Birthday Balloon Garland Kit",            "price": 44.99,  "img": "pastel balloon garland"},
        {"name": "Under the Sea Birthday Balloon Bundle",          "price": 29.99,  "img": "under the sea balloon"},
        {"name": "Unicorn Birthday Balloon Centerpiece",           "price": 22.99,  "img": "unicorn balloon"},
        {"name": "Latex Birthday Balloon Assortment 100 Pack",     "price": 16.99,  "img": "latex birthday balloon pack"},
        {"name": "Giant Balloon with Balloons Inside Surprise",    "price": 19.99,  "img": "giant stuffed balloon"},
      ],

      "Wedding & Anniversary Balloons": [
        {"name": "Mr. & Mrs. White Wedding Foil Balloon Set",      "price": 29.99,  "img": "wedding balloon set"},
        {"name": "Wedding Balloon Arch — White & Gold",            "price": 59.99,  "img": "wedding balloon arch"},
        {"name": "Giant Heart Foil Balloon Red 36\"",              "price": 14.99,  "img": "heart balloon wedding"},
        {"name": "Just Married Mylar Balloon Bouquet",             "price": 24.99,  "img": "just married balloon"},
        {"name": "Rose Gold Anniversary Balloon Garland Kit",      "price": 49.99,  "img": "rose gold balloon garland"},
        {"name": "25th Silver Anniversary Foil Balloons",          "price": 19.99,  "img": "silver anniversary balloon"},
        {"name": "50th Golden Anniversary Balloon Set",            "price": 22.99,  "img": "golden anniversary balloon"},
        {"name": "Engagement Congratulations Foil Balloon",        "price": 12.99,  "img": "engagement balloon"},
        {"name": "Love Heart Balloon Cluster Bouquet",             "price": 27.99,  "img": "love heart balloon"},
      ],

      "Baby Shower Balloons": [
        {"name": "It's a Boy Blue Baby Shower Balloon Set",        "price": 24.99,  "img": "baby shower balloon boy"},
        {"name": "It's a Girl Pink Baby Shower Balloon Set",       "price": 24.99,  "img": "baby shower balloon girl"},
        {"name": "Gender Reveal Confetti Pop Balloon",             "price": 14.99,  "img": "gender reveal balloon"},
        {"name": "Baby Shower Balloon Garland Kit Pastel",         "price": 44.99,  "img": "baby shower balloon garland"},
        {"name": "Oh Baby Foil Letter Balloon Set",                "price": 19.99,  "img": "oh baby balloon"},
        {"name": "Elephant Theme Baby Shower Balloons",            "price": 29.99,  "img": "elephant baby shower balloon"},
        {"name": "Gender Reveal Party Balloon Arch Kit",           "price": 54.99,  "img": "gender reveal arch"},
        {"name": "Baby Feet Foil Balloon Set",                     "price": 12.99,  "img": "baby feet balloon"},
        {"name": "Safari Baby Shower Balloon Pack",                "price": 19.99,  "img": "safari baby shower balloon"},
      ],

      "Holiday Balloons": [
        {"name": "Christmas Santa Foil Balloon Set",               "price": 22.99,  "img": "christmas balloon decoration"},
        {"name": "Christmas Balloon Arch Red & Green Kit",         "price": 44.99,  "img": "christmas balloon arch"},
        {"name": "Happy New Year Gold Foil Balloon Bundle",        "price": 24.99,  "img": "new year balloon"},
        {"name": "Halloween Spider Web Balloon Set",               "price": 19.99,  "img": "halloween balloon"},
        {"name": "Easter Bunny Pastel Balloon Pack",               "price": 17.99,  "img": "easter balloon"},
        {"name": "Independence Day Red White Blue Balloon Set",    "price": 19.99,  "img": "4th of july balloon"},
        {"name": "Valentine's Heart Balloon Bouquet",              "price": 22.99,  "img": "valentines day balloon"},
        {"name": "Mother's Day Floral Balloon Bouquet",            "price": 22.99,  "img": "mothers day balloon"},
        {"name": "Father's Day Blue & Gold Balloon Set",           "price": 19.99,  "img": "fathers day balloon"},
      ],

      "Graduation Balloons": [
        {"name": "Congratulations Grad Gold Balloon Set",          "price": 24.99,  "img": "graduation balloon"},
        {"name": "Class of 2025 Foil Graduation Balloon",          "price": 14.99,  "img": "class of 2025 balloon"},
        {"name": "Graduation Cap Foil Balloon Large",              "price": 12.99,  "img": "graduation cap balloon"},
        {"name": "Graduation Balloon Arch Kit Black & Gold",       "price": 49.99,  "img": "graduation arch balloon"},
        {"name": "You Did It! Grad Balloon Bouquet",               "price": 29.99,  "img": "graduation bouquet balloon"},
        {"name": "Tassel Worth the Hassle Foil Balloon",           "price": 11.99,  "img": "tassel graduation balloon"},
        {"name": "Diploma Foil Balloon & Bouquet Set",             "price": 27.99,  "img": "diploma graduation balloon"},
        {"name": "High School Graduation Balloon Centerpiece",     "price": 32.99,  "img": "high school graduation balloon"},
      ],

      "Party Decorations": [
        {"name": "Balloon Pump Electric — Fast Inflate",           "price": 29.99,  "img": "electric balloon pump"},
        {"name": "Balloon Weights Set of 12",                      "price": 9.99,   "img": "balloon weights"},
        {"name": "Ribbon & Curling Ribbon 10-Color Pack",          "price": 7.99,   "img": "curling ribbon balloons"},
        {"name": "Balloon Arch Strip Kit 40ft",                    "price": 12.99,  "img": "balloon arch strip"},
        {"name": "Helium Balloon Time Tank (50 balloons)",         "price": 44.99,  "img": "helium balloon tank"},
        {"name": "Confetti Cannons Party Poppers Set of 12",       "price": 14.99,  "img": "confetti cannon party"},
        {"name": "Metallic Fringe Curtain Backdrop",               "price": 11.99,  "img": "fringe curtain backdrop"},
        {"name": "Round Foil Balloon Assortment 18\" (12 Pack)",   "price": 19.99,  "img": "foil balloon assortment"},
      ],

    }
  },

  # ═══════════════════════════════════════════════════════════════════
  # SITE 5: Cigars, Tobacco & Vape — 21+ AGE GATE REQUIRED
  # countrycovecigars.com | age-verified e-commerce
  # ═══════════════════════════════════════════════════════════════════
  "cigars": {
    "website_name": "Country Cove Cigars & Smoke",
    "domain": "countrycovecigars.com",
    "categories": {

      "Premium Cigars": [
        {"name": "Romeo y Julieta Churchill Natural (Box of 25)",   "price": 199.99, "img": "romeo julieta cigars"},
        {"name": "Arturo Fuente Hemingway Short Story (5-Pack)",    "price": 54.99,  "img": "arturo fuente cigars"},
        {"name": "Cohiba Signature Series Toro (3-Pack)",           "price": 89.99,  "img": "cohiba cigars"},
        {"name": "Macanudo Cafe Hyde Park (Box of 25)",             "price": 149.99, "img": "macanudo cigars"},
        {"name": "Padron 1964 Anniversary Maduro Corona (5-Pack)",  "price": 79.99,  "img": "padron anniversary cigar"},
        {"name": "Montecristo White Series Toro (5-Pack)",          "price": 49.99,  "img": "montecristo cigar"},
        {"name": "Rocky Patel Vintage 1999 Churchill (5-Pack)",     "price": 59.99,  "img": "rocky patel vintage cigar"},
        {"name": "Oliva Serie V Melanio Figurado (5-Pack)",         "price": 64.99,  "img": "oliva serie v cigar"},
        {"name": "Perdomo Habano Bourbon Barrel Aged Toro (5-Pack)","price": 44.99,  "img": "perdomo bourbon cigar"},
        {"name": "My Father Cigars Le Bijou 1922 Toro (5-Pack)",    "price": 74.99,  "img": "my father cigar"},
        {"name": "Drew Estate Liga Privada No. 9 Toro (5-Pack)",    "price": 69.99,  "img": "liga privada cigar"},
        {"name": "CAO Flavours Bella Vanilla (5-Pack)",             "price": 29.99,  "img": "flavored cigar"},
        {"name": "Davidoff Grand Cru No. 2 (5-Pack)",               "price": 119.99, "img": "davidoff cigar"},
        {"name": "H. Upmann 1844 Classic Toro (Box of 25)",         "price": 179.99, "img": "upmann classic cigar"},
        {"name": "Nub Cameroon 460 by Oliva (5-Pack)",              "price": 39.99,  "img": "nub cigar short fat"},
      ],

      "Pipe Tobacco": [
        {"name": "Captain Black Gold Pipe Tobacco 1.5oz Pouch",    "price": 12.99,  "img": "captain black pipe tobacco"},
        {"name": "Prince Albert Classic Pipe Tobacco 1.5oz",       "price": 9.99,   "img": "prince albert tobacco"},
        {"name": "Sutliff Mixture No. 79 Pipe Tobacco 1.5oz",      "price": 11.99,  "img": "pipe tobacco pouch"},
        {"name": "Mac Baren HH Old Dark Fired Pipe Tobacco",        "price": 14.99,  "img": "mac baren pipe tobacco"},
        {"name": "McClelland Christmas Cheer Pipe Tobacco 4oz",     "price": 24.99,  "img": "christmas pipe tobacco"},
        {"name": "Dunhill My Mixture 965 Pipe Tobacco 50g",         "price": 19.99,  "img": "dunhill pipe tobacco"},
        {"name": "Corncob Missouri Meerschaum Pipe — Classic",      "price": 12.99,  "img": "corncob pipe"},
        {"name": "Briar Pipe — Bent Bulldog Smooth Finish",         "price": 49.99,  "img": "briar pipe tobacco pipe"},
        {"name": "Pipe Cleaning Kit — 100 Pipe Cleaners + Tamper",  "price": 9.99,   "img": "pipe cleaning kit"},
      ],

      "Vape & E-Cigarettes": [
        {"name": "Elf Bar BC5000 Disposable Vape — Blue Razz Ice",  "price": 17.99,  "img": "elf bar disposable vape"},
        {"name": "Elf Bar BC5000 Disposable — Watermelon Ice",      "price": 17.99,  "img": "watermelon vape disposable"},
        {"name": "Lost Mary MO5000 Disposable — Peach Mango",       "price": 18.99,  "img": "lost mary vape disposable"},
        {"name": "Geek Bar Pulse 15000 — Strawberry Banana",        "price": 22.99,  "img": "geek bar pulse vape"},
        {"name": "Vuse Alto Pods 2-Pack — Menthol",                 "price": 15.99,  "img": "vuse alto vape pods"},
        {"name": "JUUL 2 Device Starter Kit",                       "price": 34.99,  "img": "juul vape device"},
        {"name": "Vaporesso Xros 3 Pod System Kit",                 "price": 29.99,  "img": "vaporesso pod system"},
        {"name": "SMOK Nord 5 Pod System Kit",                      "price": 44.99,  "img": "smok nord pod kit"},
        {"name": "Naked 100 Vape Juice — Amazing Mango 60ml",       "price": 21.99,  "img": "naked 100 vape juice"},
        {"name": "Cuttwood Boss Reserve E-Liquid 60ml",             "price": 19.99,  "img": "premium vape juice"},
        {"name": "VaporFi Grand Reserve 60ml — Strawberry Fields",  "price": 24.99,  "img": "vape eliquid bottle"},
        {"name": "Hyde Rebel Pro 5000 Puffs — Grape Ice",           "price": 19.99,  "img": "hyde rebel vape"},
      ],

      "Lighters & Accessories": [
        {"name": "Xikar HP4 Quad Torch Lighter — Black",           "price": 79.99,  "img": "xikar torch lighter"},
        {"name": "Vector Nitro Triple Flame Torch Lighter",         "price": 49.99,  "img": "vector torch lighter"},
        {"name": "Colibri Julius Single Soft Flame Lighter",        "price": 39.99,  "img": "colibri cigar lighter"},
        {"name": "Zippo Classic Chrome Windproof Lighter",          "price": 24.99,  "img": "zippo lighter"},
        {"name": "Vertigo Cyclone Triple Torch Lighter — Blue",     "price": 29.99,  "img": "cyclone torch lighter"},
        {"name": "Colibri Quasar Quadruple Jet Lighter",            "price": 59.99,  "img": "colibri quad flame lighter"},
        {"name": "Xikar XO Double Guillotine Cutter — Black",       "price": 49.99,  "img": "xikar cigar cutter"},
        {"name": "Colibri Julius V-Cut Cigar Cutter",               "price": 34.99,  "img": "v-cut cigar cutter"},
        {"name": "Boveda 72% RH Humidity Pack 2-Way 5-Pack",        "price": 12.99,  "img": "boveda humidity pack cigar"},
        {"name": "Craftsman's Bench 50-Cigar Travel Humidor",       "price": 89.99,  "img": "cigar humidor travel"},
        {"name": "Quality Importers Desktop Humidor — 100 Cigars",  "price": 149.99, "img": "desktop humidor cigars"},
        {"name": "Ashton 8-Cigar Sampler Gift Set",                 "price": 79.99,  "img": "cigar gift sampler"},
      ],

    }
  },

  # ═══════════════════════════════════════════════════════════════════
  # SITE 6: Lotto — Informational / Referral (no tickets sold)
  # countrycovelotto.com | NY Lottery info and referral
  # ═══════════════════════════════════════════════════════════════════
  "lotto": {
    "website_name": "Country Cove Lotto",
    "domain": "countrycovelotto.com",
    "categories": {

      "New York Lottery Games — Info": [
        {"name": "Powerball — How to Play Guide",                  "price": 0.00,   "img": "powerball lottery ticket"},
        {"name": "Mega Millions — Jackpot Info & Odds",            "price": 0.00,   "img": "mega millions lottery"},
        {"name": "NY Lotto — Pick Your Numbers Guide",             "price": 0.00,   "img": "new york lottery game"},
        {"name": "Cash4Life — Win $1,000/Day for Life Info",       "price": 0.00,   "img": "cash4life lottery ny"},
        {"name": "Take 5 — NY Daily Draw Game Guide",              "price": 0.00,   "img": "take5 ny lottery"},
        {"name": "Numbers & Win 4 — Daily Games Info",             "price": 0.00,   "img": "numbers lottery ticket"},
        {"name": "Quick Draw — Keno Style Game Info",              "price": 0.00,   "img": "quick draw keno lottery"},
        {"name": "Pick 10 — NY Lottery Pick 10 Guide",            "price": 0.00,   "img": "pick 10 lottery ny"},
      ],

      "Scratch-Off Tickets — Available In Store": [
        {"name": "$1 Scratch-Off — In Store Only",                 "price": 1.00,   "img": "scratch off lottery ticket"},
        {"name": "$2 Scratch-Off — In Store Only",                 "price": 2.00,   "img": "scratch off ticket winner"},
        {"name": "$5 Scratch-Off — In Store Only",                 "price": 5.00,   "img": "5 dollar scratch ticket"},
        {"name": "$10 Scratch-Off — In Store Only",                "price": 10.00,  "img": "10 dollar scratch lottery"},
        {"name": "$20 Scratch-Off Premium — In Store Only",        "price": 20.00,  "img": "premium scratch off ticket"},
        {"name": "$30 Scratch-Off Jackpot — In Store Only",        "price": 30.00,  "img": "jackpot scratch off lottery"},
        {"name": "Holiday Scratch-Off Gift Set — 5 Tickets",       "price": 15.00,  "img": "holiday lottery scratch ticket"},
        {"name": "Birthday Lottery Ticket Gift Pack — 10 Mix",     "price": 25.00,  "img": "birthday lottery gift"},
      ],

      "Lucky Lottery Accessories": [
        {"name": "Lucky Scratch-Off Coin Tool 10-Pack",            "price": 3.99,   "img": "scratch off coin tool"},
        {"name": "Lottery Quick Pick Checklist Pad",               "price": 4.99,   "img": "lottery checklist pad"},
        {"name": "Lucky Numbers Journal — Track Your Picks",       "price": 9.99,   "img": "lottery journal notebook"},
        {"name": "NYS Lottery Official Ticket Holder & Organizer", "price": 7.99,   "img": "lottery ticket holder"},
        {"name": "\"Lucky You\" Lottery Gift Bag Set",             "price": 12.99,  "img": "lottery gift bag set"},
      ],

    }
  },

  # ═══════════════════════════════════════════════════════════════════
  # SITE 7: Document Services
  # countrycoveprintservices.com | print, copy, fax, notary, shipping
  # ═══════════════════════════════════════════════════════════════════
  "document_services": {
    "website_name": "Country Cove Print & Copy",
    "domain": "countrycoveprintservices.com",
    "categories": {

      "Print Services": [
        {"name": "Black & White Print — Per Page",                 "price": 0.15,   "img": "black white document printing"},
        {"name": "Color Print — Per Page",                         "price": 0.79,   "img": "color document printing"},
        {"name": "Photo Print 4x6 (Glossy)",                       "price": 0.39,   "img": "photo printing 4x6"},
        {"name": "Photo Print 5x7 (Glossy)",                       "price": 1.29,   "img": "photo printing 5x7"},
        {"name": "Photo Print 8x10 (Glossy)",                      "price": 2.99,   "img": "photo printing 8x10"},
        {"name": "Poster Print 11x17 Color",                       "price": 3.99,   "img": "poster printing 11x17"},
        {"name": "Poster Print 18x24 Large Format",                "price": 14.99,  "img": "large format poster print"},
        {"name": "Business Cards — 250 Count (2-Sided Color)",     "price": 29.99,  "img": "business cards printing"},
        {"name": "Flyer Printing 50-Pack (8.5x11 Full Color)",     "price": 24.99,  "img": "flyer printing service"},
        {"name": "Brochure Printing Tri-Fold 50-Pack",             "price": 39.99,  "img": "brochure printing"},
        {"name": "Resume Printing — Single Page Professional",     "price": 1.99,   "img": "resume printing"},
        {"name": "Booklet Printing 8-Page Saddle Stitch 25-Pack",  "price": 49.99,  "img": "booklet printing service"},
      ],

      "Copy Services": [
        {"name": "Self-Serve B&W Copy — Per Page",                 "price": 0.10,   "img": "copy machine black white"},
        {"name": "Self-Serve Color Copy — Per Page",               "price": 0.69,   "img": "color copy machine"},
        {"name": "Bulk Copies B&W — 100 Pages",                    "price": 7.99,   "img": "bulk copying document"},
        {"name": "Bulk Copies Color — 50 Pages",                   "price": 24.99,  "img": "color bulk copy service"},
        {"name": "Double-Sided Copy — Per Sheet",                  "price": 0.20,   "img": "double sided copy"},
        {"name": "Legal Size Copy 8.5x14 — Per Page",              "price": 0.25,   "img": "legal size document copy"},
        {"name": "11x17 Tabloid Copy — Per Page",                  "price": 0.50,   "img": "tabloid size copy"},
      ],

      "Binding & Finishing": [
        {"name": "Spiral / Coil Binding — Per Document",           "price": 3.99,   "img": "spiral binding document"},
        {"name": "Comb Binding — Per Document",                    "price": 2.99,   "img": "comb binding"},
        {"name": "Lamination — Letter Size Per Sheet",             "price": 1.99,   "img": "document lamination"},
        {"name": "Lamination — Business Card Per Card",            "price": 0.75,   "img": "business card lamination"},
        {"name": "Stapling — Per Document",                        "price": 0.25,   "img": "document stapling"},
        {"name": "Hole Punching — Per Document",                   "price": 0.25,   "img": "hole punch document"},
        {"name": "Folding Service — Per Sheet",                    "price": 0.15,   "img": "document folding service"},
        {"name": "Cutting / Trimming — Per Document",              "price": 0.50,   "img": "paper trimming cutting"},
        {"name": "Hard Cover Binding — Per Document",              "price": 14.99,  "img": "hard cover book binding"},
      ],

      "Fax & Scan Services": [
        {"name": "Fax — First Page (USA Domestic)",                "price": 1.99,   "img": "fax machine document"},
        {"name": "Fax — Additional Pages (USA Domestic)",          "price": 0.99,   "img": "fax document service"},
        {"name": "International Fax — Per Page",                   "price": 3.99,   "img": "international fax service"},
        {"name": "Scan to Email — Per Page",                       "price": 0.25,   "img": "scan to email document"},
        {"name": "Scan to USB — Per Page",                         "price": 0.50,   "img": "scan to usb drive"},
        {"name": "Receive Fax — Per Page",                         "price": 0.50,   "img": "receive fax service"},
        {"name": "Scan — High Resolution 600 DPI Per Page",        "price": 0.75,   "img": "high resolution scanning"},
      ],

      "Notary & Legal Services": [
        {"name": "Notary Service — Per Signature/Stamp",           "price": 2.00,   "img": "notary service stamp"},
        {"name": "Notary — Multiple Signatures Same Document",     "price": 5.00,   "img": "notary public document"},
        {"name": "Document Witnessing Service",                    "price": 5.00,   "img": "document witness service"},
        {"name": "Certified True Copy — Per Document",             "price": 5.00,   "img": "certified copy document"},
        {"name": "Fingerprinting Service — Per Set",               "price": 15.00,  "img": "fingerprinting service"},
        {"name": "Apostille Preparation Assistance",               "price": 25.00,  "img": "apostille document service"},
      ],

      "Shipping & Mailbox Services": [
        {"name": "UPS Shipping Drop-Off — Label Required",         "price": 2.99,   "img": "ups shipping drop off"},
        {"name": "FedEx Drop-Off Service — Label Required",        "price": 2.99,   "img": "fedex drop off package"},
        {"name": "USPS Mailing & Postage — Assistance Fee",        "price": 1.99,   "img": "usps mailing service"},
        {"name": "Package Packaging & Wrapping Service",           "price": 4.99,   "img": "package wrapping service"},
        {"name": "Mailbox Rental — Monthly",                       "price": 19.99,  "img": "mailbox rental service"},
        {"name": "Package Receiving & Holding — Per Package",      "price": 3.99,   "img": "package receiving holding"},
        {"name": "Certified Mail Assistance (USPS)",               "price": 4.99,   "img": "certified mail usps"},
      ],

    }
  },

}

# ─── HELPERS ────────────────────────────────────────────────────────

def fetch_image_b64(keyword):
    try:
        url = f"https://loremflickr.com/400/400/{keyword.replace(' ', ',')}"
        r = requests.get(url, timeout=15, allow_redirects=True)
        if r.status_code == 200 and len(r.content) > 1000:
            return base64.b64encode(r.content).decode('utf-8')
    except Exception as e:
        print(f"      Image fetch failed ({keyword}): {e}")
    return None

def get_or_create_categ(models, uid, name, parent_id=None):
    domain = [('name', '=', name)]
    if parent_id:
        domain.append(('parent_id', '=', parent_id))
    existing = models.execute_kw(DB, uid, PASS, 'product.category', 'search', [domain])
    if existing:
        return existing[0]
    vals = {'name': name}
    if parent_id:
        vals['parent_id'] = parent_id
    return models.execute_kw(DB, uid, PASS, 'product.category', 'create', [vals])

def get_or_create_website(models, uid, name, domain_name):
    # Normalize domain — try with and without https://
    domain_bare = domain_name.replace('https://', '').replace('http://', '')
    domain_full = f'https://{domain_bare}'

    # Search by domain first (most reliable, handles name mismatches)
    for d in [domain_full, domain_bare]:
        existing = models.execute_kw(DB, uid, PASS, 'website', 'search_read',
            [[('domain', '=', d)]], {'fields': ['id', 'name']})
        if existing:
            print(f"  Website '{existing[0]['name']}' found by domain (ID {existing[0]['id']}) — using it")
            return existing[0]['id']

    # Fallback: search by name
    existing = models.execute_kw(DB, uid, PASS, 'website', 'search_read',
        [[('name', '=', name)]], {'fields': ['id']})
    if existing:
        print(f"  Website '{name}' found by name (ID {existing[0]['id']}) — using it")
        return existing[0]['id']

    wid = models.execute_kw(DB, uid, PASS, 'website', 'create',
        [{'name': name, 'domain': domain_full}])
    print(f"  Created website '{name}' (ID {wid})")
    return wid

def remove_old_website(models, uid, old_name):
    """Remove legacy/wrong websites by name."""
    existing = models.execute_kw(DB, uid, PASS, 'website', 'search_read',
        [[('name', 'like', old_name)]], {'fields': ['id', 'name']})
    for site in existing:
        try:
            models.execute_kw(DB, uid, PASS, 'website', 'unlink', [[site['id']]])
            print(f"  Removed old website: '{site['name']}' (ID {site['id']})")
        except Exception as e:
            print(f"  Could not remove '{site['name']}': {e} — archive instead")
            try:
                models.execute_kw(DB, uid, PASS, 'website', 'write',
                    [[site['id']], {'active': False}])
                print(f"  Archived '{site['name']}'")
            except:
                pass

def create_product(models, uid, name, price, categ_id, img_keyword, website_id=None):
    print(f"      + {name[:60]}")
    img = fetch_image_b64(img_keyword)
    vals = {
        'name': name,
        'list_price': price,
        'categ_id': categ_id,
        'type': 'service',
        'sale_ok': True,
    }
    if img:
        vals['image_1920'] = img
    pid = models.execute_kw(DB, uid, PASS, 'product.template', 'create', [vals])
    if website_id and pid:
        try:
            models.execute_kw(DB, uid, PASS, 'product.template', 'write',
                [[pid], {'website_id': website_id, 'is_published': True}])
        except Exception:
            pass
    return pid

def setup_hub(models, uid):
    """Ensure the hub website exists with the correct name."""
    hub_names = ['Country Cove LI', 'Long Island Convenience', 'Country Cove Hub']
    for name in hub_names:
        existing = models.execute_kw(DB, uid, PASS, 'website', 'search_read',
            [[('name', '=', name)]], {'fields': ['id', 'name']})
        if existing:
            print(f"  Hub found: '{existing[0]['name']}' (ID {existing[0]['id']})")
            return existing[0]['id']
    # Not found — create it
    wid = models.execute_kw(DB, uid, PASS, 'website', 'create',
        [{'name': 'Country Cove LI', 'domain': 'countrycoveli.com'}])
    print(f"  Hub created: 'Country Cove LI' (ID {wid})")
    return wid

# ─── MAIN ────────────────────────────────────────────────────────────

def main():
    print("\n" + "="*60)
    print("  Country Cove Inc — Full 7-Store Setup")
    print("  All correct Country Cove branding + domains")
    print("="*60 + "\n")

    common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
    uid = common.authenticate(DB, USER, PASS, {})
    if not uid:
        print("FAILED: Authentication failed. Check credentials.")
        sys.exit(1)
    print(f"Connected as UID {uid}\n")
    models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')

    # ── Step 0: Skip cleanup — correct websites already in place ──
    print("\n[0] Skipping cleanup — websites already correct.")

    # ── Step 1: Ensure hub exists ─────────────────────────────────
    print("\n[1] Setting up Hub website (countrycoveli.com)...")
    setup_hub(models, uid)

    # ── Step 2: Create all 7 stores with products ─────────────────
    total_created = 0

    for store_key, store in STORES.items():
        print(f"\n{'-'*60}")
        print(f"  STORE [{store_key.upper()}]: {store['website_name']}")
        print(f"  Domain: {store['domain']}")
        print(f"{'-'*60}")

        wid = get_or_create_website(models, uid, store['website_name'], store['domain'])
        root_categ_id = get_or_create_categ(models, uid, store['website_name'])

        store_count = 0
        for categ_name, products in store['categories'].items():
            print(f"\n  [Category] {categ_name} ({len(products)} products)")
            categ_id = get_or_create_categ(models, uid, categ_name, root_categ_id)

            for p in products:
                try:
                    create_product(models, uid, p['name'], p['price'], categ_id, p['img'], wid)
                    store_count += 1
                    total_created += 1
                    time.sleep(0.2)
                except Exception as e:
                    print(f"      FAILED: {p['name'][:50]} — {e}")

        print(f"\n  DONE: {store['website_name']}: {store_count} products created")

    print(f"\n{'='*60}")
    print(f"  COMPLETE")
    print(f"  Total products: {total_created} across {len(STORES)} stores")
    print(f"\n  Websites created:")
    for s in STORES.values():
        print(f"    * {s['website_name']} ({s['domain']})")
    print(f"\n  NOTE: Cigars site (countrycovecigars.com) requires")
    print(f"        a 21+ age gate — add HTML/JS via Website Editor")
    print(f"        after this script completes.")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
