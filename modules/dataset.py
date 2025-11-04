""" Module for loading the survey dataset."""
from pathlib import Path
import pandas as pd
from modules.assets import links_from_secrets
import streamlit as st



_SECRET_KEYS = ("mxmh_csv", "updated_df", "survey_url")

_LOCAL_FALLBACKS = (
     Path("mxmh_survey_results.csv"),
     Path("Data_Science_Survey.csv"),
)




def load_survey(key: str | None = "mxmh_csv") -> pd.DataFrame:
     """Load the survey dataset from a remote URL or local file."""

     if key:
          url = links_from_secrets(key)
          if url:
               try:
                    return pd.read_csv(url, low_memory=False)
               except Exception:
                    pass
     # fall back to local file
     path = Path(__file__).resolve().parents[1] / "data" / "mxmh_survey_results.csv"
     return pd.read_csv(path, low_memory=False)