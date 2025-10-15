import modules.bootstrap
from modules.app_core import config, survey, page_header
import streamlit as st

config("Lucas")
df = survey()
page_header("Lucas")

def page_lucas():
    st.header("lucas's analysis")
    st.info("This page is under construction.")