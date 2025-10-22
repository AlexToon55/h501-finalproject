import pandas as pd
import plotly.express as px
import streamlit as st

#streamlit
st.set_page_config(page_title="Music & Mental Health", layout="wide")
st.title("🎵 Music & Mental Health Survey Analysis (Interactive Dashboard)")

#load database
df = pd.read_csv("mxmh_survey_results.csv")

#select columns
health_cols = ["Anxiety", "Depression", "Insomnia", "OCD"]
genre_cols = [c for c in df.columns if c.startswith("Frequency [")]

#drop rows with missing key values
df_clean = df.dropna(subset=health_cols + ["Hours per day", "Exploratory", "Music effects"])

#convert frequency and health columns to numeric
df_clean[genre_cols] = df_clean[genre_cols].apply(pd.to_numeric, errors="coerce")
df_clean[health_cols] = df_clean[health_cols].apply(pd.to_numeric, errors="coerce")

#create metrics
df_clean["Variety"] = (df_clean[genre_cols] > 0).sum(axis=1)
df_clean["Avg_health"] = df_clean[health_cols].mean(axis=1)

#sidebar filters
st.sidebar.header("🧭 Filter Data")

#hours listening
min_hours, max_hours = int(df_clean["Hours per day"].min()), int(df_clean["Hours per day"].max())
hours_range = st.sidebar.slider("🎚 Hours Listening per Day", min_hours, max_hours, (min_hours, max_hours))

#average health score
min_health, max_health = float(df_clean["Avg_health"].min()), float(df_clean["Avg_health"].max())
health_range = st.sidebar.slider("🧠 Average Mental Health Score", min_health, max_health, (min_health, max_health))

#dataframe
filtered_df = df_clean[
    (df_clean["Hours per day"].between(hours_range[0], hours_range[1])) &
    (df_clean["Avg_health"].between(health_range[0], health_range[1]))
].copy()

# --- Layout: 2 columns ---
col1, col2 = st.columns(2)

# -----------------------------------------
# 1. Hours Listening vs Average Health
# -----------------------------------------
with col1:
    st.subheader("Hours Listening vs Mental Health")

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
        title="Does listening longer affect mental health?"
    )
    fig1.update_traces(marker=dict(size=7))
    st.plotly_chart(fig1, use_container_width=True)

# -----------------------------------------
# 2. Exploratory vs Reported Music Effects
# -----------------------------------------
with col2:
    st.subheader("Exploring New Genres vs Reported Effects")

    fig2 = px.histogram(
        filtered_df,
        x="Music effects",
        color="Exploratory",
        barmode="group",
        text_auto=True,
        title="Exploring new genres/artists vs reported effects on mental health",
        labels={"Music effects": "Reported Effect of Music", "count": "Number of Respondents"}
    )
    fig2.update_layout(xaxis_tickangle=20)
    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------------------
# 3. BPM vs Mental Health Visualization
# -----------------------------------------
st.subheader("🎚 Relationship Between BPM and Mental Health")

if "BPM" in filtered_df.columns:
    # --- Scatter Plot: BPM vs Avg Health ---
    st.markdown("#### 🔹 Scatter: Does faster music correlate with better or worse mental health?")
    fig3 = px.scatter(
        filtered_df,
        x="BPM",
        y="Avg_health",
        color="Exploratory",
        trendline="ols",
        opacity=0.7,
        title="BPM (Beats Per Minute) vs Average Mental Health",
        labels={
            "BPM": "Beats Per Minute (Preferred Tempo)",
            "Avg_health": "Average Mental Health Score",
            "Exploratory": "Explores New Genres"
        },
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig3.update_traces(marker=dict(size=8))
    st.plotly_chart(fig3, use_container_width=True)

    # --- Box Plot: Group BPM ranges ---
    st.markdown("#### 🔹 Box Plot: Mental Health Across BPM Ranges")

    # Define BPM categories for visualization
    bins = [0, 80, 100, 120, 140, 200]
    labels = ["Slow (<80)", "Medium (80–100)", "Moderate (100–120)", "Fast (120–140)", "Very Fast (>140)"]
    filtered_df["BPM_Range"] = pd.cut(filtered_df["BPM"], bins=bins, labels=labels, include_lowest=True)

    fig4 = px.box(
        filtered_df,
        x="BPM_Range",
        y="Avg_health",
        color="BPM_Range",
        title="Mental Health Scores Across BPM Ranges",
        labels={"BPM_Range": "Tempo Range", "Avg_health": "Average Mental Health Score"},
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig4.update_layout(showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)

else:
    st.info("⚠️ BPM data not found in this dataset.")
