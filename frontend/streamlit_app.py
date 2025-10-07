from pathlib import Path
import sys

# Make sure the project root is in sys.path for module imports
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pandas as pd
import plotly.express as px
import streamlit as st




# navbar

#styling
styles = {
    "nav": {"background-color": "#ffffff"},
    "span": {"padding": "0px 15px"},
    "active": {"background-color": "#51575c", "color": "white"},
}

try:
    from streamlit_navigation_bar import st_navbar
    has_navbar = True
except Exception:
    has_navbar = False

from modules.survey_extract import list_survey 

from modules.mood import MoodAnalysis

APP_TITLE = "Mental Health in the Tech Industry"
CSV_PATH = project_root / "data" / "mxmh_survey_results.csv"

# PAGES

def page_home():
    st.title(APP_TITLE)
    st.write(
        """
        This app analyzes a survey on.......
        The data comes from a survey conducted by.....
        The survey was conducted in ..... and contains responses from over ..... individuals working in......
        """
    )
    st.markdown("- Data source: URL NEEDED HERE")
    
def page_mood():
    st.header("Mood recommender")
    ma = MoodAnalysis(csv_path=str(CSV_PATH))
    df = ma.clean()

    st.subheader("BPM vs symptoms")
    rho = ma.spearman_bpm_vs_scales()
    st.dataframe(rho, use_container_width=True)

    st.subheader('Genres ranked by % reporting "Improved" mood after listening')
    recs = ma.improve_table(min_n=30)
    st.dataframe(recs, use_container_width=True)

    top5 = recs.head(5).rename(columns={"improve_pct": "Improve %"})
    fig = px.bar(
        top5,
        x="Fav genre",
        y="Improve %",
        text="Improve %",
        title="Recommended Genres",
        labels={
            "Fav genre": "Favorite Genre",
            "Improve %": "% Reporting Improved Mood",
        },
    )
    fig.update_traces(texttemplate="%{text:.0%}", textposition="outside")
    fig.update_yaxes(tickformat="%")
    st.plotly_chart(fig, use_container_width=True)


def page_tessa():
    st.header("Tessa's analysis")
    st.info("This page is under construction.")

def page_mohid():
    st.header("mohids's analysis")
    st.info("This page is under construction.")

def page_roshan():
    st.header("roshan's analysis")
    st.info("This page is under construction.")

def page_lucas():
    st.header("lucas's analysis")
    st.info("This page is under construction.")

def page_nathan():
    st.header("nathan's analysis")
    st.info("This page is under construction.")

PAGES = {
    "Home": page_home,
    "Mood Recommender": page_mood,
    "Tessa": page_tessa,
    "mohid": page_mohid,
    "roshan": page_roshan,
    "lucas": page_lucas,
    "nathan": page_nathan,
}


# layout
st.set_page_config(page_title=APP_TITLE, layout="wide")


# routing
page_names = list(PAGES.keys())

if has_navbar:
    selected = st_navbar(page_names, styles=styles) 
else:
    selected = st.sidebar.selectbox("Navigate", page_names)
PAGES[selected]()