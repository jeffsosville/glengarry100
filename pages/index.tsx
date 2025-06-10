import { useEffect, useState } from "react";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

// Capitalization utility
function toTitleCase(str?: string) {
  return str
    ? str.replace(/\w\S*/g, (txt) => txt.charAt(0).toUpperCase() + txt.substring(1).toLowerCase())
    : "";
}

type Broker = {
  id: string;
  broker_name: string;
  company_name: string;
  leaderboard_score: number;
  active_listings?: number;
  sold_listings?: number;
  city?: string;
  state?: string;
  companyurl?: string;
  companyUrl_clean?: string;
  listings_url?: string;
};

export default function Home() {
  const [brokers, setBrokers] = useState<Broker[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchBrokers() {
      const { data, error } = await supabase
        .from("all_brokers")
        .select("*")
        .order("leaderboard_score", { ascending: false })
        .limit(100);

      if (error) {
        console.error("Error loading brokers:", error.message);
      } else {
        setBrokers(data || []);
      }

      setLoading(false);
    }

    fetchBrokers();
  }, []);

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">🏆 The Glengarry 100</h1>
      <p className="text-xl text-gray-700 text-center mb-8">
       Ranked by Verified Listings. No Paywalls, No Ads.
      </p>

      {loading ? (
        <p>Loading leaderboard...</p>
      ) : (
        brokers.map((b, index) => {
          const trophy =
            index === 0 ? "🥇" : index === 1 ? "🥈" : index === 2 ? "🥉" : "";

          return (
            <div key={b.id} className="border rounded-xl p-4 mb-4 shadow">
              <h2 className="text-xl font-semibold">
                {index + 1}. {trophy}{" "}
                <a
                  href={b.companyUrl_clean || "#"}
                  className="text-blue-600 hover:underline"
                  target="_blank"
                >
                  {toTitleCase(b.company_name)}
                </a>
              </h2>
              <p className="text-sm text-gray-600">
                {toTitleCase(b.city)}, {b.state?.toUpperCase()} — Score: {b.leaderboard_score} |{" "}
                Active Listings:{" "}
                <a
                  href={b.listings_url || "#"}
                  className="text-blue-600 hover:underline"
                  target="_blank"
                >
                  {b.active_listings || 0}
                </a>{" "}
                | Sold: {b.sold_listings || 0}
              </p>
            </div>
          );
        })
      )}
    </div>
  );
}
