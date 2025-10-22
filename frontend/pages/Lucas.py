import modules.bootstrap
from modules.app_core import config, survey, page_header
from modules.nav import sidebar
import streamlit as st

config("Lucas") # sets the page title and icon
sidebar() # add any extra sidebar elements here
df = survey() # load and cache the dataset
page_header("Lucas")

def page_lucas():
    st.header("lucas's analysis")
    st.info("This page is under construction.")