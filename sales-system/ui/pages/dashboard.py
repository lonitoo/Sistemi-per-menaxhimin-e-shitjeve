import streamlit as st
import pandas as pd

def show_dashboard():
    st.title("📊 Sales Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Daily Sales (€)", "3,750")
    col2.metric("Weekly Sales (€)", "18,420")
    col3.metric("Monthly Sales (€)", "77,460")

    st.markdown("### 📈 Monthly Sales Growth")

    data = {
        "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
        "Sales": [1200, 1800, 2400, 3100, 3800]
    }
    df = pd.DataFrame(data)

    st.bar_chart(df.set_index("Month"))
