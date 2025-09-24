# Get the data from the survey project
import pandas as pd


def load_survey():
   # bring the data in as a dataframe
   url = "data/mxmh_survey_results.csv"
   return pd.read_csv(url)

