import streamlit as st
import requests

st.set_page_config(page_title="Login", layout="centered")

st.title("🔐 Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    try:
        res = requests.post(
    "http://auth-service:8001/login",
    json={"username": username, "password": password},
    timeout=5
)

        if res.status_code == 200:
            st.session_state.token = res.json()["access_token"]
            st.success("Login successful ✅")
            st.switch_page("Home.py")
        else:
            st.error("Username ose password gabim ❌")

    except Exception as e:
        st.error(f"Gabim lidhjeje me auth-service: {e}")
