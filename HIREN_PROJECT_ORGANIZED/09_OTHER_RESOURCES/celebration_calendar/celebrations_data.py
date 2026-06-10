"""
365-Day Celebration Calendar for Long Island, Plainview, NY USA
All days that matter for a gift basket & balloon business.
Each entry includes category, offer template, and email/WhatsApp copy.
"""

from datetime import date
from typing import List, Dict

# ─────────────────────────────────────────────────────────────────────────────
# FIXED-DATE celebrations (same date every year)
# ─────────────────────────────────────────────────────────────────────────────
FIXED_CELEBRATIONS = [
    # ── JANUARY ──
    {"month": 1, "day": 1,  "name": "New Year's Day",               "category": "Federal Holiday",  "emoji": "🎆", "discount": 15, "theme": "new_year"},
    {"month": 1, "day": 6,  "name": "Three Kings Day (Epiphany)",   "category": "Religious",        "emoji": "👑", "discount": 10, "theme": "holiday"},
    {"month": 1, "day": 15, "name": "National Hat Day",             "category": "Fun Days",         "emoji": "🎩", "discount": 5,  "theme": "fun"},
    {"month": 1, "day": 16, "name": "National Get to Know Your Customer Day","category": "Business", "emoji": "🤝", "discount": 10, "theme": "corporate"},
    {"month": 1, "day": 26, "name": "National Spouses Day",         "category": "Love & Romance",   "emoji": "💑", "discount": 12, "theme": "romance"},

    # ── FEBRUARY ──
    {"month": 2, "day": 2,  "name": "Groundhog Day",                "category": "Fun Days",         "emoji": "🦔", "discount": 5,  "theme": "fun"},
    {"month": 2, "day": 9,  "name": "National Pizza Day",           "category": "Food Days",        "emoji": "🍕", "discount": 8,  "theme": "food"},
    {"month": 2, "day": 11, "name": "National Make a Friend Day",   "category": "Social",           "emoji": "🤝", "discount": 10, "theme": "friendship"},
    {"month": 2, "day": 13, "name": "Galentine's Day",              "category": "Love & Romance",   "emoji": "💕", "discount": 15, "theme": "romance"},
    {"month": 2, "day": 14, "name": "Valentine's Day",              "category": "Major Holiday",    "emoji": "❤️", "discount": 20, "theme": "valentine"},
    {"month": 2, "day": 20, "name": "National Love Your Pet Day",   "category": "Fun Days",         "emoji": "🐾", "discount": 10, "theme": "fun"},

    # ── MARCH ──
    {"month": 3, "day": 1,  "name": "National Employee Appreciation Day", "category": "Business",  "emoji": "👔", "discount": 15, "theme": "corporate"},
    {"month": 3, "day": 8,  "name": "International Women's Day",    "category": "Major Holiday",    "emoji": "👩", "discount": 15, "theme": "womens_day"},
    {"month": 3, "day": 10, "name": "National Pack Your Lunch Day", "category": "Food Days",        "emoji": "🥪", "discount": 5,  "theme": "food"},
    {"month": 3, "day": 14, "name": "Pi Day",                       "category": "Fun Days",         "emoji": "🥧", "discount": 3,  "theme": "fun"},
    {"month": 3, "day": 17, "name": "St. Patrick's Day",            "category": "Cultural",         "emoji": "☘️", "discount": 17, "theme": "st_patricks"},
    {"month": 3, "day": 20, "name": "First Day of Spring",          "category": "Seasonal",         "emoji": "🌸", "discount": 10, "theme": "spring"},
    {"month": 3, "day": 22, "name": "World Water Day",              "category": "Awareness",        "emoji": "💧", "discount": 5,  "theme": "awareness"},
    {"month": 3, "day": 26, "name": "Holi (Festival of Colors)",    "category": "Cultural",         "emoji": "🎨", "discount": 10, "theme": "holi"},

    # ── APRIL ──
    {"month": 4, "day": 1,  "name": "April Fool's Day",             "category": "Fun Days",         "emoji": "🤡", "discount": 10, "theme": "fun"},
    {"month": 4, "day": 2,  "name": "World Autism Awareness Day",   "category": "Awareness",        "emoji": "💙", "discount": 5,  "theme": "awareness"},
    {"month": 4, "day": 5,  "name": "National Deep Dish Pizza Day", "category": "Food Days",        "emoji": "🍕", "discount": 5,  "theme": "food"},
    {"month": 4, "day": 7,  "name": "World Health Day",             "category": "Awareness",        "emoji": "🏥", "discount": 10, "theme": "health"},
    {"month": 4, "day": 14, "name": "National Pecan Day",           "category": "Food Days",        "emoji": "🥜", "discount": 5,  "theme": "food"},
    {"month": 4, "day": 16, "name": "National Stress Awareness Day","category": "Wellness",         "emoji": "🧘", "discount": 15, "theme": "wellness"},
    {"month": 4, "day": 20, "name": "National Lookalike Day",       "category": "Fun Days",         "emoji": "👯", "discount": 5,  "theme": "fun"},
    {"month": 4, "day": 22, "name": "Earth Day",                    "category": "Awareness",        "emoji": "🌍", "discount": 10, "theme": "eco"},
    {"month": 4, "day": 25, "name": "Administrative Professionals Day","category": "Business",      "emoji": "📋", "discount": 15, "theme": "corporate"},
    {"month": 4, "day": 27, "name": "National Tell a Story Day",    "category": "Fun Days",         "emoji": "📖", "discount": 5,  "theme": "fun"},

    # ── MAY ──
    {"month": 5, "day": 1,  "name": "May Day / International Workers Day", "category": "Holiday",  "emoji": "🌷", "discount": 10, "theme": "spring"},
    {"month": 5, "day": 4,  "name": "Star Wars Day",                "category": "Pop Culture",      "emoji": "⭐", "discount": 10, "theme": "fun"},
    {"month": 5, "day": 5,  "name": "Cinco de Mayo",                "category": "Cultural",         "emoji": "🌮", "discount": 15, "theme": "cultural"},
    {"month": 5, "day": 6,  "name": "National Nurses Day",          "category": "Appreciation",     "emoji": "👩‍⚕️","discount": 20, "theme": "nurse"},
    {"month": 5, "day": 10, "name": "National Clean Up Your Room Day","category": "Fun Days",       "emoji": "🧹", "discount": 5,  "theme": "fun"},
    {"month": 5, "day": 12, "name": "International Nurses Day",     "category": "Appreciation",     "emoji": "💊", "discount": 20, "theme": "nurse"},
    {"month": 5, "day": 15, "name": "National Chocolate Chip Cookie Day","category": "Food Days",   "emoji": "🍪", "discount": 8,  "theme": "food"},
    {"month": 5, "day": 18, "name": "Armed Forces Day",             "category": "Federal Holiday",  "emoji": "🎖️","discount": 15, "theme": "military"},
    {"month": 5, "day": 21, "name": "National Memo Day",            "category": "Business",         "emoji": "📝", "discount": 5,  "theme": "corporate"},
    {"month": 5, "day": 25, "name": "National Wine Day",            "category": "Food Days",        "emoji": "🍷", "discount": 15, "theme": "food"},

    # ── JUNE ──
    {"month": 6, "day": 1,  "name": "National Donut Day",           "category": "Food Days",        "emoji": "🍩", "discount": 8,  "theme": "food"},
    {"month": 6, "day": 5,  "name": "World Environment Day",        "category": "Awareness",        "emoji": "🌿", "discount": 10, "theme": "eco"},
    {"month": 6, "day": 8,  "name": "World Oceans Day",             "category": "Awareness",        "emoji": "🌊", "discount": 5,  "theme": "awareness"},
    {"month": 6, "day": 14, "name": "Flag Day",                     "category": "US Holiday",       "emoji": "🇺🇸", "discount": 10, "theme": "patriotic"},
    {"month": 6, "day": 18, "name": "International Picnic Day",     "category": "Fun Days",         "emoji": "🧺", "discount": 10, "theme": "summer"},
    {"month": 6, "day": 19, "name": "Juneteenth",                   "category": "Federal Holiday",  "emoji": "✊", "discount": 15, "theme": "cultural"},
    {"month": 6, "day": 21, "name": "First Day of Summer",          "category": "Seasonal",         "emoji": "☀️", "discount": 15, "theme": "summer"},
    {"month": 6, "day": 21, "name": "World Music Day",              "category": "Cultural",         "emoji": "🎵", "discount": 10, "theme": "fun"},
    {"month": 6, "day": 24, "name": "National Pralines Day",        "category": "Food Days",        "emoji": "🍬", "discount": 8,  "theme": "food"},
    {"month": 6, "day": 27, "name": "National Sunglasses Day",      "category": "Fun Days",         "emoji": "😎", "discount": 10, "theme": "summer"},

    # ── JULY ──
    {"month": 7, "day": 1,  "name": "National Postal Worker Day",   "category": "Appreciation",     "emoji": "📬", "discount": 10, "theme": "appreciation"},
    {"month": 7, "day": 4,  "name": "Independence Day (4th of July)","category": "Federal Holiday", "emoji": "🎆", "discount": 20, "theme": "fourth_july"},
    {"month": 7, "day": 7,  "name": "National Chocolate Day",       "category": "Food Days",        "emoji": "🍫", "discount": 12, "theme": "food"},
    {"month": 7, "day": 14, "name": "Bastille Day",                 "category": "Cultural",         "emoji": "🥖", "discount": 10, "theme": "cultural"},
    {"month": 7, "day": 17, "name": "World Emoji Day",              "category": "Fun Days",         "emoji": "😊", "discount": 5,  "theme": "fun"},
    {"month": 7, "day": 18, "name": "National Ice Cream Day",       "category": "Food Days",        "emoji": "🍦", "discount": 10, "theme": "summer"},
    {"month": 7, "day": 26, "name": "Disability Independence Day",  "category": "Awareness",        "emoji": "♿", "discount": 10, "theme": "awareness"},
    {"month": 7, "day": 30, "name": "National Friendship Day",      "category": "Social",           "emoji": "👫", "discount": 15, "theme": "friendship"},

    # ── AUGUST ──
    {"month": 8, "day": 1,  "name": "National Girlfriends Day",     "category": "Social",           "emoji": "👭", "discount": 15, "theme": "friendship"},
    {"month": 8, "day": 5,  "name": "National Underwear Day",       "category": "Fun Days",         "emoji": "🩲", "discount": 5,  "theme": "fun"},
    {"month": 8, "day": 7,  "name": "National Lighthouse Day",      "category": "Long Island Special","emoji": "🏮","discount": 10, "theme": "long_island"},
    {"month": 8, "day": 8,  "name": "International Cat Day",        "category": "Fun Days",         "emoji": "🐱", "discount": 10, "theme": "fun"},
    {"month": 8, "day": 10, "name": "National Lazy Day",            "category": "Fun Days",         "emoji": "😴", "discount": 10, "theme": "fun"},
    {"month": 8, "day": 12, "name": "International Youth Day",      "category": "Awareness",        "emoji": "🌟", "discount": 10, "theme": "awareness"},
    {"month": 8, "day": 13, "name": "National Left Handers Day",    "category": "Fun Days",         "emoji": "✋", "discount": 5,  "theme": "fun"},
    {"month": 8, "day": 16, "name": "National Bratwurst Day",       "category": "Food Days",        "emoji": "🌭", "discount": 8,  "theme": "food"},
    {"month": 8, "day": 19, "name": "World Photography Day",        "category": "Cultural",         "emoji": "📷", "discount": 10, "theme": "cultural"},
    {"month": 8, "day": 26, "name": "National Dog Day",             "category": "Fun Days",         "emoji": "🐶", "discount": 10, "theme": "fun"},
    {"month": 8, "day": 28, "name": "National Race Your Mouse Day", "category": "Fun Days",         "emoji": "🖱️","discount": 5,  "theme": "fun"},

    # ── SEPTEMBER ──
    {"month": 9, "day": 5,  "name": "International Day of Charity", "category": "Awareness",        "emoji": "🤲", "discount": 10, "theme": "charity"},
    {"month": 9, "day": 11, "name": "Patriot Day (9/11 Remembrance)","category": "US Memorial",     "emoji": "🕊️","discount": 0,  "theme": "memorial"},
    {"month": 9, "day": 13, "name": "National Grandparents Day",    "category": "Family",           "emoji": "👴👵","discount": 20, "theme": "grandparents"},
    {"month": 9, "day": 15, "name": "Hispanic Heritage Month Begins","category": "Cultural",        "emoji": "🌺", "discount": 15, "theme": "cultural"},
    {"month": 9, "day": 17, "name": "National Apple Dumpling Day",  "category": "Food Days",        "emoji": "🍎", "discount": 8,  "theme": "food"},
    {"month": 9, "day": 20, "name": "National Pepperoni Pizza Day", "category": "Food Days",        "emoji": "🍕", "discount": 8,  "theme": "food"},
    {"month": 9, "day": 21, "name": "World Alzheimer's Day",        "category": "Awareness",        "emoji": "💜", "discount": 10, "theme": "awareness"},
    {"month": 9, "day": 22, "name": "First Day of Fall/Autumn",     "category": "Seasonal",         "emoji": "🍂", "discount": 15, "theme": "fall"},
    {"month": 9, "day": 23, "name": "National Checkers Day",        "category": "Fun Days",         "emoji": "🎮", "discount": 5,  "theme": "fun"},
    {"month": 9, "day": 26, "name": "National Pancake Day",         "category": "Food Days",        "emoji": "🥞", "discount": 8,  "theme": "food"},
    {"month": 9, "day": 29, "name": "World Heart Day",              "category": "Health",           "emoji": "❤️", "discount": 10, "theme": "health"},

    # ── OCTOBER ──
    {"month": 10, "day": 1, "name": "International Coffee Day",     "category": "Food Days",        "emoji": "☕", "discount": 10, "theme": "food"},
    {"month": 10, "day": 2, "name": "World Smile Day (1st Fri Oct)","category": "Fun Days",         "emoji": "😊", "discount": 10, "theme": "fun"},
    {"month": 10, "day": 3, "name": "National Boyfriend Day",       "category": "Love & Romance",   "emoji": "💑", "discount": 15, "theme": "romance"},
    {"month": 10, "day": 4, "name": "World Animal Day",             "category": "Awareness",        "emoji": "🐾", "discount": 10, "theme": "fun"},
    {"month": 10, "day": 10, "name": "World Mental Health Day",     "category": "Wellness",         "emoji": "🧠", "discount": 15, "theme": "wellness"},
    {"month": 10, "day": 11, "name": "National Coming Out Day",     "category": "Cultural",         "emoji": "🌈", "discount": 10, "theme": "cultural"},
    {"month": 10, "day": 14, "name": "Indigenous Peoples Day / Columbus Day","category": "Federal Holiday","emoji": "🌎","discount": 10, "theme": "holiday"},
    {"month": 10, "day": 16, "name": "World Food Day",              "category": "Awareness",        "emoji": "🌽", "discount": 10, "theme": "food"},
    {"month": 10, "day": 19, "name": "Sweetest Day",                "category": "Love & Romance",   "emoji": "🍬", "discount": 15, "theme": "romance"},
    {"month": 10, "day": 22, "name": "National Nut Day",            "category": "Food Days",        "emoji": "🥜", "discount": 8,  "theme": "food"},
    {"month": 10, "day": 28, "name": "National Chocolate Day",      "category": "Food Days",        "emoji": "🍫", "discount": 12, "theme": "food"},
    {"month": 10, "day": 29, "name": "National Cat Day",            "category": "Fun Days",         "emoji": "🐱", "discount": 10, "theme": "fun"},
    {"month": 10, "day": 31, "name": "Halloween",                   "category": "Major Holiday",    "emoji": "🎃", "discount": 20, "theme": "halloween"},

    # ── NOVEMBER ──
    {"month": 11, "day": 1,  "name": "Diwali (varies ~Oct-Nov)",    "category": "Cultural",         "emoji": "🪔", "discount": 20, "theme": "diwali"},
    {"month": 11, "day": 1,  "name": "All Saints' Day",             "category": "Religious",        "emoji": "✝️","discount": 5,  "theme": "religious"},
    {"month": 11, "day": 8,  "name": "National STEM/STEAM Day",     "category": "Education",        "emoji": "🔬", "discount": 10, "theme": "education"},
    {"month": 11, "day": 11, "name": "Veterans Day",                "category": "Federal Holiday",  "emoji": "🎖️","discount": 20, "theme": "military"},
    {"month": 11, "day": 13, "name": "World Kindness Day",          "category": "Awareness",        "emoji": "💛", "discount": 15, "theme": "kindness"},
    {"month": 11, "day": 14, "name": "World Diabetes Day",          "category": "Health",           "emoji": "💙", "discount": 10, "theme": "health"},
    {"month": 11, "day": 19, "name": "International Men's Day",     "category": "Social",           "emoji": "👨", "discount": 15, "theme": "mens_day"},
    {"month": 11, "day": 23, "name": "National Cashew Day",         "category": "Food Days",        "emoji": "🥜", "discount": 8,  "theme": "food"},
    {"month": 11, "day": 25, "name": "National Parfait Day",        "category": "Food Days",        "emoji": "🍨", "discount": 8,  "theme": "food"},
    {"month": 11, "day": 28, "name": "Thanksgiving Day (4th Thu Nov)","category": "Federal Holiday","emoji": "🦃", "discount": 20, "theme": "thanksgiving"},
    {"month": 11, "day": 29, "name": "Black Friday",                "category": "Shopping",         "emoji": "🛍️","discount": 30, "theme": "sale"},
    {"month": 11, "day": 30, "name": "Cyber Monday Eve",            "category": "Shopping",         "emoji": "💻", "discount": 25, "theme": "sale"},

    # ── DECEMBER ──
    {"month": 12, "day": 1,  "name": "World AIDS Day",              "category": "Awareness",        "emoji": "🎗️","discount": 5,  "theme": "awareness"},
    {"month": 12, "day": 2,  "name": "Cyber Monday",                "category": "Shopping",         "emoji": "💻", "discount": 25, "theme": "sale"},
    {"month": 12, "day": 4,  "name": "National Cookie Day",         "category": "Food Days",        "emoji": "🍪", "discount": 10, "theme": "food"},
    {"month": 12, "day": 6,  "name": "St. Nicholas Day",            "category": "Religious",        "emoji": "🎅", "discount": 15, "theme": "holiday"},
    {"month": 12, "day": 7,  "name": "Pearl Harbor Remembrance Day","category": "US Memorial",      "emoji": "🕊️","discount": 0,  "theme": "memorial"},
    {"month": 12, "day": 10, "name": "Human Rights Day",            "category": "Awareness",        "emoji": "✊", "discount": 10, "theme": "awareness"},
    {"month": 12, "day": 14, "name": "National Bouillabaisse Day",  "category": "Food Days",        "emoji": "🍲", "discount": 8,  "theme": "food"},
    {"month": 12, "day": 15, "name": "Bill of Rights Day",          "category": "US Holiday",       "emoji": "🇺🇸", "discount": 5, "theme": "patriotic"},
    {"month": 12, "day": 19, "name": "Hanukkah Begins (varies)",    "category": "Major Holiday",    "emoji": "🕎", "discount": 20, "theme": "hanukkah"},
    {"month": 12, "day": 21, "name": "First Day of Winter",         "category": "Seasonal",         "emoji": "❄️", "discount": 10, "theme": "winter"},
    {"month": 12, "day": 24, "name": "Christmas Eve",               "category": "Major Holiday",    "emoji": "🎄", "discount": 25, "theme": "christmas"},
    {"month": 12, "day": 25, "name": "Christmas Day",               "category": "Major Holiday",    "emoji": "🎁", "discount": 25, "theme": "christmas"},
    {"month": 12, "day": 26, "name": "Kwanzaa Begins",              "category": "Cultural",         "emoji": "🕯️","discount": 15, "theme": "cultural"},
    {"month": 12, "day": 26, "name": "Boxing Day",                  "category": "Cultural",         "emoji": "📦", "discount": 20, "theme": "sale"},
    {"month": 12, "day": 31, "name": "New Year's Eve",              "category": "Major Holiday",    "emoji": "🥂", "discount": 20, "theme": "new_year"},
]

