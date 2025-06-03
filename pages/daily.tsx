import { useEffect, useState } from "react";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

type Listing = {
  id: string;
  business_name: string;
  location: string;
  asking_price?: number;
  cash_flow?: number;
  broker_name?: string;
  broker_id?: string;
  created_at?: string;
};

export default function Daily() {
  const [listings, setListings] = useState<Listing[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchListings() {
      const { data, error } = await supabase
        .from("daily_listings") // ✅ clean, renamed table
        .select("*")
        .order("created_at", { ascending: false })
        .limit(50);

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
      <h1 className="text-3xl font-bold mb-6">📬 Daily Listings Digest</h1>

      {loading ? (
        <p>Loading listings...</p>
      ) : listings.length === 0 ? (
        <p>No listings found.</p>
      ) : (
        listings.map((l) => (
          <div key={l.id} className="border rounded-xl p-4 mb-4 shadow">
            <h2 className="text-xl font-semibold">{l.business_name}</h2>
            <p className="text-sm text-gray-600 mb-1">
              {l.location} —{" "}
              {l.asking_price ? `Asking: $${l.asking_price.toLocaleString()}` : "No asking price"}
              {l.cash_flow ? ` | Cash Flow: $${l.cash_flow.toLocaleString()}` : ""}
            </p>
            <p className="text-sm text-gray-600">
              Broker:{" "}
              {l.broker_id ? (
                <a
                  href={`/broker/${l.broker_id}`}
                  className="text-blue-600 hover:underline"
                >
                  {l.broker_name || "View Profile"}
                </a>
              ) : (
                l.broker_name || "Unknown"
              )}
            </p>
          </div>
        ))
      )}
    </div>
  );
}
