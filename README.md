# h501-finalproject

## Abstract/Overview
This project explores the relationship between music listening habits and mental health using an interactive Streamlit web application. The app loads a survey dataset about listener demographics, preferred genres, and self-reported mental health indicators to let users explore trends and consider how music consumption correlates with mood. Stakeholders such as mental-health researchers, music therapists, and streaming product teams could benefit from quick visual summaries of how genre preferences and listening duration align with the well-being of listeners, informing recommendations and feature design.

## Data Description
- **Source**: A survey file (`mxmh_survey_results.csv` renamed to `Data_Science_Survey.csv`) derived from a public Music & Mental Health dataset from Kaggle.
- **Contents**: Columns capture demographic attributes (age range, country, etc.), listening behaviors (hours per day, primary genre, exploratory), and self-reported mental health measures (depression, anxiety, insomnia, OCD) along with mood ratings. 
- **Cleaning/Handling**: Data are read with pandas using `low_memory=False` to preserve column types. Missing values are handled implicitly by pandas. Additional cleaning and modeling steps are planned in subsequent iterations.

## Algorithm Description
1. **Configuration**: `modules/app_core.config` sets a wide Streamlit layout and page title.
2. **Data Loading**: `modules/app_core.survey` calls `modules/dataset.py` to retrieve the CSV from secrets when available or from the local repository otherwise, and caches the DataFrame via `st.cache_data` for responsive navigation.
3. **Navigation**: `modules/nav.py` builds the sidebar to route between pages.
4. **Presentation**: The home page (`frontend/streamlit_app.py`) displays a sample of the dataset, explains shared data usage, and lists outstanding tasks (e.g., mood recommendation modeling, additional visualizations). Additional pages under `frontend/pages/` involve interactive graphs and collecting user input.

## Tools Used
- **Streamlit**: Front-end framework for rapid interactive dashboards and multipage navigation within our app.
- **pandas / numpy**: Data loading, tabular manipulation, and caching.
- **plotly, matplotlib, seaborn**: Visualization libraries for our graphs and charts.
- **statsmodels**: Statistical modeling experiments for deeper analysis of music and mood relationships.
- **Conda**: Environment management via `env_app.yml` for reproducible dependency setup.

## Ethical Concerns
- **Sensitive self-reports**: Survey responses include mental health indicators. Data must be stored both securely and anonymously while including clear disclaimers that insights are observational rather than diagnostic.
- **Sampling bias**: Survey respondents may not necessarily represent broader populations, so visualizations and any future models should highlight limitations and avoid overgeneralization.
- **User impact**: Mood recommendations or interpretations should not replace professional advice. Interfaces should use supportive language and avoid triggering content.

## To setup the project to run locally. First clone and then: 
### With conda, activiate the packages listed in env_app.yml
conda env create -f env_app.yml
conda activate H501-finalproject



### To test this application run this command: 
CD to project
python -m streamlit run frontend/streamlit_app.py


### Commands if your env file already exists
conda env create -f env_app.yml
conda activate H501-finalproject

### command to update the requirements file which is NEEDED for streamlit hosting
pip freeze > requirements.txt


## PROD Environment URL: https://h501-finalproject.streamlit.app/
## TOON Environment URL: https://h501-finalproject-xstblhshf5njjr4pzqzcfm.streamlit.app/



## Project Tree
/h501-finalproject
├── data/
│   └── Data_Science_Survey.csv
├── frontend/
│   ├── assets/
│   ├── pages/
│   │   ├── BrianApp.py
│   │   ├── Interactive.py
│   │   └── Mood_Analyser.py
│   ├── requirements.txt
│   └── streamlit_app.py
├── modules/
│   ├── __init__.py
│   ├── app_core.py
│   ├── assets.py
│   ├── bootstrap.py
│   ├── BrianApp.py
│   ├── dataset.py
│   ├── mood.py
│   └── nav.py
├── env_app.yml
├── README.md
├── requirements.txt
└── scratch area.ipynb
