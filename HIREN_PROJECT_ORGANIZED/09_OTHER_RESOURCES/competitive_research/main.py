"""
Main Orchestrator: runs competitive research for all 7 Hiren Kumar websites.

For each website:
  1. Finds top 10 competitors via DuckDuckGo
  2. Scrapes competitor products + prices
  3. Extracts public business contact info (emails, phones)
  4. Downloads product images
  5. Builds a formatted Excel report with 6 tabs

Output goes to:  ScrappedMaterial/<NN_WebsiteName>/
  - competitors_analysis.xlsx  (full report)
  - products_pricing.xlsx      (products-only flat sheet)
  - contacts.xlsx              (contacts-only flat sheet)
  - images/                    (downloaded product images)
"""

import sys
import os
import time
import json
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Allow imports from competitive_research/ folder
sys.path.insert(0, str(Path(__file__).parent))

from config import WEBSITES, BASE_OUTPUT, DELAY_BETWEEN_SITES, MAX_IMAGES_PER_COMPETITOR
from finder import search_competitors
from scraper import extract_products, extract_contact_info, get_all_images_from_site
from downloader import download_competitor_images
from reporter import build_excel_report

try:
    from colorama import init, Fore, Style
    init()
    def ok(msg): print(Fore.GREEN + "  ✓ " + msg + Style.RESET_ALL)
    def warn(msg): print(Fore.YELLOW + "  ⚠ " + msg + Style.RESET_ALL)
    def err(msg): print(Fore.RED + "  ✗ " + msg + Style.RESET_ALL)
    def head(msg): print(Fore.CYAN + "\n" + "="*60 + f"\n  {msg}\n" + "="*60 + Style.RESET_ALL)
except ImportError:
    def ok(msg): print(f"  OK: {msg}")
    def warn(msg): print(f"  WARN: {msg}")
    def err(msg): print(f"  ERROR: {msg}")
    def head(msg): print(f"\n{'='*60}\n  {msg}\n{'='*60}")


