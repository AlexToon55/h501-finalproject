from io import BytesIO
import base64
import os
from typing import Optional

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# Streamlit page config
st.set_page_config(page_title="Music & Mental Health Explorer", layout="wide", initial_sidebar_state="expanded")

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


try:
    from ydata_profiling import ProfileReport
    import streamlit.components.v1 as components
    has_profile = True
except Exception:
    has_profile = False

# Streamlit page config
st.set_page_config(page_title="Music & Mental Health Explorer", layout="wide", initial_sidebar_state="expanded")
sns.set_theme(style="whitegrid")
sns.set_palette("inferno")

# -----------------------
# Utility functions
# -----------------------
@st.cache_data
def load_csv(uploaded_file) -> pd.DataFrame:
    if uploaded_file is None:
        return None
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        # Try with different encodings or separators
        uploaded_file.seek(0)
        try:
            df = pd.read_csv(uploaded_file, encoding='latin1')
        except Exception:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, sep=None, engine='python')  # best-effort
    return df

@st.cache_data
def try_local_default():
    # Try to mimic the notebook's original path if present in runtime environment.
    possible_paths = [
        "/Users/roshannaidu/Desktop/h501-finalproject/Me/mxmh_survey_results.csv",
        "/mnt/data/mxmh_survey_results.csv",
        "/mnt/data/term1 copy/mxmh_survey_results.csv",
        "./mxmh_survey_results.csv",
    ]
    for p in possible_paths:
        if os.path.exists(p):
            try:
                return pd.read_csv(p)
            except Exception:
                pass
    return None

def df_overview(df: pd.DataFrame):
    st.write("**Shape:**", df.shape)
    st.write("**Columns:**", len(df.columns))
    with st.expander("Show dtypes and missing counts"):
        dtypes = pd.DataFrame({
            "dtype": df.dtypes.astype(str),
            "missing": df.isna().sum(),
            "unique": df.nunique()
        })
        st.dataframe(dtypes)

def missing_heatmap(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(14, 2))
    sns.heatmap(pd.DataFrame(df.isnull().sum()).T, annot=True, fmt='d', cmap='inferno', cbar=False, ax=ax)
    ax.set_title("Missing values count per column")
    st.pyplot(fig)

def missing_barplot(df: pd.DataFrame):
    import missingno as msno
    fig = msno.bar(df, figsize=(12,4), color=(0.24,0.12,0.28))
    st.pyplot(fig.figure)

@st.cache_data
def compute_profile(df: pd.DataFrame):
    # Return HTML of profile report
    profile = ProfileReport(df, title="Profiling Report", minimal=True, progress_bar=False)
    return profile.to_html()

def get_download_link_df(df: pd.DataFrame, filename: str = "cleaned.csv"):
    towrite = BytesIO()
    df.to_csv(towrite, index=False)
    towrite.seek(0)
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download {filename}</a>'
    return href

# -----------------------
# App layout
# -----------------------
st.title("🎧 Music & Mental-health — Interactive EDA")

sidebar = st.sidebar

# Directly load the predefined dataset
df = try_local_default()

# Sidebar quick options
show_profile = sidebar.checkbox("Generate profiling report", value=False, help="Requires ydata-profiling installed.")
show_missingno = sidebar.checkbox("Show missing no. bar chart", value=False)
clean_bpm = sidebar.checkbox("Fill BPM missing values with median", value=True)

# Main flow
if df is None:
    st.stop()

# Basic cleaning from notebook
if "BPM" in df.columns and clean_bpm:
    try:
        df["BPM"] = pd.to_numeric(df["BPM"], errors="coerce")
        if df["BPM"].isnull().sum() > 0:
            df["BPM"].fillna(df["BPM"].median(), inplace=True)
    except Exception:
        pass

# Show overview
with st.container():
    st.header("Dataset overview")
    df_overview(df)
    if st.button("Show first 10 rows"):
        st.dataframe(df.head(10))

# Duplicates
dups = df[df.duplicated()]
if len(dups) > 0:
    st.warning(f"Found {len(dups)} duplicated rows. You can remove them using the button below.")
    if st.button("Remove duplicates"):
        df = df.drop_duplicates().reset_index(drop=True)
        st.success("Duplicates removed.")
else:
    st.info("No duplicated rows found.")

# Profiling report
if show_profile:
    if not has_profile:
        st.error("ydata-profiling not installed in this environment. Install with `pip install ydata-profiling`.")
    else:
        st.header("Profiling report")
        with st.spinner("Generating profiling report"):
            profile_html = compute_profile(df)
        components.html(profile_html, height=800, scrolling=True)
        if st.button("Save profiling report to file (profile.html)"):
            with open("profile_report.html", "w", encoding="utf-8") as f:
                f.write(profile_html)
            st.success("Saved profile_report.html to the working directory.")

