import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Premium Analytics Dashboard",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for high-end aesthetics and interactive effects
st.markdown("""
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main background */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Card styling */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 25px !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1) !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease !important;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.15) !important;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.8) !important;
    }

    /* Hero section */
    .hero-container {
        padding: 100px 20px;
        text-align: center;
        background: white;
        border-radius: 30px;
        margin-bottom: 50px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.05);
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }

    .hero-subtitle {
        font-size: 1.2rem;
        color: #666;
        max-width: 600px;
        margin: 0 auto;
    }

    /* Section animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stHeader, .stPlotlyChart {
        animation: fadeIn 0.8s ease-out forwards;
    }
    
    /* Better button style */
    .stDownloadButton button {
        background: linear-gradient(90deg, #1f77b4, #2c3e50);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }
    .stDownloadButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(31, 119, 180, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            return df
        except Exception as e:
            st.error(f"Error loading file: {e}")
            return None
    return None

def show_welcome_screen():
    st.markdown("""
        <div class="hero-container">
            <h1 class="hero-title">Professional Data Intelligence</h1>
            <p class="hero-subtitle">
                Unlock the power of your data. Upload your professional dataset in the sidebar to generate a comprehensive, 
                interactive dashboard with real-time analytics and deep-dive insights.
            </p>
            <div style="margin-top: 40px; color: #1f77b4;">
                <p><b>Awaiting Input Dataset...</b></p>
                <div style="font-size: 40px;">📂</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def main():
    # Sidebar for data input
    st.sidebar.title("💎 Dashboard Setup")
    st.sidebar.markdown("Configure your analysis environment.")
    uploaded_file = st.sidebar.file_uploader("Upload your CSV dataset", type=["csv"], help="Select a CSV file to begin analysis.")
    
    # Check if a file is uploaded
    if uploaded_file is None:
        show_welcome_screen()
        st.sidebar.info("Please upload a CSV file to enable the dashboard features.")
        st.stop()
    
    # Load data only after upload
    df = load_data(uploaded_file)

    if df is not None:
        # Preprocessing
        cols = df.columns.tolist()
        if 'Date' in cols:
            df['Date'] = pd.to_datetime(df['Date'])
        
        st.title("🚀 Data Intelligence Dashboard")
        st.success("Dataset successfully processed and loaded.")
        
        # --- Metrics Row ---
        st.header("📊 Key Performance Indicators")
        col1, col2, col3, col4 = st.columns(4)
        
        total_users = df['User_ID'].nunique() if 'User_ID' in cols else len(df)
        total_sessions = df['Session_ID'].nunique() if 'Session_ID' in cols else len(df)
        conversion_rate = (df['Converted'].mean() * 100) if 'Converted' in cols else 0
        avg_engagement = df['Engagement_Time'].mean() if 'Engagement_Time' in cols else 0
        
        col1.metric("Unique Users", f"{total_users:,}", delta_color="normal")
        col2.metric("Total Sessions", f"{total_sessions:,}", delta_color="normal")
        col3.metric("Conversion Rate", f"{conversion_rate:.2f}%", delta_color="inverse")
        col4.metric("Avg Engagement", f"{avg_engagement:.1f}s", delta_color="normal")

        # --- Graphical Section ---
        st.write("---")
        st.header("📈 Visual Distribution & Trends")
        
        row1_col1, row1_col2 = st.columns(2)
        
        with row1_col1:
            st.subheader("Distribution Channels")
            if 'Source' in cols:
                source_counts = df['Source'].value_counts().reset_index()
                source_counts.columns = ['Source', 'Count']
                fig_source = px.pie(source_counts, values='Count', names='Source', hole=0.5,
                                   color_discrete_sequence=px.colors.sequential.RdBu,
                                   title="Traffic by Source")
                fig_source.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#FFFFFF', width=2)))
                fig_source.update_layout(showlegend=False, margin=dict(t=30, b=10, l=10, r=10))
                st.plotly_chart(fig_source, width="stretch")
            else:
                st.info("Source data not available for visualization.")

        with row1_col2:
            st.subheader("Mobile vs Desktop")
            if 'Device' in cols:
                device_counts = df['Device'].value_counts().reset_index()
                device_counts.columns = ['Device', 'Count']
                fig_device = px.bar(device_counts, x='Device', y='Count', 
                                   color='Count', color_continuous_scale='Blues',
                                   title="Usage by Device Type")
                fig_device.update_layout(xaxis_title="", yaxis_title="Total Hits", showlegend=False)
                st.plotly_chart(fig_device, width="stretch")
            else:
                st.info("Device data not available for visualization.")

        st.write("---")
        
        row2_col1, row2_col2 = st.columns([2, 1])
        
        with row2_col1:
            st.subheader("Engagement Over Time")
            if 'Date' in cols:
                daily_traffic = df.groupby('Date').size().reset_index(name='Hits')
                fig_trend = px.area(daily_traffic, x='Date', y='Hits', title="Traffic Volume Trend")
                fig_trend.update_traces(line_color='#1f77b4', fillcolor='rgba(31, 119, 180, 0.2)')
                fig_trend.update_layout(hovermode="x unified", xaxis_title="", yaxis_title="Total Sessions")
                st.plotly_chart(fig_trend, width="stretch")
            else:
                st.info("Temporal data not available for trend analysis.")
                
        with row2_col2:
            st.subheader("Global Footprint")
            if 'Country' in cols:
                country_counts = df['Country'].value_counts().head(10).reset_index()
                country_counts.columns = ['Country', 'Count']
                fig_country = px.bar(country_counts, y='Country', x='Count', orientation='h',
                                    color='Count', color_continuous_scale='GnBu',
                                    title="Top 10 Regions")
                fig_country.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
                st.plotly_chart(fig_country, width="stretch")
            else:
                st.info("Geographic data not available.")

        # --- Deep Dive Section ---
        st.write("---")
        st.header("🔍 Dataset Abstract & Deep Dive")
        
        tabs = st.tabs(["💎 Statistical Abstract", "🗺️ Page Flow", "👥 User behavior", "📦 Raw Dataset"])
        
        with tabs[0]:
            st.subheader("Data Summary Profile")
            st.write("Comprehensive statistical profile of your uploaded dataset.")
            
            num_tab, cat_tab = st.columns(2)
            with num_tab:
                st.markdown("**Numerical Metrics**")
                numeric_df = df.select_dtypes(include=['number'])
                if not numeric_df.empty:
                    st.dataframe(numeric_df.describe().T.style.background_gradient(cmap='Blues'), width="stretch")
                else:
                    st.write("No numeric columns detected.")
            
            with cat_tab:
                st.markdown("**Categorical Metrics**")
                categorical_df = df.select_dtypes(include=['object'])
                if not categorical_df.empty:
                    cat_summary = []
                    for col in categorical_df.columns:
                        cat_summary.append({
                            "Column": col,
                            "Uniq": df[col].nunique(),
                            "Mode": df[col].mode()[0] if not df[col].mode().empty else "N/A",
                            "Nulls": df[col].isnull().sum()
                        })
                    st.dataframe(pd.DataFrame(cat_summary).set_index("Column"), width="stretch")
                else:
                    st.write("No categorical columns detected.")

        with tabs[1]:
            st.subheader("Top Landing Pages")
            if 'Page' in cols:
                page_metrics = df.groupby('Page').size().reset_index(name='Visits')
                fig_pages = px.treemap(page_metrics, path=['Page'], values='Visits',
                                      color='Visits', color_continuous_scale='Blues',
                                      title="Page Popularity Map")
                st.plotly_chart(fig_pages, width="stretch")
            else:
                st.info("Page data not found.")

        with tabs[2]:
            st.subheader("User Conversion Funnel")
            if 'User_Type' in cols and 'Converted' in cols:
                conv_stats = df.groupby('User_Type')['Converted'].mean().reset_index()
                conv_stats['Rate'] = conv_stats['Converted'] * 100
                fig_funnel = px.funnel(conv_stats, x='Rate', y='User_Type', title="Conversion by User Status")
                st.plotly_chart(fig_funnel, width="stretch")
            else:
                st.info("Conversion metrics not found.")

        with tabs[3]:
            st.subheader("Data Inspector")
            st.dataframe(df.head(100), width="stretch")
            
            # Actionable download
            try:
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Full Analyzed Dataset",
                    data=csv,
                    file_name=f'analyzed_data_{datetime.now().strftime("%Y%m%d")}.csv',
                    mime='text/csv',
                )
            except Exception as e:
                st.error(f"Download generation failed: {e}")

    # Sidebar Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Antigravity Intelligence** v2.0")
    st.sidebar.caption("High-performance analysis engine.")

if __name__ == "__main__":
    main()
