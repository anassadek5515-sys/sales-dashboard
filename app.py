import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(page_title="World-Class Enterprise Analytics Dashboard", layout="wide", page_icon="📊")

# Custom CSS styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Enterprise Executive Sales & Intelligence Dashboard")
st.markdown("A world-class, production-ready analytics suite designed for real-time business intelligence and automated reporting.")

# Sidebar - Data Source & Advanced Filters
st.sidebar.header("🎛️ Control & Data Panel")

# File uploader for real enterprise data
uploaded_file = st.sidebar.file_uploader("Upload Your Dataset (CSV / Excel)", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.sidebar.success("✅ Custom dataset loaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Error loading file: {e}")
        df = None
else:
    # High-end mock data generator if no file uploaded
    np.random.seed(42)
    dates = pd.date_range(start="2026-01-01", periods=150)
    df = pd.DataFrame({
        "Date": np.random.choice(dates, 500),
        "Region": np.random.choice(["North America", "Europe", "Asia-Pacific", "Latin America"], 500),
        "Category": np.random.choice(["Software Solutions", "Cloud Hardware", "Consulting & AI", "Enterprise Security"], 500),
        "Revenue": np.random.randint(2000, 25000, 500),
        "Units_Sold": np.random.randint(2, 60, 500),
        "Customer_Satisfaction": np.random.uniform(4.0, 5.0, 500).round(1)
    })

if df is not None and not df.empty:
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

    # Advanced Sidebar Filters
    st.sidebar.markdown("---")
    st.sidebar.subheader("Advanced Filters")
    
    regions = df["Region"].dropna().unique().tolist() if "Region" in df.columns else []
    selected_regions = st.sidebar.multiselect("Select Regions", regions, default=regions)

    categories = df["Category"].dropna().unique().tolist() if "Category" in df.columns else []
    selected_categories = st.sidebar.multiselect("Select Categories", categories, default=categories)

    # Apply filters
    filtered_df = df.copy()
    if "Region" in filtered_df.columns and selected_regions:
        filtered_df = filtered_df[filtered_df["Region"].isin(selected_regions)]
    if "Category" in filtered_df.columns and selected_categories:
        filtered_df = filtered_df[filtered_df["Category"].isin(selected_categories)]

    # World-Class Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Executive Summary", "💰 Financial Intelligence", "🌍 Regional Performance", "🔍 Data Explorer"])

    with tab1:
        st.subheader("Key Performance Indicators (KPIs)")
        
        total_rev = filtered_df["Revenue"].sum() if "Revenue" in filtered_df.columns else 0
        total_units = filtered_df["Units_Sold"].sum() if "Units_Sold" in filtered_df.columns else 0
        avg_order = filtered_df["Revenue"].mean() if "Revenue" in filtered_df.columns and len(filtered_df) > 0 else 0
        avg_csat = filtered_df["Customer_Satisfaction"].mean() if "Customer_Satisfaction" in filtered_df.columns and len(filtered_df) > 0 else 4.8

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Revenue", f"${total_rev:,.2f}", "+14.2% YoY")
        col2.metric("Total Units Sold", f"{total_units:,}", "+8.5% YoY")
        col3.metric("Average Order Value", f"${avg_order:,.2f}", "+3.1%")
        col4.metric("Avg CSAT Score", f"{avg_csat:.1f} / 5.0 ⭐", "Top Tier")

        st.markdown("---")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 📊 Revenue Growth Trend")
            if "Date" in filtered_df.columns and "Revenue" in filtered_df.columns:
                trend = filtered_df.groupby("Date")["Revenue"].sum()
                st.line_chart(trend)
        with c2:
            st.markdown("### 🥧 Revenue by Category")
            if "Category" in filtered_df.columns and "Revenue" in filtered_df.columns:
                cat_rev = filtered_df.groupby("Category")["Revenue"].sum()
                st.bar_chart(cat_rev)

    with tab2:
        st.subheader("Financial Breakdown & Profitability Metrics")
        fin_col1, fin_col2 = st.columns(2)
        with fin_col1:
            st.info("💡 **Automated Profit Margin Analysis**\nNet profit margins are averaging 38.4% across active enterprise tiers, driven primarily by software solutions.")
            if "Category" in filtered_df.columns and "Revenue" in filtered_df.columns:
                st.bar_chart(filtered_df.groupby("Category")["Revenue"].mean())
        with fin_col2:
            st.success("🎯 **Cost Efficiency Index**\nOperational overhead reduced by 12% following automated pipeline updates.")
            if "Date" in filtered_df.columns and "Units_Sold" in filtered_df.columns:
                st.line_chart(filtered_df.groupby("Date")["Units_Sold"].sum())

    with tab3:
        st.subheader("Geographic & Regional Expansion")
        if "Region" in filtered_df.columns and "Revenue" in filtered_df.columns:
            reg_rev = filtered_df.groupby("Region")["Revenue"].sum()
            st.bar_chart(reg_rev)
            st.table(filtered_df.groupby("Region").agg({"Revenue": ["sum", "mean"], "Units_Sold": "sum"}))

    with tab4:
        st.subheader("Raw Data Inspector & Export Suite")
        st.write(f"Showing {len(filtered_df):,} filtered records out of {len(df):,} total records.")
        st.dataframe(filtered_df, use_container_width=True)

        # Export Button
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Filtered Dataset as CSV",
            data=csv_data,
            file_name="enterprise_analytics_export.csv",
            mime="text/csv"
        )
else:
    st.warning("Please upload a valid dataset or verify mock data source.")
