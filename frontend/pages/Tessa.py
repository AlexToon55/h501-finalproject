import modules.bootstrap
from modules.app_core import config, survey, page_header
import streamlit as st

config("Tessa")
df = survey()
page_header("Tessa")

def page_tessa():
    st.header("Tessa's analysis")
    st.info("This page is under construction.")