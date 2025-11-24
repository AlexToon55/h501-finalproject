import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
import plotly.graph_objects as go

from modules.app_core import config, survey, page_header
from modules.nav import sidebar

#streamlit setup
st.set_page_config(page_title="Music & Mental Health", layout="wide")






# Custom CSS Styling
st.markdown(
    """
    <style>
        /* Global Style */
        body {
            font-family: 'Helvetica Neue', sans-serif;
            background-color: #1e1e2f;
            color: #f0f0f0;
        }

        /* Sidebar Styling */
        .css-1d391kg {
            background-color: #2a2a3e;
            color: #f0f0f0;
        }

        .css-1d391kg .sidebar .sidebar-content {
            background-color: #2a2a3e;
        }

        .css-1d391kg .sidebar .sidebar-header {
            font-size: 22px;
            font-weight: bold;
            color: #f0f0f0;
        }

        .css-1d391kg .sidebar .sidebar-content .css-hk4d7z {
            color: #e5e5e5;
        }

        /* Streamlit Title and Header */
        h1 {
            color: #8c8c8c;
            font-size: 3em;
            margin-bottom: 20px;
        }

        h2, h3 {
            color: #f5b800;
            font-weight: bold;
        }

        h4 {
            color: #f5b800;
            font-size: 1.4em;
        }

        /* Streamlit Button */
        .stButton button {
            background-color: #ff9000;
            color: white;
            border: 1px solid #ff9000;
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
            padding: 10px 20px;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }

        .stButton button:hover {
            background-color: #f5b800;
            transform: scale(1.05);
        }

        /* Streamlit Container */
        .stContainer {
            background-color: #242430;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.2);
            margin-bottom: 20px;
        }

        /* Streamlit Dataframe Style */
        .stDataFrame {
            border-radius: 10px;
            border: 1px solid #444;
            box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.2);
        }

        /* Streamlit Sidebar Input Field */
        .css-1l5o3a5 {
            background-color: #1e1e2f;
            color: #fff;
            border: 1px solid #444;
            border-radius: 5px;
            padding: 10px;
            font-size: 14px;
        }

        /* Plot Styling */
        .stPlotlyChart {
            background-color: #2a2a3e;
            border-radius: 10px;
        }

        /* Streamlit Expander */
        .stExpander {
            background-color: #343454;
            color: white;
        }

        /* Streamlit Input Slider */
        .stSlider {
            background-color: #2a2a3e;
            color: white;
        }

        .stSlider input {
            color: white;
        }

        /* Custom Hover Effects for Tables */
        .stDataFrame tbody tr:hover {
            background-color: #f5b800;
            color: black;
            cursor: pointer;
        }

        /* Responsive Layout Tweaks */
        @media only screen and (max-width: 768px) {
            h1 {
                font-size: 2em;
            }
            h2 {
                font-size: 1.5em;
            }
        }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
        /* Global Style */
        body {
            font-family: 'Helvetica Neue', sans-serif;
            background-color: #1e1e2f;
            color: #f0f0f0;
            overflow: hidden;
        }

        /* Falling Emojis Animation */
        @keyframes fall {
            0% {
                transform: translateY(-100px);
                opacity: 1;
            }
            100% {
                transform: translateY(100vh);
                opacity: 0;
            }
        }

        .falling-emoji {
            position: absolute;
            top: -50px;
            font-size: 18px; /* Tiny emojis for a big rain effect */
            animation: fall 5s infinite linear;
            z-index: 9999;
            pointer-events: none;
        }

        .brain {
            animation-duration: 6s;
            font-size: 15px;
        }

        .music-note {
            animation-duration: 4s;
            font-size: 20px;
        }

        .headphones {
            animation-duration: 5s;
            font-size: 18px;
        }

        .emoji1 { left: 5%; animation-duration: 6s; }
        .emoji2 { left: 15%; animation-duration: 5s; }
        .emoji3 { left: 25%; animation-duration: 7s; }
        .emoji4 { left: 35%; animation-duration: 6s; }
        .emoji5 { left: 45%; animation-duration: 8s; }
        .emoji6 { left: 55%; animation-duration: 4s; }
        .emoji7 { left: 65%; animation-duration: 6s; }
        .emoji8 { left: 75%; animation-duration: 7s; }
        .emoji9 { left: 85%; animation-duration: 5s; }
        .emoji10 { left: 95%; animation-duration: 6s; }
        .emoji11 { left: 10%; animation-duration: 4s; }
        .emoji12 { left: 20%; animation-duration: 8s; }
        .emoji13 { left: 30%; animation-duration: 6s; }
        .emoji14 { left: 40%; animation-duration: 5s; }
        .emoji15 { left: 50%; animation-duration: 7s; }
        .emoji16 { left: 60%; animation-duration: 6s; }
        .emoji17 { left: 70%; animation-duration: 5s; }
        .emoji18 { left: 80%; animation-duration: 7s; }
        .emoji19 { left: 90%; animation-duration: 4s; }
        .emoji20 { left: 15%; animation-duration: 5s; }
        .emoji21 { left: 25%; animation-duration: 6s; }
        .emoji22 { left: 35%; animation-duration: 7s; }
        .emoji23 { left: 45%; animation-duration: 6s; }
        .emoji24 { left: 55%; animation-duration: 8s; }
        .emoji25 { left: 65%; animation-duration: 4s; }
        .emoji26 { left: 75%; animation-duration: 6s; }
        .emoji27 { left: 85%; animation-duration: 7s; }
        .emoji28 { left: 95%; animation-duration: 5s; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="falling-emoji brain emoji1">🧠</div>
    <div class="falling-emoji brain emoji2">🧠</div>
    <div class="falling-emoji brain emoji3">🧠</div>
    <div class="falling-emoji brain emoji4">🧠</div>
    <div class="falling-emoji brain emoji5">🧠</div>
    <div class="falling-emoji brain emoji6">🧠</div>
    <div class="falling-emoji brain emoji7">🧠</div>
    <div class="falling-emoji brain emoji8">🧠</div>
    <div class="falling-emoji brain emoji9">🧠</div>
    <div class="falling-emoji brain emoji10">🧠</div>
    
    <div class="falling-emoji music-note emoji11">🎶</div>
    <div class="falling-emoji music-note emoji12">🎵</div>
    <div class="falling-emoji music-note emoji13">🎧</div>
    <div class="falling-emoji music-note emoji14">🎼</div>
    <div class="falling-emoji music-note emoji15">🎤</div>
    <div class="falling-emoji music-note emoji16">🎶</div>
    <div class="falling-emoji music-note emoji17">🎵</div>
    <div class="falling-emoji music-note emoji18">🎧</div>
    <div class="falling-emoji music-note emoji19">🎼</div>
    <div class="falling-emoji music-note emoji20">🎤</div>
    
    <div class="falling-emoji headphones emoji21">🎧</div>
    <div class="falling-emoji headphones emoji22">🎧</div>
    <div class="falling-emoji headphones emoji23">🎧</div>
    <div class="falling-emoji headphones emoji24">🎧</div>
    <div class="falling-emoji headphones emoji25">🎧</div>
    <div class="falling-emoji headphones emoji26">🎧</div>
    <div class="falling-emoji headphones emoji27">🎧</div>
    <div class="falling-emoji headphones emoji28">🎧</div>
    <div class="falling-emoji headphones emoji29">🎧</div>
    <div class="falling-emoji headphones emoji30">🎧</div>
    """,
    unsafe_allow_html=True
)