# Missingness visuals
st.header("Missing values")
missing_heatmap(df)
if show_missingno:
    try:
        missing_barplot(df)
    except Exception as e:
        st.error("missing no. plotting failed: " + str(e))

# Quick statistics selector
st.header("Exploratory Data Analysis")
col1, col2 = st.columns([2,1])
with col1:
    st.subheader("Select columns / view")
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    view_mode = st.radio("View mode", options=["Numeric summary", "Categorical counts", "Custom plot"])
    if view_mode == "Numeric summary":
        if numeric_cols:
            sel_num = st.multiselect("Numeric columns (select to describe)", numeric_cols, default=numeric_cols[:6])
            if sel_num:
                st.dataframe(df[sel_num].describe().T)
        else:
            st.info("No numeric columns found.")
    elif view_mode == "Categorical counts":
        if cat_cols:
            sel_cat = st.selectbox("Choose a categorical column", cat_cols)
            counts = df[sel_cat].value_counts().reset_index()
            counts.columns = [sel_cat, "count"]
            st.dataframe(counts)
            fig = px.bar(counts, x=sel_cat, y="count", title=f"Counts for {sel_cat}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No categorical columns found.")
    else:
        st.write("Custom plotting")
        plot_x = st.selectbox("X column", options=df.columns.tolist())
        plot_y = st.selectbox("Y column (optional)", options=[None] + df.columns.tolist())
        plot_kind = st.selectbox("Plot kind", ["scatter", "bar", "hist", "box"])
        try:
            if plot_kind == "scatter" and plot_y:
                fig = px.scatter(df, x=plot_x, y=plot_y, color=None, hover_data=df.columns.tolist(), title=f"{plot_x} vs {plot_y}")
                st.plotly_chart(fig, use_container_width=True)
            elif plot_kind == "bar":
                agg = df.groupby(plot_x).size().reset_index(name="count")
                fig = px.bar(agg, x=plot_x, y="count", title=f"Bar of {plot_x}")
                st.plotly_chart(fig, use_container_width=True)
            elif plot_kind == "hist":
                fig = px.histogram(df, x=plot_x, nbins=30, title=f"Distribution of {plot_x}")
                st.plotly_chart(fig, use_container_width=True)
            elif plot_kind == "box" and plot_y:
                fig = px.box(df, x=plot_x, y=plot_y, title=f"Box: {plot_y} by {plot_x}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Choose columns appropriate for the plot kind.")
        except Exception as e:
            st.error("Plotting error: " + str(e))

with col2:
    st.subheader("Correlation matrix")
    if numeric_cols:
        corr = df[numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(8,6))
        sns.heatmap(corr, annot=True, cmap='inferno', ax=ax)
        st.pyplot(fig)
    else:
        st.info("No numeric columns to compute correlation.")



candidate_age = [c for c in df.columns if "Age" in c or c.lower()=="age"]
candidate_service = [c for c in df.columns if "Primary streaming" in c or "service" in c.lower() or "Primary streaming service"==c]
candidate_genre = [c for c in df.columns if "Fav genre" in c or "genre" in c.lower()]

age_col = candidate_age[0] if candidate_age else (st.selectbox("Choose age column (if present)", options=["None"] + df.columns.tolist()) if st.checkbox("Select age column manually") else None)
service_col = candidate_service[0] if candidate_service else None
genre_col = candidate_genre[0] if candidate_genre else None

# Age group sliders / filters
st.subheader("Age group analysis")
if age_col and age_col in df.columns:
    try:
        df[age_col] = pd.to_numeric(df[age_col], errors='coerce')
        min_age = int(np.nanmin(df[age_col])) if not np.isnan(np.nanmin(df[age_col])) else 0
        max_age = int(np.nanmax(df[age_col])) if not np.isnan(np.nanmax(df[age_col])) else 100
        age_range = st.slider("Filter age range", min_value=min_age, max_value=max_age, value=(min_age, max_age))
        filtered = df[(df[age_col] >= age_range[0]) & (df[age_col] <= age_range[1])]
        st.write(f"Rows after age filter: {filtered.shape[0]}")
        if service_col and service_col in df.columns:
            agg = filtered[service_col].value_counts().reset_index()
            agg.columns = [service_col, "count"]
            fig = px.bar(agg, x=service_col, y="count", title=f"Preferred streaming service for ages {age_range[0]}-{age_range[1]}")
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error("Age analysis failed: " + str(e))
else:
    st.info("No obvious age column found. If your dataset contains an 'Age' column, check the sidebar 'Select age column manually' to set it.")

