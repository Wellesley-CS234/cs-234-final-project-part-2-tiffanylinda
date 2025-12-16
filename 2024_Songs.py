# Author: Tiffany Lin
# Description: CS 234 Final Project Streamlit
# Importing all the necessary libraries
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# --- 1. Load Data ---

st.set_page_config(layout="wide", page_title="Song Pageview Leaderboard & Artist Analysis")
data = pd.read_csv("song_st.csv")
data2 =  pd.read_csv("main.csv")
data3 = pd.read_csv("classification.csv")

# Creating tabs so that each section is organized

intro, data_summary, features, classification, hypothesis, visuals, summary = st.tabs(["1. Introduction",
        "2. Data Summary",
        "3. New Features",
        "4. Text Classification",
        "5. Hypothesis Testing",
        "6. Interactive Visualization",
        "7. Summary"
        ])

with intro:

    # -- Title ---
    st.title("🎶 Interactive Song Pageview Leaderboard & Artist Analysis 🏆")

    # --- Introduction ---
    st.header("Introduction")
    st.write("""
             It's the year 2024, and another popular artist such as Taylor Swift has released their new album, **The Tortured Poets Department**.
            We expect to see a lot of buzz and attention directed towards the release of this album. 
            In order to investigate how interested the public is in this album, we might decide to go look at the number of pageviews
            that the album is accumulating. A lot of internet users like to use Wikipedia as a source of information, so we decide to 
            use the pageview data from Wikipedia.
            However, as we soon realize, the number of pageviews will always fluctuate, especially since the album was released
            in April 2024. Some fans might argue that the album should be up for contention of Album of the Year at the Grammy's.
            In order to understand and further one's argument for what artists and songs should be winnning Artist of the Year, or Song of the Year,
            let's investigate which artists and which songs dominated 2024.
            
            As we investigate which artists dominated the searches of the public in 2024, it's also interesting to see
            how much attention (measured in pageviews) is actually directed towards popular artists vs smaller artists.
             
            """)
    
    st.write("Therefore, the three main research questions I decided to investigate are:")
    st.write("1. Who were the most popular artists in 2024?")
    st.write("2. What were the most popular songs of 2024?")
    st.write("3. How much attention was on popular artists compared to smaller artists?")

    st.write("""My preliminary assumptions lead me to believe that the most popular artists will be artists 
             such as Taylor Swift, Beyonce, etc. 
             
             The most popular songs will most likely be from the top/popular artists.

             We might see about 80 percent of the total pageview data being dominated by the top artists.
             
             """)

with data_summary:
    st.header("Data Summary")
    st.write("""
    The data I worked with consists of the 2024 Wikipedia DPDP data for "en.wikipedia" in the US.
    The data was converted into a file that is hosted in the Wellesley CS server.
    In order to collect the data for my analysis, I first queried for all the song articles that were in the DuckDB database.
    My query grouped each song by their month in the year and their monthly pageview count.

    This means that an article/song by a specific artist could show up twice, 
    but the two rows would be different because they would be from different months.         
    I also made sure that each song in the query got the unique qid in order to not have issues later on. 
             
    Some additional notes regarding the data:
    1. The encoding for some of the article/song names needed to be decoded.
    2. I also cleaned the article titles/song titles so that they were more readable.
             
    After I did my first round of data collection, I saved the data into a csv and proceeded to get the wikidata for 
    each article using their qid. 
    The Wikidata provided information regarding the genre of the song and artists listed on the song.
             
    I then added the genre and artist data into my new main csv. 

    I use this data to investigate my first questions about which songs were the most popular in 2024,
     and which artists were the most popular in 2024.
    """)
    st.markdown("-- Descriptive Statistics --")

    total_unique_artists = data["artist"].nunique()

    total_unique_songs = data["qid"].nunique()

    total_unique_genres = data["genre"].nunique()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Total Unique Artists",
            value=f"{total_unique_artists:,}" 
        )
        st.caption(f"Count from the column: **{"artist"}**")

    with col2:
        st.metric(
            label="Total Unique Songs",
            value=f"{total_unique_songs:,}"
        )
        st.caption(f"Count from the column: **{"qid"}**")

    with col3:
        st.metric(
            label="Total Unique Genres",
            value=f"{total_unique_genres:,}"
        )
        st.caption(f"Count from the column: **{"genre"}**")
        
    st.markdown("---")
    
    st.info(
        f"""
        **Summary of Counts:**
        * Unique Artists: **{total_unique_artists:,}**
        * Unique Songs: **{total_unique_songs:,}**
        * Unique Genres: **{total_unique_genres:,}**
        """
    )

with features:
    st.header("Features")
    st.write("""
    The new feature that I will be adding to my dataset is theme of the song. 
    In order to get these features, I combined song lyric data from three different Kaggle datasets and 
    found the songs that matched with my main csv. 
    
    Therefore, it is important to note that there will be less songs and artists in this dataset.

    """)
    ### insert descriptive statistics about number of songs and artists in this new dataset

    # Showing what the Kaggle data combined with my main csv looks like
    st.markdown("-- My Kaggle datasets merged with main csv --")
    st.dataframe(data2, use_container_width=True)

    st.markdown("-- The lyrics column in my data -")
    lyrics_col = data2["lyrics"]
    st.dataframe(lyrics_col, use_container_width=True, hide_index=True)


with classification:
    st.header("Classification Results")
    st.write("It is important to note that there will be less songs and artists in this dataset as it is the same one from the previous section but with the classification results added.")

    st.markdown("-- My dataset with classification label --")
    st.dataframe(data3, use_container_width=True)

    st.markdown("-- The column in my data -")
    song_theme_col = data3["theme"]
    st.dataframe(song_theme_col, use_container_width=True, hide_index=True)

    distribution_df = data3["theme"].value_counts().reset_index()
    distribution_df.columns = ["theme", 'Count'] # Rename columns for Altair
    
    st.subheader(f"Distribution of Labels in: **{"theme"}**")
    st.dataframe(distribution_df, use_container_width=True, hide_index=True)
    chart = alt.Chart(distribution_df).mark_bar().encode(
        # The x-axis is the label (e.g., 'Genre')
        x=alt.X("theme", sort='-y', title="theme"), # Sort by count (y-axis) descending
        
        # The y-axis is the count
        y=alt.Y('Count', title='Frequency (Count)'),
        
        # Color the bars based on the label (optional, but good)
        color="theme", 
        
        # Add tooltips for interactivity
        tooltip=["theme", 'Count']
    ).properties(
        title=f"Label Distribution for '{"theme"}'"
    ).interactive() # Allows zooming and panning

    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)


with hypothesis:
    st.write("Below is the way I investigated the distribution of page views across all the artists in the data.")
    # --- 5. Top N Artist Total Pageview Analysis (No monthly filter here, as it's *total accumulated* views) ---
    st.header("Top N Artist Total Accumulated Pageview Analysis (All Months)")
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
    # Results of calculating the precentage that are dominated by popular artists vs smaller artists

with visuals:

    # --- 3. Song Leaderboard Controls ---
    st.header("Top N Song Leaderboard")
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

with summary:
    st.header("Summary & Ethical Considerations ")
    st.write("""
    The key takeaways from my investigation show that the top artists are: 
    The top songs of 2024 are:.
    About something percent of attention is directed towards popular artists vs smaller artists.

    I'm am fairly confident that the results are reliable because…

    I used zero-shot classification, but was not able to assess the model's accuracy as I did not have ground truth data.

    There isn't any major ethical concerns as the data was collected from public sources. 

    I find that my results do expose a bias towards popular artists dominating 2024. 

    """)