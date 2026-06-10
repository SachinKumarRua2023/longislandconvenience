#!/usr/bin/env python3
"""
Download all 9 fan images to disk so you can VIEW them and confirm they're correct.
Files saved to: HirenTask\preview_images\
"""
import os, requests, sys
sys.stdout.reconfigure(encoding='utf-8')
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

OUT = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\preview_images"
os.makedirs(OUT, exist_ok=True)

sess = requests.Session()
sess.mount('https://', HTTPAdapter(max_retries=Retry(total=2, backoff_factor=1)))
HDR = {'User-Agent':'Mozilla/5.0','Referer':'https://www.pexels.com/'}

def pex(pid):
    return f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?auto=compress&cs=tinysrgb&w=800"

# All 9 images we intend to use — (filename, pexels_id, what_it_should_show)
IMAGES = [
    # Printing Services
    ("1_printing_L_document.jpg",   4386431, "Printing-L: should show DOCUMENT PRINTING / paper coming out of printer"),
    ("2_printing_C_printer.jpg",    4792268, "Printing-C: should show OFFICE PRINTER MACHINE (main/center image)"),
    ("3_printing_R_tshirt.jpg",     3626580, "Printing-R: should show T-SHIRT / CUSTOM PRINT / screen printing"),
    # Business Cards
    ("4_bizcard_L_card_marble.jpg", 6476587, "BizCard-L: should show BUSINESS CARD on clean surface"),
    ("5_bizcard_C_cards_spread.jpg",4974916, "BizCard-C: should show STACK / SPREAD of business cards (main/center)"),
    ("6_bizcard_R_cards_hand.jpg",  7709258, "BizCard-R: should show BUSINESS CARDS held in hand / presented"),
    # Mailing
    ("7_mailing_L_packing.jpg",    4439337, "Mailing-L: should show PERSON PACKING / SEALING a box"),
    ("8_mailing_C_packages.jpg",   4483967, "Mailing-C: should show STACK OF PACKAGES / shipping boxes (main/center)"),
    ("9_mailing_R_delivery.jpg",   6868481, "Mailing-R: should show DELIVERY / packages at door"),
]

print("Downloading 9 fan images to preview_images\\ folder...")
print(r"Open Windows Explorer -> Desktop -> HirenTask -> preview_images" + "\n")

results = []
for fname, pid, desc in IMAGES:
    url = pex(pid)
    fpath = os.path.join(OUT, fname)
    try:
        r = sess.get(url, headers=HDR, timeout=20)
        if r.status_code == 200 and len(r.content) > 5000:
            with open(fpath, 'wb') as f:
                f.write(r.content)
            kb = len(r.content)//1024
            print(f"  OK   {fname} ({kb}KB)")
            results.append((fname, pid, desc, 'OK', kb))
        else:
            print(f"  FAIL {fname} — status={r.status_code} size={len(r.content)}")
            results.append((fname, pid, desc, 'FAIL', 0))
    except Exception as e:
        print(f"  ERR  {fname} — {e}")
        results.append((fname, pid, desc, 'ERR', 0))

print(f"\n{'='*65}")
print("REVIEW EACH IMAGE — tell me which ones are WRONG:")
print(f"{'='*65}")
for fname, pid, desc, status, kb in results:
    mark = "✓" if status == 'OK' else "✗ FAILED"
    print(f"\n  {mark}  {fname}")
    print(f"      Pexels ID: {pid}")
    print(f"      EXPECTED:  {desc}")

print(f"\n{'='*65}")
print(f"Files saved to: {OUT}")
print("Open that folder, look at each image, then tell me:")
print("  - Which number images are WRONG")
print("  - What the image ACTUALLY shows (wrong subject)")
print("We will replace those IDs immediately.")
print(f"{'='*65}")

# Also open the folder in Windows Explorer
os.startfile(OUT)
