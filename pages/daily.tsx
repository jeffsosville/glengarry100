import { useEffect, useState } from "react";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

type Listing = {
  id: string;
  header: string;
  location: string;
  price: number;
  description: string;
};

export default function DailyListings() {
  const [listings, setListings] = useState<Listing[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchListings = async () => {
      const { data, error } = await supabase
        .from("daily_listings")
        .select("id, header, location, price, description")
        .limit(50);

      if (error) {
        setError(error.message);
        console.error("Error loading listings:", error.message);
      } else {
        setListings(data);
        console.log("Listings:", data);
      }
    };

    fetchListings();
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">📬 Daily Listings Digest</h1>

      {error && (
        <div className="text-red-500 font-mono mb-4">
          🧪 Error: {error}
        </div>
      )}

      {!listings?.length && !error && (
        <div className="text-gray-500">📬 No listings found.</div>
      )}

      {listings?.length > 0 && (
        <ul className="space-y-4">
          {listings.map((listing) => (
            <li
              key={listing.id}
              className="border rounded p-4 shadow hover:bg-gray-50 transition"
            >
              <h2 className="text-lg font-semibold">{listing.header}</h2>
              <p className="text-sm text-gray-600">{listing.location}</p>
              {listing.price && (
                <p className="text-green-700 font-bold">
                  💲{listing.price.toLocaleString()}
                </p>
              )}
              <p className="text-sm mt-2">{listing.description}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
