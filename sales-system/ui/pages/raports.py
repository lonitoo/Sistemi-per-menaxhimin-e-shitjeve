import streamlit as st
import requests
import pandas as pd

def show_reports():
    st.title("📑 Sales Reports")

    if st.button("Load Daily Sales"):
        res = requests.get("http://127.0.0.1:8000/sales/daily")
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            st.dataframe(df)
        else:
            st.error("Failed to load data")
