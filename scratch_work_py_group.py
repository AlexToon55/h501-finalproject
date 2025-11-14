import pandas as pd
import plotly.express as px
import streamlit as st

# Load Data
url = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vRkL35eEcZvs9VtRLf8aIkow3SOybhdZpqOyHMNsia523mKec7sSGAiECVoG9WKaBFtliAXrO5itez3/"
    "pub?gid=760116139&single=true&output=csv"
)
df = pd.read_csv(url)

#Clean & Prepare Columns
df.columns = df.columns.str.strip()
health_cols = ['Anxiety', 'Depression', 'Insomnia', 'OCD']
genre_col = 'Fav genre'

# Ensure numeric
for col in health_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Streamlit Page Config
st.set_page_config(page_title="Music & Mental Health Dashboard", layout="wide")
st.title(" Music & Mental Health Dashboard")

# Sidebar for Interactivity
st.sidebar.header("🎧 Filters")

# Genre dropdown
genres = sorted(df[genre_col].dropna().unique())
selected_genre = st.sidebar.selectbox("Select Genre", ["All"] + genres)

# Individual sliders for each mental health column (integers only)
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

# Filter data dynamically
filtered_df = df.copy()

# Apply genre filter
if selected_genre != "All":
    filtered_df = filtered_df[filtered_df[genre_col] == selected_genre]

# Apply score filters
for col, (low, high) in score_filters.items():
    filtered_df = filtered_df[(filtered_df[col] >= low) & (filtered_df[col] <= high)]

# Summary Stats
st.markdown(
    f"""
    **Total Respondents (after filtering):** {filtered_df.shape[0]}  
    **Average Listening Hours per Day:** {filtered_df['Hours per day'].mean():.2f}  
    **Average Age of Respondents:** {filtered_df['Age'].mean():.2f}  
    **Total Genres in Filtered Data:** {filtered_df['Fav genre'].nunique()}
    """,
    unsafe_allow_html=True
)

# Prepare Health Data 
health_df = filtered_df[[genre_col] + health_cols].copy()
health_df[health_cols] = (health_df[health_cols] >= 5).astype(int)
health_df = health_df[health_df[health_cols].sum(axis=1) >= 2]

melted = health_df.melt(id_vars=genre_col, var_name='Mental Health Issue', value_name='Has Issue')
summary_health = melted.groupby([genre_col, 'Mental Health Issue'])['Has Issue'].mean().reset_index()
summary_health['Has Issue'] *= 100

# Charts
custom_blues = ['#6BAED6', '#3182BD', '#08519C', '#08306B']

# Chart 1: Multiple Mental Health Issues by Genre
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

# Chart 2: Average Listening Hours by Genre
summary_hours = filtered_df.groupby('Fav genre')['Hours per day'].mean().reset_index()
fig2 = px.bar(
    summary_hours,
    x='Fav genre',
    y='Hours per day',
    title="Average Daily Listening Hours by Genre",
    color='Hours per day',
    color_continuous_scale='Blues'
)
fig2.update_layout(xaxis_tickangle=45, yaxis_title="Hours", title_font_size=20)

# Chart 3: Music Effects by Genre
filtered_health = filtered_df[filtered_df[health_cols].ge(5).sum(axis=1) >= 2]
summary_effects = filtered_health.groupby(['Fav genre', 'Music effects']).size().reset_index(name='Count')
fig3 = px.bar(
    summary_effects,
    x='Fav genre',
    y='Count',
    color='Music effects',
    barmode='stack',
    title="Beliefs About Music's Mental Health Effects by Genre",
    color_discrete_sequence=custom_blues
)
fig3.update_layout(xaxis_tickangle=45, yaxis_title="Number of Respondents", title_font_size=20)

# Chart 4: Respondents per Genre
summary_counts = filtered_df['Fav genre'].value_counts().reset_index()
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

# Tabs Layout
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