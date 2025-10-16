# importing the libraries
import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np

# reading the csv
df = pd.read_csv('mxmh_survey_results.csv')

# setting the title
st.title("Music's Effects on Mental Health Issues")

# setting an image
st.image('MentalHealth.jpg', width = 700)


# setting the first input
st.header('Select Your Age Group')
age_groups = ['10-15', '16-20', '21-30', '31-40', '41-50', '51-60', '60+']
age_group = st.selectbox('Age Group', age_groups)
st.write(f'Selected age group: {age_group}')

# setting favorite music type
st.header('What is Your Favorite Music Genre?')
genres = df['Fav genre'].unique()
sorted_genres = sorted(genres)
genre = st.selectbox('Music Genres', sorted_genres)
st.write(f'Selected genre: {genre}')

