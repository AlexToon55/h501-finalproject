from pathlib import Path
from modules.assets import links_from_secrets

def sidebar():
    import streamlit as st


    root = Path(__file__).resolve().parents[1]
    local_img = root / "frontend" / "assets" / "marvelteam.jpg"
    remote_img = links_from_secrets("marvelteam")

    with st.sidebar:
        if remote_img:
            st.image(str(remote_img), width="stretch")
        elif local_img.exists():
            st.image(str(local_img), width="stretch")

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