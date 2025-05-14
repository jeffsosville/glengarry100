import streamlit as st
import pandas as pd
import ast
from supabase import create_client, Client

# --- Supabase Setup ---
SUPABASE_URL = "https://rxbaimgjakefhxsaksdl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4YmFpbWdqYWtlZmh4c2Frc2RsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NjYyNjQ0OSwiZXhwIjoyMDYyMjAyNDQ5fQ.aFgdVDkCCjYLX8b6y03Cz85SGiq2FYB8auF4hgLimUs"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="The Glengarry 100", layout="wide")
st.title("🏆 The Glengarry 100")

# --- Broker Fetching ---
def fetch_all_brokers(table_name="all_brokers", total_rows=7500, chunk_size=1000):
    brokers = []
    for start in range(0, total_rows, chunk_size):
        end = start + chunk_size - 1
        response = supabase.table(table_name).select("*").range(start, end).execute()
        if not response.data:
            break
        brokers.extend(response.data)
    return brokers

# --- Initial Sidebar Setup ---
st.sidebar.header("Search & Filter")
search_term = st.sidebar.text_input("Search by name or company")
city_filter, state_filter, industry_filter = [], [], []

# Load quick sample to generate dropdown options
sample_data = supabase.table("all_brokers").select("*").range(0, 99).execute().data
sample_df = pd.DataFrame(sample_data)
if 'expertise_tags' in sample_df.columns:
    sample_df['expertise_tags'] = sample_df['expertise_tags'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith("[") else [])
    tag_options = sorted(set(tag for tags in sample_df['expertise_tags'] for tag in tags))
else:
    tag_options = []

# Now populate filter UI
city_filter = st.sidebar.multiselect("Filter by city", sorted(sample_df['city'].dropna().unique()))
state_filter = st.sidebar.multiselect("Filter by state", sorted(sample_df['state'].dropna().str.upper().unique()))
industry_filter = st.sidebar.multiselect("Filter by industry/niche", tag_options)

# Check if filters are active
filters_active = any([search_term, city_filter, state_filter, industry_filter])

# --- Fetch Data ---
if filters_active:
    data = fetch_all_brokers("all_brokers")
else:
    data = sample_data

df = pd.DataFrame(data)
if df.empty:
    st.warning("No brokers found.")
    st.stop()

df = df.sort_values(by='leaderboard_score', ascending=False).reset_index(drop=True)
df['rank'] = df.index + 1

# Reparse tags from full data if available
if 'expertise_tags' in df.columns:
    df['expertise_tags'] = df['expertise_tags'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith("[") else [])

# --- Apply filters ---
if search_term:
    df = df[df.apply(
        lambda row: search_term.lower() in str(row.get('broker_name', '')).lower() or
                    search_term.lower() in str(row.get('company_name', '')).lower(), axis=1)]

if city_filter:
    df = df[df['city'].isin(city_filter)]

if state_filter:
    df = df[df['state'].str.upper().isin(state_filter)]

if industry_filter:
    df = df[df['expertise_tags'].apply(lambda tags: any(tag in tags for tag in industry_filter))]

if not filters_active:
    df = df.head(100)

# --- Display Brokers ---
for _, row in df.iterrows():
    rank = row['rank']
    name = (row.get('company_name') or 'Unknown').title()
    broker = row.get('broker_name', '').title()
    location = f"{row.get('city', '').title()}, {row.get('state', '').upper()}"
    phone = row.get('phone', '')
    active = row.get('active_listings', 0)
    sold = row.get('sold_listings', 0)
    score = row.get('leaderboard_score', 0)
    url = row.get('listings_url') or row.get('companyurl') or row.get('companyUrl') or "#"

    medal = ""
    if rank == 1: medal = "🥇"
    elif rank == 2: medal = "🥈"
    elif rank == 3: medal = "🥉"

    st.markdown(f"""
    <div style='border:1px solid #333; padding:10px; border-radius:5px; margin-bottom:10px;'>
        <b>{medal} {rank}. <a href='{url}' target='_blank'>{name}</a></b> | {location} | {phone}<br>
        Active: {active} | Sold: {sold} | Score: {score} | <a href='{url}' target='_blank'>View Listings</a>
    </div>
    """, unsafe_allow_html=True)
    if st.button(f"🔍 View Listings for {broker}", key=f"view_{rank}"):
        st.subheader(f"Listings for {broker}")

    listings_resp = supabase.table("external_broker_listings") \
        .select("*") \
        .eq("broker_name", row.get("broker_name", "")) \
        .execute()


    listings_resp = supabase.table("external_broker_listings") \
        .select("*") \
        .eq("broker_name", broker) \
        .execute()

    listings = listings_resp.data or []

    if listings:
        for listing in listings:
            with st.expander(f"{listing['title']} | {listing['location']} | {listing['asking_price']}"):
                st.write(f"**Route Type:** {listing.get('route_type', '')}")
                st.write(f"**Cash Flow:** {listing.get('cash_flow', 'N/A')}")
                st.write(f"**Status:** {listing.get('status', 'N/A')}")
                if listing.get('detail_url'):
                    st.markdown(f"[🔗 View Full Listing]({listing['detail_url']})")
    else:
        st.info("No listings found for this broker.")


if df.empty:
    st.info("No matching brokers.")