# ─────────────────────────────────────────────────────────────────────────────
# FLOATING-DATE celebrations (computed per year) — returned by get_floating()
# ─────────────────────────────────────────────────────────────────────────────
def get_floating_celebrations(year: int) -> List[Dict]:
    """Return floating-date celebrations for a given year."""
    import calendar

    def nth_weekday(year, month, weekday, n):
        """Return date of nth weekday (0=Mon … 6=Sun) in month. n=1 means first."""
        cal = calendar.monthcalendar(year, month)
        count = 0
        for week in cal:
            if week[weekday] != 0:
                count += 1
                if count == n:
                    return date(year, month, week[weekday])
        return None

    def last_weekday(year, month, weekday):
        cal = calendar.monthcalendar(year, month)
        for week in reversed(cal):
            if week[weekday] != 0:
                return date(year, month, week[weekday])
        return None

    MON, TUE, WED, THU, FRI, SAT, SUN = 0,1,2,3,4,5,6

    events = []

    def add(d, name, category, emoji, discount, theme):
        if d:
            events.append({
                "date": d, "name": name, "category": category,
                "emoji": emoji, "discount": discount, "theme": theme,
                "month": d.month, "day": d.day,
            })

    # MLK Day — 3rd Monday Jan
    add(nth_weekday(year, 1, MON, 3), "Martin Luther King Jr. Day", "Federal Holiday", "✊", 15, "cultural")
    # Presidents Day — 3rd Monday Feb
    add(nth_weekday(year, 2, MON, 3), "Presidents' Day", "Federal Holiday", "🇺🇸", 10, "patriotic")
    # Mardi Gras — 47 days before Easter (Fat Tuesday)
    easter = _calc_easter(year)
    mardi_gras = date.fromordinal(easter.toordinal() - 47)
    add(mardi_gras, "Mardi Gras / Fat Tuesday", "Cultural", "🎭", 15, "fun")
    # Valentine's already fixed
    # Easter Sunday
    add(easter, "Easter Sunday", "Major Holiday", "🐣", 20, "easter")
    # Good Friday (2 days before Easter)
    add(date.fromordinal(easter.toordinal() - 2), "Good Friday", "Religious", "✝️", 5, "religious")
    # Mother's Day — 2nd Sunday May
    add(nth_weekday(year, 5, SUN, 2), "Mother's Day", "Major Holiday", "🌹", 25, "mothers_day")
    # Memorial Day — last Monday May
    add(last_weekday(year, 5, MON), "Memorial Day", "Federal Holiday", "🎖️", 15, "military")
    # Father's Day — 3rd Sunday June
    add(nth_weekday(year, 6, SUN, 3), "Father's Day", "Major Holiday", "👔", 25, "fathers_day")
    # Labor Day — 1st Monday Sep
    add(nth_weekday(year, 9, MON, 1), "Labor Day", "Federal Holiday", "👷", 20, "holiday")
    # Columbus/Indigenous Day — 2nd Monday Oct
    add(nth_weekday(year, 10, MON, 2), "Columbus/Indigenous Peoples Day", "Federal Holiday", "🌎", 10, "holiday")
    # Thanksgiving — 4th Thursday Nov
    add(nth_weekday(year, 11, THU, 4), "Thanksgiving Day", "Federal Holiday", "🦃", 20, "thanksgiving")
    # Black Friday (day after Thanksgiving)
    tg = nth_weekday(year, 11, THU, 4)
    if tg:
        add(date.fromordinal(tg.toordinal() + 1), "Black Friday", "Shopping", "🛍️", 30, "sale")
        add(date.fromordinal(tg.toordinal() + 4), "Cyber Monday", "Shopping", "💻", 25, "sale")
    # Administrative Professionals Day (Wednesday of last full week Apr)
    add(nth_weekday(year, 4, WED, 4), "Administrative Professionals Day", "Business", "📋", 15, "corporate")
    # Boss's Day — Oct 16 (already fixed, skip)
    # Grandparents Day — 1st Sunday after Labor Day
    ld = nth_weekday(year, 9, MON, 1)
    if ld:
        add(date.fromordinal(ld.toordinal() + 6), "National Grandparents Day", "Family", "👴👵", 20, "grandparents")
    # National Boss Day Oct 16 fixed
    # Long Island specific: Hamptons Season Opens (Memorial Day weekend)
    if tg:  # reuse for reference
        pass
    # Teacher Appreciation Week (1st full week May, Tuesday)
    add(nth_weekday(year, 5, TUE, 1), "Teacher Appreciation Day", "Appreciation", "🍎", 20, "teachers")

    return events


