""" Module for loading the survey dataset."""
from pathlib import Path
import pandas as pd
from modules.assets import links_from_secrets


def load_survey(path: str | None = "mxmh_csv") -> pd.DataFrame:
     if path is not None:
          try:
               url = links_from_secrets(path)
               if url:
                  return pd.read_csv(url)
          except Exception:
               pass

     # fall back to local file
     path = Path(__file__).resolve().parents[1] / "data" / "mxmh_survey_results.csv"
     return pd.read_csv(path)
