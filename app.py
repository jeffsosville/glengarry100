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

# --- Fetch All Brokers ---
def fetch_all_brokers(table_name="all_brokers", total_rows=7500, chunk_size=1000):
    brokers = []
    for start in range(0, total_rows, chunk_size):
        end = start + chunk_size - 1
        response = supabase.table(table_name).select("*").range(start, end).execute()
        if not response.data:
            break
        brokers.extend(response.data)
    return brokers

# --- Sidebar UI ---
st.sidebar.header("Search & Filter")
search_term = st.sidebar.text_input("Search by name or company")

# Fetch full dataset
full_data = fetch_all_brokers("all_brokers")
df = pd.DataFrame(full_data)

if df.empty:
    st.warning("No brokers found.")
    st.stop()

# Rank & Parse
df = df.sort_values(by='leaderboard_score', ascending=False).reset_index(drop=True)
df['rank'] = df.index + 1

if 'expertise_tags' in df.columns:
    df['expertise_tags'] = df['expertise_tags'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith("[") else [])

# Dropdowns
city_filter = st.sidebar.multiselect("Filter by city", sorted(df['city'].dropna().unique()))
state_filter = st.sidebar.multiselect("Filter by state", sorted(df['state'].dropna().str.upper().unique()))
tag_options = sorted(set(tag for tags in df['expertise_tags'] if isinstance(tags, list) for tag in tags))
industry_filter = st.sidebar.multiselect("Filter by industry/niche", tag_options)

filters_active = any([search_term, city_filter, state_filter, industry_filter])

# --- Apply filters ---
filtered_df = df.copy()

if search_term:
    filtered_df = filtered_df[filtered_df.apply(
        lambda row: search_term.lower() in str(row.get('broker_name', '')).lower() or
                    search_term.lower() in str(row.get('company_name', '')).lower(), axis=1)]

if city_filter:
    filtered_df = filtered_df[filtered_df['city'].isin(city_filter)]

if state_filter:
    filtered_df = filtered_df[filtered_df['state'].str.upper().isin(state_filter)]

if industry_filter:
    filtered_df = filtered_df[filtered_df['expertise_tags'].apply(lambda tags: any(tag in tags for tag in industry_filter))]

# If no filters, limit to top 100 only
if not filters_active:
    filtered_df = df.head(100)

# Preserve original leaderboard rank
filtered = filtered_df.merge(df[['broker_name', 'company_name', 'rank']], on=['broker_name', 'company_name'], how='left')

if filtered.empty:
    st.info("No matching brokers.")
    st.stop()

# --- Display Brokers ---
for _, row in filtered.iterrows():
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
