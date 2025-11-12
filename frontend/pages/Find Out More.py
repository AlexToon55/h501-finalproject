import modules.bootstrap
from modules.app_core import config, survey, page_header
from modules.nav import sidebar
import streamlit as st

config("Find Out More!") # sets the page title and icon
sidebar() # add any extra sidebar elements here
df = survey() # load and cache the dataset
page_header("Find Out more!")

def page_FindOutMore():
    st.title("Find Out More!")
    st.write("""
    This application was created to explore the relationship between music and mental health. 
    Through data collected from a survey, we aim to understand how different music genres, listening habits, 
    and streaming services impact mental well-being.

    **Data Source:**
    The data used in this application was collected via a survey distributed to various demographics. 
    It includes information on age groups, favorite music genres, primary streaming services, 
    daily listening frequency, and self-reported mental health conditions.

    **How to Use This App:**
    - Navigate through the different pages using the sidebar.
    - Input your preferences and see how they compare with the survey data.
    - Explore visualizations that highlight trends and insights from the data.

    **About the Creator:**
    This app was developed by [Your Name], a passionate advocate for mental health awareness and music therapy. 
    For more information or to get in touch, please visit [Your Website or Contact Info].

    We hope you find this application informative and engaging!
    """)