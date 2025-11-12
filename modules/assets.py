from __future__ import annotations
import re
from urllib.parse import urlparse, parse_qs
import streamlit as st


def _gdrive_download(url: str) -> str:
    ''' Convert a Google Drive sharing URL to a direct download link.'''
    if not url:
        return url
    m = re.search(r"/d/([a-zA-Z0-9_-]+)", url) or re.search(r"[?&]id=([a-zA-Z0-9_-]+)", url)

    return f"https://drive.google.com/uc?export=download&id={m.group(1)}" if m else url
    

def links_from_secrets(key: str) -> str | None:
    ''' Retrieve and convert a link from Streamlit secrets.'''
    import streamlit as st
    val = st.secrets.get(key, None)
    return _gdrive_download(val) if val else None