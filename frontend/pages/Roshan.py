import modules.bootstrap
from modules.app_core import config, survey, page_header
import streamlit as st

config("Roshan")
df = survey()
page_header("Roshan")

def page_roshan():
    st.header("roshan's analysis")
    st.info("This page is under construction.")