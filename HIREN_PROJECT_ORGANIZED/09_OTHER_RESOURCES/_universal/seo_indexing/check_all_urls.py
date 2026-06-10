#!/usr/bin/env python3
"""Live HTTP check for all blog URLs in BLOG_URLS_GOOGLE_INSPECT.md"""
import sys, requests
sys.stdout.reconfigure(encoding="utf-8")

sess = requests.Session()
sess.headers.update({"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1)"})

URLS = [
    # LIC blog index
    "https://www.longislandconvenience.com/blog",
    # Sports & Trading Cards
    "https://www.longislandconvenience.com/blog/sports-trading-cards-2/how-to-get-your-trading-cards-psa-graded-on-long-island-1",
    "https://www.longislandconvenience.com/blog/sports-trading-cards-2/best-pokemon-card-sets-to-buy-in-long-island-2025-guide-2",
    "https://www.longislandconvenience.com/blog/sports-trading-cards-2/pokemon-cards-long-island-new-york-where-to-buy-in-plainview-8",
    "https://www.longislandconvenience.com/blog/sports-trading-cards-2/trading-cards-nassau-county-ny-complete-buyers-guide-9",
    "https://www.longislandconvenience.com/blog/sports-trading-cards-2/mtg-magic-the-gathering-cards-long-island-singles-booster-boxes-in-plainview-ny-12",
    "https://www.longislandconvenience.com/blog/sports-trading-cards-2/yu-gi-oh-cards-nassau-county-ny-buy-packs-singles-at-hirens-plainview-shop-13",
    "https://www.longislandconvenience.com/blog/sports-trading-cards-2/one-piece-trading-card-game-long-island-booster-boxes-singles-in-plainview-ny-14",
    "https://www.longislandconvenience.com/blog/sports-trading-cards-2/sports-cards-plainview-ny-vintage-baseball-basketball-football-cards-in-nassau-county-15",
    "https://www.longislandconvenience.com/blog/sports-trading-cards-2/buy-sell-trade-cards-long-island-best-card-shop-prices-in-nassau-county-ny-16",
    "https://www.longislandconvenience.com/blog/sports-trading-cards-2/pokemon-cards-long-island-buy-sell-trade-plainview-ny-44",
    # Print & Mail
    "https://www.longislandconvenience.com/blog/print-mail-services-4/same-day-business-card-printing-in-plainview-ny-how-it-works-3",
    "https://www.longislandconvenience.com/blog/print-mail-services-4/banner-printing-for-long-island-events-complete-guide-4",
    "https://www.longislandconvenience.com/blog/print-mail-services-4/print-shop-plainview-ny-hirens-same-day-printing-vs-online-services-11",
    "https://www.longislandconvenience.com/blog/print-mail-services-4/notary-public-services-plainview-ny-walk-in-notarization-in-nassau-county-17",
    "https://www.longislandconvenience.com/blog/print-mail-services-4/mailbox-rental-po-box-alternative-plainview-ny-private-mail-service-nassau-county-18",
    "https://www.longislandconvenience.com/blog/print-mail-services-4/shipping-services-plainview-ny-ups-fedex-usps-drop-off-in-nassau-county-19",
    # Balloons & Party Decor
    "https://www.longislandconvenience.com/blog/balloons-party-decor-3/custom-balloon-arrangements-for-long-island-events-birthday-graduation-more-6",
    "https://www.longislandconvenience.com/blog/balloons-party-decor-3/wedding-balloon-decorations-long-island-arch-centerpiece-setup-in-nassau-county-20",
    "https://www.longislandconvenience.com/blog/balloons-party-decor-3/baby-shower-balloon-decorations-nassau-county-gender-reveal-party-decor-plainview-ny-21",
    "https://www.longislandconvenience.com/blog/balloons-party-decor-3/graduation-party-balloons-plainview-ny-class-of-2026-decorations-long-island-22",
    "https://www.longislandconvenience.com/blog/balloons-party-decor-3/corporate-event-balloons-long-island-office-party-grand-opening-decor-nassau-county-23",
    "https://www.longislandconvenience.com/blog/balloons-party-decor-3/graduation-balloon-arch-long-island-ny-2026-guide-43",
    # Gift Baskets
    "https://www.longislandconvenience.com/blog/gift-baskets-gifts-5/best-gift-baskets-for-fathers-day-on-long-island-2025-5",
    "https://www.longislandconvenience.com/blog/gift-baskets-gifts-5/custom-gift-baskets-nassau-county-ny-personalized-for-any-occasion-24",
    "https://www.longislandconvenience.com/blog/gift-baskets-gifts-5/corporate-gift-baskets-long-island-bulk-orders-branded-gifts-for-nassau-county-businesses-25",
    "https://www.longislandconvenience.com/blog/gift-baskets-gifts-5/holiday-gift-baskets-long-island-christmas-hanukkah-new-year-gifts-nassau-county-26",
    "https://www.longislandconvenience.com/blog/gift-baskets-gifts-5/birthday-gift-baskets-long-island-same-day-pickup-in-plainview-nassau-county-ny-27",
    "https://www.longislandconvenience.com/blog/gift-baskets-gifts-5/graduation-gift-baskets-long-island-ny-class-of-2026-41",
    # Convenience & Grocery
    "https://www.longislandconvenience.com/blog/convenience-grocery-7/best-convenience-store-plainview-ny-local-shop-for-everyday-essentials-nassau-county-28",
    "https://www.longislandconvenience.com/blog/convenience-grocery-7/late-night-convenience-store-nassau-county-open-late-in-plainview-ny-29",
    "https://www.longislandconvenience.com/blog/convenience-grocery-7/local-grocery-shopping-plainview-ny-fresh-snacks-household-items-nassau-county-30",
    "https://www.longislandconvenience.com/blog/convenience-grocery-7/cold-drinks-quick-bites-plainview-ny-beverages-snacks-nassau-county-long-island-31",
    # IT & Cyber
    "https://www.longislandconvenience.com/blog/it-cyber-services-8/it-support-services-plainview-ny-local-tech-help-for-nassau-county-businesses-32",
    "https://www.longislandconvenience.com/blog/it-cyber-services-8/cyber-security-consulting-long-island-protect-your-nassau-county-business-33",
    "https://www.longislandconvenience.com/blog/it-cyber-services-8/computer-repair-nassau-county-fast-turnaround-at-hirens-plainview-ny-tech-shop-34",
    # JHD blog index
    "https://www.jhdadvisor.com/blog",
    # JHD posts
    "https://www.jhdadvisor.com/blog/jhd-advisor-growth-lab-9/top-10-it-services-every-business-should-automate-in-2026-45",
    "https://www.jhdadvisor.com/blog/jhd-advisor-growth-lab-9/how-agentic-ai-workflows-are-changing-small-business-operations-46",
    "https://www.jhdadvisor.com/blog/jhd-advisor-growth-lab-9/n8n-automation-ideas-for-ecommerce-stores-47",
    "https://www.jhdadvisor.com/blog/jhd-advisor-growth-lab-9/odoo-vs-shopify-vs-woocommerce-which-ecommerce-stack-should-you-choose-48",
    "https://www.jhdadvisor.com/blog/jhd-advisor-growth-lab-9/how-to-build-a-web-app-mvp-without-wasting-six-months-49",
    "https://www.jhdadvisor.com/blog/jhd-advisor-growth-lab-9/ai-chatbots-that-actually-convert-leads-50",
    "https://www.jhdadvisor.com/blog/jhd-advisor-growth-lab-9/seo-geo-and-ai-overviews-the-new-search-playbook-51",
    "https://www.jhdadvisor.com/blog/jhd-advisor-growth-lab-9/what-business-owners-should-know-about-api-integrations-52",
    "https://www.jhdadvisor.com/blog/jhd-advisor-growth-lab-9/cybersecurity-basics-for-ai-powered-businesses-53",
    "https://www.jhdadvisor.com/blog/jhd-advisor-growth-lab-9/daily-automation-scorecard-what-to-measure-every-morning-54",
    "https://www.jhdadvisor.com/blog/jhd-advisor-growth-lab-9/what-are-ai-agents-and-why-every-business-should-know-about-them-in-2026-55",
    "https://www.jhdadvisor.com/blog/jhd-advisor-growth-lab-9/geo-vs-seo-how-to-rank-in-ai-overviews-chatgpt-answers-and-answer-engines-in-2026-56",
    "https://www.jhdadvisor.com/blog/jhd-advisor-growth-lab-9/n8n-automation-in-2026-the-10-workflows-every-service-business-should-build-first-57",
    "https://www.jhdadvisor.com/blog/jhd-advisor-growth-lab-9/odoo-17-vs-shopify-vs-woocommerce-which-ecommerce-stack-should-you-choose-in-2026-58",
    "https://www.jhdadvisor.com/blog/jhd-advisor-growth-lab-9/how-to-build-an-ai-chatbot-that-actually-converts-leads-not-just-answers-faqs-59",
    "https://www.jhdadvisor.com/blog/jhd-advisor-growth-lab-9/business-intelligence-dashboards-in-2026-what-to-measure-and-how-to-automate-your-kpi-reports-60",
    "https://www.jhdadvisor.com/blog/jhd-advisor-growth-lab-9/cybersecurity-in-the-age-of-ai-what-small-businesses-must-do-in-2026-61",
    "https://www.jhdadvisor.com/blog/jhd-advisor-growth-lab-9/how-to-build-and-launch-a-saas-mvp-in-90-days-without-wasting-your-budget-62",
    "https://www.jhdadvisor.com/blog/jhd-advisor-growth-lab-9/api-integrations-for-business-in-2026-how-to-connect-your-tools-and-stop-losing-data-between-systems-63",
    "https://www.jhdadvisor.com/blog/jhd-advisor-growth-lab-9/prompt-engineering-for-business-in-2026-how-to-write-ai-prompts-that-get-consistent-useful-results-64",
    "https://www.jhdadvisor.com/blog/jhd-advisor-growth-lab-9/local-seo-for-service-businesses-in-2026-the-complete-long-island-and-new-york-playbook-65",
    "https://www.jhdadvisor.com/blog/jhd-advisor-growth-lab-9/the-automation-roi-calculator-how-to-measure-what-your-workflows-are-actually-saving-66",
]

