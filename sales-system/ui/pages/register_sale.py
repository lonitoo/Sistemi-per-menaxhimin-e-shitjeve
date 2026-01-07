import streamlit as st
import requests
from datetime import date

def show_register_sale():
    st.title("➕ Register New Sale")

    with st.form("sale_form"):
        product = st.selectbox("Product Code", ["M01AB", "M01AE", "N02BA", "N02BE"])
        quantity = st.number_input("Quantity", min_value=1)
        sale_date = st.date_input("Sale Date", value=date.today())
        submitted = st.form_submit_button("💾 Save Sale")

    if submitted:
        payload = {
            "product_code": product,
            "quantity": quantity,
            "sale_date": str(sale_date)
        }
        res = requests.post("http://127.0.0.1:8000/sales", json=payload)
        if res.status_code == 200:
            st.success("Sale registered successfully (API call OK)")
        else:
            st.warning("API endpoint not ready yet (DB comes next)")
