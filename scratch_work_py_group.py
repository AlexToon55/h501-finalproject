# Converted from notebook: scratch work_py group.ipynb
# This script loads survey data from a public Google Sheets CSV export
# and generates a Plotly grouped bar chart for respondents with >=2
# moderate-to-high health issue scores (>=5).

import pandas as pd
import plotly.express as px

# Load data from Google Sheets (public CSV link)
url = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vRkL35eEcZvs9VtRLf8aIkow3SOybhdZpqOyHMNsia523mKec7sSGAiECVoG9WKaBFtliAXrO5itez3/"
    "pub?gid=760116139&single=true&output=csv"
)

def load_and_prepare(url: str) -> pd.DataFrame:
    """Load the CSV from the given URL and prepare the health-by-genre dataframe.

    Returns a dataframe in long format with columns: 'Fav genre', 'Health Issue', 'Has Issue'
    where 'Has Issue' is 0/1 and only rows with >=2 issues per respondent are kept.
    """
    df = pd.read_csv(url)

    health_cols = ["Anxiety", "Depression", "Insomnia", "OCD"]
    genre_col = "Fav genre"

    # Keep only relevant columns and convert to binary (>=5 -> 1)
    health_df = df[[genre_col] + health_cols].copy()
    health_df[health_cols] = (health_df[health_cols] >= 5).astype(int)

    # Keep only rows where at least 2 health issues are >=5
    health_df = health_df[health_df[health_cols].sum(axis=1) >= 2]

    # Melt to long format
    melted = health_df.melt(id_vars=genre_col, var_name="Health Issue", value_name="Has Issue")

    return melted


def summarize_percent_by_genre(melted: pd.DataFrame) -> pd.DataFrame:
    """Compute percentage of respondents per genre reporting each health issue.

    Expects melted with columns: 'Fav genre', 'Health Issue', 'Has Issue'
    """
    summary = (
        melted.groupby(["Fav genre", "Health Issue"])['Has Issue']
        .mean()
        .reset_index()
    )
    summary['Has Issue'] *= 100
    return summary


def make_plot(summary: pd.DataFrame):
    custom_blues = ["#6BAED6", "#3182BD", "#08519C", "#08306B"]
    fig = px.bar(
        summary,
        x='Fav genre',
        y='Has Issue',
        color='Health Issue',
        barmode='group',
        title="Percentage of Respondents with ≥2 Moderate to High Health Issues by Music Genre",
        color_discrete_sequence=custom_blues,
    )
    fig.update_layout(xaxis_tickangle=45, yaxis_title="% of People")
    return fig


if __name__ == '__main__':
    melted = load_and_prepare(url)
    summary = summarize_percent_by_genre(melted)
    fig = make_plot(summary)
    fig.show()