def _calc_easter(year: int) -> date:
    """Anonymous Gregorian algorithm for Easter date."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


# ─────────────────────────────────────────────────────────────────────────────
# Email / WhatsApp message templates per theme
# ─────────────────────────────────────────────────────────────────────────────
MESSAGE_TEMPLATES = {
    "valentine": {
        "subject": "💕 Valentine's Day is {days} days away — Gift Baskets from $35!",
        "email_body": """Dear {name},

Love is in the air! 💕 Valentine's Day is just {days} days away, and the perfect gift basket from LI Gift Basket is waiting for your special someone.

🎁 Our Valentine's Collection includes:
• Chocolate & Roses Basket — $49
• Wine & Cheese Lovers Basket — $75
• Spa & Pampering Basket — $65
• Personalized Sweet Hearts Basket — $55

🚚 FREE delivery across Long Island for orders over $60!
📦 Order by {order_by} for guaranteed Valentine's delivery.

Use code LOVE{year} for {discount}% OFF your order!

Shop now: https://ligiftbasket.com

With love,
LI Gift Basket Team
📍 Plainview, Long Island, NY
📞 (516) 555-0100""",
        "whatsapp": "💕 Valentine's Day is {days} days away! Send a gorgeous gift basket to your special someone. FREE delivery on Long Island! Use code LOVE{year} for {discount}% off. Shop: https://ligiftbasket.com 🎁",
    },
    "mothers_day": {
        "subject": "🌹 Mother's Day is {days} days away — She Deserves the Best!",
        "email_body": """Dear {name},

