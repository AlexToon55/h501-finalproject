from pathlib import Path

def sidebar():
    import streamlit as st

    root = Path(__file__).resolve().parents[1]
    img = root / "frontend" / "assets" / "marvelteam.jpg"


    with st.sidebar:
        if img.exists():
            st.image(str(img), use_column_width=True)

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