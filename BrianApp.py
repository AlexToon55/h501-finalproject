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
genre = st.multiselect('Music Genres', sorted_genres)
st.write(f"Selected genre(s): {', '.join(genre)}")

# setting music listening service
st.header('Source of Music')
services = df['Primary streaming service'].dropna().unique()
sorted_services = sorted(services)
service = st.multiselect('Music Service', sorted_services)
st.write(f"Selected service(s): {', '.join(service)}")

# setting music listening frequency
st.header('Daily Music Listening Frequency')
listening_options = ['Less than 1 hour', '1 - 2 hours', '2 - 3 hours', \
    '3 - 4 hours', '4 - 5 hours', '5 - 6 hours', '7 or more hours']
daily_listening = st.selectbox('Listening Hours', listening_options)
st.write(f'Selected daily listening amount: {daily_listening}')

# setting mental health condition
st.header('Mental Health Condition')
conditions = ['Anxiety', 'Depression', 'Insomnia', 'OCD']
condition = st.multiselect('Condition', conditions)
st.write(f'Selected condition(s): {', '. join(condition)}')

# setting condition rating subheader
st.subheader('Condition Rating')
levels = ['0 (none)', '1 (low)', '2', '3', '4', '5', '6', \
    '7', '8', '9', '10 (high)']
level = st.selectbox('Rating Level', levels)
st.write(f'Selecting condition level: {level}')

