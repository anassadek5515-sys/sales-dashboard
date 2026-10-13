import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Executive Sales & Analytics Dashboard", layout="wide")

# Title and description
st.title("📊 Executive Sales & Analytics Dashboard")
st.markdown("Real-time interactive dashboard for monitoring key business metrics and sales performance.")

# Sidebar filters
st.sidebar.header("Filter Options")
region = st.sidebar.multiselect("Select Region", ["North America", "Europe", "Asia-Pacific", "Latin America"], default=["North America", "Europe"])
category = st.sidebar.multiselect("Select Category", ["Software", "Hardware", "Consulting Services"], default=["Software", "Hardware"])

# Mock Data Generation
np.random.seed(42)
dates = pd.date_range(start="2026-01-01", periods=100)
data = pd.DataFrame({
    "Date": np.random.choice(dates, 300),
    "Region": np.random.choice(["North America", "Europe", "Asia-Pacific", "Latin America"], 300),
    "Category": np.random.choice(["Software", "Hardware", "Consulting Services"], 300),
    "Revenue": np.random.randint(1000, 15000, 300),
    "Units_Sold": np.random.randint(5, 50, 300)
})

# Filter data
filtered_data = data[(data["Region"].isin(region)) & (data["Category"].isin(category))]

# KPI Summary Cards
col1, col2, col3, col4 = st.columns(4)
total_revenue = filtered_data["Revenue"].sum()
total_units = filtered_data["Units_Sold"].sum()
avg_order = filtered_data["Revenue"].mean() if len(filtered_data) > 0 else 0

col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Units Sold", f"{total_units:,}")
col3.metric("Average Order Value", f"${avg_order:,.2f}")
col4.metric("Active Regions", len(region))

st.markdown("---")

# Charts
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Revenue Trend Over Time")
    revenue_trend = filtered_data.groupby("Date")["Revenue"].sum().reset_index()
    fig1 = px.line(revenue_trend, x="Date", y="Revenue", title="Daily Revenue Trend")
    st.plotly_chart(fig1, use_container_width=True)

with chart_col2:
    st.subheader("Revenue by Product Category")
    category_revenue = filtered_data.groupby("Category")["Revenue"].sum().reset_index()
    fig2 = px.pie(category_revenue, values="Revenue", names="Category", hole=0.4, title="Revenue Distribution")
    st.plotly_chart(fig2, use_container_width=True)

# Data Table
st.subheader("Recent Transactions")
st.dataframe(filtered_data.head(10), use_container_width=True)