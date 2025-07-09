# franchise_scrapers/routes_for_sale.py

"""
Scraper for RoutesForSale.net
Parses static HTML list of route opportunities and infers category (Bimbo, FedEx, Flowers, etc.)
Normalizes and outputs structured listings.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils.normalize import normalize_listing
import json
import os

URL = "https://www.routesforsale.net/route-listings.html"
BASE = "https://www.routesforsale.net"

def scrape_routes_for_sale():
    print("[RoutesForSale] Starting scrape...")

    resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, "html.parser")

    listings = []
    seen_urls = set()

    all_links = soup.select("table td a[href^='/']")

    for a in all_links:
        try:
            title = a.get_text(strip=True)
            href = a.get("href")
            if not href or "route-listings.html" in href or "contact" in href:
                continue

            full_url = BASE + href if href.startswith("/") else href
            if full_url in seen_urls:
                continue
            seen_urls.add(full_url)

            # Try to extract price from title
            price = None
            if "$" in title:
                try:
                    price = "$" + title.split("$")[-1].split()[0].replace(",", "").strip()
                except:
                    pass

            # Infer category from title
            lowered = title.lower()
            category = None
            if "bimbo" in lowered:
                category = "Bimbo"
            elif "flowers" in lowered:
                category = "Flowers"
            elif "fedex" in lowered:
                category = "FedEx"
            elif "bread" in lowered:
                category = "Bread"
            elif "snapple" in lowered:
                category = "Snapple"
            elif "pepsi" in lowered:
                category = "Pepsi"
            elif "mission" in lowered:
                category = "Mission Tortilla"
            elif "vending" in lowered:
                category = "Vending"
            elif "pool" in lowered:
                category = "Pool Supplies"
            else:
                category = "Other"

            raw = {
                "title": title,
                "detail_url": full_url,
                "asking_price": price,
                "cash_flow": None,
                "down_payment": None,
                "description": category  # inferred type
            }

            normalized = normalize_listing(raw, source="routesforsale")
            listings.append(normalized)

        except Exception as e:
            print(f"[RoutesForSale] Parse error: {e}")
            continue

    print(f"[RoutesForSale] ✅ Scraped {len(listings)} listings.")
    return listings

# CLI runner
if __name__ == "__main__":
    results = scrape_routes_for_sale()
    print(f"\nSample:\n{json.dumps(results[0], indent=2)}")

    outdir = "outputs/listings"
    os.makedirs(outdir, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
    path = os.path.join(outdir, f"routes_for_sale_{ts}.json")
    with open(path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved to {path}")