ok = []; fail = []; redir = []

for url in URLS:
    try:
        r = sess.get(url, timeout=20, allow_redirects=False)
        s = r.status_code
        short = url.replace("https://www.", "").replace("longislandconvenience.com","LIC").replace("jhdadvisor.com","JHD")
        if s == 200:
            ok.append(url)
            print(f"  [200 OK ] {short[-70:]}")
        elif s in (301, 302, 308):
            loc = r.headers.get("Location", "")
            redir.append((url, s, loc))
            print(f"  [{s} RDR] {short[-70:]}  -> {loc[-40:]}")
        else:
            fail.append((url, s))
            print(f"  [{s} ERR] {short[-70:]}")
    except Exception as e:
        fail.append((url, str(e)[:60]))
        print(f"  [NET ERR] {url[-70:]}")

print("\n" + "="*60)
print(f"  200 OK:     {len(ok):3d}")
print(f"  Redirects:  {len(redir):3d}")
print(f"  Errors:     {len(fail):3d}")
print(f"  Total:      {len(URLS):3d}")
print("="*60)

if fail:
    print("\nFAILED:")
    for u, s in fail:
        print(f"  [{s}] {u}")

if redir:
    print("\nREDIRECTS (check if destination is correct):")
    for u, s, l in redir:
        print(f"  [{s}] {u}")
        print(f"       -> {l}")
