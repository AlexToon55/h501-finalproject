import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
import plotly.graph_objects as go

from modules.app_core import config, survey, page_header
from modules.nav import sidebar

#streamlit setup
st.set_page_config(page_title="Music & Mental Health", layout="wide")

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
st.header("Does Musical Curiosity Influence Reported Mental Health Effects?")

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

#tempo and mental health
st.header("Does Tempo (BPM) Relate to Mental Health?")

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

