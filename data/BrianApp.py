# importing the libraries
import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np

# reading the csv
df = pd.read_csv('mxmh_survey_results.csv')

# setting the title
st.title('Music Effects on Mental Health Issues')

# setting an image
st.image('MentalHealth.jpg', width = 1000)