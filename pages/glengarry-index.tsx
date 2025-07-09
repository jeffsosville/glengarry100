import Link from "next/link";

export default function GlengarryIndexPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-12 text-base leading-relaxed space-y-6">
      <h1 className="text-4xl font-bold">Glengarry 100</h1>
      <h2 className="text-xl font-semibold">The Open SMB Marketplace Index</h2>
      <p className="text-lg font-medium">Verified Brokers. Transparent Listings. No Paywalls.</p>

      <hr className="my-8" />

      <h3 className="text-2xl font-semibold">Mission</h3>
      <p>
        Glengarry100 is the open, verifiable alternative to BizBuySell and CoStar — a transparent, broker-first database
        of businesses for sale. We spotlight the top 100 brokers by real listing activity, not pay-to-play placement.
      </p>
      <p>
        We believe small business M&A deserves the same openness Wikipedia brought to knowledge and Linux brought to code.
        Brokers hate paywalls. Buyers hate junk. We're here to fix both.
      </p>

      <h3 className="text-2xl font-semibold mt-10">What We’ve Built So Far</h3>
      <ul className="list-disc list-inside space-y-2">
        <li>Daily-scraped listings from brokers sites (via public API scraping)</li>
        <li>Matched listings to known broker websites (~2,000 URLs)</li>
        <li>Live leaderboard at glengarry100.vercel.app</li>
        <li>Master Broker Directory with over 2,000+ brokers (broker_master_public.csv)</li>
      </ul>

      <h3 className="text-2xl font-semibold mt-10">Core Philosophy</h3>
      <ul className="list-disc list-inside space-y-2">
        <li>Openness over gatekeeping</li>
        <li>Verification over spam</li>
        <li>Broker-first over pay-to-rank</li>
        <li>Transparency over clickbait</li>
      </ul>

      <blockquote className="border-l-4 border-gray-400 pl-4 italic">
        “Good software comes from transparency and iteration.” — Linus Torvalds
      </blockquote>
      <blockquote className="border-l-4 border-gray-400 pl-4 italic">
        “Imagine a world in which every person has free access to all knowledge.” — Jimmy Wales
      </blockquote>

      <h3 className="text-2xl font-semibold mt-10">What You Can Do</h3>

      <p className="font-semibold">Developers:</p>
      <ul className="list-disc list-inside space-y-1">
        <li>Help us build scrapers for major franchise brokers (e.g. Transworld, Sunbelt, Murphy, VR)</li>
        <li>Expand our matching engine to connect scraped listings to broker sites</li>
        <li>Verify listings, deduplicate spam, and analyze relist churn</li>
        <li>Create tools that let brokers push listings directly via open schema</li>
      </ul>

      <p className="font-semibold mt-6">Data Detectives:</p>
      <ul className="list-disc list-inside space-y-1">
        <li>Help label "zombie listings" or fake listings in our dataset</li>
        <li>Identify brokers with no real activity</li>
        <li>Help clean and score the 50,000+ records already scraped</li>
      </ul>

      <p className="font-semibold mt-6">Outreach / Community:</p>
      <ul className="list-disc list-inside space-y-1">
        <li>Join our cold email campaign to franchise offices</li>
        <li>Submit verified listing sitemaps or direct URLs</li>
        <li>Spread the word on Twitter, Reddit, Hacker News, Indie Hackers, Product Hunt</li>
      </ul>

      <h3 className="text-2xl font-semibold mt-10">The Glengarry Index (Coming Soon)</h3>
      <ul className="list-disc list-inside space-y-1">
        <li>Daily audit of total vs. verified listings</li>
        <li>Zombie and duplicate count</li>
        <li>Broker leaderboard by real activity</li>
        <li>Downloadable CSV snapshot each day</li>
      </ul>

      <h3 className="text-2xl font-semibold mt-10">Tech Stack</h3>
      <ul className="list-disc list-inside space-y-1">
        <li>Frontend: Next.js + Tailwind + Vercel</li>
        <li>Backend: Supabase (Postgres + Auth)</li>
        <li>Scrapers: Python + curl_cffi + BeautifulSoup + SerpAPI</li>
        <li>Open Data: CSV-based, GitHub-first</li>
      </ul>

      <h3 className="text-2xl font-semibold mt-10">Future Vision</h3>
      <ul className="list-disc list-inside space-y-1">
        <li>A public, verified marketplace API — free for buyers, sellers, and brokers</li>
        <li>Live broker dashboards to manage listings</li>
        <li>Transparency tools (response time, listing score, reviews)</li>
        <li>Expansion into commercial real estate and franchises</li>
      </ul>

      <h3 className="text-2xl font-semibold mt-10">Why This Matters</h3>
      <p>
        BizBuySell claims 50,000+ listings — but we’ve found only ~8,000 real ones.
        CoStar charges brokers $1,000/month just to access their own marketplace.
      </p>
      <p>
        We’re not just a startup. We’re a reckoning.
        This is Glengarry. And we’re just getting started.
      </p>

      <h3 className="text-2xl font-semibold mt-10">Contact / Contribute</h3>
      <p>Twitter: @glengarry100</p>
      <p>Email: jasosville@gmail.com</p>
      <p>Site: glengarry100.vercel.app</p>

      <hr className="my-8" />

      <p className="font-semibold text-lg">“Always be verifying.” — Not Alec Baldwin</p>

      <hr className="my-8" />

      <Link href="/daily">
        <a className="inline-block bg-black text-white px-6 py-3 rounded-lg shadow hover:bg-gray-800 transition">
          View Today’s Verified Listings
        </a>
      </Link>
    </div>
  );
}
