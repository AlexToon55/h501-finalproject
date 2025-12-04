""" Core application functions for the Streamlit app. """

def config(page_title: str):
    """ Configure the Streamlit app with a title and wide layout. """
    import streamlit as st
    st.set_page_config(page_title=page_title, layout="wide")


def survey():
    """ Load and cache the survey dataset. then activate streamlit once the page has called set_page_config """
    import streamlit as st
    from modules.dataset import load_survey
    
    @st.cache_data(show_spinner=False)
    def _load():
        return load_survey()
    return _load()

def page_header(title: str):
    """ Display a standardized page header. """
    import streamlit as st
    st.header(title)
    st.info(f"Music & Mental Health - {title}")

def kpis(df):
# Display key performance indicators (KPIs) from the dataset.
    import streamlit as st
    pass 