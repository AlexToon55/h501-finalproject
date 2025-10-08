import pandas as pd
import plotly.express as px
import streamlit as st

# --- Streamlit Setup ---
st.set_page_config(page_title="Music & Mental Health", layout="wide")
st.title("🎵 Music & Mental Health Survey Analysis (Interactive Dashboard)")

# --- Load dataset ---
@st.cache_data
def load_data():
    return pd.read_csv("mxmh_survey_results.csv")

df = load_data()

# --- Select relevant columns ---
health_cols = ["Anxiety", "Depression", "Insomnia", "OCD"]
genre_cols = [c for c in df.columns if c.startswith("Frequency [")]

# Drop rows with missing key values
df_clean = df.dropna(subset=health_cols + ["Hours per day", "Exploratory", "Music effects"])

# Convert frequency & health columns to numeric
df_clean[genre_cols] = df_clean[genre_cols].apply(pd.to_numeric, errors="coerce")
df_clean[health_cols] = df_clean[health_cols].apply(pd.to_numeric, errors="coerce")

# --- Create metrics ---
df_clean["Variety"] = (df_clean[genre_cols] > 0).sum(axis=1)
df_clean["Avg_health"] = df_clean[health_cols].mean(axis=1)

# --- Sidebar filters ---
st.sidebar.header("🧭 Filter Data")

# Hours listening filter
min_hours, max_hours = int(df_clean["Hours per day"].min()), int(df_clean["Hours per day"].max())
hours_range = st.sidebar.slider("🎚 Hours Listening per Day", min_hours, max_hours, (min_hours, max_hours))

# Average health score filter
min_health, max_health = float(df_clean["Avg_health"].min()), float(df_clean["Avg_health"].max())
health_range = st.sidebar.slider("🧠 Average Mental Health Score", min_health, max_health, (min_health, max_health))

# Genre filter
selected_genres = st.sidebar.multiselect(
    "🎵 Select Genres (for variety calculation)",
    options=genre_cols,
    default=genre_cols[:5]
)

# Filter the dataframe
filtered_df = df_clean[
    (df_clean["Hours per day"].between(hours_range[0], hours_range[1])) &
    (df_clean["Avg_health"].between(health_range[0], health_range[1]))
].copy()

# --- Layout: 2 columns ---
col1, col2 = st.columns(2)

# -----------------------------------------
# 1. Hours Listening vs Avg Health
# -----------------------------------------
with col1:
    st.subheader("🎧 Hours Listening vs Mental Health")

    fig1 = px.scatter(
        filtered_df,
        x="Hours per day",
        y="Avg_health",
        opacity=0.6,
        trendline=None,  # <-- explicitly disable trendline
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
# 2. Exploratory vs Music Effects
# -----------------------------------------
with col2:
    st.subheader("🎶 Exploring New Genres vs Reported Effects")

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
# 3. Variety vs Health
# -----------------------------------------
if selected_genres:
    st.subheader("🎵 Variety of Genres vs Mental Health")

    filtered_df["Selected_Variety"] = (filtered_df[selected_genres] > 0).sum(axis=1)

    fig3 = px.scatter(
        filtered_df,
        x="Selected_Variety",
        y="Avg_health",
        opacity=0.6,
        trendline=None,  # <-- explicitly disable trendline
        color_discrete_sequence=["#2ca02c"],
        labels={
            "Selected_Variety": "Number of Genres Listened To",
            "Avg_health": "Average Mental Health Score"
        },
        title="Does listening to more genres affect mental health?"
    )
    fig3.update_traces(marker=dict(size=7))
    st.plotly_chart(fig3, use_container_width=True)
