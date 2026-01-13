import requests
import streamlit as st

import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

# If Render provides just the hostname (e.g., example.onrender.com), prepend https://
# BUT if it is an internal service name (like 'quarterclose-backend'), keep it as http://
if not API_URL.startswith("http"):
    if "." not in API_URL: # Likely an internal service name
        API_URL = f"http://{API_URL}:8000" # Attempt direct port access
    else:
        API_URL = f"https://{API_URL}"

def get_data(endpoint: str):
    try:
        response = requests.get(f"{API_URL}{endpoint}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

def post_data(endpoint: str, data: dict = None, files: dict = None, params: dict = None):
    try:
        response = requests.post(f"{API_URL}{endpoint}", json=data, files=files, params=params)
        if response.status_code == 400:
             return {"error": response.json().get("detail", "Bad Request"), "status_code": 400}
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error posting data: {e}")
        return None

def load_css():
    with open('frontend/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
