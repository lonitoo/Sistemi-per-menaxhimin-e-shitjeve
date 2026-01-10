import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.linear_model import LinearRegression
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


st.set_page_config(page_title="Sales Analytics (PowerBI Style)", layout="wide")

# Simple "PowerBI-like" header styling
st.markdown(
    """
    <style>
      .block-container { padding-top: 1.2rem; }
      div[data-testid="stMetricValue"] { font-size: 26px; }
      div[data-testid="stMetricLabel"] { opacity: 0.75; }
      .small-note { opacity: 0.75; font-size: 13px; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 Sales Analytics Dashboard")




DATA_PATH = Path("/app/data/sales_long.csv")

@st.cache_data
def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Nuk u gjet file: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    # Date parsing - mixed formats safe
    df["date"] = pd.to_datetime(df["date"], format="mixed", errors="coerce")
    df = df.dropna(subset=["date"])

    # Ensure columns exist
    needed = {"product_code", "quantity"}
    missing = needed - set(df.columns)
    if missing:
        raise ValueError(f"Mungojnë kolonat: {missing}")

    # Coerce numeric
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0.0)

    return df

try:
    raw = load_data()
except Exception as e:
    st.error(f"Gabim gjatë leximit të të dhënave: {e}")
    st.stop()


st.sidebar.header("🔎 Filtra")

products = sorted(raw["product_code"].dropna().unique().tolist())
if not products:
    st.error("Nuk ka asnjë product_code në dataset.")
    st.stop()

selected_product = st.sidebar.selectbox("Product", products, index=0)

min_date = raw["date"].min().date()
max_date = raw["date"].max().date()

date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

group_by = st.sidebar.selectbox("Group by", ["Daily", "Weekly", "Monthly"], index=0)

forecast_days = st.sidebar.slider("Forecast days", 7, 180, 30)
ma_window = st.sidebar.slider("Moving average window", 3, 60, 7)

show_table = st.sidebar.checkbox("Show raw preview", value=True)



df = raw[raw["product_code"] == selected_product].copy()
df = df[(df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)].copy()
df = df.sort_values("date")

if df.empty:
    st.warning("Nuk ka të dhëna për këtë filtër. Ndrysho produktin ose datat.")
    st.stop()


def aggregate(df_in: pd.DataFrame, mode: str) -> pd.DataFrame:
    d = df_in.copy()
    if mode == "Daily":
        d["bucket"] = d["date"].dt.floor("D")
    elif mode == "Weekly":
        d["bucket"] = d["date"].dt.to_period("W").dt.start_time
    else:  # Monthly
        d["bucket"] = d["date"].dt.to_period("M").dt.start_time

    out = d.groupby("bucket", as_index=False)["quantity"].sum()
    out = out.rename(columns={"bucket": "date"}).sort_values("date")
    return out

series = aggregate(df, group_by)


total_qty = float(series["quantity"].sum())
avg_qty = float(series["quantity"].mean())
max_qty = float(series["quantity"].max())


trend_delta = None
if len(series) >= 2:
    last = series["quantity"].iloc[-1]
    prev = series["quantity"].iloc[-2]
    trend_delta = float(last - prev)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Quantity", f"{total_qty:,.2f}")
k2.metric("Average / period", f"{avg_qty:,.2f}")
k3.metric("Max / period", f"{max_qty:,.2f}")
k4.metric("Trend (last vs prev)", f"{series['quantity'].iloc[-1]:,.2f}", delta=None if trend_delta is None else f"{trend_delta:,.2f}")



st.divider()


tab_overview, tab_forecast, tab_diag, tab_export = st.tabs(["📌 Overview", "🔮 Forecast", "🧪 Diagnostics", "⬇️ Export"])


with tab_overview:
    c1, c2 = st.columns([2, 1])

    
    fig1, ax1 = plt.subplots(figsize=(12, 4))
    ax1.plot(series["date"], series["quantity"], label=f"{group_by} quantity", alpha=0.9)
    ax1.set_title(f"{selected_product} — Quantity over time ({group_by})")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Quantity")
    ax1.legend()
    c1.pyplot(fig1, use_container_width=True)

    
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.hist(series["quantity"].values, bins=25)
    ax2.set_title("Distribution of quantity")
    ax2.set_xlabel("Quantity")
    ax2.set_ylabel("Frequency")
    c2.pyplot(fig2, use_container_width=True)

   
    st.subheader("📉 Moving Average")
    series_ma = series.copy()
    series_ma["ma"] = series_ma["quantity"].rolling(window=ma_window).mean()

    fig_ma, ax_ma = plt.subplots(figsize=(12, 4))
    ax_ma.plot(series_ma["date"], series_ma["quantity"], alpha=0.35, label="Actual")
    ax_ma.plot(series_ma["date"], series_ma["ma"], label=f"{ma_window}-period MA")
    ax_ma.set_title("Actual vs Moving Average")
    ax_ma.legend()
    st.pyplot(fig_ma, use_container_width=True)

    if show_table:
        with st.expander("📄 Preview (aggregated data)"):
            st.dataframe(series.tail(50), use_container_width=True)


with tab_forecast:
    st.subheader("🔮 Linear Regression Forecast (simple & stable)")

   
    work = series.copy()
    work["t"] = np.arange(len(work))
    X = work[["t"]]
    y = work["quantity"]

    model = LinearRegression()
    model.fit(X, y)

    future_t = np.arange(len(work), len(work) + forecast_days)

    
    freq = "D" if group_by == "Daily" else ("W" if group_by == "Weekly" else "MS")
    future_dates = pd.date_range(start=work["date"].iloc[-1], periods=forecast_days + 1, freq=freq)[1:]

    forecast = model.predict(future_t.reshape(-1, 1))

    residuals = y - model.predict(X)
    std = float(np.std(residuals)) if len(residuals) > 1 else 0.0
    upper = forecast + 1.96 * std
    lower = forecast - 1.96 * std

    figf, axf = plt.subplots(figsize=(12, 4))
    axf.plot(work["date"], work["quantity"], label="Actual", alpha=0.5)
    axf.plot(future_dates, forecast, label="Forecast")
    axf.fill_between(future_dates, lower, upper, alpha=0.2, label="95% CI")
    axf.set_title(f"Forecast — {selected_product} ({group_by})")
    axf.legend()
    st.pyplot(figf, use_container_width=True)

   
    forecast_df = pd.DataFrame({
        "date": future_dates,
        "forecast_quantity": forecast,
        "lower_bound": lower,
        "upper_bound": upper
    })

    st.markdown("**Forecast preview**")
    st.dataframe(forecast_df.head(30), use_container_width=True)


with tab_diag:
    st.subheader("🧪 Model diagnostics")

   
    work = series.copy()
    work["t"] = np.arange(len(work))
    X = work[["t"]]
    y = work["quantity"]

    model = LinearRegression()
    model.fit(X, y)
    y_hat = model.predict(X)
    residuals = y - y_hat

    colA, colB = st.columns(2)

    fig_r, ax_r = plt.subplots(figsize=(8, 4))
    ax_r.plot(work["date"], residuals)
    ax_r.axhline(0)
    ax_r.set_title("Residuals over time")
    colA.pyplot(fig_r, use_container_width=True)

    fig_sc, ax_sc = plt.subplots(figsize=(8, 4))
    ax_sc.scatter(y_hat, residuals)
    ax_sc.axhline(0)
    ax_sc.set_title("Residuals vs Predicted")
    ax_sc.set_xlabel("Predicted")
    ax_sc.set_ylabel("Residual")
    colB.pyplot(fig_sc, use_container_width=True)

    mae = float(np.mean(np.abs(residuals)))
    rmse = float(np.sqrt(np.mean(residuals**2)))

    m1, m2, m3 = st.columns(3)
    m1.metric("MAE", f"{mae:,.3f}")
    m2.metric("RMSE", f"{rmse:,.3f}")
    m3.metric("Data points", f"{len(work)}")

   

with tab_export:
    st.subheader("⬇️ Export")

    st.download_button(
        "Download filtered RAW (product only) CSV",
        df.to_csv(index=False),
        file_name=f"raw_{selected_product}.csv",
        mime="text/csv"
    )

    agg_export = series.copy()
    st.download_button(
        "Download aggregated series CSV",
        agg_export.to_csv(index=False),
        file_name=f"agg_{selected_product}_{group_by.lower()}.csv",
        mime="text/csv"
    )


    work = series.copy()
    work["t"] = np.arange(len(work))
    X = work[["t"]]
    y = work["quantity"]
    model = LinearRegression().fit(X, y)

    future_t = np.arange(len(work), len(work) + forecast_days)
    freq = "D" if group_by == "Daily" else ("W" if group_by == "Weekly" else "MS")
    future_dates = pd.date_range(start=work["date"].iloc[-1], periods=forecast_days + 1, freq=freq)[1:]
    forecast = model.predict(future_t.reshape(-1, 1))

    residuals = y - model.predict(X)
    std = float(np.std(residuals)) if len(residuals) > 1 else 0.0
    upper = forecast + 1.96 * std
    lower = forecast - 1.96 * std

    forecast_df = pd.DataFrame({
        "date": future_dates,
        "forecast_quantity": forecast,
        "lower_bound": lower,
        "upper_bound": upper
    })

    st.download_button(
        "Download forecast CSV",
        forecast_df.to_csv(index=False),
        file_name=f"forecast_{selected_product}_{group_by.lower()}.csv",
        mime="text/csv"
    )


