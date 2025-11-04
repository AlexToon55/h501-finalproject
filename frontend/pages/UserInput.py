# importing the libraries
import modules.bootstrap
from modules.app_core import config, survey, page_header
from modules.nav import sidebar
import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np
import plotly.express as px

config("User Input") # sets the page title and icon
sidebar() # add any extra sidebar elements here
# df = survey() # load and cache the dataset
page_header("Give Your Feedback")

# reading the csv
df = pd.read_csv('updateddf.csv')

# setting the title
st.title("How Has Music Impacted You?")

# setting an image
st.image('mental-health-blog.jpg', width = 500)

