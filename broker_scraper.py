import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import sqlite3
from datetime import datetime
import logging
from dataclasses import dataclass
from urllib.parse import urlparse
import json
from typing import List, Optional

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class BusinessListing:
    url: str
    broker_name: str = "N/A"
    company_name: str = "N/A"
    broker_city: str = "N/A"
    broker_state: str = "N/A"
    broker_phone: str = "N/A"
    broker_email: str = "N/A"
    title: str = "N/A"
    price: str = "N/A"
    location: str = "N/A"
    description: str = "N/A"
    business_type: str = "N/A"
    contact_info: str = "N/A"
    scraped_date: str = ""
    active_listings_count: int = 0

class CSVBusinessScraper:
    def __init__(self, csv_file: str, max_workers: int = 10):
        self.csv_file = csv_file
        self.max_workers = max_workers
        self.listings = []
        self.failed_urls = []
        self.requests_per_second = 2
        self.domain_last_request = {}
        self.db_path = "scraping_progress.db"
        self.init_database()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }

    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scraped_listings (
                url TEXT PRIMARY KEY,
                broker_name TEXT,
                company_name TEXT,
                broker_city TEXT,
                broker_state TEXT,
                broker_phone TEXT,
                broker_email TEXT,
                active_listings_count INTEGER,
                title TEXT,
                price TEXT,
                location TEXT,
                description TEXT,
                business_type TEXT,
                contact_info TEXT,
                scraped_date TEXT,
                success BOOLEAN
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS failed_urls (
                url TEXT PRIMARY KEY,
                error_message TEXT,
                attempts INTEGER DEFAULT 1,
                last_attempt TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def load_urls_from_csv(self) -> List[dict]:
        try:
            df = pd.read_csv(self.csv_file)
            url_data = []
            for _, row in df.iterrows():
                if pd.notna(row.get('listing_url')):
                    url_data.append({
                        'url': row['listing_url'],
                        'broker_name': row.get('broker_name', 'N/A'),
                        'company_name': row.get('company_name', 'N/A'),
                        'city': row.get('city', 'N/A'),
                        'state': row.get('state', 'N/A'),
                        'phone': row.get('phone', 'N/A'),
                        'email': row.get('email', 'N/A'),
                        'active_listings': row.get('active_listings', 0),
                        'company_url': row.get('companyUrl', 'N/A')
                    })
            logger.info(f"Loaded {len(url_data)} URLs from {self.csv_file}")
            return url_data
        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            return []

    def get_already_scraped(self) -> set:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT url FROM scraped_listings WHERE success = 1')
        scraped = {row[0] for row in cursor.fetchall()}
        conn.close()
        return scraped

    def rate_limit_domain(self, url: str):
        domain = urlparse(url).netloc
        now = time.time()
        if domain in self.domain_last_request:
            time_since_last = now - self.domain_last_request[domain]
            min_interval = 1.0 / self.requests_per_second
            if time_since_last < min_interval:
                time.sleep(min_interval - time_since_last)
        self.domain_last_request[domain] = time.time()

    def extract_listing_data(self, soup: BeautifulSoup, url: str, broker_info: dict) -> BusinessListing:
        def safe_extract(selectors: List[str]) -> str:
            for selector in selectors:
                try:
                    element = soup.select_one(selector)
                    if element:
                        return element.get_text(strip=True)
                except:
                    continue
            return "N/A"

        domain = urlparse(url).netloc.lower()
        title_selectors = ['h1', '.listing-title', '.business-title']
        price_selectors = ['.price', '.asking-price']
        location_selectors = ['.location', '.address']
        description_selectors = ['.description', '.summary']
        business_type_selectors = ['.business-type', '.category']
        contact_selectors = ['.contact', '.phone', '.email']

        return BusinessListing(
            url=url,
            broker_name=broker_info.get('broker_name', 'N/A'),
            company_name=broker_info.get('company_name', 'N/A'),
            broker_city=broker_info.get('city', 'N/A'),
            broker_state=broker_info.get('state', 'N/A'),
            broker_phone=broker_info.get('phone', 'N/A'),
            broker_email=broker_info.get('email', 'N/A'),
            active_listings_count=broker_info.get('active_listings', 0),
            title=safe_extract(title_selectors),
            price=safe_extract(price_selectors),
            location=safe_extract(location_selectors),
            description=safe_extract(description_selectors),
            business_type=safe_extract(business_type_selectors),
            contact_info=safe_extract(contact_selectors),
            scraped_date=datetime.now().isoformat()
        )

    def scrape_single_url(self, url_data: dict) -> Optional[BusinessListing]:
        url = url_data['url']
        try:
            self.rate_limit_domain(url)
            session = requests.Session()
            session.headers.update(self.headers)
            response = session.get(url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            listing = self.extract_listing_data(soup, url, url_data)
            self.save_to_database(listing, success=True)
            return listing
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            failed_listing = BusinessListing(
                url=url,
                broker_name=url_data.get('broker_name', 'N/A'),
                company_name=url_data.get('company_name', 'N/A')
            )
            self.save_to_database(failed_listing, success=False, error=str(e))
            return None

    def save_to_database(self, listing: BusinessListing, success: bool = True, error: str = ""):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if success:
            cursor.execute('''
                INSERT OR REPLACE INTO scraped_listings 
                (url, broker_name, company_name, broker_city, broker_state, broker_phone, broker_email,
                 active_listings_count, title, price, location, description, business_type, contact_info, scraped_date, success)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                listing.url, listing.broker_name, listing.company_name, listing.broker_city,
                listing.broker_state, listing.broker_phone, listing.broker_email,
                listing.active_listings_count, listing.title, listing.price, listing.location,
                listing.description, listing.business_type, listing.contact_info,
                listing.scraped_date, success
            ))
        else:
            cursor.execute('''
                INSERT INTO failed_urls (url, error_message, attempts, last_attempt)
                VALUES (?, ?, 1, ?)
                ON CONFLICT(url) DO UPDATE SET 
                    attempts = attempts + 1,
                    error_message = excluded.error_message,
                    last_attempt = excluded.last_attempt
            ''', (listing.url, error, datetime.now().isoformat()))
        conn.commit()
        conn.close()

    def scrape_all_urls(self):
        all_url_data = self.load_urls_from_csv()
        if not all_url_data:
            logger.error("No URLs found in CSV file")
            return
        already_scraped = self.get_already_scraped()
        urls_to_scrape = [data for data in all_url_data if data['url'] not in already_scraped]
        logger.info(f"Scraping {len(urls_to_scrape)} URLs ({len(already_scraped)} already done)")
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_url = {
                executor.submit(self.scrape_single_url, url_data): url_data['url']
                for url_data in urls_to_scrape
            }
            completed = 0
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    listing = future.result()
                    if listing:
                        self.listings.append(listing)
                    completed += 1
                    if completed % 50 == 0:
                        logger.info(f"Progress: {completed}/{len(urls_to_scrape)} URLs processed")
                except Exception as e:
                    logger.error(f"Error processing {url}: {e}")
        logger.info(f"Scraping completed. {len(self.listings)} listings scraped successfully")

    def export_results(self, format: str = 'csv'):
        if not self.listings:
            self.load_from_database()
        if format == 'csv':
            df = pd.DataFrame([listing.__dict__ for listing in self.listings])
            filename = f"business_listings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(filename, index=False)
            logger.info(f"Results exported to {filename}")
        elif format == 'json':
            filename = f"business_listings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump([listing.__dict__ for listing in self.listings], f, indent=2)
            logger.info(f"Results exported to {filename}")

    def load_from_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM scraped_listings WHERE success = 1')
        rows = cursor.fetchall()
        self.listings = [BusinessListing(*row[:16]) for row in rows]
        conn.close()
        logger.info(f"Loaded {len(self.listings)} listings from database")

    def get_stats(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM scraped_listings WHERE success = 1')
        successful = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM failed_urls')
        failed = cursor.fetchone()[0]
        conn.close()
        return {
            'successful': successful,
            'failed': failed,
            'total': successful + failed,
            'success_rate': f"{(successful / (successful + failed) * 100):.1f}%" if (successful + failed) > 0 else "0%"
        }

def main():
    scraper = CSVBusinessScraper(csv_file="data/broker_master_public.csv", max_workers=10)
    scraper.scrape_all_urls()
    scraper.export_results('csv')
    scraper.export_results('json')
    stats = scraper.get_stats()
    print(f"Scraping Stats: {stats}")

if __name__ == "__main__":
    main()
