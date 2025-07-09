import Link from 'next/link';

export default function GlengarryIndexPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-4">Glengarry 100: The Open SMB Marketplace Index</h1>
      <p className="text-lg font-medium mb-6">Verified Brokers. Transparent Listings. No Paywalls.</p>

      <div className="prose prose-sm sm:prose lg:prose-lg mb-10 max-w-none">
        <h2>🌍 Mission</h2>
        <p>
          Glengarry100 is the open, verifiable alternative to BizBuySell and CoStar — a transparent,
          broker-first database of businesses for sale. We spotlight the top 100 brokers by real listing
          activity, not pay-to-play placement.
        </p>
        <p>
          We believe small business M&A deserves the same openness Wikipedia brought to knowledge and
          Linux brought to code. Brokers hate paywalls. Buyers hate junk. We're here to fix both.
        </p>

        <h2>🔍 What We’ve Built So Far</h2>
        <ul>
          <li>Daily-scraped listings from brokers sites (via public API scraping)</li>
          <li>Matched listings to known broker websites (~2,000 URLs)</li>
          <li>Live leaderboard at <a href="https://glengarry100.vercel.app">glengarry100.vercel.app</a></li>
          <li>Master Broker Directory with over 2,000+ brokers (<code>broker_master_public.csv</code>)</li>
        </ul>

        <h2>🧠 Core Philosophy</h2>
        <ul>
          <li>Openness over gatekeeping</li>
          <li>Verification over spam</li>
          <li>Broker-first over pay-to-rank</li>
          <li>Transparency over clickbait</li>
        </ul>
        <blockquote>
          <p>🧠 Linus Torvalds: "Good software comes from transparency and iteration."</p>
          <p>🌐 Jimmy Wales: "Imagine a world in which every person has free access to all knowledge."</p>
        </blockquote>
        <p>We're applying those ideas to business buying/selling.</p>

        <h2>🚀 What You Can Do</h2>
        <h3>🧑‍💻 Developers:</h3>
        <ul>
          <li>Help us build scrapers for major franchise brokers (e.g. Transworld, Sunbelt, Murphy, VR)</li>
          <li>Expand our matching engine to connect scraped listings to broker sites</li>
          <li>Help us verify listings, deduplicate spam, and analyze relist churn</li>
          <li>Create tools that let brokers push listings directly via open schema</li>
        </ul>

        <h3>🕵️‍♂️ Data Detectives:</h3>
        <ul>
          <li>Help label "zombie listings" or fake listings in our scraped dataset</li>
          <li>Identify brokers with no real activity</li>
          <li>Help us clean and score the 50,000+ records already scraped</li>
        </ul>

        <h3>📬 Outreach/Community:</h3>
        <ul>
          <li>Join our cold email campaign to franchise offices</li>
          <li>Submit verified listing sitemaps or direct URLs to speed up matching</li>
          <li>Spread the word on Twitter, Reddit, Hacker News, Indie Hackers, Product Hunt</li>
        </ul>

        <h2>📊 The Glengarry Index (Coming Soon)</h2>
        <ul>
          <li>Total scraped vs verified listings</li>
          <li>Junk/fake/zombie listing count</li>
          <li>Broker leaderboard by real activity</li>
          <li>CSV export of each day’s snapshot</li>
        </ul>

        <h2>🔧 Tech Stack</h2>
        <ul>
          <li>Frontend: Next.js + Tailwind + Vercel</li>
          <li>Backend: Supabase (Postgres + Auth)</li>
          <li>Scrapers: Python + curl_cffi + BeautifulSoup + SerpAPI</li>
          <li>Open Data: CSV-based, GitHub-first</li>
        </ul>

        <h2>🏗️ Future Vision</h2>
        <ul>
          <li>A public, verified marketplace API — free for buyers, sellers, brokers</li>
          <li>Live broker dashboards to claim, manage, and push listings</li>
          <li>Broker transparency tools (response time, listing score, reviews)</li>
          <li>Expansion into CRE and franchise data</li>
        </ul>

        <h2>📎 Files in This Repo</h2>
        <ul>
          <li><code>broker_master_public.csv</code>: deduped, enriched public broker dataset</li>
          <li><code>bizbuysell_listings.json</code>: current scraped dataset (daily updated)</li>
          <li><code>pages/</code>: frontend pages (/, /daily, /glengarry-index)</li>
          <li><code>components/</code>: leaderboard + broker cards</li>
          <li><code>lib/</code>: Supabase and matching utilities</li>
        </ul>

        <h2>🙌 Why This Matters</h2>
        <p>
          BizBuySell claims 50,000+ listings — but we’ve found only ~8,000 real ones. <br />
          CoStar charges brokers $1,000/month to see their own marketplace. <br />
          We’re not just a startup. We’re a reckoning.
        </p>
        <p><strong>This is Glengarry. And we’re just getting started.</strong></p>

        <h2>📫 Contact / Contribute</h2>
        <p>
          Twitter: <a href="https://twitter.com/glengarry100">@glengarry100</a><br />
          Email: <a href="mailto:jasosville@gmail.com">jasosville@gmail.com</a><br />
          Site: <a href="https://glengarry100.vercel.app">glengarry100.vercel.app</a>
        </p>

        <blockquote>
          <p>“Always be verifying.” — Not Alec Baldwin</p>
        </blockquote>
      </div>

      <a
        href="/bizbuysell_listings_daily.csv"
        download
        className="inline-block mb-6 text-blue-600 underline hover:text-blue-800"
      >
        📥 Download Today's Audit CSV
      </a>

      <div className="overflow-x-auto mb-8">
        <table className="table-auto w-full border-collapse border border-gray-300 text-sm">
          <thead>
            <tr className="bg-gray-100">
              <th className="border px-4 py-2 text-left">Category</th>
              <th className="border px-4 py-2 text-right">Count</th>
              <th className="border px-4 py-2 text-right">% of Total</th>
            </tr>
          </thead>
          <tbody>
            <tr><td className="border px-4 py-2">Total Listings Audited</td><td className="border px-4 py-2 text-right">52,436</td><td className="border px-4 py-2 text-right">100.00%</td></tr>
            <tr><td className="border px-4 py-2">Listings with Broker Info</td><td className="border px-4 py-2 text-right">32,453</td><td className="border px-4 py-2 text-right">61.89%</td></tr>
            <tr><td className="border px-4 py-2">Listings with Broker + Financials</td><td className="border px-4 py-2 text-right">20,481</td><td className="border px-4 py-2 text-right">39.06%</td></tr>
            <tr><td className="border px-4 py-2">Unmatched Listings (No Broker)</td><td className="border px-4 py-2 text-right">19,983</td><td className="border px-4 py-2 text-right">38.11%</td></tr>
            <tr><td className="border px-4 py-2">Unmatched + Fallback Contact Only</td><td className="border px-4 py-2 text-right">4,090</td><td className="border px-4 py-2 text-right">7.80%</td></tr>
            <tr><td className="border px-4 py-2">Unmatched + Fallback Contact + Financials</td><td className="border px-4 py-2 text-right">551</td><td className="border px-4 py-2 text-right">1.05%</td></tr>
            <tr className="font-bold bg-yellow-50"><td className="border px-4 py-2">Fully Real Listings After All Filters</td><td className="border px-4 py-2 text-right">17,652</td><td className="border px-4 py-2 text-right">33.66%</td></tr>
          </tbody>
        </table>
      </div>

      <p className="mb-6">
        Only 1 in 3 listings on BizBuySell are real: they have a broker, financials, and a valid source. The rest? Duplicates, ghost listings, franchise ads, or financial black boxes.
      </p>

      <p className="mb-6 font-semibold">
        You're not browsing 52,000 businesses for sale. You're browsing 17,000 maybe real ones.
      </p>

      <p className="mb-8 text-lg font-medium">This is why we built the Glengarry Index.</p>

      <Link href="/daily">
        <a className="inline-block bg-black text-white px-6 py-3 rounded-lg shadow hover:bg-gray-800 transition">
          🔎 View Today's Verified Listings
        </a>
      </Link>
    </div>
  );
}
