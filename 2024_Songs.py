import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# --- 1. Load Data ---
@st.cache_data
def load_data():
    """
    Loads the song data from the CSV file.
    
    EXPECTED COLUMNS: 'month', 'article' (song name), 'monthly_pageviews', 'artist', 'genre'.
    """

    try:
        # Load the CSV
        # NOTE: Updated file name to 'song_st.csv' as per your provided code
        df = pd.read_csv("song_st.csv") 
    except FileNotFoundError:
        st.error("Error: 'song_st.csv' not found. Please create it or check the file path.")
        st.stop()
    
    # 1. Rename 'pageviews' column to 'monthly_pageviews' (if it exists)
    if 'pageviews' in df.columns:
        df = df.rename(columns={'pageviews': 'monthly_pageviews'})
    
    # Ensure 'monthly_pageviews' is a numeric type for calculations
    df['monthly_pageviews'] = pd.to_numeric(df['monthly_pageviews'], errors='coerce')
    
    # Ensure 'artist' and 'month' columns exist and are correct types
    if 'artist' not in df.columns:
        st.error("Error: The CSV file must contain an 'artist' column.")
        st.stop()
    if 'month' not in df.columns:
        st.error("Error: The CSV file must contain a 'month' column for monthly analysis.")
        st.stop()
        
    df['artist'] = df['artist'].astype(str)
    df['month'] = df['month'].astype(str)
    
    # Drop rows with missing data in key columns
    df = df.dropna(subset=['monthly_pageviews', 'article', 'artist', 'month'])
    
    return df

st.set_page_config(layout="wide", page_title="Song Pageview Leaderboard & Artist Analysis")
data = load_data()

# --- 2. Title ---
st.title("🎶 Interactive Song Pageview Leaderboard & Artist Analysis 🏆")

# --- Introduction & Data Summary ---
st.header("Introduction")
st.write("What were the most popular songs in 2024? This analysis uses **Monthly Pageviews** as the metric.")
# ... (rest of original intro)

st.header("Data Summary")
# ... (rest of original summary)
st.markdown("---")


# --- 3. Song Leaderboard Controls ---
st.header("1. Top N Song Leaderboard")
st.markdown("Adjust the controls below to customize the top songs visualization, including selecting a month.")

# Get unique months for selection
# --- MODIFICATION 1: REVERSE SORT FOR DROPDOWN ---
# Sorts months (e.g., alphabetically 'April', 'March'...) and then reverses the order (e.g., 'March', 'April'...)
unique_months = sorted(data['month'].unique(), reverse=True) 

col_month, col_count, col_sort = st.columns([1, 1, 1])

with col_month:
    # **NEW MONTH SELECTION WIDGET**
    selected_month = st.selectbox(
        "Select **Month** to Analyze:",
        options=unique_months,
        index=0, # Default to the FIRST item in the reversed list (the latest month)
        key='month_select'
    )

with col_count:
    # Leaderboard Count Slider
    # Filter data for the selected month for accurate length count
    data_filtered_month = data[data['month'] == selected_month]
    
    leaderboard_count = st.slider(
        "Select **Top N** Songs:",
        min_value=10,
        # Max limited to 100 or the total number of songs in the selected month
        max_value=min(100, len(data_filtered_month)), 
        value=20,
        step=5,
        key='top_n_slider'
    )

with col_sort:
    # Sort Option Selectbox
    sort_option = st.selectbox(
        "Sort Leaderboard By:",
        options=['Monthly Pageviews (Descending)', 'Song Name (Alphabetical)'],
        index=0,
        key='sort_option_select'
    )

st.markdown("---")

# --- 4. Interactive Top N Leaderboard Visualization (Horizontal Bar Chart) ---

# Filter the data based on the selected month
df_leaderboard = data_filtered_month.sort_values(
    by='monthly_pageviews', 
    ascending=False
).head(leaderboard_count).copy()


if sort_option == 'Song Name (Alphabetical)':
    # Sort by the 'article' column (alphabetically)
    df_leaderboard = df_leaderboard.sort_values(by='article', ascending=True)
    y_sort_order = None 
else: # Monthly Pageviews (Descending)
    df_leaderboard = df_leaderboard.sort_values(by='monthly_pageviews', ascending=False)
    # Altair sort by the max value of monthly_pageviews
    y_sort_order = alt.EncodingSortField(field="monthly_pageviews", op="max", order='descending')


# Create the Altair Bar Chart
chart_leaderboard = alt.Chart(df_leaderboard).mark_bar().encode(
    y=alt.Y('article', sort=y_sort_order, title=None), 
    x=alt.X('monthly_pageviews', title='Monthly Pageviews', axis=alt.Axis(format='~s')), 
    tooltip=['article', alt.Tooltip('monthly_pageviews', title='Monthly Pageviews')] 
).properties(
    title=f"Top {leaderboard_count} Songs by Monthly Pageviews in {selected_month}"
).interactive()

st.altair_chart(chart_leaderboard, use_container_width=True)

st.subheader(f"Raw Data for Top Songs in {selected_month}")
# Display the raw data for the visualized subset
st.dataframe(df_leaderboard[['article', 'monthly_pageviews']].rename(
    columns={'article': 'Song Name', 'monthly_pageviews': 'Monthly Pageviews'}), 
    use_container_width=True
)

st.markdown("---")
st.markdown("---")

# --- 5. Top N Artist Total Pageview Analysis (No monthly filter here, as it's *total accumulated* views) ---
st.header("2. Top N Artist Total Accumulated Pageview Analysis (All Months)")
st.write("This section aggregates the pageviews across **all months and all songs** for each artist in the dataset to determine who had the highest **total accumulated pageviews** across the year.")


# --- Data Preparation for Artist Analysis (Uses ALL data for ACCUMULATED total) ---
# 1. Group by artist and sum the pageviews
artist_summary = data.groupby('artist')['monthly_pageviews'].sum().reset_index()
artist_summary.columns = ['artist', 'total_pageviews']

# 2. Sort the artists by their total pageviews (descending)
artist_summary = artist_summary.sort_values(by='total_pageviews', ascending=False)


# --- Artist Analysis Controls ---
max_artists = min(50, len(artist_summary))

artist_n_slider = st.slider(
    "Select **Top N** Artists to Analyze:",
    min_value=5,
    max_value=max_artists, 
    value=15,
    step=1,
    key='top_n_artists_slider'
)

# --- Visualization for Top N Artists ---
df_top_artists = artist_summary.head(artist_n_slider).copy()

# Create the Altair Bar Chart for Artists
# --- MODIFICATION 2: VERTICAL BAR CHART ---
chart_artists = alt.Chart(df_top_artists).mark_bar(color='#E91E63').encode(
    # X-axis for the CATEGORY (Artist)
    x=alt.X('artist', sort='-y', title='Artist', axis=alt.Axis(labels=True, labelAngle=-45)), 
    # Y-axis for the VALUE (Total Pageviews)
    y=alt.Y('total_pageviews', title='Total Accumulated Pageviews', axis=alt.Axis(format='~s')),
    # Tooltip setup
    tooltip=['artist', alt.Tooltip('total_pageviews', format=',', title='Total Pageviews')] 
).properties(
    title=f"Top {artist_n_slider} Artists by Total Accumulated Pageviews (All Data)"
).interactive()

st.altair_chart(chart_artists, use_container_width=True)

st.subheader("Raw Data for Top Artists (All Data)")
# Display the raw data for the visualized subset
st.dataframe(df_top_artists.rename(
    columns={'total_pageviews': 'Total Accumulated Pageviews'}), 
    use_container_width=True
)