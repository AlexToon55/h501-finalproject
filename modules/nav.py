from pathlib import Path
from modules.assets import links_from_secrets

def sidebar():
    import streamlit as st
    with st.sidebar:
        st.sidebar.markdown("Music & Mental Health Analysis App")
        st.sidebar.caption("Group 4 - H501 Final Project")

        st.sidebar.divider()

        st.sidebar.caption("Meet the Team")
        st.image('frontend/assets/marvel_team.jpg', width='stretch')

        st.sidebar.divider()
        # Team Members
        st.sidebar.caption("Alex Toon (HULK)")
        st.sidebar.caption("Nathanael Jeffries (Captain America)")
        st.sidebar.caption("Tessa Joseph ()")
        st.sidebar.caption("Roshan Naidu (Thor Odinson)")
        st.sidebar.caption("Mohid Qadeer ()")
        st.sidebar.caption("Lucas Tetrault ()")
        st.sidebar.caption("Special Guest: Brian Blandino ()")

        st.sidebar.divider()

        # Extras 
        st.sidebar.markdown("Links")
        st.page_link(
            "https://www.kaggle.com/code/melissamonfared/mental-health-music-relationship-analysis-eda",
            label = "Kaggle Notebook",
            icon = "🔗",
            )
        
        st.page_link(
            "https://github.com/AlexToon55/h501-finalproject",
            label = "GitHub Repository",
            icon = "🔗",
            )
