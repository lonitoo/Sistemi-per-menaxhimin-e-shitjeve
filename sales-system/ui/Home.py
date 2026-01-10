import streamlit as st


if "token" not in st.session_state:
    st.warning("Duhet të kyçeni për të vazhduar 🔒")
    st.switch_page("pages/login.py")
    st.stop()


if "token" not in st.session_state:
    st.title("🔐 Sales Analytics System")
    st.info("Ju lutem bëni login për të vazhduar.")
    st.stop()

with st.sidebar:
    st.markdown(
        """
        <style>
        .sidebar-logout {
            position: fixed;
            bottom: 20px;
            width: 90%;
        }
        .sidebar-logout button {
            background-color: #d9534f;
            color: white;
            width: 100%;
            border-radius: 6px;
            height: 40px;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="sidebar-logout">', unsafe_allow_html=True)
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.switch_page("streamlit_test.py")
    st.markdown('</div>', unsafe_allow_html=True)



st.title("🏠 Home")

st.markdown("""
### Sistemi për Analizën e Shitjeve

Ky aplikacion shërben për:
- 📊 Vizualizimin e të dhënave të shitjeve
- 📈 Analizë statistikore
- 🔮 Parashikim (Forecast) bazuar në të dhëna historike
- 📄 Mbështetje për vendimmarrje

""")
            
st.divider()


st.subheader("📌 Navigim i shpejtë")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Dashboard"):
        st.switch_page("pages/dashboard.py")

with col2:
    if st.button("🔮 Forecast"):
        st.switch_page("pages/forecast.py")

with col3:
    if st.button("📈 instant_product"):
        st.switch_page("pages/instant_product.py")

st.divider()

st.success("✅ Sistemi gati për analizë")
st.caption("Sales Analytics System – Elab-analyse")
