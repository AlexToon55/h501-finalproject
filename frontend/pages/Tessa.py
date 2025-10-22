import modules.bootstrap
from modules.app_core import config, survey, page_header
from modules.nav import sidebar
import streamlit as st

config("Tessa")
sidebar() # add any extra sidebar elements here
df = survey() # load and cache the dataset
page_header("Tessa")

def page_tessa():
    st.header("Tessa's analysis")
    st.info("This page is under construction.")