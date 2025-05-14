from bs4 import BeautifulSoup
import requests
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

BROKER_NAME = "Ron Slusser"
COMPANY_NAME = "Routes For Sale"
SOURCE_URL = "https://www.routesforsale.net/route-listings.html"

def scrape_all_tables():
    res = requests.get(SOURCE_URL)
    soup = BeautifulSoup(res.text, "html.parser")

    headers = soup.find_all(["h3", "h4"])
    inserted = 0

    for header in headers:
        # Get next <table> after this header
        table = header.find_next("table")
        if not table:
            continue

        route_type = header.get_text(strip=True)
        rows = table.select("tbody tr")
        
        for row in rows:
            cells = row.find_all("td")
            if len(cells) < 7:
                continue

            detail_url = cells[6].find("a")["href"] if cells[6].find("a") else None

            data = {
                "broker_name": BROKER_NAME,
                "company_name": COMPANY_NAME,
                "source_url": SOURCE_URL,
                "route_type": route_type,
                "title": cells[0].get_text(strip=True),
                "location": cells[1].get_text(strip=True),
                "asking_price": cells[2].get_text(strip=True),
                "financing": cells[3].get_text(strip=True),
                "cash_flow": cells[4].get_text(strip=True),
                "status": cells[5].get_text(strip=True),
                "detail_url": detail_url,
            }

            print(f"✅ {data['route_type']} | {data['title']} | {data['location']} | {data['asking_price']}")
            supabase.table("external_broker_listings").insert(data).execute()
            inserted += 1

    print(f"\n🎉 Inserted {inserted} listings across all tables.")

if __name__ == "__main__":
    scrape_all_tables()
