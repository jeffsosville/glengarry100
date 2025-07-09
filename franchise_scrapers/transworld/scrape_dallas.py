import requests
import json
import time
from datetime import datetime

def normalize_listing(raw):
    return {
        "title": raw.get("name"),
        "listing_id": str(raw.get("id")),
        "source": "tworld_dallas",
        "source_url": "https://www.tworld.com" + raw.get("url", ""),
        "location": {
            "city": raw.get("city"),
            "state": raw.get("state"),
            "county": None
        },
        "price": raw.get("c_listing_price__c"),
        "cash_flow": raw.get("c_discretionary_earnings__c"),
        "gross_revenue": raw.get("c_gross_revenue__c"),
        "down_payment": raw.get("c_down_payment__c"),
        "description": raw.get("c_teaser__c"),
        "broker": {
            "name": None,
            "email": None,
            "phone": None
        },
        "date_scraped": datetime.utcnow().isoformat()
    }

def scrape_tworld_dallas():
    base_url = "https://www.tworld.com/api/listings"
    tribe_slug = "dallasfortworthcentral"
    page = 1
    all_listings = []

    while True:
        payload = {
            "page": page,
            "per_page": 20,
            "country": {"value": 4, "name": "United States"},
            "sort": {"value": "-c_listing_price__c", "name": "Price ($$$ to $)"},
            "tribe_slug": tribe_slug
        }

        print(f"[TWorld Dallas] Fetching page {page}...")
        resp = requests.post(base_url, json=payload)
        resp.raise_for_status()
        data = resp.json()

        raw_listings = data.get("results", [])
        if not raw_listings:
            print("[TWorld Dallas] No more listings.")
            break

        for raw in raw_listings:
            all_listings.append(normalize_listing(raw))

        if not data.get("has_next"):
            break

        page += 1
        time.sleep(1)

    print(f"[TWorld Dallas] ✅ Scraped {len(all_listings)} listings.")
    return all_listings


if __name__ == "__main__":
    listings = scrape_tworld_dallas()

    # Save locally
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
    output_path = f"outputs/listings/tworld_dallas_{ts}.json"
    with open(output_path, "w") as f:
        json.dump(listings, f, indent=2)
    print(f"📄 Results saved to {output_path}")

    # Optional: push to Supabase
    # from supabase import insert_bulk
    # insert_bulk("external_broker_listings", listings)
