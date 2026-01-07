import streamlit as st

st.set_page_config(
    page_title="Sales Management System",
    page_icon="📊",
    layout="wide"
)

st.sidebar.title("📂 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Register Sale", "Reports"]
)

if page == "Dashboard":
    from pages.dashboard import show_dashboard
    show_dashboard()

elif page == "Register Sale":
    from pages.register_sale import show_register_sale
    show_register_sale()

elif page == "Reports":
    from pages.reports import show_reports
    show_reports()
