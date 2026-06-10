"""
Capital One Statement Downloader
Uses your existing Chrome session — no credentials stored.
Run once with --setup to link your Chrome profile, then run normally to download.
"""

import os
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# --- Config ---
DOWNLOAD_DIR = Path(os.getenv("STATEMENT_DOWNLOAD_DIR", "capitalone_statements"))
# Your Chrome user data dir — the script uses your existing logged-in session
CHROME_PROFILE = os.getenv(
    "CHROME_USER_DATA_DIR",
    r"C:\Users\Sachin Kumar\AppData\Local\Google\Chrome\User Data"
)
CHROME_PROFILE_NAME = os.getenv("CHROME_PROFILE_NAME", "Default")


def find_chrome_executable():
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Users\Sachin Kumar\AppData\Local\Google\Chrome\Application\chrome.exe",
    ]
    for path in candidates:
        if Path(path).exists():
            return path
    return None


def download_statements(months: int = 3, headless: bool = False):
    from playwright.sync_api import sync_playwright

    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[+] Saving statements to: {DOWNLOAD_DIR.resolve()}")

    chrome_exe = find_chrome_executable()
    if not chrome_exe:
        print("[!] Chrome not found. Install Chrome or set CHROME_USER_DATA_DIR in .env")
        sys.exit(1)

    with sync_playwright() as p:
        # Launch using your existing Chrome profile (already logged in to Capital One)
        context = p.chromium.launch_persistent_context(
            user_data_dir=CHROME_PROFILE,
            channel="chrome",
            executable_path=chrome_exe,
            headless=headless,
            accept_downloads=True,
            args=["--profile-directory=" + CHROME_PROFILE_NAME],
            slow_mo=500,  # Human-like pacing to avoid bot detection
        )

        page = context.new_page()

        print("[+] Opening Capital One...")
        page.goto("https://myaccounts.capitalone.com/")
        page.wait_for_load_state("networkidle", timeout=30000)

        # Check if logged in
        if "welcome" in page.url.lower() or "login" in page.url.lower():
            print("[!] Not logged in. Please log into Capital One in the Chrome window that opened.")
            print("    After logging in, press Enter here to continue...")
            input()
            page.wait_for_load_state("networkidle", timeout=60000)

        print(f"[+] Logged in. Page: {page.url}")

        # Find all account cards on the dashboard
        page.wait_for_selector("body", timeout=15000)
        time.sleep(2)

        # Capital One shows account tiles — find them
        accounts = []
        # Try multiple selectors Capital One uses
        selectors_to_try = [
            "[data-testid='account-card']",
            ".account-card",
            "[aria-label*='account']",
            "a[href*='/account/']",
        ]
        for sel in selectors_to_try:
            found = page.query_selector_all(sel)
            if found:
                accounts = found
                print(f"[+] Found {len(found)} account(s) using selector: {sel}")
                break

        if not accounts:
            print("[!] Could not auto-detect accounts. Taking a screenshot for inspection...")
            page.screenshot(path="capitalone_debug.png")
            print("    Saved: capitalone_debug.png — review it to see page structure")
            # Fall back: try navigating directly to statements URL pattern
            _try_direct_statement_download(page, DOWNLOAD_DIR, months)
        else:
            for i, account in enumerate(accounts):
                account_name = account.inner_text().strip().split("\n")[0] or f"account_{i+1}"
                print(f"\n[+] Processing: {account_name}")
                try:
                    account.click()
                    page.wait_for_load_state("networkidle", timeout=15000)
                    _download_account_statements(page, DOWNLOAD_DIR, account_name, months)
                    page.go_back()
                    page.wait_for_load_state("networkidle", timeout=10000)
                    time.sleep(1)
                except Exception as e:
                    print(f"    [!] Error on account {account_name}: {e}")
                    page.screenshot(path=f"debug_account_{i}.png")

        print(f"\n[+] Done. Statements saved to: {DOWNLOAD_DIR.resolve()}")
        context.close()


def _download_account_statements(page, download_dir: Path, account_name: str, months: int):
    """Navigate to statements tab and download PDFs."""
    # Look for Statements/Documents tab
    statement_selectors = [
        "text=Statements",
        "text=Documents",
        "[data-testid*='statement']",
        "a[href*='statement']",
        "a[href*='document']",
        "button:has-text('Statements')",
    ]
    clicked = False
    for sel in statement_selectors:
        try:
            el = page.query_selector(sel)
            if el:
                el.click()
                page.wait_for_load_state("networkidle", timeout=10000)
                clicked = True
                print(f"    [+] Opened statements tab")
                break
        except Exception:
            continue

    if not clicked:
        print(f"    [!] Could not find statements tab for {account_name}")
        page.screenshot(path=f"debug_no_statements_{account_name[:20]}.png")
        return

    time.sleep(2)

    # Find PDF download links
    pdf_links = page.query_selector_all("a[href*='.pdf'], a[download], button:has-text('PDF'), a:has-text('Download')")
    print(f"    [+] Found {len(pdf_links)} statement(s)")

    safe_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in account_name)
    account_folder = download_dir / safe_name
    account_folder.mkdir(parents=True, exist_ok=True)

    downloaded = 0
    for link in pdf_links[:months]:  # limit to requested months
        try:
            with page.expect_download(timeout=30000) as dl_info:
                link.click()
            dl = dl_info.value
            filename = dl.suggested_filename or f"statement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            save_path = account_folder / filename
            dl.save_as(save_path)
            print(f"    [+] Downloaded: {filename}")
            downloaded += 1
            time.sleep(1)
        except Exception as e:
            print(f"    [!] Download failed: {e}")

    print(f"    [+] {downloaded} statement(s) saved to {account_folder}")


def _try_direct_statement_download(page, download_dir: Path, months: int):
    """Fallback: navigate directly to known Capital One statement URLs."""
    print("[+] Trying direct navigation to statements page...")
    urls_to_try = [
        "https://myaccounts.capitalone.com/ui/accounts/statement",
        "https://myaccounts.capitalone.com/ui/accounts/documents",
    ]
    for url in urls_to_try:
        try:
            page.goto(url)
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            pdf_links = page.query_selector_all("a[href*='.pdf'], a[download], a:has-text('Download')")
            if pdf_links:
                print(f"[+] Found {len(pdf_links)} statement(s) at {url}")
                _download_account_statements(page, download_dir, "statements", months)
                return
        except Exception as e:
            print(f"    [!] {url} failed: {e}")

    print("[!] Could not find statements automatically.")
    print("    Taking debug screenshot: capitalone_debug_final.png")
    page.screenshot(path="capitalone_debug_final.png", full_page=True)


def main():
    parser = argparse.ArgumentParser(description="Capital One Statement Downloader")
    parser.add_argument("--months", type=int, default=3, help="Number of recent statements to download (default: 3)")
    parser.add_argument("--headless", action="store_true", help="Run browser in background (default: visible)")
    parser.add_argument("--install-browser", action="store_true", help="Install Playwright browsers first")
    args = parser.parse_args()

    if args.install_browser:
        os.system("playwright install chrome")
        return

    download_statements(months=args.months, headless=args.headless)


if __name__ == "__main__":
    main()