#introduction
st.title("Music & Mental Health Survey Analysis")
st.markdown("""
Welcome to the **Music & Mental Health Interactive Dashboard**.

This page explores how
- **Listening time**
- **Exploratory behavior (trying new genres/artists)**
- **Tempo (BPM)**
- **Favorite genres & listening style**
- **Age groups**

relate to certain mental health conditions such as **anxiety, depression, insomnia, and OCD**.

Use the sidebar filters to shape your story.
""")

#sidebar navigation
sidebar()

#load dataset
from modules.app_core import survey
df = survey()

# Identify key columns
health_cols = [c for c in df.columns if any(x in c for x in ["Anxiety", "Depression", "Insomnia", "OCD"])]
genre_cols = [c for c in df.columns if c.startswith("Frequency [")]
bpm_col = "BPM" if "BPM" in df.columns else None

#frequency map for listening type
freq_map = {
    "Never": 0,
    "Rarely": 1,
    "Sometimes": 2,
    "Very frequently": 3
}

#convert frequency columns to numeric
genre_freq_cols = [col for col in df.columns if col.startswith("Frequency")]
df[genre_freq_cols] = df[genre_freq_cols].replace(freq_map)
df["active_genre_count"] = (df[genre_freq_cols] >= 2).sum(axis=1)
df["listening_type"] = df["active_genre_count"].apply(lambda x: "Single" if x == 1 else "Multiple")

