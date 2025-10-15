import modules.bootstrap
from modules.app_core import config, survey, page_header
import streamlit as st

config("Nathan")
df = survey()
page_header("Nathan")

def page_nathan():
    st.header("nathan's analysis")
    st.info("This page is under construction.")