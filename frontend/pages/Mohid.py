import modules.bootstrap
from modules.app_core import config, survey, page_header
from modules.nav import sidebar
import streamlit as st

config("Mohid") # sets the page title and icon
sidebar() # add any extra sidebar elements here
df = survey() # load and cache the dataset
page_header("Mohid")

def page_mohid():
    st.header("mohids's analysis")
    st.info("This page is under construction.")