import streamlit as st
from modules.app_core import config, survey, page_header

config("Mood recommender")
df = survey()
page_header("Mood recommender")

def page_mood():
    st.header("Mood recommender")
    ma = MoodAnalysis(csv_path=str(CSV_PATH))
    df = ma.clean()

    st.subheader("BPM vs symptoms")
    rho = ma.spearman_bpm_vs_scales()
    st.dataframe(rho, use_container_width=True)

    st.subheader('Genres ranked by % reporting "Improved" mood after listening')
    recs = ma.improve_table(min_n=30)
    st.dataframe(recs, use_container_width=True)

    top5 = recs.head(5).rename(columns={"improve_pct": "Improve %"})
    fig = px.bar(
        top5,
        x="Fav genre",
        y="Improve %",
        text="Improve %",
        title="Recommended Genres",
        labels={
            "Fav genre": "Favorite Genre",
            "Improve %": "% Reporting Improved Mood",
        },
    )
    fig.update_traces(texttemplate="%{text:.0%}", textposition="outside")
    fig.update_yaxes(tickformat="%")
    st.plotly_chart(fig, use_container_width=True)