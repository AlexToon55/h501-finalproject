""" Module for loading the survey dataset."""
from pathlib import Path
import pandas as pd


def load_survey(path: str | None = None) -> pd.DataFrame:
    if path is None:
         path = Path(__file__).resolve().parents[1] / "data" / "mxmh_survey_results.csv"
    return pd.read_csv(path)
