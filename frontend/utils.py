import requests
import streamlit as st

API_URL = "http://localhost:8000"

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
