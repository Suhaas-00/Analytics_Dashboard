import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Enterprise Analytics Dashboard",
    page_icon="📊",
    layout="wide",
)

# =========================
# PREMIUM CSS
# =========================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
    color: white;
}
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    transition: 0.3s;
}
[data-testid="stMetric"]:hover {
    transform: scale(1.05);
}
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================
def load_data(file):
    df = pd.read_csv(file)
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df

# =========================
# SIDEBAR
# =========================
st.sidebar.title("⚙️ Filters")

uploaded_file = st.sidebar.file_uploader("Upload Dataset", type=["csv"])

if uploaded_file is None:
    st.title("📊 Enterprise Analytics Platform")
    st.info("Upload your dataset to begin analysis.")
    st.stop()

df = load_data(uploaded_file)

# Date filter
if "Date" in df.columns:
    min_date = df["Date"].min()
    max_date = df["Date"].max()
    date_range = st.sidebar.date_input(
        "Select Date Range",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    df = df[(df["Date"] >= pd.to_datetime(date_range[0])) &
            (df["Date"] <= pd.to_datetime(date_range[1]))]

# Traffic source filter
if "Source" in df.columns:
    sources = st.sidebar.multiselect(
        "Filter by Source",
        options=df["Source"].unique(),
        default=df["Source"].unique()
    )
    df = df[df["Source"].isin(sources)]

# =========================
# HEADER
# =========================
st.title("🚀 Enterprise Analytics Dashboard")
st.caption("High-performance business intelligence interface")

# =========================
# KPI SECTION
# =========================
st.markdown("## 📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

total_users = df["User_ID"].nunique() if "User_ID" in df.columns else len(df)
total_sessions = df["Session_ID"].nunique() if "Session_ID" in df.columns else len(df)
conversions = df["Converted"].sum() if "Converted" in df.columns else 0
conversion_rate = df["Converted"].mean() * 100 if "Converted" in df.columns else 0

col1.metric("Total Users", f"{total_users:,}")
col2.metric("Sessions", f"{total_sessions:,}")
col3.metric("Conversions", f"{conversions:,}")
col4.metric("Conversion Rate", f"{conversion_rate:.2f}%")

st.divider()

# =========================
# TRAFFIC ANALYSIS
# =========================
st.markdown("## 🌐 Traffic Analysis")

c1, c2 = st.columns(2)

if "Source" in df.columns:
    source_data = df["Source"].value_counts().reset_index()
    source_data.columns = ["Source", "Count"]
    fig1 = px.pie(
        source_data,
        names="Source",
        values="Count",
        hole=0.5,
        template="plotly_dark"
    )
    c1.plotly_chart(fig1, use_container_width=True)

if "Country" in df.columns:
    country_data = df["Country"].value_counts().head(10).reset_index()
    country_data.columns = ["Country", "Count"]
    fig2 = px.bar(
        country_data,
        x="Count",
        y="Country",
        orientation="h",
        template="plotly_dark"
    )
    c2.plotly_chart(fig2, use_container_width=True)

st.divider()

# =========================
# BEHAVIOUR ANALYSIS
# =========================
st.markdown("## 🔍 User Behaviour")

c3, c4 = st.columns(2)

if "Page" in df.columns:
    page_data = df["Page"].value_counts().reset_index()
    page_data.columns = ["Page", "Visits"]
    fig3 = px.treemap(
        page_data,
        path=["Page"],
        values="Visits",
        template="plotly_dark"
    )
    c3.plotly_chart(fig3, use_container_width=True)

if "Device" in df.columns:
    device_data = df["Device"].value_counts().reset_index()
    device_data.columns = ["Device", "Count"]
    fig4 = px.bar(
        device_data,
        x="Device",
        y="Count",
        color="Device",
        template="plotly_dark"
    )
    c4.plotly_chart(fig4, use_container_width=True)

st.divider()

# =========================
# CONVERSION TREND
# =========================
if "Date" in df.columns and "Converted" in df.columns:
    st.markdown("## 📈 Conversion Trend")

    trend = df.groupby("Date")["Converted"].mean().reset_index()
    trend["Conversion Rate"] = trend["Converted"] * 100

    fig5 = px.line(
        trend,
        x="Date",
        y="Conversion Rate",
        template="plotly_dark"
    )
    st.plotly_chart(fig5, use_container_width=True)

st.divider()

# =========================
# RAW DATA
# =========================
st.markdown("## 📦 Dataset Preview")
st.dataframe(df.head(100), use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.caption("Enterprise Analytics Suite v3.0")
