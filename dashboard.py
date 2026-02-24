import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Premium Analytics Dashboard",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------
# DATA LOADER
# ----------------------------
def load_data(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

# ----------------------------
# MAIN APP
# ----------------------------
def main():

    st.sidebar.title("💎 Dashboard Setup")
    uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

    if uploaded_file is None:
        st.title("Professional Data Intelligence")
        st.info("Upload a CSV file to activate dashboard.")
        st.stop()

    df = load_data(uploaded_file)

    if df is None:
        st.stop()

    # Convert Date column if exists
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    cols = df.columns.tolist()

    st.title("🚀 Data Intelligence Dashboard")
    st.success("Dataset successfully loaded.")

    # ==========================
    # KPI SECTION
    # ==========================
    st.header("📊 Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    total_users = df["User_ID"].nunique() if "User_ID" in cols else len(df)
    total_sessions = df["Session_ID"].nunique() if "Session_ID" in cols else len(df)
    conversion_rate = df["Converted"].mean() * 100 if "Converted" in cols else 0
    avg_engagement = df["Engagement_Time"].mean() if "Engagement_Time" in cols else 0

    col1.metric("Unique Users", f"{total_users:,}")
    col2.metric("Total Sessions", f"{total_sessions:,}")
    col3.metric("Conversion Rate", f"{conversion_rate:.2f}%")
    col4.metric("Avg Engagement", f"{avg_engagement:.1f}s")

    st.divider()

    # ==========================
    # VISUAL SECTION
    # ==========================
    st.header("📈 Traffic Analysis")

    c1, c2 = st.columns(2)

    with c1:
        if "Source" in cols:
            source_counts = df["Source"].value_counts().reset_index()
            source_counts.columns = ["Source", "Count"]
            fig = px.pie(source_counts, values="Count", names="Source", hole=0.5)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Source column not available.")

    with c2:
        if "Device" in cols:
            device_counts = df["Device"].value_counts().reset_index()
            device_counts.columns = ["Device", "Count"]
            fig = px.bar(device_counts, x="Device", y="Count")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Device column not available.")

    st.divider()

    # ==========================
    # TIME TREND
    # ==========================
    if "Date" in cols:
        st.header("📅 Conversion Trend")

        daily_conv = df.groupby("Date")["Converted"].mean().reset_index()
        daily_conv["Conversion Rate"] = daily_conv["Converted"] * 100

        fig = px.line(daily_conv, x="Date", y="Conversion Rate")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ==========================
    # COUNTRY ANALYSIS
    # ==========================
    if "Country" in cols:
        st.header("🌍 Top Countries")

        country_counts = df["Country"].value_counts().head(10).reset_index()
        country_counts.columns = ["Country", "Count"]

        fig = px.bar(country_counts, x="Count", y="Country", orientation="h")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ==========================
    # PAGE ANALYSIS
    # ==========================
    if "Page" in cols:
        st.header("🗺 Top Pages")

        page_counts = df["Page"].value_counts().reset_index()
        page_counts.columns = ["Page", "Visits"]

        fig = px.treemap(page_counts, path=["Page"], values="Visits")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ==========================
    # STATISTICAL SUMMARY
    # ==========================
    st.header("📊 Statistical Summary")

    numeric_df = df.select_dtypes(include=["number"])

    if not numeric_df.empty:
        st.subheader("Numeric Columns")
        st.dataframe(numeric_df.describe().T)
    else:
        st.info("No numeric columns detected.")

    categorical_df = df.select_dtypes(include=["object"])

    if not categorical_df.empty:
        st.subheader("Categorical Columns")
        summary = []
        for col in categorical_df.columns:
            summary.append({
                "Column": col,
                "Unique": df[col].nunique(),
                "Mode": df[col].mode()[0] if not df[col].mode().empty else "N/A",
                "Null Values": df[col].isnull().sum()
            })
        st.dataframe(pd.DataFrame(summary))
    else:
        st.info("No categorical columns detected.")

    st.divider()

    # ==========================
    # RAW DATA + DOWNLOAD
    # ==========================
    st.header("📦 Raw Dataset Preview")

    st.dataframe(df.head(100))

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Dataset",
        csv,
        file_name=f"analyzed_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("Analytics Engine v2.1")

# ----------------------------
if __name__ == "__main__":
    main()
