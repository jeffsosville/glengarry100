import { useEffect, useState } from "react";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

type Listing = {
  id: number;
  header: string;
  location: string;
  price: number;
  cashFlow: number;
  ebitda: number;
  description: string;
  brokerContactFullName: string;
  brokerCompany: string;
  listings_url: string;
};

export default function DailyListings() {
  const [listings, setListings] = useState<Listing[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchListings = async () => {
      const { data, error } = await supabase
        .from("todays_listings") // ✅ NEW table name
        .select("*")
        .or("price.not.is.null,cashFlow.not.is.null,ebitda.not.is.null")
        .not("listings_url", "is", null)
        .limit(100); // removed .order("created_at") for safety

      if (error) {
        setError(error.message);
        console.error("Error loading listings:", error.message);
      } else {
        setListings(data);
      }
    };

    fetchListings();
  }, []);

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">🧮 Verified Listings — Today</h1>

      {error && <div className="text-red-500">Error: {error}</div>}
      {!listings?.length && !error && (
        <div className="text-gray-500">Loading verified listings...</div>
      )}

      <ul className="space-y-6">
        {listings?.map((listing) => (
          <li
            key={listing.id}
            className="border p-4 rounded-lg shadow hover:bg-gray-50 transition"
          >
            <h2 className="text-xl font-semibold mb-1">
              {listing.listings_url ? (
                <a
                  href={listing.listings_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline"
                >
                  {listing.header || "Untitled Listing"}
                </a>
              ) : (
                listing.header || "Untitled Listing"
              )}
            </h2>

            <p className="text-sm text-gray-600 mb-1">
              {listing.location || "Unknown location"}
            </p>

            {listing.price && (
              <p className="text-green-700 font-bold">
                💰 ${listing.price.toLocaleString()}
              </p>
            )}

            {listing.cashFlow && (
              <p className="text-blue-700 text-sm">
                💵 Cash Flow: ${listing.cashFlow.toLocaleString()}
              </p>
            )}

            {listing.ebitda && (
              <p className="text-blue-500 text-sm">
                📊 EBITDA: ${listing.ebitda.toLocaleString()}
              </p>
            )}

            <p className="text-sm mt-2 text-gray-700">
              Broker:{" "}
              <strong>
                {listing.brokerContactFullName
                  ? `${listing.brokerContactFullName} (${listing.brokerCompany})`
                  : "Unknown"}
              </strong>
            </p>

            {listing.description && (
              <p className="text-sm mt-2 text-gray-600 line-clamp-3">
                {listing.description}
              </p>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
