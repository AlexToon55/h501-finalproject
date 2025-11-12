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

# setting the age entry
st.header('Enter Your Age')
age = st.number_input('Age', min_value=1, max_value=100, step=1)
# Check if age is valid (Streamlit’s number_input already restricts range)
if 1 <= age <= 100:
    st.write(f'Your age is: {age}')
else:
    st.error('Please enter a valid age between 1 and 100.')

# setting favorite music type
st.header('What is Your Favorite Music Genre?')
genres = df['Fav genre'].unique()
sorted_genres = sorted(genres)
genre = st.selectbox('Music Genres', sorted_genres)
st.write(f'Selected genre: {genre}')

# setting music listening service
st.header('Source of Music')
services = df['Primary streaming service'].dropna().unique()
sorted_services = sorted(services)
service = st.selectbox('Music Service', sorted_services)
st.write(f"Selected service: {service}")

# setting music listening frequency
st.header('Daily Music Listening Frequency')
listening_options = ['Less than 1 hour', '1 - 2 hours', '2 - 3 hours', \
    '3 - 4 hours', '4 - 5 hours', '5 - 6 hours', '7 or more hours']
daily_listening = st.selectbox('Listening Hours', listening_options)
st.write(f'Selected daily listening amount: {daily_listening}')
if daily_listening in ['Less than 1 hour', '1 - 2 hours']:
    listening_frequency = 'Infrequently'
elif daily_listening in ['2 - 3 hours', '3 - 4 hours']:
    listening_frequency = 'Frequently'
else:
    listening_frequency = 'Very frequently'
# selected_genres = ', '.join(genre)  # Convert list to comma-separated string
st.write(f'Based on your selection, you listen to {genre} music: {listening_frequency}')

# setting mental health condition
st.header('Mental Health Condition')
conditions = ['Anxiety', 'Depression', 'Insomnia', 'OCD']
condition = st.multiselect('Condition', conditions)
st.write(f'Selected condition(s): {', '. join(condition)}')

# Create sliders dynamically for each selected condition
condition_ratings = {}
for cond in condition:
    rating = st.slider(f'Rate your {cond} level (0 = none, 10 = high)', 
                       min_value=0, max_value=10, value=5)
    condition_ratings[cond] = rating
    
# Display the condition ratings
if condition_ratings:
    st.write("Your condition ratings:")
    for cond, rating in condition_ratings.items():
        st.write(f"{cond}: {rating}")

# Asking about music impact on mental health
st.header('How has music impacted your mental health?')
st.subheader('Please choose one of the following:')
improvement_level = ['No effect', 'Slightly improved', 'Greatly Improved',\
    'Worsened']
improvement_choice = st.selectbox("Music's Effect on your Mental Health:", improvement_level)
st.write(f'You chose: {improvement_choice}')

# creating a dictionary to display selections
selections = {
    'Age': age,
    'Favorite Music Genre': genre,
    'Music Listening Service': service,
    'Daily Listening': daily_listening,
    'Listening Frequency': listening_frequency,
    'Mental Health Condition': condition,
    'Condition Rating': ', '.join([f"{k}: {v}" for k, v in condition_ratings.items()]),
    "Music's Effect on Mental Health": improvement_choice
}

# removing the brackets from the selections dictionary
selections = {
    key: ', '.join(value) if isinstance(value, list) else value
    for key, value in selections.items()
}

# setting the header for the selected options
st.header('Selected Options')

# converting the Prediction Data to a Dataframe
selections_df = pd.DataFrame(selections.items(), columns = ['Option', 'Selection'])

# generate HTML table without the index
table_html = selections_df.to_html(index=False, classes="table", border=0)

# setting html table options
st.markdown(
    """
    <style>
    .table {
        width: 100%;
        border-collapse: collapse;
    }
    .table th, .table td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    .table th {
        background-color: #f2f2f2;
        color: #333; /* Darker text color for better readability */
        font-weight: bold;
        font-size: 16px; /* Adjust font size */
    }
    .stMarkdown h2 {
        color: #333; /* Match header color to table styling */
        font-weight: bold;
        font-size: 24px;
        margin-bottom: 15px; /* Add spacing below the header */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# render the table
st.markdown(table_html, unsafe_allow_html=True)

# --- Confirmation and Consent ---
st.header("Confirmation and Consent")

# Ask the two required confirmation questions — default blank state
confirm_selections = st.radio(
    "Are these selections correct?",
    ["Select an option", "Yes", "No"],
    index=0
)

st.write("")  # spacing

st.subheader("Permission")
st.write(
    "Do you consent to allowing us to collect this information and post it anonymously for others to see?\n\n"
    "_If you choose 'Yes', the information will be collected for study and made publicly visible._"
)

consent_to_share = st.radio(
    "Please confirm:",
    ["Select an option", "Yes", "No"],
    index=0
)

# Define the CSV file path where data will be saved
submissions_file = "user_submissions.csv"

# Add a submit button to make user intent explicit
submitted = st.button("Submit My Feedback")

if submitted:
    if confirm_selections == "Yes" and consent_to_share == "Yes":
        selections["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_data = pd.DataFrame([selections])

        try:
            existing_df = pd.read_csv(submissions_file)
            updated_df = pd.concat([existing_df, user_data], ignore_index=True)
        except FileNotFoundError:
            updated_df = user_data

        updated_df.to_csv(submissions_file, index=False)
        st.success("✅ Thank you for your participation! Your feedback has been recorded.")
        st.header("All Anonymous Submissions")
        st.dataframe(updated_df.style.hide(axis="index"), use_container_width=True)

    elif confirm_selections == "Select an option" or consent_to_share == "Select an option":
        st.warning("⚠️ Please make selections for both confirmation and consent before submitting.")
    elif confirm_selections != "Yes":
        st.warning("Please confirm that your selections are correct before submitting.")
    elif consent_to_share != "Yes":
        st.warning("You must consent to anonymous sharing before submission.")
