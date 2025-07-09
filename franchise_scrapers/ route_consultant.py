# route_consultant.py

import requests
import json
import os
from datetime import datetime
from utils.normalize import normalize_listing  # assumes same pattern you're using

def scrape_route_consultant():
    print("[RouteConsultant] Scraping via POST API...")

    url = "https://listings.routeconsultant.com/wp-json/routeconsultant/v1/filter-routes"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    data = "region=&category=&price=&sba=0&offset=0"

    resp = requests.post(url, headers=headers, data=data)
    resp.raise_for_status()

    json_data = resp.json()
    listings = []

    for item in json_data.get("data", []):
        try:
            raw = {
                "title": item.get("title", "").strip(),
                "detail_url": item.get("permalink"),
                "asking_price": item.get("asking_price", "").strip(),
                "cash_flow": item.get("cashflow", "").strip(),
                "down_payment": item.get("downpayment", "").strip(),
                "location": item.get("location", "").strip(),
            }
            normalized = normalize_listing(raw, source="routeconsultant")
            listings.append(normalized)
        except Exception as e:
            print(f"[RouteConsultant] Parse error: {e}")
            continue

    print(f"[RouteConsultant] ✅ Scraped {len(listings)} listings.")
    return listings

# Save to JSON
if __name__ == "__main__":
    results = scrape_route_consultant()
    if results:
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
        path = f"outputs/listings/routeconsultant_{ts}.json"
        os.makedirs("outputs/listings", exist_ok=True)
        with open(path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"📄 Saved to {path}")
