# importing the libraries
import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np
import plotly.express as px

# reading the csv
df = pd.read_csv('updateddf.csv')

# setting the title
st.title("Music's Effects on Mental Health Issues")

# setting an image
st.image('MentalHealth.jpg', width = 700)

# setting the age group
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
if daily_listening in ['Less than 1 hour', '1 - 2 hours']:
    listening_frequency = 'infrequently'
elif daily_listening in ['2 - 3 hours', '3 - 4 hours']:
    listening_frequency = 'frequently'
else:
    listening_frequency = 'very frequently'
selected_genres = ', '.join(genre)  # Convert list to comma-separated string
st.write(f'Based on your selection, you listen to {selected_genres}: {listening_frequency}')

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

# creating a conditional graph
st.header("Music Types' Effect on Conditions")
if condition:
    # Step 1: Filter rows where 'Music effects' is 'Improve'
    filtered_df = df[df["Music effects"] == "Improve"]

    # Step 2: Include rows where at least one condition is 5 or greater
    condition_columns = ["Anxiety", "Depression", "Insomnia", "OCD"]
    filtered_df = filtered_df[filtered_df[condition_columns].ge(5).any(axis=1)]

    # Step 3: Extract music types with 'Very frequently'
    frequency_columns = [col for col in df.columns if col.startswith("Frequency")]
    music_type_conditions = filtered_df.melt(
        id_vars=condition_columns + ["Music effects"], 
        value_vars=frequency_columns, 
        var_name="Music Type", 
        value_name="Frequency"
    )
    music_type_conditions = music_type_conditions[music_type_conditions["Frequency"] == "Very frequently"]

    # Step 4: Count occurrences by Music Type and Condition
    music_type_conditions["Music Type"] = music_type_conditions["Music Type"].str.extract(r"\[(.*?)]")  # Extract music type
    condition_counts = music_type_conditions.melt(
        id_vars=["Music Type"], 
        value_vars=condition_columns, 
        var_name="Condition", 
        value_name="Severity"
    )
    condition_counts = condition_counts[condition_counts["Severity"] >= 5]
    result = condition_counts.groupby(["Music Type", "Condition"]).size().reset_index(name="Count")

    # Filter the data based on selected conditions
    filtered_result = result[result["Condition"].isin(condition)]

    # Step 5: Create a grouped bar chart
    fig = px.bar(
        filtered_result,
        x="Music Type",
        y="Count",
        color="Condition",
        title="Conditions Improving by Listening to Music Types 'Very Frequently'",
        labels={"Count": "Count of Conditions Improving", "Music Type": "Music Types", "Condition": "Condition"},
        barmode="group",
        text="Count"
    )

    # Display the chart
    st.plotly_chart(fig)

selections = {
    'Age Group': age_group,
    'Favorite Music Genre(s)': genre,
    'Music Listening Service': service,
    'Daily Listening': daily_listening,
    'Listening Frequency': listening_frequency,
    'Mental Health Condition': condition,
    'Condition Rating': level,
}

# converting the selections to a dataframe
selections_df = pd.DataFrame(selections.items(), columns = ['Option', 'Selection'])

# setting the header for the selected options
st.header('Selected Options')
