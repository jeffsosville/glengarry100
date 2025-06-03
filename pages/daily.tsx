import { useEffect, useState } from "react";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

type Listing = Record<string, any>; // Generic debug shape

export default function Daily() {
  const [listings, setListings] = useState<Listing[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchListings() {
      const { data, error } = await supabase
        .from("daily_listings")
        .select("*")
        .limit(10);

      console.log("Listings:", data);
      console.log("Error:", error);

      if (error) {
        console.error("Error loading listings:", error.message);
      } else {
        setListings(data || []);
      }

      setLoading(false);
    }

    fetchListings();
  }, []);

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">🧪 Daily Listings Debug</h1>

      {loading ? (
        <p>Loading listings...</p>
      ) : listings.length === 0 ? (
        <p>No listings found.</p>
      ) : (
        listings.map((l, index) => (
          <div
            key={l.id || index}
            className="border rounded-xl p-4 mb-4 shadow text-sm"
          >
            <pre className="whitespace-pre-wrap break-all">
              {JSON.stringify(l, null, 2)}
            </pre>
          </div>
        ))
      )}
    </div>
  );
}
