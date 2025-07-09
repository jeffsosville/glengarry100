# vestedbb_api.py

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from utils.normalize import normalize_listing

def scrape_vestedbb_api(max_pages=50):
    print("[VestedBB-API] Scraping via POST endpoint...")

    url = "https://www.vestedbb.com/script/listing_search_ajax.php"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    listings = []
    seen_urls = set()

    for page_num in range(1, max_pages + 1):
        print(f"[VestedBB-API] Requesting page {page_num}...")
        payload = {
            "page": str(page_num),
            "default_search": "1",
            "sort_by": "ListingDate:HL",
        }

        resp = requests.post(url, headers=headers, data=payload)
        if not resp.ok or not resp.text.strip():
            print(f"[VestedBB-API] Stopped at page {page_num} (empty or error).")
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.select(".product-box")
        print(f"[VestedBB-API] Found {len(cards)} listings")

        if not cards:
            break

        for card in cards:
            try:
                a_tag = card.select_one(".name a")
                title = a_tag.text.strip()
                detail_url = a_tag["href"]
                if not detail_url.startswith("http"):
                    detail_url = "https://www.vestedbb.com/" + detail_url.lstrip("/")

                if detail_url in seen_urls:
                    continue
                seen_urls.add(detail_url)

                def clean_money(li):
                    return (
                        li.text.split(":", 1)[-1].replace("$", "").replace(",", "").strip()
                        if li else None
                    )

                raw = {
                    "title": title,
                    "source_url": detail_url,
                    "asking_price": clean_money(card.find("li", string=lambda s: s and "Asking Price:" in s)),
                    "cash_flow": clean_money(card.find("li", string=lambda s: s and "Cash Flow:" in s)),
                    "down_payment": clean_money(card.find("li", string=lambda s: s and "Down Payment:" in s)),
                }

                normalized = normalize_listing(raw, source="vestedbb")
                listings.append(normalized)

            except Exception as e:
                print(f"[VestedBB-API] Parse error: {e}")
                continue

    print(f"[VestedBB-API] ✅ Scraped {len(listings)} listings.")
    return listings

# CLI runner
if __name__ == "__main__":
    results = scrape_vestedbb_api()

    print("\n🧪 Sample output:")
    print(json.dumps(results[0], indent=2) if results else "None")

    out_dir = "outputs/listings"
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
    path = os.path.join(out_dir, f"vestedbb_api_{ts}.json")

    with open(path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n📄 Results saved to {path}")
