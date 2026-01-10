import streamlit as st
import pandas as pd
import streamlit as st


if "token" not in st.session_state:
    st.warning("Duhet të kyçeni për të vazhduar 🔒")
    st.switch_page("pages/login.py")
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
        st.switch_page("Home.py")
    st.markdown('</div>', unsafe_allow_html=True)


st.set_page_config(page_title="Sales Management", layout="wide")
st.title("📦 Sales & Inventory Management")

# INIT STORAGE
if "products" not in st.session_state:
    st.session_state.products = []

if "sales" not in st.session_state:
    st.session_state.sales = []

# ---------------- PRODUCTS ----------------
st.subheader("➕ Add Product")

with st.form("product_form"):
    name = st.text_input("Product Name")
    price = st.number_input("Unit Price (€)", min_value=0.0, step=0.1)
    stock = st.number_input("Initial Stock", min_value=0, step=1)
    add_product = st.form_submit_button("Add Product")

    if add_product:
        if name:
            st.session_state.products.append({
                "name": name,
                "price": price,
                "stock": stock
            })
            st.success("Product added successfully")
        else:
            st.error("Product name required")

# ---------------- PRODUCTS TABLE ----------------
st.subheader("📋 Products")
products_df = pd.DataFrame(st.session_state.products)
st.dataframe(products_df, use_container_width=True)

# ---------------- SALES ----------------
st.subheader("🧾 Register Sale")

if st.session_state.products:
    product_names = [p["name"] for p in st.session_state.products]

    with st.form("sale_form"):
        product = st.selectbox("Product", product_names)
        quantity = st.number_input("Quantity", min_value=1, step=1)
        submit_sale = st.form_submit_button("Register Sale")

        if submit_sale:
            prod = next(p for p in st.session_state.products if p["name"] == product)

            if quantity > prod["stock"]:
                st.error("Not enough stock available")
            else:
                total = quantity * prod["price"]
                prod["stock"] -= quantity

                st.session_state.sales.append({
                    "product": product,
                    "quantity": quantity,
                    "unit_price": prod["price"],
                    "total": total
                })

                st.success(f"Sale registered – Total €{total:.2f}")
else:
    st.info("Add products first")

# ---------------- SALES TABLE ----------------
st.subheader("📊 Sales Records")
sales_df = pd.DataFrame(st.session_state.sales)
st.dataframe(sales_df, use_container_width=True)