def run_for_website(site_key: str, site_config: Dict, base_output: Path):
    """Run full competitive research pipeline for one website."""
    folder_name = site_config["folder"]
    site_output = base_output / folder_name
    images_dir = site_output / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    head(f"{folder_name} — {site_config['business_name']}")
    start = datetime.now()

    # ---------- 1. Find Competitors ----------
    print("\n  [1/5] Finding top competitors via DuckDuckGo...")
    competitors = []
    try:
        competitors = search_competitors(site_key, site_config)
        ok(f"Found {len(competitors)} competitors")
    except Exception as e:
        err(f"Competitor search failed: {e}")
        competitors = []

    if not competitors:
        warn("No competitors found — creating empty report.")

    # ---------- 2. Scrape Products ----------
    print(f"\n  [2/5] Scraping products from {len(competitors)} competitor sites...")
    all_products: List[Dict] = []
    for comp in competitors[:8]:  # limit to 8 to keep runtime reasonable
        comp_url = comp.get("url", "")
        comp_name = comp.get("name", comp.get("domain", ""))
        print(f"    Scraping: {comp_name} ({comp_url[:60]}...)")
        try:
            products = extract_products(comp_url, comp_name, site_config.get("product_categories", []))
            all_products.extend(products)
            if products:
                ok(f"  {len(products)} products from {comp_name}")
            else:
                warn(f"  No products from {comp_name}")
        except Exception as e:
            warn(f"  Error scraping {comp_name}: {e}")
        time.sleep(DELAY_BETWEEN_SITES * 0.5)

    ok(f"Total products scraped: {len(all_products)}")

    # ---------- 3. Extract Contact Info ----------
    print(f"\n  [3/5] Extracting public business contacts...")
    all_contacts: List[Dict] = []
    for comp in competitors[:10]:
        comp_url = comp.get("url", "")
        comp_name = comp.get("name", comp.get("domain", ""))
        print(f"    Contacts: {comp_name}")
        try:
            contact = extract_contact_info(comp_url)
            contact["competitor"] = comp_name
            contact["domain"] = comp.get("domain", "")
            all_contacts.append(contact)
        except Exception as e:
            warn(f"  Contact error for {comp_name}: {e}")
            all_contacts.append({
                "competitor": comp_name,
                "domain": comp.get("domain", ""),
                "email": "", "phone": "", "address": "", "contact_page": "",
            })
        time.sleep(DELAY_BETWEEN_SITES * 0.3)

    found_contacts = sum(1 for c in all_contacts if c.get("email") or c.get("phone"))
    ok(f"Contacts with info: {found_contacts}/{len(all_contacts)}")

    # ---------- 4. Download Images ----------
    print(f"\n  [4/5] Downloading product images...")
    all_image_records: List[Dict] = []
    per_competitor_limit = max(2, MAX_IMAGES_PER_COMPETITOR // max(len(competitors), 1))

    for comp in competitors[:8]:
        comp_url = comp.get("url", "")
        comp_name = comp.get("name", comp.get("domain", ""))
        print(f"    Images: {comp_name}")
        try:
            image_urls = get_all_images_from_site(comp_url, limit=per_competitor_limit + 3)
            # Also collect image_urls from scraped products
            for p in all_products:
                if p.get("competitor") == comp_name and p.get("image_url"):
                    if p["image_url"] not in image_urls:
                        image_urls.insert(0, p["image_url"])

            records = download_competitor_images(
                image_urls=image_urls,
                output_dir=images_dir,
                competitor_name=comp_name,
                max_images=per_competitor_limit,
            )
            # Link saved filenames back to products
            for p in all_products:
                if p.get("competitor") == comp_name and p.get("image_url"):
                    for r in records:
                        if r.get("image_url") == p.get("image_url"):
                            p["saved_image"] = r.get("saved_filename", "")
            all_image_records.extend(records)
        except Exception as e:
            warn(f"  Image error for {comp_name}: {e}")
        time.sleep(DELAY_BETWEEN_SITES * 0.3)

    saved_images = sum(1 for r in all_image_records if r.get("status") == "OK")
    ok(f"Images downloaded: {saved_images}/{len(all_image_records)}")

    # ---------- 5. Build Excel ----------
    print(f"\n  [5/5] Building Excel reports...")
    try:
        main_excel = site_output / "competitors_analysis.xlsx"
        build_excel_report(
            output_path=main_excel,
            site_config=site_config,
            competitors=competitors,
            products=all_products,
            contacts=all_contacts,
            image_records=all_image_records,
        )
        ok(f"Main report: {main_excel.name}")

        # Also save flat products CSV for quick import
        if all_products:
            import pandas as pd
            df_prod = pd.DataFrame(all_products)
            prod_xlsx = site_output / "products_pricing.xlsx"
            df_prod.to_excel(prod_xlsx, index=False, engine="openpyxl")
            ok(f"Products flat: {prod_xlsx.name}")

        if all_contacts:
            import pandas as pd
            df_cont = pd.DataFrame(all_contacts)
            cont_xlsx = site_output / "contacts.xlsx"
            df_cont.to_excel(cont_xlsx, index=False, engine="openpyxl")
            ok(f"Contacts flat: {cont_xlsx.name}")

    except Exception as e:
        err(f"Excel build failed: {e}")
        traceback.print_exc()

    # ---------- Summary ----------
    elapsed = (datetime.now() - start).seconds
    print(f"\n  Done in {elapsed}s — {len(competitors)} competitors, "
          f"{len(all_products)} products, {saved_images} images")

    return {
        "site": site_key,
        "competitors": len(competitors),
        "products": len(all_products),
        "contacts_with_info": found_contacts,
        "images_saved": saved_images,
        "output_folder": str(site_output),
        "elapsed_seconds": elapsed,
    }


def main(sites_to_run: List[str] = None):
    """
    Run research for all 7 sites (or a subset if sites_to_run is provided).
    sites_to_run: list of site keys from WEBSITES dict, e.g. ["LIGiftBasket"]
    """
    base_output = Path(BASE_OUTPUT)
    base_output.mkdir(parents=True, exist_ok=True)

    if sites_to_run:
        selected = {k: v for k, v in WEBSITES.items() if k in sites_to_run}
    else:
        selected = WEBSITES

    print(f"\n{'='*60}")
    print(f"  HIREN KUMAR — COMPETITIVE RESEARCH SYSTEM")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Websites: {len(selected)}")
    print(f"  Output: {base_output}")
    print(f"{'='*60}")

    all_summaries = []
    for site_key, site_config in selected.items():
        try:
            summary = run_for_website(site_key, site_config, base_output)
            all_summaries.append(summary)
        except Exception as e:
            err(f"FATAL error for {site_key}: {e}")
            traceback.print_exc()
            all_summaries.append({"site": site_key, "error": str(e)})

        time.sleep(DELAY_BETWEEN_SITES)

    # Final summary report
    print(f"\n{'='*60}")
    print(f"  ALL DONE — FINAL SUMMARY")
    print(f"{'='*60}")
    total_comp = total_prod = total_img = 0
    for s in all_summaries:
        site = s.get("site", "?")
        comp = s.get("competitors", 0)
        prod = s.get("products", 0)
        imgs = s.get("images_saved", 0)
        total_comp += comp
        total_prod += prod
        total_img += imgs
        print(f"  {site:30s} | {comp:3d} comps | {prod:4d} products | {imgs:4d} images")
    print(f"  {'TOTAL':30s} | {total_comp:3d} comps | {total_prod:4d} products | {total_img:4d} images")

    # Save summary JSON
    summary_path = base_output / "research_summary.json"
    with open(summary_path, "w") as f:
        json.dump({
            "run_date": datetime.now().isoformat(),
            "sites": all_summaries,
            "totals": {
                "competitors": total_comp,
                "products": total_prod,
                "images": total_img,
            }
        }, f, indent=2)
    print(f"\n  Summary saved: {summary_path}")
    print(f"\n  Open ScrappedMaterial/ to see all results!")


if __name__ == "__main__":
    # Parse optional site filter from command line
    # Usage: python main.py                    (run all)
    # Usage: python main.py LIGiftBasket       (run one)
    # Usage: python main.py LIGiftBasket LongIslandBalloons  (run some)
    filter_sites = sys.argv[1:] if len(sys.argv) > 1 else None
    main(sites_to_run=filter_sites)