#clean and prepare data
df_clean = df.dropna(subset=health_cols + ["Hours per day", "Exploratory", "Music effects"])
df_clean[genre_cols] = df_clean[genre_cols].apply(pd.to_numeric, errors="coerce")
df_clean[health_cols] = df_clean[health_cols].apply(pd.to_numeric, errors="coerce")

#add listening type
if "listening_type" in df.columns:
    df_clean["listening_type"] = df.loc[df_clean.index, "listening_type"]

#define age groups
if "Age" in df_clean.columns:
    df_clean["Age_Group"] = pd.cut(
        df_clean["Age"],
        bins=[0, 25, 40, 60, 100],
        labels=["18-25", "26-40", "41-60", "60+"],
        include_lowest=True
    )

#variety and average mental health
df_clean["Variety"] = (df_clean[genre_cols] > 0).sum(axis=1)
df_clean["Avg_health"] = df_clean[health_cols].mean(axis=1)

#sidebar filters header
st.sidebar.header("Filter Data")

#hours per day filter
min_hours, max_hours = int(df_clean["Hours per day"].min()), int(df_clean["Hours per day"].max())
hours_range = st.sidebar.slider(
    "Hours Listening per Day",
    min_hours,
    max_hours,
    (min_hours, max_hours)
)

#average mental health filter
min_health, max_health = float(df_clean["Avg_health"].min()), float(df_clean["Avg_health"].max())
health_range = st.sidebar.slider(
    "Average Mental Health Score",
    float(np.floor(min_health)),
    float(np.ceil(max_health)),
    (float(np.floor(min_health)), float(np.ceil(max_health)))
)

#bpm filter
if bpm_col and bpm_col in df_clean.columns:
    bpm_min = int(df_clean[bpm_col].min())
    bpm_max = int(min(df_clean[bpm_col].max(), 250))  # cap BPM at 250
    bpm_range = st.sidebar.slider(
        "BPM (Beats Per Minute)",
        bpm_min,
        bpm_max,
        (bpm_min, bpm_max)
    )
else:
    bpm_range = None

#apply filters
filtered_df = df_clean[
    (df_clean["Hours per day"].between(hours_range[0], hours_range[1])) &
    (df_clean["Avg_health"].between(health_range[0], health_range[1]))
].copy()

if bpm_range and bpm_col and bpm_col in filtered_df.columns:
    filtered_df = filtered_df[filtered_df[bpm_col].between(bpm_range[0], bpm_range[1])]

#summary of current selections
st.subheader("Current Data Slice")
st.markdown(f"""
- **Participants shown:** `{len(filtered_df)}`  
- **Hours per day filter:** `{hours_range[0]}–{hours_range[1]} hours`  
- **Average mental health score filter:** `{health_range[0]:.1f}–{health_range[1]:.1f}`
""")

st.divider()

#hours listening vs mental health
st.header("Does More Listening Affect Mental Health?")

st.markdown("""
Our first question is pretty simple: **Do people who listen to music for more hours per day report better or worse mental health on average?**
""")

if not filtered_df.empty:
    fig1 = px.scatter(
        filtered_df,
        x="Hours per day",
        y="Avg_health",
        trendline="ols",
        opacity=0.6,
        color_discrete_sequence=["#1f77b4"],
        labels={
            "Hours per day": "Hours Listening per Day",
            "Avg_health": "Average Mental Health Score"
        },
        title="Hours Listening per Day vs Average Mental Health"
    )
    fig1.update_traces(marker=dict(size=7))
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("No data available for the selected filters.")

