from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st
from modules.app_core import config, survey, page_header, kpis
from modules.nav import sidebar


config("Home") # sets the page title and icon
sidebar() # add any extra sidebar elements here
df = survey() # load and cache the dataset

# header 
page_header("Home")
st.write("All pages share the same dataset, loaded and cached at the app level:")
st.dataframe(df.head(20), use_container_width=True)

# Table of what is left to do for the project in a table
st.header("Project To-Do List")
data = {
    "Task": [
        "Complete Find out more",
        "Test user input page for validation",
        "Implement an ML model for mood recommendation for user input page",
        "Add More Visualizations",
        "Improve Data Cleaning",
        "Optimize Performance / better loading screen"]
}
# Displaying the table
st.table(data)