Mother's Day is coming up in just {days} days — time to show Mom how much she means to you! 🌹

✨ Our Best-Selling Mother's Day Baskets:
• Mom's Spa Day Retreat — $85
• Gourmet Treat Basket — $70
• Tea & Relaxation Set — $55
• Fresh Flowers & Chocolates — $65
• Grand Mother's Luxury Basket — $120

🌸 Add a FREE personalized card with any order!
🚚 Same-day delivery available in Nassau & Suffolk County.

Order by {order_by} for guaranteed Mother's Day delivery.
Use code MOM{discount} for {discount}% OFF!

Order now: https://ligiftbasket.com

Warmly,
LI Gift Basket — Plainview, Long Island, NY""",
        "whatsapp": "🌹 Mother's Day is {days} days away! Surprise Mom with a beautiful gift basket. FREE card + delivery on Long Island. Use MOM{discount} for {discount}% off! 👉 https://ligiftbasket.com",
    },
    "christmas": {
        "subject": "🎄 Christmas Gift Baskets — Order Early, Save Big!",
        "email_body": """Dear {name},

The most magical time of the year is almost here! 🎄✨

Spread joy this Christmas with LI Gift Basket's holiday collections:

🎁 2024 Holiday Specials:
• Holiday Cheer Basket — $75
• Christmas Cookie & Cocoa Set — $55
• Family Feast Basket — $110
• Corporate Holiday Gift Set (10+ units) — From $45/each
• Premium Wine & Cheese Holiday Box — $95

