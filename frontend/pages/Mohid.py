import modules.bootstrap
from modules.app_core import config, survey, page_header
import streamlit as st

config("Mohid")
df = survey()
page_header("Mohid")

def page_mohid():
    st.header("mohids's analysis")
    st.info("This page is under construction.")