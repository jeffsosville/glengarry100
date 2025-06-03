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
  price?: number;
  description?: string;
};

export default function Daily() {
  const [listings, setListings] = useState<Listing[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchListings() {
      const { data, error } = await supabase
        .from("public_daily_listings")
        .select(`
          id,
          header,
          location,
          price,
          description
        `)
        .limit(50);

      console.log("Listings:", data);
      if (error) {
        console.error("Error loading listings:", error.message);
      }
      setListings(data || []);
      setLoading(false);
    }

    fetchListings();
  }, []);

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">📬 Daily Listings Digest</h1>

      {loading ? (
        <p>Loading listings...</p>
      ) : listings.length === 0 ? (
        <p>No listings found.</p>
      ) : (
        listings.map((l) => (
          <div key={l.id} className="border rounded-xl p-4 mb-4 shadow">
            <h2 className="text-xl font-semibold text-blue-700 mb-1">
              {l.header}
            </h2>

            <p className="text-sm text-gray-600 mb-1">
              {l.location}
              {l.price ? ` — $${l.price.toLocaleString()}` : ""}
            </p>

            {l.description && (
              <p className="text-sm text-gray-700 italic">
                {l.description.length > 180
                  ? l.description.slice(0, 180) + "…"
                  : l.description}
              </p>
            )}
          </div>
        ))
      )}
    </div>
  );
}
