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

# --- Sidebar Filters ---
st.sidebar.header("Search & Filter")
search_term = st.sidebar.text_input("Search by name or company")

# --- Fetch all brokers fresh every time ---
data = fetch_all_brokers("all_brokers")
df = pd.DataFrame(data)
if df.empty:
    st.warning("No brokers found.")
    st.stop()

# --- Cleanup + parse tags ---
if 'expertise_tags' in df.columns:
    df['expertise_tags'] = df['expertise_tags'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith("[") else [])
    tag_options = sorted(set(tag for tags in df['expertise_tags'] for tag in tags))
else:
    df['expertise_tags'] = [[] for _ in range(len(df))]
    tag_options = []

# --- Sidebar Filters (dynamic) ---
city_filter = st.sidebar.multiselect("Filter by city", sorted(df['city'].dropna().unique()))
state_filter = st.sidebar.multiselect("Filter by state", sorted(df['state'].dropna().str.upper().unique()))
industry_filter = st.sidebar.multiselect("Filter by industry/niche", tag_options)

# --- Apply Search ---
if search_term:
    search_lower = search_term.lower()
    df = df[df.apply(
        lambda row: search_lower in str(row.get('broker_name') or '').lower() or
                    search_lower in str(row.get('company_name') or '').lower(), axis=1)]

# --- Apply Other Filters ---
if city_filter:
    df = df[df['city'].isin(city_filter)]
if state_filter:
    df = df[df['state'].str.upper().isin(state_filter)]
if industry_filter:
    df = df[df['expertise_tags'].apply(lambda tags: any(tag in tags for tag in industry_filter))]

# --- Dedupe by company_name ---
df['clean_name'] = df['company_name'].str.lower().str.strip()
df = df.drop_duplicates(subset='clean_name', keep='first')

# --- Sort + Rank ---
df = df[df['leaderboard_score'].notnull()]
df = df.sort_values(by='leaderboard_score', ascending=False).reset_index(drop=True)
df['rank'] = df.index + 1

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

# --- Optional: Debug Data ---
if st.sidebar.checkbox("Show debug table"):
    st.dataframe(df[['rank', 'company_name', 'broker_name', 'leaderboard_score', 'listings_url']])
