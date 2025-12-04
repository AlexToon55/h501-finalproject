import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import base64

from modules.nav import sidebar

# PAGE CONFIG
st.set_page_config(
    page_title="Music & Mental Health Dashboard",
    layout="wide",
)

# Sticky sidebar nav
sidebar() 

# HEADER BANNER (Violet background)
st.markdown(
    """
    <div style="
        background: linear-gradient(90deg, #A78BFA, #C4B5FD);
        padding: 26px 35px;
        border-radius: 12px;
        color: white;
        margin-bottom: 30px;">
        <h1 style="margin: 0; font-size: 36px;">🎶 Music & Mental Health Dashboard</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# INTRO + DISCLAIMER + ORIGINAL INSIGHT LIST
st.markdown(
    """
    ### 💬 About This Dashboard

    Music shapes mood, influences focus, and supports emotional well-being.  
    This dashboard explores how **listening habits**, **favorite genres**, and  
    **self-reported mental health** interact across a wide range of listeners.

    You’ll find insights on:
    - Daily listening time  
    - Favorite genres  
    - Music’s emotional effects  
    - Mental health indicators (anxiety, depression, insomnia, OCD) 

    Scroll through to discover meaningful connections between music and well-being.

    🔎 *Note: These visualizations show self-reported survey data for exploration only.  
    They do **not** diagnose mental-health conditions.*
    """
)

st.markdown("<hr style='margin:30px 0;'>", unsafe_allow_html=True)

# LOAD DATA
url = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vRkL35eEcZvs9VtRLf8aIkow3SOybhdZpqOyHMNsia523mKec7sSGAiECVoG9WKaBFtliAXrO5itez3/"
    "pub?gid=760116139&single=true&output=csv"
)
df = pd.read_csv(url)
df.columns = df.columns.str.strip()

health_cols = ['Anxiety', 'Depression', 'Insomnia', 'OCD']
genre_col = "Fav genre"

# Ensure the health columns are numeric
for col in health_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# SIDEBAR FILTERS
st.sidebar.header("🎧 Filters")

genres = sorted(df[genre_col].dropna().unique())
selected_genre = st.sidebar.selectbox("Select Genre", ["All"] + genres)

score_filters = {}
for col in health_cols:
    min_val = int(df[col].min())
    max_val = int(df[col].max())
    score_filters[col] = st.sidebar.slider(
        f"{col} Score Range",
        min_value=min_val,
        max_value=max_val,
        value=(min_val, max_val),
        step=1
    )

filtered_df = df.copy()

# Apply genre filter
if selected_genre != "All":
    filtered_df = filtered_df[filtered_df[genre_col] == selected_genre]

# Apply mental health filters
for col, (low, high) in score_filters.items():
    filtered_df = filtered_df[(filtered_df[col] >= low) & (filtered_df[col] <= high)]

# WARNING IF SAMPLE TOO SMALL
if filtered_df.shape[0] < 50:
    st.warning("⚠️ Many responses were removed, so the results may not reflect everyone’s opinions.")

# KPI CARDS
st.markdown(
    """
    <style>
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        cursor: default !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# KPIs
total_resp = filtered_df.shape[0]
avg_hours = filtered_df["Hours per day"].mean()
avg_age = filtered_df["Age"].mean()
genre_count = filtered_df["Fav genre"].nunique()

k1, k2, k3, k4 = st.columns(4)

k1.metric("👥 Respondents", total_resp)
k2.metric("⏱ Avg Listening (hrs/day)", f"{avg_hours:.2f}")
k3.metric("🎂 Avg Age", f"{avg_age:.1f}")
k4.metric("🎵 Genres Present", genre_count)

st.markdown("<hr style='margin:30px 0;'>", unsafe_allow_html=True)

# 1. MENTAL HEALTH BY GENRE
st.header("Mental Health Indicators by Genre (Average Scores)")

summary_health = filtered_df.groupby(genre_col)[health_cols].mean().reset_index()
summary_health = summary_health.melt(id_vars=genre_col, var_name='Mental Health Issue', value_name='Average Score')

fig1 = px.bar(
    summary_health,
    x=genre_col,
    y='Average Score',
    color='Mental Health Issue',
    barmode='group',
    color_discrete_sequence=px.colors.qualitative.Pastel1 
)
fig1.update_layout(xaxis_tickangle=45)
st.plotly_chart(fig1, use_container_width=True)

# Insight
top_issue = summary_health.groupby(genre_col)['Average Score'].mean().idxmax()
top_value = summary_health.groupby(genre_col)['Average Score'].mean().max()

st.markdown(
    f"""
    <div style="background:#FFF7FA; padding:15px; border-radius:10px; margin-top:10px;">
        <b>🔍 Insight:</b><br>
        <i>Genres vary in average mental-health scores.  
        Currently, <b>{top_issue}</b> has the highest overall average score (~{top_value:.2f}).</i>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr style='margin:30px 0;'>", unsafe_allow_html=True)

# 2. AVERAGE LISTENING HOURS
st.header("Average Listening Hours by Genre")

summary_hours = filtered_df.groupby('Fav genre')['Hours per day'].mean().reset_index()

fig2 = px.bar(
    summary_hours,
    x='Fav genre',
    y='Hours per day',
    color='Hours per day',
    color_continuous_scale=['#F1FAEE','#A8DADC','#457B9D','#1D3557']  # Hues of Blue for soft, calm theme
)
fig2.update_layout(xaxis_tickangle=45)
st.plotly_chart(fig2, use_container_width=True)

max_genre = summary_hours.loc[summary_hours['Hours per day'].idxmax(), 'Fav genre']
max_val = summary_hours['Hours per day'].max()

st.markdown(
    f"""
    <div style="background:#F7FAFF; padding:15px; border-radius:10px; margin-top:10px;">
        <b>🎧 Insight:</b><br>
        <i>Fans of <b>{max_genre}</b> currently listen the most, averaging  
        about <b>{max_val:.2f} hours/day</b>.</i>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr style='margin:30px 0;'>", unsafe_allow_html=True)

# 3. EMOTIONAL IMPACT
st.header("Music’s Emotional Impact by Genre")

summary_effects = filtered_df.groupby(['Fav genre', 'Music effects']).size().reset_index(name='Count')

fig3 = px.bar(
    summary_effects,
    x='Fav genre',
    y='Count',
    color='Music effects',
    barmode='stack',
    color_discrete_sequence=px.colors.qualitative.Pastel1
)
fig3.update_layout(
    xaxis_tickangle=45,
    yaxis_title="Number of Respondents Reporting Emotional Impact"
)

st.plotly_chart(fig3, use_container_width=True)

top_effect_genre = summary_effects.groupby('Fav genre')['Count'].sum().idxmax()
top_effect = summary_effects.groupby('Music effects')['Count'].sum().idxmax()

st.markdown(
    f"""
    <div style="background:#FFF9F3; padding:15px; border-radius:10px; margin-top:10px;">
        <b>🎭 Emotional Insight:</b><br>
        <i>Listeners of <b>{top_effect_genre}</b> show the strongest emotional
        response overall.  
        The most commonly reported emotional effect is <b>{top_effect}</b>.</i>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr style='margin:30px 0;'>", unsafe_allow_html=True)

# 4. GENRE POPULARITY
st.header("Genre Popularity")

# Count the number of times each genre appears
summary_counts = filtered_df['Fav genre'].value_counts().reset_index()
summary_counts.columns = ['Fav genre', 'Count']

# Plot the genre popularity as a bar chart
fig4 = px.bar(
    summary_counts,
    x='Fav genre',
    y='Count',
    color='Count',
    color_continuous_scale=['#A8DADC','#7FB3B5', '#457B9D', '#1D3557'] # Hues of Blue for consistency
)

fig4.update_layout(
    xaxis_tickangle=45,
    yaxis_title="Number of Respondents Choosing Genre" 
)

st.plotly_chart(fig4, use_container_width=True)

# Get the genre with the maximum count for the insight
top_genre = summary_counts.loc[summary_counts['Count'].idxmax(), 'Fav genre']

st.markdown(
    f"""
    <div style="background:#F4FFFA; padding:15px; border-radius:10px; margin-top:10px;">
        <b>⭐ Popularity Insight:</b><br>
        <i><b>{top_genre}</b> is currently the most frequently selected favorite genre.</i>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("<br><br>", unsafe_allow_html=True)

# 5. BRAIN WAVES & MUSIC
st.header("🧠 Brain Waves, Emotions & Music")
st.markdown("<br><br>", unsafe_allow_html=True)
# Brain Waves Image (centered)
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image(
        "frontend/assets/BrainWaves.jpg",
        caption="Brain wave frequency ranges and associated states",
        width=450   # adjust this number (300–450 works nicely)
    )

# Brain Waves Section
st.markdown(
    """
    <div style="background:#F0F4FF; padding:20px; border-radius:12px; margin-top:10px;">
        <h3>Brain Waves</h3>
        <p>
        Gamma Waves >30 Hz (Associated with ability to process auditory and visual stimuli and our ability to learn)​<br>
        Beta Waves 12-30 Hz (Associated with highest levels of attention)(Signify Alertness and Logic)(Beta waves of 22-30 Hz can be characterized as anxiety)​<br>
        Alpha Waves 8-12 Hz (Associated with relaxed wakefulness and unique thoughts)(Aid in mental coordination and calmness)​<br>
        Theta Waves 4-8 Hz (Associated with creativity, memory, and dreams)(Are not an external factor but are believed to be a part of the inner sense of the body)​<br>
        Delta Waves 1-4 Hz (Associated with deep sleep and relaxation)(Their presence leads to less anxiety, improved sleep, and relief from headaches)(Deteriorate as you age)
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Brain Waves → Emotions → Music
st.markdown(
    """
    <div style="background:#E8F5E9; padding:20px; border-radius:12px; margin-top:10px;">
        <h3>Brain Waves → Emotions → Music</h3>
        <p>
        Gamma Waves > Joy/Insightful > complex and dynamic genres (Metal/Complex Jazz)​<br>
        Beta Waves > Active thinking/Anxiety > Fast Pop/EDM​<br>
        Alpha Waves > Focused/Balanced/Mindful > Lofi/Chill/Soft Rock​<br>
        Theta Waves > Creativity/Memory > Acoustic/Relaxing Music​<br>
        Delta Waves > Sleep/Restorative/Healing > Ambient/Classical
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Load image and encode as base64
with open("frontend/assets/Neurable.jpg", "rb") as img_file:
    encoded_img = base64.b64encode(img_file.read()).decode()

# Neurable section with text and image together
st.markdown(
    f"""
    <div style="display: flex; align-items: center; background:#FFF7FA; padding:20px; border-radius:12px; margin-top:10px;">
        <div style="flex: 2; padding-right:20px;">
            <h3>Neurable (Wearable brain wave scanning headset)</h3>
            <p>
            Uses EEG to measure brain waves and displays in app. You choose what type of activity you are doing (work, study, entertainment, creative).<br>
            The app displays high, medium, and low focus moments throughout the day and tells you what activity you were doing as long as you enter in your info.<br>
            Currently can be a bit limited in reading brain waves (interference such as hair).<br>
            <a href="https://www.wired.com/story/this-brain-tracking-device-wants-to-help-you-work-smarter/" target="_blank">Read more here</a>
            </p>
        </div>
        <div style="flex: 1;">
            <img src="data:image/jpeg;base64,{encoded_img}" style="width:100%; border-radius:12px;">
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Future Outlook Section
st.markdown(
    """
    <div style="background:#FFF8E1; padding:20px; border-radius:12px; margin-top:10px;">
        <h3>Future Outlook</h3>
        <p>
        Currently users can see how our app turns listening habits into insights, and insights into emotional awareness.  
        Devices like the Neurable brain wave headset can help us learn more about the connections between music and mental health.  
        Repeated data gathering can help optimize the user music experience and improve mental and emotional health.  
        Imagine what real-time data could do to close the loop between emotion, music, and mental health!
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr style='margin:30px 0;'>", unsafe_allow_html=True)
