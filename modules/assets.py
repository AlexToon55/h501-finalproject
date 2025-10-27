from __future__ import annotations
import re
from urllib.parse import urlparse, parse_qs



def _gdrive_download(url: str | None) -> str | None:
    """ Convert a Google Drive sharing URL to a direct download URL. """
    if not url or "drive.google.com" not in url:
        return url

    marker = "/file/d/"
    
    if marker in url:
        file_id = url.split(marker, 1)[1].split("/", 1)[0]
        return f"https://drive.google.com/uc?export=download&id={file_id}"

    if "open?id=" in url:
        file_id = url.split("open?id=", 1)[1].split("&", 1)[0]
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    return url

def links_from_secrets(key: str) -> str | None:
    try: 
        import streamlit as st
        raw_links = st.secrets.get(key)
    except Exception:
        return None
    return _gdrive_download(raw_links) if isinstance(raw_links, str) else None