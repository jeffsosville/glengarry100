Glengarry 100: The Open SMB Marketplace Index

Verified Brokers. Transparent Listings. No Paywalls.

🌍 Mission

Glengarry100 is the open, verifiable alternative to BizBuySell and CoStar — a transparent, broker-first database of businesses for sale. We spotlight the top 100 brokers by real listing activity, not pay-to-play placement.

We believe small business M&A deserves the same openness Wikipedia brought to knowledge and Linux brought to code. Brokers hate paywalls. Buyers hate junk. We're here to fix both.

🔍 What We’ve Built So Far

Daily-scraped listings from brokers sites (via public API scraping)

Matched listings to known broker websites (~2,000 URLs)

Live leaderboard at glengarry100.vercel.app

Master Broker Directory with over 2,000+ brokers (see broker_master_public.csv)

🧠 Core Philosophy

Openness over gatekeeping

Verification over spam

Broker-first over pay-to-rank

Transparency over clickbait

Inspired by the values of:

🧠 Linus Torvalds: "Good software comes from transparency and iteration."

🌐 Jimmy Wales: "Imagine a world in which every person has free access to all knowledge."

We're applying those ideas to business buying/selling.

🚀 What You Can Do

🧑‍💻 Developers:

Help us build scrapers for major franchise brokers (e.g. Transworld, Sunbelt, Murphy, VR)

Expand our matching engine to connect scraped listings to broker sites

Help us verify listings, deduplicate spam, and analyze relist churn

Create tools that let brokers push listings directly via open schema

🕵️‍♂️ Data Detectives:

Help label "zombie listings" or fake listings in our scraped dataset

Identify brokers with no real activity

Help us clean and score the 50,000+ records already scraped

📬 Outreach/Community:

Join our cold email campaign to franchise offices

Submit verified listing sitemaps or direct URLs to speed up matching

Spread the word on Twitter, Reddit, Hacker News, Indie Hackers, Product Hunt

📊 The Glengarry Index (Coming Soon)

A daily-updated transparency report showing:

Total scraped vs verified listings

Junk/fake/zombie listing count

Broker leaderboard by real activity

CSV export of each day’s snapshot

🔧 Tech Stack

Frontend: Next.js + Tailwind + Vercel

Backend: Supabase (Postgres + Auth)

Scrapers: Python + curl_cffi + BeautifulSoup + SerpAPI

Open Data: CSV-based, GitHub-first

🏗️ Future Vision

A public, verified marketplace API — free for buyers, sellers, brokers

Live broker dashboards to claim, manage, and push listings

Broker transparency tools (response time, listing score, reviews)

Expansion into CRE and franchise data

📎 Files in This Repo

broker_master_public.csv: deduped, enriched public broker dataset

bizbuysell_listings.json: current scraped dataset (daily updated)

pages/: frontend pages (/, /daily, /glengarry-index)

components/: leaderboard + broker cards

lib/: Supabase and matching utilities

🙌 Why This Matters

BizBuySell claims 50,000+ listings — but we’ve found only ~8,000 real ones.
CoStar charges brokers $1,000/month to see their own marketplace.
We’re not just a startup. We’re a reckoning.

This is Glengarry. And we’re just getting started.

Project Governance & Contributors
Glengarry100 is spearheaded by Jeff Sosville, with community contributions welcomed via pull requests, issues, and research submissions.

We operate under a benevolent dictator model to keep the mission focused and high signal:

PRs are welcome

Contributions are openly credited

Final direction, roadmap, and strategic pivots are stewarded by Jeff

Major contributions will be publicly acknowledged on our site and in release notes.


📫 Contact / Contribute

Twitter: @glengarry100

Email: jasosville@gmail.com

Site: glengarry100.vercel.app

"Always be verifying." — Not Alec Baldwin
