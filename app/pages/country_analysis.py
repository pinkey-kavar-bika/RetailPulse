import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_data, charts, helpers, formatters
from utils.constants import *

def show(filter_values: dict | None = None) -> None:
    # LOAD DATA
    country = load_data.load_country()

    # APPLY FILTERS (from centralized sidebar)
    filtered = country.copy()
    if filter_values:
        if filter_values.get("country") and filter_values["country"] != "All":
            filtered = filtered[filtered["Country"] == filter_values["country"]]

    # PAGE HEADER
    helpers.render_page_header("🌍 Country Analysis", "Analyze country-wise sales performance, customers and revenue contribution.")

    # KPI CALCULATIONS
    total_countries = filtered["Country"].nunique()
    total_revenue = filtered["TotalRevenue"].sum()
    total_orders = filtered["TotalOrders"].sum()
    total_customers = filtered["TotalCustomers"].sum()
    avg_revenue_customer = filtered["AverageRevenuePerCustomer"].mean()

    # KPI CARDS
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("Countries", formatters.number(total_countries))
    with c2:
        st.metric("Revenue", formatters.currency(total_revenue, 2))
    with c3:
        st.metric("Orders", formatters.number(int(total_orders)))
    with c4:
        st.metric("Customers", formatters.number(int(total_customers)))
    with c5:
        st.metric("Avg Revenue / Customer", formatters.currency(avg_revenue_customer, 2))

    st.divider()

    # REVENUE BY COUNTRY
    left, right = st.columns(2)
    with left:
        st.subheader("💰 Revenue by Country")
        revenue = (
            filtered
            .sort_values("TotalRevenue", ascending=False)
        )
        fig = px.bar(
            revenue,
            x="Country",
            y="TotalRevenue",
            text_auto=".2s",
            color="TotalRevenue",
            color_continuous_scale="Blues"
        )
        charts.render(fig, height=CHART_MD, xaxis_title="Country", yaxis_title="Revenue ($)", coloraxis_showscale=False)

    # CUSTOMERS BY COUNTRY
    with right:
        st.subheader("👥 Customers by Country")
        customers = (
            filtered
            .sort_values("TotalCustomers", ascending=False)
        )
        fig = px.bar(
            customers,
            x="Country",
            y="TotalCustomers",
            text_auto=True,
            color="TotalCustomers",
            color_continuous_scale="Greens"
        )
        charts.render(fig, height=CHART_MD, xaxis_title="Country", yaxis_title="Customers", coloraxis_showscale=False)

    st.divider()

    # TOTAL ORDERS BY COUNTRY
    st.subheader("📦 Orders by Country")
    orders = (
        filtered
        .sort_values("TotalOrders", ascending=False)
    )
    fig = px.bar(
        orders,
        x="Country",
        y="TotalOrders",
        text_auto=True,
        color="TotalOrders",
        color_continuous_scale="Oranges"
    )
    charts.render(fig, height=CHART_MD, xaxis_title="Country", yaxis_title="Total Orders", coloraxis_showscale=False)

    st.divider()

    # QUANTITY SOLD BY COUNTRY
    left, right = st.columns(2)
    with left:
        st.subheader("📦 Quantity Sold by Country")
        quantity = (
            filtered
            .sort_values("TotalQuantity", ascending=False)
        )
        fig = px.bar(
            quantity,
            x="Country",
            y="TotalQuantity",
            text_auto=True,
            color="TotalQuantity",
            color_continuous_scale="Purples"
        )
        charts.render(fig, height=CHART_MD, xaxis_title="Country", yaxis_title="Quantity Sold", coloraxis_showscale=False)

    # AVERAGE REVENUE PER CUSTOMER
    with right:
        st.subheader("💵 Average Revenue per Customer")
        avg_rev = (
            filtered
            .sort_values("AverageRevenuePerCustomer", ascending=False)
        )
        fig = px.bar(
            avg_rev,
            x="Country",
            y="AverageRevenuePerCustomer",
            text_auto=".2f",
            color="AverageRevenuePerCustomer",
            color_continuous_scale="Teal"
        )
        charts.render(fig, height=CHART_MD, xaxis_title="Country", yaxis_title="Average Revenue ($)", coloraxis_showscale=False)

    st.divider()

    # REVENUE VS CUSTOMERS
    st.subheader("🌍 Revenue vs Customers")
    fig = px.scatter(
        filtered,
        x="TotalCustomers",
        y="TotalRevenue",
        size="TotalOrders",
        color="TotalQuantity",
        hover_name="Country",
        hover_data=["AverageRevenuePerCustomer"],
        color_continuous_scale="Viridis"
    )
    charts.render(fig, height=CHART_LG, xaxis_title="Total Customers", yaxis_title="Total Revenue ($)")

    st.divider()

    # COUNTRY SUMMARY TABLE
    st.subheader("📋 Country Performance Summary")
    summary = filtered.copy()
    summary = summary.sort_values("TotalRevenue", ascending=False)
    st.dataframe(
        summary[
            [
                "Country",
                "TotalRevenue",
                "TotalOrders",
                "TotalCustomers",
                "TotalQuantity",
                "AverageRevenuePerCustomer"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # BUSINESS INSIGHTS
    highest_revenue = filtered.loc[filtered["TotalRevenue"].idxmax()]
    highest_customers = filtered.loc[filtered["TotalCustomers"].idxmax()]

    left, right = st.columns(2)
    with left:
        st.success(f"""
### 💰 Highest Revenue Country
**Country**
{highest_revenue['Country']}

**Revenue**
{formatters.currency(highest_revenue['TotalRevenue'], 2)}

**Orders**
{formatters.number(int(highest_revenue['TotalOrders']))}
""")

    with right:
        st.info(f"""
### 👥 Largest Customer Base
**Country**
{highest_customers['Country']}

**Customers**
{formatters.number(int(highest_customers['TotalCustomers']))}

**Average Revenue / Customer**
{formatters.currency(highest_customers['AverageRevenuePerCustomer'], 2)}
""")

    st.divider()

    # DOWNLOAD REPORT
    st.download_button(
        "📥 Download Country Analysis Report",
        data=filtered.to_csv(index=False),
        file_name="country_analysis_report.csv",
        mime="text/csv",
        key="download_country_analysis"
    )

    st.divider()

    # EXECUTIVE SUMMARY
    st.subheader("📌 Executive Summary")
    st.success(f"""
### Country Performance Summary
• Total Countries Analysed : **{formatters.number(total_countries)}**
• Total Revenue : **{formatters.currency(total_revenue, 2)}**
• Total Orders : **{formatters.number(int(total_orders))}**
• Total Customers : **{formatters.number(int(total_customers))}**
• Average Revenue per Customer : **{formatters.currency(avg_revenue_customer, 2)}**
• Identify countries contributing the highest revenue.
• Compare customer base and order volume across markets.
• Support business expansion and regional marketing decisions.
""")

    st.divider()
    helpers.render_footer("Country Analysis Dashboard")