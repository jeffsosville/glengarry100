import Link from 'next/link';

export default function GlengarryIndexPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-6">The Glengarry Index</h1>
      <p className="mb-4 text-lg">
        We audited all 52,000+ listings on BizBuySell. Here’s what we found—and what it means for anyone serious about buying or selling a business.
      </p>

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

      <a
        href="/data/glengarry_index_audit.csv"
        download
        className="inline-block text-blue-600 underline hover:text-blue-800 transition mb-8"
      >
        ⬇️ Download Full CSV Audit
      </a>

      <p className="mb-8 text-lg font-medium">
        This is why we built the Glengarry Index.
      </p>

      <Link href="/daily">
        <a className="inline-block bg-black text-white px-6 py-3 rounded-lg shadow hover:bg-gray-800 transition">
          🔎 View Today's Verified Listings
        </a>
      </Link>
    </div>
  );
}