# Top genres
st.subheader("Top genres & relationships")

import warnings
import matplotlib.pyplot as plt
import seaborn as sns

# Suppress warnings
warnings.filterwarnings("ignore")

# --- KDE plots section ---
st.header("KDE Plots Analysis")
# Create a figure with 4 subplots arranged in a 4x4 grid (first part of your KDE plotting code)
plt.figure(figsize=(20, 15))
plt.subplot(4, 4, 1)
sns.kdeplot(data=df, x='Age', y='Anxiety', hue='Hours per day', color='r', alpha=.7, weights=None, fill=True, multiple='fill', palette='inferno')
plt.grid()

plt.subplot(4, 4, 2)
sns.kdeplot(data=df, x='Age', y='Insomnia', hue='Hours per day', color='r', alpha=.7, weights=None, fill=True, multiple='fill', palette='inferno')
plt.grid()

plt.subplot(4, 4, 3)
sns.kdeplot(data=df, x='Age', y='Depression', hue='Hours per day', color='r', alpha=.7, weights=None, fill=True, multiple='fill', palette='inferno')
plt.grid()

plt.subplot(4, 4, 4)
sns.kdeplot(data=df, x='Age', y='OCD', hue='Hours per day', color='r', alpha=.7, weights=None, fill=True, multiple='fill', palette='inferno')
plt.grid()

# Show the first set of KDE plots in Streamlit
st.pyplot(plt.gcf())  # Use plt.gcf() to show the current figure

# Create a second grid of KDE plots (the 2x2 grid)
fig, axs = plt.subplots(2, 2, figsize=(15, 15))

# KDE plots for different relationships in the dataset
sns.kdeplot(x='Age', y='Hours per day', data=df, ax=axs[0, 0], color='#065A60')
axs[0, 0].set_title('Age vs Hours per day')
axs[0, 0].grid()

sns.kdeplot(x='Depression', y='Anxiety', data=df, ax=axs[0, 1], color='#144552')
axs[0, 1].set_title('Depression vs Anxiety')
axs[0, 1].grid()

sns.kdeplot(x='Anxiety', y='Insomnia', data=df, ax=axs[1, 0], color='#212F45')
axs[1, 0].set_title('Anxiety vs Insomnia')
axs[1, 0].grid()

sns.kdeplot(x='Depression', y='Hours per day', data=df, ax=axs[1, 1], color='#312244')
axs[1, 1].set_title('Depression vs Hours per day')
axs[1, 1].grid()

# Adjust the layout and show the second set of KDE plots in Streamlit
plt.tight_layout()
st.pyplot(fig)

# --- 3D Scatter Plot section ---
st.header("3D Scatter Plot (Insomnia vs Anxiety vs Depression)")

# Check if required columns are available in the dataset
required_columns = ['Insomnia', 'Anxiety', 'Depression', 'Age']
if all(col in df.columns for col in required_columns):
    try:
        # Create the 3D scatter plot using Plotly
        fig = px.scatter_3d(df, 
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


if genre_col and genre_col in df.columns:
    try:
        top_n = st.slider("Top N genres", 3, 20, 6)
        top_genres = df[genre_col].value_counts().nlargest(top_n).index.tolist()
        top_df = df[df[genre_col].isin(top_genres)]
        counts = top_df[genre_col].value_counts().reset_index()
        counts.columns = [genre_col, "count"]
        fig = px.bar(counts, x=genre_col, y="count", title=f"Top {top_n} {genre_col}")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error("Top genre plotting failed: " + str(e))
else:
    st.info("No genre column auto-detected.")

# Multi-plot grid (best-effort)
st.subheader("Multi-plot insights")
try:
    # attempt to choose meaningful numeric columns used in notebook
    chosen_nums = numeric_cols[:6] if numeric_cols else []
    if chosen_nums:
        sel = st.multiselect("Choose numeric columns to compare (up to 6)", chosen_nums, default=chosen_nums[:3])
        if sel:
            fig, axes = plt.subplots(len(sel), 1, figsize=(10, 4*len(sel)))
            if len(sel) == 1:
                axes = [axes]
            for ax, col in zip(axes, sel):
                sns.histplot(df[col].dropna(), kde=True, ax=ax)
                ax.set_title(f"Distribution of {col}")
            st.pyplot(fig)
except Exception as e:
    st.error("Multi-plot failed: " + str(e))

# Export cleaned data
st.header("Export / Save")
st.markdown(get_download_link_df(df, filename="cleaned_mxmh.csv"), unsafe_allow_html=True)

st.markdown("---")