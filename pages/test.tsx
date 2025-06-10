 import { useEffect } from "react";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export default function Test() {
  useEffect(() => {
    const fetch = async () => {
      const { data, error } = await supabase
        .from("todays_listings")
        .select("*")
        .limit(5);

      console.log("🧪 TEST DATA:", data);
      console.error("🧪 TEST ERROR:", error);
    };

    fetch();
  }, []);

  return <h1>🧪 Testing Supabase Fetch...</h1>;
}
