# importing the libraries
import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer 
from sklearn.decomposition import PCA

from modules.assets import links_from_secrets

# reading the csv
from modules.app_core import survey
df = survey()
df = df[(df["BPM"].isna()) | ((df["BPM"] >= 40) & (df["BPM"] <= 250))]

# define numerical features
features = ['Age', 'Hours per day', 'BPM', 'Anxiety','Depression','Insomnia','OCD']

# setting the title
st.title("Music and Mental Health")

# setting an image
st.image('frontend/assets/mental_health.jpg', width = 500) 

# setting the age slider
st.header('Select Your Age')
age = st.slider('Age', min_value=10, max_value=80, value=25)
st.write(f'Selected age: {age}')

# setting favorite music type
st.header('What is Your Favorite Music Genre?')
genres = df['Fav genre'].unique()
sorted_genres = sorted(genres)
genre = st.multiselect('Music Genres', sorted_genres)
st.write(f"Selected genre(s): {', '.join(genre)}")

# setting music tempo (BPM)
st.subheader("Select Music Tempo (BPM)")
bpm = st.slider(
    "Choose your preferred tempo:",
    min_value=40,
    max_value=240,
    value=120, 
    step=1)
st.write(f"Selected Tempo: **{bpm} BPM**")

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

# Convert to a single numeric value for k-means
listening_mapping = {
    'Less than 1 hour': 0.5,
    '1 - 2 hours': 1.5,
    '2 - 3 hours': 2.5,
    '3 - 4 hours': 3.5,
    '4 - 5 hours': 4.5,
    '5 - 6 hours': 5.5,
    '7 or more hours': 7
}
avg_hours = listening_mapping[daily_listening]

# setting mental health condition
st.header('Mental Health Condition')
conditions = ['Anxiety', 'Depression', 'Insomnia', 'OCD']
condition = st.multiselect('Condition', conditions)
st.write(f"Selected condition(s): {', '. join(condition)}")

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

# Impute missing values before scaling
imputer = SimpleImputer(strategy='median')
df_imputed = df[features].copy()
df_imputed[features] = imputer.fit_transform(df_imputed[features])

# Scale values
scaler = StandardScaler()
X = scaler.fit_transform(df_imputed[features])

# Train Model
kmeans = KMeans(n_clusters = 3, random_state = 42)

# Add cluster labels to the DataFrame
df_imputed['Cluster'] = kmeans.fit_predict(X)

# Make principal components
pca = PCA(n_components = 3)
X_pca = pca.fit_transform(X)

# Store PCA values for plotting
df_imputed["Mental Health Severity(PCA1)"] = X_pca[:, 0]
df_imputed["Tempo Range(PCA2)"] = X_pca[:, 1]
df_imputed["Listening Style(PCA3)"] = X_pca[:, 2]



# creating a dictionary to display selections
selections = {
    'Age': age,
    'Favorite Music Genre(s)': genre,
    'Music Tempo (BPM)': bpm,
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

# 3D scatter plot
df_imputed["Cluster"] = df_imputed["Cluster"].astype(str).str.strip()

fig = px.scatter_3d(df_imputed, 
                 x = 'Mental Health Severity(PCA1)', 
                 y = 'Tempo Range(PCA2)',
                 z = 'Listening Style(PCA3)',
                 color = 'Cluster',
                 title="K-Means Clustering into 3 groups"
                 )
cluster_color_map = {
    "0": "#0B3C5D",  
    "1": "#F4D03F",  
    "2": "#800000"   
}

for cluster in fig.data:
    cluster_name = cluster.name.strip()
    if cluster_name in cluster_color_map:
        cluster.marker.color = cluster_color_map[cluster_name]

        
fig.update_traces(marker=dict(size=6, opacity=0.75))
fig.update_layout(
    legend_title="Cluster",
    legend=dict(itemsizing='constant'),
)

fig.update_layout(
    legend_traceorder="normal",
    category_orders={"Cluster": [0, 1, 2]}  # enforce order
)
st.plotly_chart(fig, use_container_width=True)

# Cluster definitions
st.subheader("Cluster 0: High Distress · Heavy Use · Fast BPM")  
st.subheader("Cluster 1: Stable Mood · Light Use · Neutral BPM")  
st.subheader("Cluster 2: Low Distress · Moderate Use · Fast BPM + Insomnia")

# All conditions expected by the model
all_conditions = ['Anxiety', 'Depression', 'Insomnia', 'OCD']

# Fill unselected conditions with rating = 0
complete_ratings = {
    cond: condition_ratings.get(cond, 0) for cond in all_conditions
}
# dictionary for numerical inputs
user_data = {
    'Age': [age],
    'Hours per day': [avg_hours],
    'BPM': [bpm],
    'Anxiety': [complete_ratings['Anxiety']],
    'Depression': [complete_ratings['Depression']],
    'Insomnia': [complete_ratings['Insomnia']],
    'OCD': [complete_ratings['OCD']]
}
# convert dictionary to dataframe
user_df = pd.DataFrame(user_data, columns=features)

# Scale input values and predict user cluster
user_scaled = scaler.transform(user_df)
user_cluster = kmeans.predict(user_scaled)[0]

# Define Recommendations
recommendations = {
    0: (
        "You show high emotional distress and heavy music use with fast BPM. "
        "Try reducing fast-tempo tracks and shifting toward slower, calming music. "
        "Pair your listening with short breaks or grounding exercises for better mood regulation."
    ),
    1: (
        "Your profile shows stable mood, light music use, and neutral BPM. "
        "Maintain your balanced listening habits and use music for focus, relaxation, or creativity."
    ),
    2: (
        "You show low distress and moderate listening with a preference for fast BPM, but possible insomnia. "
        "Try avoiding high-BPM music late at night and use calm or slow ambient tracks to support sleep."
    )
}

# cluster recommendations
st.subheader(f"You belong to **Cluster {user_cluster}**")
st.write(recommendations[user_cluster])