🛷 Order by December 20 for Christmas Eve delivery!
🎅 FREE gift wrapping on all orders this December!

Use code XMAS{year} for {discount}% OFF your order.

Shop: https://ligiftbasket.com

Happy Holidays,
LI Gift Basket
Plainview, Long Island, NY 🗽""",
        "whatsapp": "🎄 Christmas is {days} days away! Order your holiday gift baskets NOW. FREE wrapping + Long Island delivery. Use XMAS{year} for {discount}% off! 🎁 https://ligiftbasket.com",
    },
    "thanksgiving": {
        "subject": "🦃 Thanksgiving Gift Baskets — Share Gratitude This Year!",
        "email_body": """Dear {name},

Thanksgiving is just {days} days away! 🦃 This year, show your gratitude with a beautiful gift basket.

🍂 Our Thanksgiving Collection:
• Harvest Feast Basket — $80
• Gourmet Stuffed Turkey Basket — $95
• Cranberry & Wine Set — $70
• Grateful Family Basket — $65
• Corporate Thank You Basket — From $50

Use code THANKS{year} for {discount}% OFF any order!
Free delivery across Long Island.

Order by {order_by}: https://ligiftbasket.com

Happy Thanksgiving from the LI Gift Basket family! 🍁""",
        "whatsapp": "🦃 Thanksgiving is {days} days away! Share gratitude with a beautiful gift basket. Free Long Island delivery. Use THANKS{year} for {discount}% off! 🍂 https://ligiftbasket.com",
    },
    "default": {
        "subject": "{emoji} {celebration} — Special Gift Basket Offer Just for You!",
        "email_body": """Dear {name},

