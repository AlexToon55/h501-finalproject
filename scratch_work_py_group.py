import pandas as pd
import plotly.express as px
import streamlit as st

# load data
url = ( 
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vRkL35eEcZvs9VtRLf8aIkow3SOybhdZpqOyHMNsia523mKec7sSGAiECVoG9WKaBFtliAXrO5itez3/"
    "pub?gid=760116139&single=true&output=csv"
)
df = pd.read_csv(url)

# === Page Config ===
st.set_page_config(page_title=" Music & Mental Health Dashboard", layout="wide")

st.markdown(
    f"""
    #  Music & Mental Health Dashboard

    **Total Respondents:** {df.shape[0]}  
    **Average Listening Hours per Day:** {df['Hours per day'].mean():.2f}  
    **Average Age of Respondents:** {df['Age'].mean():.2f}  
    **Total Genres:** {df['Fav genre'].nunique()}
    """,
    unsafe_allow_html=True
)

# === Prepare Health Data ===
health_cols = ['Anxiety', 'Depression', 'Insomnia', 'OCD']
genre_col = 'Fav genre'

health_df = df[[genre_col] + health_cols].copy()
health_df[health_cols] = (health_df[health_cols] >= 5).astype(int)
health_df = health_df[health_df[health_cols].sum(axis=1) >= 2]

melted = health_df.melt(id_vars=genre_col, var_name='Mental Health Issue', value_name='Has Issue')
summary_health = melted.groupby([genre_col, 'Mental Health Issue'])['Has Issue'].mean().reset_index()
summary_health['Has Issue'] *= 100

# === Charts ===
custom_blues = ['#6BAED6', '#3182BD', '#08519C', '#08306B']
fig1 = px.bar(
    summary_health,
    x=genre_col,
    y='Has Issue',
    color='Mental Health Issue',
    barmode='group',
    title="Proportion of Respondents with Multiple Mental Health Issues by Genre",
    color_discrete_sequence=custom_blues
)
fig1.update_layout(xaxis_tickangle=45, yaxis_title="% of Respondents", title_font_size=20)

# Average Listening Hours by Genre
summary_hours = df.groupby('Fav genre')['Hours per day'].mean().reset_index()
fig2 = px.bar(
    summary_hours,
    x='Fav genre',
    y='Hours per day',
    title="Average Daily Listening Hours by Genre",
    color='Hours per day',
    color_continuous_scale='Blues'
)
fig2.update_layout(xaxis_tickangle=45, yaxis_title="Hours", title_font_size=20)

# Music Effects Chart
filtered_df = df[df[health_cols].ge(5).sum(axis=1) >= 2]
summary_effects = filtered_df.groupby(['Fav genre', 'Music effects']).size().reset_index(name='Count')
custom_blues_2 = ['#6BAED6', '#3182BD', '#08519C']
fig3 = px.bar(
    summary_effects,
    x='Fav genre',
    y='Count',
    color='Music effects',
    barmode='stack',
    title="Beliefs About Music's Mental Health Effects by Genre",
    color_discrete_sequence=custom_blues_2
)
fig3.update_layout(xaxis_tickangle=45, yaxis_title="Number of Respondents", title_font_size=20)

# Example fourth chart: number of respondents per genre
summary_counts = df['Fav genre'].value_counts().reset_index()
summary_counts.columns = ['Fav genre', 'Count']
fig4 = px.bar(
    summary_counts,
    x='Fav genre',
    y='Count',
    title="Number of Respondents per Genre",
    color='Count',
    color_continuous_scale='Blues'
)
fig4.update_layout(xaxis_tickangle=45, yaxis_title="Count", title_font_size=20)

# === Tabs Layout ===
tab1, tab2, tab3, tab4 = st.tabs([
    "Multiple Mental Health Issues", "Avg Listening Hours", 
    "Music Effects", "Respondents per Genre"
])

with tab1:
    st.plotly_chart(fig1, use_container_width=True)
with tab2:
    st.plotly_chart(fig2, use_container_width=True)
with tab3:
    st.plotly_chart(fig3, use_container_width=True)
with tab4:
    st.plotly_chart(fig4, use_container_width=True)