st.divider()

#exploratory behavior vs how music affects them
st.header("🧭 Does Musical Curiosity Influence Reported Mental Health Effects?")

st.markdown("""
Next, we will look at **exploratory** behavior or whether people like to discover new artists and genres
and how that relates to the effects that they say music has on them.
""")

if not filtered_df.empty:
    fig2 = px.histogram(
        filtered_df,
        x="Music effects",
        color="Exploratory",
        barmode="group",
        text_auto=True,
        title="Exploring New Genres/Artists vs Reported Effects on Mental Health",
        labels={
            "Music effects": "Reported Effect of Music",
            "count": "Number of Respondents",
            "Exploratory": "Explores New Genres/Artists"
        }
    )
    fig2.update_layout(xaxis_tickangle=20)
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("No data available for the selected filters.")

st.divider()









# --- 3D Scatter Plot section ---
st.header("3D Scatter Plot (Insomnia vs Anxiety vs Depression)")

# Check if required columns are available in the dataset
required_columns = ['Insomnia', 'Anxiety', 'Depression', 'Age']
if all(col in filtered_df.columns for col in required_columns):
    try:
        # Create the 3D scatter plot using Plotly
        fig = px.scatter_3d(filtered_df, 
                            x='Insomnia', 
                            y='Anxiety', 
                            z='Depression', 
                            color='Age', 
                            color_continuous_scale="PRGn", 
                            template='plotly_white')
        
        # Update the marker size for better visualization
        fig.update_traces(marker=dict(size=5))
        
        # Render the plot in the Streamlit app
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error rendering 3D scatter plot: {str(e)}")
else:
    st.warning("Dataset does not contain the required columns for the 3D plot. Please ensure 'Insomnia', 'Anxiety', 'Depression', and 'Age' are available.")


#tempo and mental health
st.header("🎵 Does Tempo (BPM) Relate to Mental Health?")

st.markdown("""
Tempo, measured in **beats per minute (BPM)**, is often associated with our moods and energy levels.  
**Do people who prefer faster or slower music report different mental health outcomes?**
""")

