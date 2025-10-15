import modules.bootstrap
from modules.app_core import config, survey, page_header
from modules.nav import sidebar
import streamlit as st

config("Roshan")
sidebar() # add any extra sidebar elements here
df = survey() # load and cache the dataset
page_header("Roshan")

def page_roshan():
    st.header("roshan's analysis")
    st.info("This page is under construction.")