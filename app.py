import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Glengarry 100", layout="wide")
st.title("\U0001F4BC Glengarry 100 — Top Business Brokers")

# Fetch brokers and listings from Supabase
@st.cache_data(show_spinner=False)
def load_data():
    brokers_resp = supabase.table("all brokers").select("*").execute()
    listings_resp = supabase.table("bizbuysell_listings_flat").select("*").execute()
    brokers_df = pd.DataFrame(brokers_resp.data)
    listings_df = pd.DataFrame(listings_resp.data)
    return brokers_df, listings_df

brokers_df, listings_df = load_data()

# Count listings per broker_id
listing_counts = listings_df.groupby("broker_id").size().reset_index(name="listing_count")

# Ensure both keys are strings before merging
listing_counts["broker_id"] = listing_counts["broker_id"].astype(str)
brokers_df["id"] = brokers_df["id"].astype(str)

# Merge listing counts into brokers
brokers_df = brokers_df.merge(listing_counts, how="left", left_on="id", right_on="broker_id")
brokers_df["listing_count"] = brokers_df["listing_count"].fillna(0).astype(int)

# Sort and display top 100
top_brokers = brokers_df.sort_values("listing_count", ascending=False).head(100).reset_index(drop=True)

for idx, row in top_brokers.iterrows():
    with st.expander(f"{row.get('broker_name', row.get('first_name', ''))} {row.get('last_name', '')} — {row.get('company_name', '')} ({row['listing_count']} Listings)"):
        st.write(f"**Location:** {row.get('city', '')}, {row.get('state', '')}")
        st.write(f"**Phone:** {row.get('phone', row.get('broker_phone', 'N/A'))}")

        broker_listings = listings_df[listings_df["broker_id"] == row["id"]]

        for _, listing in broker_listings.iterrows():
            with st.container():
                st.markdown(f"**{listing['title']}**")
                st.write(f"{listing.get('location', '')} | {listing.get('asking_price', 'N/A')}")
                st.caption(f"Ad #: {listing.get('ad_number')}")
                st.markdown("---")