if bpm_col and bpm_col in filtered_df.columns and not filtered_df.empty:
    #scatter plot
    st.subheader("BPM vs Average Mental Health")
    fig3 = px.scatter(
        filtered_df,
        x=bpm_col,
        y="Avg_health",
        color="Exploratory",
        trendline="ols",
        opacity=0.7,
        title="BPM (Beats Per Minute) vs Average Mental Health",
        labels={
            bpm_col: "Beats Per Minute (Preferred Tempo)",
            "Avg_health": "Average Mental Health Score",
            "Exploratory": "Explores New Genres"
        },
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig3.update_traces(marker=dict(size=8))
    st.plotly_chart(fig3, use_container_width=True)

    #box plot
    st.subheader("Mental Health Across BPM Ranges (Slow to Fast)")
    num_bins = 5
    try:
        bpm_series = filtered_df[bpm_col].dropna()
        if len(bpm_series) >= num_bins:
            bins = np.quantile(bpm_series, np.linspace(0, 1, num_bins + 1))
            bins = np.clip(bins, None, 250)
            bins = np.unique(bins)  #remove duplicates
            labels = [f"{int(bins[i])}-{int(bins[i+1])}" for i in range(len(bins) - 1)]

            filtered_df["BPM_Range"] = pd.cut(
                filtered_df[bpm_col],
                bins=bins,
                labels=labels,
                include_lowest=True
            )
            filtered_df["BPM_Range"] = pd.Categorical(
                filtered_df["BPM_Range"],
                categories=labels,
                ordered=True
            )

            fig4 = px.box(
                filtered_df.sort_values("BPM_Range"),
                x="BPM_Range",
                y="Avg_health",
                color="BPM_Range",
                title="Mental Health Scores Across BPM Ranges (Slow to Fast)",
                labels={
                    "BPM_Range": "Tempo Range (BPM)",
                    "Avg_health": "Average Mental Health Score"
                },
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig4.update_layout(showlegend=False)
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("Not enough unique BPM values to create meaningful BPM ranges.")
    except Exception as e:
        st.warning(f"Could not compute BPM bins: {e}")
else:
    st.info("BPM data not found.")

st.divider()

#favvorite genres and mental health
st.header("Which Genres Are Linked to Better or Worse Mental Health?")

st.markdown("""
Different genres come with different emotions.  
Here we are comparing **average mental health scores** to their **favorite genres**.
""")

if not filtered_df.empty and "Fav genre" in filtered_df.columns:
    genre_subset = filtered_df[["Fav genre"] + health_cols].dropna()
    if not genre_subset.empty:
        genre_means = genre_subset.groupby("Fav genre")[health_cols].mean().reset_index()
        genre_means["avg_score"] = genre_means[health_cols].mean(axis=1)
        genre_means = genre_means.sort_values("avg_score")

        fig5 = px.bar(
            genre_means,
            x="Fav genre",
            y=health_cols,
            barmode="group",
            title="Average Mental Health Scores vs Favorite Genre",
            labels={
                "value": "Average Mental Health Score",
                "Fav genre": "Music Genre"
            },
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        fig5.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.warning("No genre data available after filtering.")
else:
    st.warning("Favorite genre data is not available.")

st.divider()

#listening styles
st.header("Single-Genre vs Multi-Genre Listeners")

st.markdown("""
Some people spend most of their time with one favorite genre in particular, while others spread their listening across multiple genres.  
Here we are comparing mental health outcomes between these listening styles.
""")

if "listening_type" in filtered_df.columns and not filtered_df.empty:
    subset = filtered_df[["listening_type"] + health_cols].dropna()
    if not subset.empty:
        mh_melted = subset.melt(
            id_vars="listening_type",
            value_vars=health_cols,
            var_name="Condition",
            value_name="Score"
        )

        fig6 = px.box(
            mh_melted,
            x="listening_type",
            y="Score",
            color="Condition",
            title="Single vs Multi-Genre Listeners",
            labels={"listening_type": "Listening Style"}
        )
        st.plotly_chart(fig6, use_container_width=True)
    else:
        st.warning("No data for listening type comparison after filtering.")
else:
    st.warning("listening_type not found.")

st.divider()

#age group differences
st.header("How Does Age Affect Our Listening Habits and Overall Mental Health?")

st.markdown("""
Finally, we looked at different age groups to see how mental health and listening behavior interact at different stages of life.
""")

if not filtered_df.empty and "Age_Group" in filtered_df.columns:
    #group by age and compute averages
    age_group_summary = filtered_df.groupby("Age_Group")[health_cols].mean()
    age_group_summary["Avg_Hours"] = filtered_df.groupby("Age_Group")["Hours per day"].mean()

    #heatmap
    fig7 = go.Figure(
        data=go.Heatmap(
            z=age_group_summary.values,
            x=age_group_summary.columns,
            y=age_group_summary.index,
            colorscale="RdBu",
            reversescale=True,
            text=np.round(age_group_summary.values, 2),
            texttemplate="%{text}",
            textfont={"size": 12},
            hovertemplate="Age Group: %{y}<br>%{x}: %{z:.2f}<extra></extra>"
        )
    )

    fig7.update_layout(
        title="Average Mental Health Scores + Average Hours by Age Group",
        xaxis_title="Mental Health Conditions + Avg Hours",
        yaxis_title="Age Group",
        yaxis=dict(autorange="reversed"),
        height=400,
        margin=dict(l=60, r=20, t=60, b=40)
    )

    st.plotly_chart(fig7, use_container_width=True)
else:
    st.warning("No age group data available for the selected filters.")

st.divider()

#summary
st.header("Summary")

st.markdown("""
This dashboard is meant to help you explore patterns, not to give actual medical advice.  
However, you can use it to ask questions like:

- Do people who listen more hours report better or worse mental health?
- Does exploring new genres relate to more positive effects from music?
- Are faster tempos associated with different emotional states? What about slower tempos?
- Which genres appear alongside higher or lower average mental health scores?
- Do multi-genre listeners differ from single-genre listeners?
- How do these patterns shift across different age groups?

Try adjusting the filters on the left to see how the story changes for different subsets of listeners.
"""

)






