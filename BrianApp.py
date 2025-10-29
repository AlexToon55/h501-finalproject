# importing the libraries
import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np
import plotly.express as px

# -----------------------------
# Page Config & Animated Background
# -----------------------------
st.set_page_config(page_title="Music and Mental Health", layout="wide")

# Animated falling music notes and brains
st.markdown("""
<style>
@keyframes fall {
  0% { transform: translateY(-50px) rotate(0deg); opacity: 1; }
  100% { transform: translateY(700px) rotate(360deg); opacity: 0; }
}

/* Common animation style */
.emoji {
  position: absolute;
  top: -50px;
  font-size: 28px;
  animation: fall linear infinite;
}

/* Individual emoji positions and speeds */
.note1 { left: 5%; animation-duration: 4s; }
.note2 { left: 20%; animation-duration: 5s; }
.note3 { left: 35%; animation-duration: 6s; }
.note4 { left: 55%; animation-duration: 4.5s; }
.note5 { left: 70%; animation-duration: 5.5s; }
.note6 { left: 85%; animation-duration: 6.5s; }

.brain1 { left: 10%; animation-duration: 5.2s; }
.brain2 { left: 30%; animation-duration: 6.8s; }
.brain3 { left: 50%; animation-duration: 5.7s; }
.brain4 { left: 65%; animation-duration: 7s; }
.brain5 { left: 80%; animation-duration: 6.2s; }
</style>

<!-- Falling Music Notes -->
<div class="emoji note1">🎵</div>
<div class="emoji note2">🎶</div>
<div class="emoji note3">🎵</div>
<div class="emoji note4">🎶</div>
<div class="emoji note5">🎵</div>
<div class="emoji note6">🎶</div>

<!-- Falling Brains -->
<div class="emoji brain1">🧠</div>
<div class="emoji brain2">🧠</div>
<div class="emoji brain3">🧠</div>
<div class="emoji brain4">🧠</div>
<div class="emoji brain5">🧠</div>
""", unsafe_allow_html=True)


# reading the csv
df = pd.read_csv('updateddf.csv')

# setting the title
st.title("Music and Mental Health")

# setting an image
st.image('MentalHealth.jpg', width = 500)

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
    listening_frequency = 'Infrequently'
elif daily_listening in ['2 - 3 hours', '3 - 4 hours']:
    listening_frequency = 'Frequently'
else:
    listening_frequency = 'Very frequently'
selected_genres = ', '.join(genre)  # Convert list to comma-separated string
st.write(f'Based on your selection, you listen to {selected_genres}: {listening_frequency}')

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

# creating a conditional graph
st.header("Music Types' Effect on Conditions")
if condition:
    # filter rows where 'Music effects' is 'Improve'
    filtered_df = df[df["Music effects"] == "Improve"]

    # include rows where at least one condition is 5 or greater
    condition_columns = ["Anxiety", "Depression", "Insomnia", "OCD"]
    filtered_df = filtered_df[filtered_df[condition_columns].ge(5).any(axis=1)]

    # extract music types with 'Very frequently'
    frequency_columns = [col for col in df.columns if col.startswith("Frequency")]
    music_type_conditions = filtered_df.melt(
        id_vars=condition_columns + ["Music effects"], 
        value_vars=frequency_columns, 
        var_name="Music Type", 
        value_name="Frequency"
    )
    music_type_conditions = music_type_conditions[music_type_conditions["Frequency"] == "Very frequently"]

    # count occurrences by Music Type and Condition
    music_type_conditions["Music Type"] = music_type_conditions["Music Type"].str.extract(r"\[(.*?)]")  # Extract music type
    condition_counts = music_type_conditions.melt(
        id_vars=["Music Type"], 
        value_vars=condition_columns, 
        var_name="Condition", 
        value_name="Severity"
    )
    condition_counts = condition_counts[condition_counts["Severity"] >= 5]
    result = condition_counts.groupby(["Music Type", "Condition"]).size().reset_index(name="Count")

    # filter the data based on selected conditions
    filtered_result = result[result["Condition"].isin(condition)]

    # create a grouped bar chart
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

    # display the chart
    st.plotly_chart(fig)

# creating a dictionary to display selections
selections = {
    'Age Group': age_group,
    'Favorite Music Genre(s)': genre,
    'Music Listening Service': service,
    'Daily Listening': daily_listening,
    'Listening Frequency': listening_frequency,
    'Mental Health Condition': condition,
    'Condition Rating': ', '.join([f"{k}: {v}" for k, v in condition_ratings.items()]),
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

# setting the recommendations
st.header('Recommendations')
condition_text = ", ".join(condition) if condition else "your mental health conditions"
st.subheader(f'Based on your selections, if you listen to {selected_genres} frequently, \
         it may help with your {condition_text}')
