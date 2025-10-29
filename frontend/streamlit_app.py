from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st
from modules.app_core import config, survey, page_header, kpis
from modules.nav import sidebar


config("Home") # sets the page title and icon
sidebar() # add any extra sidebar elements here
df = survey() # load and cache the dataset

# header 
page_header("Home")
st.write("All pages share the same dataset, loaded and cached at the app level:")
st.dataframe(df.head(20), use_container_width=True)

kpis(df)

# Set the page configuration with dark mode
st.set_page_config(
    page_title="Music and Mental Health",
    page_icon="🌙",  # Optional: Set a page icon
    layout="centered",  # Options: "centered" or "wide"
    initial_sidebar_state="expanded"  # Options: "expanded" or "collapsed"
)