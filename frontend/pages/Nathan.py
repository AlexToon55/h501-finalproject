import modules.bootstrap
from modules.app_core import config, survey, page_header
from modules.nav import sidebar
import streamlit as st

config("Nathan")
sidebar() # add any extra sidebar elements here
df = survey() # load and cache the dataset
page_header("Nathan")

def page_nathan():
    st.header("nathan's analysis")
    st.info("This page is under construction.")