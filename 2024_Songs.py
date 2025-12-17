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
             It's the year 2024, and yet again another popular artist such as Taylor Swift has released their new album, **The Tortured Poets Department**.
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
             such as Taylor Swift, Beyonce, etc. """)
             
    st.write("The most popular songs will most likely be from the top/popular artists.")         

    st.write("We might see about 80 percent of the total pageview data being dominated by the top artists.")        


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

    # Getting the number of unique artists, songs, and genres in my dataset
    total_unique_artists = data["artist"].nunique()

    total_unique_songs = data["qid"].nunique()

    total_unique_genres = data["genre"].nunique()
    col1, col2, col3 = st.columns(3)

    # Creating columns to display my descriptive statistics
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

with features:
    st.header("Features")
    st.write("""
    The new feature that I will be adding to my dataset is theme of the song. 
    In order to get these features, I combined song lyric data from three different Kaggle datasets and 
    found the songs that matched with my main csv. 
    
    Therefore, it is important to note that there will be less songs and artists in this dataset.

    """)
    # Descriptive statistics for this new dataset
    total_unique_artists2 = data2["artist"].nunique()

    total_unique_songs2 = data2["qid"].nunique()

    total_unique_genres2 = data2["genre"].nunique()

    col4, col5, col6 = st.columns(3)
    # Creating columns to display my descriptive statistics
    with col4:
        st.metric(
            label="Total Unique Artists",
            value=f"{total_unique_artists2:,}" 
        )
        st.caption(f"Count from the column: **{"artist"}**")

    with col5:
        st.metric(
            label="Total Unique Songs",
            value=f"{total_unique_songs2:,}"
        )
        st.caption(f"Count from the column: **{"qid"}**")

    with col6:
        st.metric(
            label="Total Unique Genres",
            value=f"{total_unique_genres2:,}"
        )
        st.caption(f"Count from the column: **{"genre"}**")
        

    # Showing what the Kaggle data combined with my main csv looks like
    st.markdown("-- My Kaggle datasets merged with main csv --")
    st.dataframe(data2, use_container_width=True)

    st.markdown("-- The lyrics column in my data -")
    lyrics_col = data2["lyrics"]
    st.dataframe(lyrics_col, use_container_width=True, hide_index=True)


with classification:
    st.header("Classification Results")
    st.write("It is important to note that there will be less songs and artists in this dataset as it is the same one from the previous section but with the classification results added.")

    # Showing what the dataset looks like
    st.markdown("-- My dataset with classification label --")
    st.dataframe(data3, use_container_width=True)

    # Showing what is in the column
    st.markdown("-- The column in my data -")
    song_theme_col = data3["theme"]
    st.dataframe(song_theme_col, use_container_width=True, hide_index=True)

    distribution_df = data3["theme"].value_counts().reset_index()
    distribution_df.columns = ["theme", 'Count'] # Renaming columns for Altair
    
    st.subheader(f"Distribution of Labels in: **{"theme"}**")
    st.dataframe(distribution_df, use_container_width=True, hide_index=True)
    chart = alt.Chart(distribution_df).mark_bar().encode(
        # X-axis is theme, sorting by count with y-axis descending
        x=alt.X("theme", sort='-y', title="theme"), 
        
        # The Y-axis is the count for each theme
        y=alt.Y('Count', title='Frequency (Count)'),
        
        # Color the bars based on the theme
        color="theme", 
        
        # Tooltips for interactivity
        tooltip=["theme", 'Count']
    ).properties(
        title=f"Label Distribution for '{"theme"}'"
    ).interactive() # Zooming and panning

    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)


with hypothesis:
    st.write("Below is the way I investigated the distribution of page views across all the artists in the data.")
    # --- Top N Artist Total Pageview Analysis ---
    st.header("Top N Artist Total Accumulated Pageview Analysis (All Months)")
    st.write("This section aggregates the pageviews across **all months and all songs** for each artist in the dataset to determine who had the highest **total accumulated pageviews** across the year.")


    # --- Data Preparation for Artist Analysis (Uses ALL data for ACCUMULATED total) ---
    # 1. Summarize and Sort
    artist_summary = data.groupby('artist')['monthly_pageviews'].sum().reset_index()
    artist_summary.columns = ['artist', 'total_pageviews']
    artist_summary = artist_summary.sort_values(by='total_pageviews', ascending=False).reset_index(drop=True)

    # 2. Calculate Programmatic Jump Detection

    # 2a. Calculate the drop-off rate between sequential artists
    # Shift(-1) brings the pageviews of the *next* artist into the current artist's row
    artist_summary['next_artist_views'] = artist_summary['total_pageviews'].shift(-1)
    artist_summary['view_drop'] = artist_summary['total_pageviews'] - artist_summary['next_artist_views']

    # Calculate the percentage drop from the current artist's views to the next artist's views
    artist_summary['pct_drop'] = (artist_summary['view_drop'] / artist_summary['total_pageviews']) * 100

    # Drop the last row which will have NaN for the next artist's views
    artist_summary_analysis = artist_summary.dropna(subset=['next_artist_views']).copy() 

    # 2b. Define and Identify the Jump
    # Setting a threshold of 60 percent
    JUMP_THRESHOLD_PCT = 60 

    # Find the first major separation point
    jump_point = artist_summary_analysis[artist_summary_analysis['pct_drop'] >= JUMP_THRESHOLD_PCT].head(1)

    # 2c. Display the Jump Detection Result
    # Initialize a safe default value for the jump artist
    jump_artist = "" 
    jump_index = -1

    if not jump_point.empty:
        jump_artist = jump_point['artist'].iloc[0]
        jump_percentage = jump_point['pct_drop'].iloc[0]
        
        st.markdown(f"""
        ### 🚨 Major Viewership Separation Detected!
        The most significant drop-off occurs after **{jump_artist}**.
        
        Pageviews dropped by **<span style='color:red; font-size: 1.2em;'>{jump_percentage:,.2f}%</span>** to the next artist, indicating a clear tier separation.
        """, unsafe_allow_html=True)
        
        # Store the index of the detected jump for visualization later
        jump_index = artist_summary[artist_summary['artist'] == jump_artist].index[0]
    else:
        st.info("No significant 'big jump' (a drop greater than 60%) was detected between sequential artists.")
        # jump_artist remains "" and jump_index remains -1, which is safe.

    # 3. Calculate Grand Total and Percentage Metrics
    grand_total_pageviews = artist_summary['total_pageviews'].sum()

    # --- Artist Analysis Controls ---
    max_artists = len(artist_summary)

    artist_n_slider = st.slider(
        "Select **Top N** Artists to Analyze:",
        min_value=1,
        max_value=max_artists, 
        value=min(10, max_artists), # Default to 10 or max artists
        step=1,
        key='top_n_artists_slider'
    )

    # --- Visualization for Top N Artists ---
    df_top_artists = artist_summary.head(artist_n_slider).copy()

    # Calculate and display the percentage metric
    top_n_pageviews = df_top_artists['total_pageviews'].sum()
    percentage_of_total = (top_n_pageviews / grand_total_pageviews) * 100

    st.markdown(f"""
    ### 📊 Key Performance Metric
    The **Top {artist_n_slider} artists** account for **<span style='color:#E91E63; font-size: 1.5em;'>{percentage_of_total:,.2f}%</span>** of the total accumulated pageviews.
    """, unsafe_allow_html=True)

    # 4. Create the Altair Bar Chart

    # Add a marker for the jump index if it's within the selected Top N
    color_condition = alt.condition(
    # jump_artist is guaranteed to be a string ("" if not found)
    alt.datum.artist == jump_artist, 
    alt.value('red'), # Color the bar red if it's the jump artist
    alt.value('#E91E63') # Otherwise use the default pink color
    )

    chart_artists = alt.Chart(df_top_artists).mark_bar().encode(
        # X-axis for the CATEGORY (Artist)
        x=alt.X('artist', sort='-y', title='Artist', axis=alt.Axis(labels=True, labelAngle=-45)), 
        # Y-axis for the VALUE (Total Pageviews)
        y=alt.Y('total_pageviews', title='Total Accumulated Pageviews', axis=alt.Axis(format='~s')),
        # Color based on the jump condition
        color=color_condition,
        # Tooltip setup
        tooltip=['artist', alt.Tooltip('total_pageviews', format=',', title='Total Pageviews')] 
    ).properties(
        title=f"Top {artist_n_slider} Artists by Total Accumulated Pageviews (All Data)"
    ).interactive()

    st.altair_chart(chart_artists, use_container_width=True)

    # 5. Raw Data Table with Percentage and Cumulative % (as before)
    df_top_artists['Percentage of Grand Total'] = (df_top_artists['total_pageviews'] / grand_total_pageviews) * 100
    df_top_artists['Cumulative %'] = df_top_artists['Percentage of Grand Total'].cumsum()

    st.subheader("Raw Data for Top Artists (All Data)")
    st.dataframe(
        df_top_artists[['artist', 'total_pageviews', 'Percentage of Grand Total', 'Cumulative %']]
            .rename(columns={'total_pageviews': 'Total Accumulated Pageviews'}), 
        use_container_width=True,
        column_config={
            "Percentage of Grand Total": st.column_config.NumberColumn(format="%.2f%%"),
            "Cumulative %": st.column_config.ProgressColumn(
                "Cumulative %",
                help="Cumulative percentage of total views",
                format="%.2f%%",
                min_value=0,
                max_value=100,
            ),
        }
    )


with visuals:

    # --- Song Leaderboard Controls ---
    st.header("Top N Song Leaderboard")
    st.markdown("Adjust the controls below to customize the top songs visualization, including selecting a month.")

    # Get unique months for selection
    # Sorts months and then reverses the order
    unique_months = sorted(data['month'].unique(), reverse=True) 

    col_month, col_count, col_sort = st.columns([1, 1, 1])

    with col_month:
        selected_month = st.selectbox(
            "Select **Month** to Analyze:",
            options=unique_months,
            index=0, 
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

    # --- Interactive Top N Leaderboard Visualization (Horizontal Bar Chart) ---

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
        # Sort by the max value of monthly_pageviews
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

    # --- TOTAL ACCUMULATION SECTION ---
    st.write("## 🏆 Overall Top Songs")

    # 1. Aggregate and Calculate Percentages
    df_total_stats = data.groupby('article')['monthly_pageviews'].sum().reset_index()
    df_total_stats.rename(columns={'monthly_pageviews': 'total_pageviews'}, inplace=True)

    # Calculate the % share of total traffic for each song
    total_site_views = df_total_stats['total_pageviews'].sum()
    df_total_stats['percent_share'] = (df_total_stats['total_pageviews'] / total_site_views) * 100

    # 2. Controls
    col_acc_1, col_acc_2 = st.columns([1, 1])

    with col_acc_1:
        total_n = st.slider(
            "Show Top N Songs Overall:",
            min_value=5,
            max_value=min(100, len(df_total_stats)),
            value=15,
            key='total_n_slider_final'
        )

    with col_acc_2:
        total_sort = st.selectbox(
            "Sort Overall By:",
            options=['Total Pageviews (High to Low)', 'Song Name (A-Z)'],
            key='total_sort_final'
        )

    # 3. Sorting Logic (Highest Views always stay on top unless A-Z is chosen)
    if total_sort == 'Song Name (A-Z)':
        df_display_total = df_total_stats.nlargest(total_n, 'total_pageviews').sort_values('article')
        y_sort_acc = None
    else:
        df_display_total = df_total_stats.nlargest(total_n, 'total_pageviews')
        y_sort_acc = alt.EncodingSortField(field="total_pageviews", order='descending')

    # 4. Visualization
    chart_total = alt.Chart(df_display_total).mark_bar(color='#29b5e8').encode(
        y=alt.Y('article:N', sort=y_sort_acc, title=None),
        x=alt.X('total_pageviews:Q', title='Total Accumulated Pageviews', axis=alt.Axis(format='~s')),
        tooltip=[
            alt.Tooltip('article', title='Song'),
            alt.Tooltip('total_pageviews', title='Total Views', format=','),
            alt.Tooltip('percent_share', title='% of Total Traffic', format='.2f') # Added percentage to tooltip
        ]
    ).properties(
        title="Cumulative Song Performance",
        height=400
    ).interactive()

    st.altair_chart(chart_total, use_container_width=True)

    # 5. Raw Data with Percentage formatting
    st.write("### Data Summary")
    st.dataframe(
        df_display_total.rename(columns={
            'article': 'Song Name', 
            'total_pageviews': 'Total Views',
            'percent_share': '% Share'
        }),
        use_container_width=True,
        column_config={
            "% Share": st.column_config.NumberColumn(format="%.2f%%") # Formats as 5.25%
        }
    )


with summary:
    st.header("Summary & Ethical Considerations ")
    st.write("""
    The key takeaways from my investigation show that the top artists are: 
             1. Taylor Swift
             2. The Beatles
             3. Eminem
             4. Sabrina Carpenter
             5. Fleetwood Mac
             6. Kendrick Lamar
             7. Connie Francis
             8. Beyonce
             9. Billie Eilish
             10. Usher
    The top songs of 2024 are:
             
    These Top 10 Artists Account for 14.88 percent of the total accumulated pageviews.
    
    The most interesting find is the big drop between Taylor Swift and the next person.
    
    Taylor makes up 3.89 percent of the total accumulated pageviews in 2024. 
             
    Therefore, that means that the rest of the artists make up 96.11 percent of the rest of the accumulated pageviews in 2024.

    I'm fairly confident that the results are for the most part reliable because the processes I took in order to make sure the songs and QID were properly processed.
    This also makes sense because in recent times, pop artists especially Taylor Swift have been dominating the music industry. 

    I used zero-shot classification, but was not able to assess the model's accuracy as I did not have ground truth data.
    One possible path I could do moving foward is using the lyric data to predict genre because I have ground truth for genre.

    There isn't any major ethical concerns as the data was collected from public sources. 

    I find that my results do expose a bias towards popular artists dominating 2024. 

    """)