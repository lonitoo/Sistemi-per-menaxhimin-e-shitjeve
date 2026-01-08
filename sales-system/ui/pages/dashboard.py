import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Sales Dashboard", layout="wide")

DATA_PATH = Path(__file__).resolve().parents[2] / "backend" / "data" / "sales_long.csv"

# -------------------------
# LOAD DATA
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    df["date"] = pd.to_datetime(
        df["date"],
        format="mixed",
        errors="coerce"
    )

    df = df.dropna(subset=["date"])
    return df


df = load_data()

# -------------------------
# UI
# -------------------------
st.title("📊 Sales Dashboard")
st.success("Të dhënat u ngarkuan me sukses")

# -------------------------
# SIDEBAR FILTERS
# -------------------------
st.sidebar.header("🔎 Filtra")

products = sorted(df["product_code"].unique())
selected_products = st.sidebar.multiselect(
    "Product code",
    products,
    default=products
)

date_range = st.sidebar.date_input(
    "Date range",
    [df["date"].min().date(), df["date"].max().date()]
)

group_by = st.sidebar.selectbox(
    "Group by",
    ["Daily", "Monthly", "Yearly"]
)

# -------------------------
# FILTER DATA
# -------------------------
filtered = df[
    (df["product_code"].isin(selected_products)) &
    (df["date"].dt.date >= date_range[0]) &
    (df["date"].dt.date <= date_range[1])
]

if filtered.empty:
    st.warning("Nuk ka të dhëna për këta filtra")
    st.stop()

# -------------------------
# AGGREGATION
# -------------------------
if group_by == "Daily":
    agg = filtered.groupby("date", as_index=False)["quantity"].sum()
elif group_by == "Monthly":
    agg = (
        filtered
        .groupby(filtered["date"].dt.to_period("M"))["quantity"]
        .sum()
        .reset_index()
    )
    agg["date"] = agg["date"].dt.to_timestamp()
else:
    agg = (
        filtered
        .groupby(filtered["date"].dt.to_period("Y"))["quantity"]
        .sum()
        .reset_index()
    )
    agg["date"] = agg["date"].dt.to_timestamp()

agg = agg.sort_values("date")

# -------------------------
# METRICS
# -------------------------
c1, c2, c3 = st.columns(3)

c1.metric("Total Quantity", f"{filtered['quantity'].sum():,.2f}")
c2.metric("Records", f"{len(filtered):,}")
c3.metric("Products", filtered["product_code"].nunique())

st.divider()

# -------------------------
# GRAPH 1 – TIME SERIES
# -------------------------
st.subheader("📈 Total Quantity over Time")

fig1, ax1 = plt.subplots(figsize=(12, 4))
ax1.plot(agg["date"], agg["quantity"])
ax1.set_xlabel("Date")
ax1.set_ylabel("Quantity")
st.pyplot(fig1)

# -------------------------
# GRAPH 2 – TOP PRODUCTS
# -------------------------
st.subheader("🏆 Top Products")

top_products = (
    filtered
    .groupby("product_code")["quantity"]
    .sum()
    .sort_values(ascending=False)
)

fig2, ax2 = plt.subplots(figsize=(8, 4))
top_products.plot(kind="bar", ax=ax2)
ax2.set_ylabel("Quantity")
st.pyplot(fig2)

# -------------------------
# GRAPH 3 – DISTRIBUTION (missing before)
# -------------------------
st.subheader("📊 Distribution of Quantity")

fig3, ax3 = plt.subplots(figsize=(8, 4))
ax3.hist(filtered["quantity"], bins=40)
ax3.set_xlabel("Quantity")
ax3.set_ylabel("Frequency")
st.pyplot(fig3)

# -------------------------
# RAW DATA
# -------------------------
st.subheader("🗄 Raw data (preview)")
st.dataframe(filtered.head(100))
