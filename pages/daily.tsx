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
  cashflow?: number;
  ebitda?: number;
  description?: string;
  urlstub?: string;
  brokerContactFullName?: string;
  brokerCompany?: string;
};

export default function Daily() {
  const [listings, setListings] = useState<Listing[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchListings() {
      const { data, error } = await supabase
        .from("daily_listings")
        .select(`
          id,
          header,
          location,
          price,
          cashflow,
          ebitda,
          description,
          urlstub,
          "brokerContactFullName",
          "brokerCompany"
        `)
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
            <h2 className="text-xl font-semibold">
              {l.urlstub ? (
                <a
                  href={`https://www.bizbuysell.com/${l.urlstub}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline"
                >
                  {l.header}
                </a>
              ) : (
                l.header
              )}
            </h2>

            <p className="text-sm text-gray-600 mb-1">
              {l.location} —{" "}
              {l.price !== undefined && <>Price: ${l.price.toLocaleString()} | </>}
              {l.cashflow !== undefined && <>Cash Flow: ${l.cashflow.toLocaleString()} | </>}
              {l.ebitda !== undefined && <>EBITDA: ${l.ebitda.toLocaleString()}</>}
            </p>

            {l.description && (
              <p className="text-sm text-gray-700 mb-2 italic">
                {l.description.length > 180
                  ? l.description.slice(0, 180) + "…"
                  : l.description}
              </p>
            )}

            {(l.brokerContactFullName || l.brokerCompany) && (
              <p className="text-sm text-gray-600">
                Broker: {l.brokerContactFullName || "Unknown"}
                {l.brokerCompany ? ` — ${l.brokerCompany}` : ""}
              </p>
            )}
          </div>
        ))
      )}
    </div>
  );
}