{celebration} is just {days} days away! 🎉

Celebrate with a beautiful gift basket from LI Gift Basket — Long Island's premier gift shop in Plainview, NY.

🎁 Our curated gift baskets start at just $35.
🚚 Free delivery across Nassau & Suffolk County on orders $60+.
🎀 Custom baskets available for any occasion.

Use code {code} for {discount}% OFF your next order!

Shop our full collection: https://ligiftbasket.com

Warm regards,
LI Gift Basket Team
📍 Plainview, Long Island, NY 11803""",
        "whatsapp": "{emoji} {celebration} is {days} days away! Celebrate with a beautiful gift basket from LI Gift Basket, Plainview NY. Use {code} for {discount}% off! Free delivery on Long Island. 🎁 https://ligiftbasket.com",
    },
}


def get_message_for_celebration(celebration: Dict, customer_name: str = "Friend",
                                 days_until: int = 7, year: int = 2026) -> Dict:
    """Generate email subject, body, and WhatsApp message for a celebration."""
    theme = celebration.get("theme", "default")
    template = MESSAGE_TEMPLATES.get(theme, MESSAGE_TEMPLATES["default"])

    order_by_days = max(days_until - 3, 1)

    vars = {
        "name": customer_name,
        "celebration": celebration["name"],
        "emoji": celebration.get("emoji", "🎁"),
        "days": days_until,
        "discount": celebration.get("discount", 10),
        "year": year,
        "order_by": f"{order_by_days} days before the event",
        "code": celebration["name"].upper().replace(" ", "")[:8] + str(year)[-2:],
    }

    subject = template["subject"].format(**vars)
    body = template["email_body"].format(**vars)
    whatsapp = template["whatsapp"].format(**vars)

    return {"subject": subject, "email_body": body, "whatsapp_message": whatsapp}


def get_all_celebrations(year: int) -> List[Dict]:
    """Return ALL celebrations for a year, sorted by date."""
    all_events = []

    for c in FIXED_CELEBRATIONS:
        try:
            d = date(year, c["month"], c["day"])
            all_events.append({**c, "date": d})
        except ValueError:
            pass

    all_events.extend(get_floating_celebrations(year))

    # Deduplicate by (month, day, name)
    seen = set()
    unique = []
    for e in all_events:
        key = (e.get("month"), e.get("day"), e.get("name"))
        if key not in seen:
            seen.add(key)
            unique.append(e)

    unique.sort(key=lambda x: (x.get("month", 0), x.get("day", 0)))
    return unique


if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    celebrations = get_all_celebrations(2026)
    print(f"\nTotal celebrations for 2026: {len(celebrations)}")
    print(f"\nSample -- next 10 from today:")
    today = date.today()
    upcoming = [c for c in celebrations if c["date"] >= today][:10]
    for c in upcoming:
        name = c['name'].encode('ascii', errors='replace').decode('ascii')
        print(f"  {c['date']} | {name} | {c['category']} | {c['discount']}% off")
