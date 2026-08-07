import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, charts, helpers, formatters
from utils.constants import *

def show() -> None:
    # =====================================================
    # LOAD DATA
    # =====================================================
    sales = load_data.load_sales()
    country = load_data.load_country()
    products = load_data.load_products()
    customers = load_data.load_segmentation()
    business = load_data.load_business_insights()

    # =====================================================
    # DASHBOARD HEADER
    # =====================================================
    helpers.render_page_header(
        "📊 RetailPulse Dashboard",
        "AI-Powered Customer Analytics & Demand Forecasting"
    )

    # =====================================================
    # KPI VALUES
    # =====================================================
    total_revenue = float(business.loc[business["Metric"] == "Total Revenue", "Value"].values[0])
    total_orders = int(business.loc[business["Metric"] == "Total Orders", "Value"].values[0])
    total_customers = int(business.loc[business["Metric"] == "Total Customers", "Value"].values[0])
    total_products = int(business.loc[business["Metric"] == "Products", "Value"].values[0])

    # =====================================================
    # KPI CARDS
    # =====================================================
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("💰 Total Revenue", formatters.currency(total_revenue))
    with c2:
        st.metric("📦 Total Orders", formatters.number(total_orders))
    with c3:
        st.metric("👥 Customers", formatters.number(total_customers))
    with c4:
        st.metric("🛍 Products", formatters.number(total_products))

    st.divider()

    # =====================================================
    # REVENUE TREND
    # =====================================================
    st.subheader("📈 Revenue Trend")
    
    revenue_trend = (
        sales
        .set_index("ds")
        .resample("ME")
        .sum()
        .reset_index()
    )

    fig = px.line(
        revenue_trend,
        x="ds",
        y="y",
        markers=True,
        color_discrete_sequence=[PRIMARY]
    )
    fig.update_traces(line=dict(width=4))
    charts.render(
        fig,
        height=CHART_MD,
        xaxis_title="Month",
        yaxis_title="Revenue ($)",
        hovermode="x unified"
    )

    st.divider()

    # =====================================================
    # MONTHLY REVENUE & DISTRIBUTION
    # =====================================================
    monthly = revenue_trend.copy()
    monthly["Month"] = monthly["ds"].dt.strftime("%b %Y")

    left, right = st.columns(2)

    with left:
        st.subheader("📅 Monthly Revenue")
        fig = px.bar(
            monthly,
            x="Month",
            y="y",
            text_auto=".2s",
            color="y",
            color_continuous_scale="Blues"
        )
        charts.render(
            fig,
            height=CHART_SM,
            xaxis_title="",
            yaxis_title="Revenue",
            coloraxis_showscale=False
        )

    with right:
        st.subheader("📊 Revenue Distribution")
        fig = px.histogram(
            sales,
            x="y",
            nbins=30,
            color_discrete_sequence=[PRIMARY_DARK]
        )
        charts.render(
            fig,
            height=CHART_SM,
            xaxis_title="Revenue",
            yaxis_title="Frequency"
        )

    st.divider()

    # =====================================================
    # TOP COUNTRIES & TOP PRODUCTS
    # =====================================================
    left, right = st.columns(2)

    with left:
        st.subheader("🌍 Top 10 Countries by Revenue")
        top_country = (
            country
            .sort_values("TotalRevenue", ascending=False)
            .head(10)
        )
        fig = px.bar(
            top_country,
            x="TotalRevenue",
            y="Country",
            orientation="h",
            text_auto=".2s",
            color="Country",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        charts.render(
            fig,
            height=CHART_LG,
            yaxis=dict(categoryorder="total ascending"),
            xaxis_title="Revenue ($)",
            yaxis_title="",
            showlegend=False
        )

    with right:
        st.subheader("🛍 Top 10 Products by Revenue")
        top_products = (
            products
            .sort_values("TotalRevenue", ascending=False)
            .head(10)
        )
        fig = px.bar(
            top_products,
            x="TotalRevenue",
            y="Description",
            orientation="h",
            text_auto=".2s",
            color="Description",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        charts.render(
            fig,
            height=CHART_LG,
            yaxis=dict(categoryorder="total ascending"),
            xaxis_title="Revenue ($)",
            yaxis_title="",
            showlegend=False
        )

    st.divider()

    # =====================================================
    # CUSTOMER SEGMENTATION
    # =====================================================
    st.subheader("👥 Customer Segmentation")

    segment_summary = (
        customers["CustomerSegment"]
        .value_counts()
        .reset_index()
    )
    segment_summary.columns = ["CustomerSegment", "Count"]
    segment_summary["Percentage"] = (
        segment_summary["Count"] / segment_summary["Count"].sum() * 100
    ).round(2)

    left, right = st.columns([1.2, 1])

    with left:
        fig = px.pie(
            segment_summary,
            names="CustomerSegment",
            values="Count",
            hole=0.60,
            color="CustomerSegment",
            color_discrete_sequence=[
                PRIMARY,
                ACCENT_GREEN,
                ACCENT_AMBER,
                ACCENT_RED,
                ACCENT_PURPLE,
                ACCENT_CYAN
            ]
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        charts.render(
            fig,
            height=CHART_MD,
            showlegend=False
        )

    with right:
        st.subheader("📋 Segment Summary")
        st.dataframe(segment_summary, use_container_width=True, hide_index=True)

    st.divider()

    # =====================================================
    # BUSINESS INSIGHTS
    # =====================================================
    st.subheader("💡 Business Insights")
    col1, col2 = st.columns(2)

    with col1:
        for _, row in business.iloc[:len(business)//2].iterrows():
            st.success(f"**{row['Metric']}**\n\n{row['Value']}")

    with col2:
        for _, row in business.iloc[len(business)//2:].iterrows():
            st.info(f"**{row['Metric']}**\n\n{row['Value']}")

    st.divider()

    # =====================================================
    # EXECUTIVE SUMMARY
    # =====================================================
    st.subheader("📌 Executive Summary")
    st.success("""
✅ Revenue is primarily driven by high-performing markets.

✅ Customer segmentation identifies valuable customer groups.

✅ Product analysis highlights the highest revenue-generating products.

✅ Country-wise analysis reveals geographic sales distribution.

✅ This dashboard provides a quick executive snapshot for strategic business decisions.
""")

    st.download_button(
        "📥 Download Executive Overview",
        data=sales.to_csv(index=False),
        file_name="executive_overview.csv",
        mime="text/csv",
        key="download_executive_overview"
    )

    st.divider()
    helpers.render_footer("AI-Powered Customer Analytics & Demand Forecasting")
