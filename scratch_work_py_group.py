import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
import plotly.graph_objects as go

from modules.nav import sidebar

# PAGE CONFIG
st.set_page_config(
    page_title="Music & Mental Health Dashboard",
    layout="wide",
)

# Sticky sidebar nav
sidebar()


# HEADER BANNER (Soft Purple)

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

# FIXED INTRO (Non-Collapsible)

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
    - Patterns across user choices  

    Scroll through to discover meaningful connections between music and mental well-being.
    """
)

st.markdown("<hr style='margin:30px 0;'>", unsafe_allow_html=True)


url = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vRkL35eEcZvs9VtRLf8aIkow3SOybhdZpqOyHMNsia523mKec7sSGAiECVoG9WKaBFtliAXrO5itez3/"
    "pub?gid=760116139&single=true&output=csv"
)
df = pd.read_csv(url)
df.columns = df.columns.str.strip()

health_cols = ['Anxiety', 'Depression', 'Insomnia', 'OCD']
genre_col = "Fav genre"

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

if selected_genre != "All":
    filtered_df = filtered_df[filtered_df[genre_col] == selected_genre]

for col, (low, high) in score_filters.items():
    filtered_df = filtered_df[(filtered_df[col] >= low) & (filtered_df[col] <= high)]

# KPI CARDS

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

# CHART – Mental Health by Genre
st.header("Mental Health Issues by Genre")

health_df = filtered_df[[genre_col] + health_cols].copy()
health_df[health_cols] = (health_df[health_cols] >= 5).astype(int)
health_df = health_df[health_df[health_cols].sum(axis=1) >= 2]

melted = health_df.melt(id_vars=genre_col, var_name='Mental Health Issue', value_name='Has Issue')
summary_health = melted.groupby([genre_col, 'Mental Health Issue'])['Has Issue'].mean().reset_index()
summary_health['Has Issue'] *= 100

fig1 = px.bar(
    summary_health,
    x=genre_col,
    y='Has Issue',
    color='Mental Health Issue',
    barmode='group',
    color_discrete_sequence=px.colors.qualitative.Pastel1
)
fig1.update_layout(xaxis_tickangle=45)
st.plotly_chart(fig1, use_container_width=True)

top_issue = summary_health.groupby(genre_col)['Has Issue'].mean().idxmax()
worst_rate = summary_health.groupby(genre_col)['Has Issue'].mean().max()
arrow = "↑ Higher concern" if worst_rate > 40 else "→ Moderate levels"

st.markdown(
    f"""
    <div style="background:#FFF7FA; padding:15px; border-radius:10px; margin-top:10px;">
        <b>🔍 Insight:</b> {arrow}<br>
        <i>Listeners of <b>{top_issue}</b> report the highest combined mental health symptoms
        (~{worst_rate:.1f}%).</i>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr style='margin:30px 0;'>", unsafe_allow_html=True)

# CHART – Average Listening Hours
st.header("Average Listening Hours by Genre")

summary_hours = filtered_df.groupby('Fav genre')['Hours per day'].mean().reset_index()

fig2 = px.bar(
    summary_hours,
    x='Fav genre',
    y='Hours per day',
    color='Hours per day',
    color_continuous_scale=px.colors.qualitative.Pastel1
)
fig2.update_layout(xaxis_tickangle=45)
st.plotly_chart(fig2, use_container_width=True)

max_genre = summary_hours.loc[summary_hours['Hours per day'].idxmax(), 'Fav genre']
max_val = summary_hours['Hours per day'].max()

trend = "↑ High listening engagement" if max_val > 3 else "→ Moderate engagement"

st.markdown(
    f"""
    <div style="background:#F7FAFF; padding:15px; border-radius:10px; margin-top:10px;">
        <b>🎧 Insight:</b> {trend}<br>
        <i>Fans of <b>{max_genre}</b> listen the most, averaging <b>{max_val:.2f} hours/day</b>.</i>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr style='margin:30px 0;'>", unsafe_allow_html=True)

# CHART – Emotional Impact
st.header("Music’s Emotional Impact by Genre")

filtered_health = filtered_df[filtered_df[health_cols].ge(5).sum(axis=1) >= 2]
summary_effects = filtered_health.groupby(['Fav genre', 'Music effects']).size().reset_index(name='Count')

fig3 = px.bar(
    summary_effects,
    x='Fav genre',
    y='Count',
    color='Music effects',
    barmode='stack',
    color_discrete_sequence=px.colors.qualitative.Pastel2
)
fig3.update_layout(xaxis_tickangle=45)
st.plotly_chart(fig3, use_container_width=True)

top_effect_genre = summary_effects.groupby('Fav genre')['Count'].sum().idxmax()
top_effect = summary_effects.groupby('Music effects')['Count'].sum().idxmax()

st.markdown(
    f"""
    <div style="background:#FFF9F3; padding:15px; border-radius:10px; margin-top:10px;">
        <b>🎭 Emotional Insight:</b><br>
        <i>Listeners of <b>{top_effect_genre}</b> show the strongest emotional response.
        The most common reported effect is <b>{top_effect}</b>.</i>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr style='margin:30px 0;'>", unsafe_allow_html=True)

# CHART – Genre Popularity
st.header("Genre Popularity")

summary_counts = filtered_df['Fav genre'].value_counts().reset_index()
summary_counts.columns = ['Fav genre', 'Count']

fig4 = px.bar(
    summary_counts,
    x='Fav genre',
    y='Count',
    color='Count',
    color_continuous_scale=px.colors.qualitative.Pastel2
)
fig4.update_layout(xaxis_tickangle=45)
st.plotly_chart(fig4, use_container_width=True)

top_genre = summary_counts.loc[summary_counts['Count'].idxmax(), 'Fav genre']

st.markdown(
    f"""
    <div style="background:#F4FFFA; padding:15px; border-radius:10px; margin-top:10px;">
        <b>⭐ Popularity Insight:</b><br>
        <i><b>{top_genre}</b> is the most frequently selected favorite genre.</i>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr style='margin:30px 0;'>", unsafe_allow_html=True)
