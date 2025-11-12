from pathlib import Path
from modules.assets import links_from_secrets

def sidebar():
    import streamlit as st
    with st.sidebar:
        st.image('frontend/assets/marvel_team.jpg', width='stretch')
        st.sidebar.markdown("Music & Mental Health")
        st.sidebar.caption("Group 4 - H501 Final Project")

        st.sidebar.divider()

        # Extras 
        st.sidebar.markdown("Links")
        st.page_link(
            "https://www.kaggle.com/code/melissamonfared/mental-health-music-relationship-analysis-eda",
            label = "Kaggle Notebook",
            icon = "🔗",
            )