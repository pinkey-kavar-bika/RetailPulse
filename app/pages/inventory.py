import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_data, charts, helpers, formatters
from utils.constants import *

def show(filter_values: dict | None = None) -> None:
    # LOAD DATA
    inventory = load_data.load_inventory()

    # APPLY FILTERS (from centralized sidebar)
    filtered = inventory.copy()
    if filter_values:
        if filter_values.get("abc_class") and filter_values["abc_class"] != "All":
            filtered = filtered[filtered["ABC_Class"] == filter_values["abc_class"]]
        if filter_values.get("movement") and filter_values["movement"] != "All":
            filtered = filtered[filtered["MovementCategory"] == filter_values["movement"]]

    # HEADER
    helpers.render_page_header("📦 Inventory Dashboard", "Monitor inventory performance, product movement and stock value.")

    # KPI CALCULATIONS
    total_products = filtered["StockCode"].nunique()
    total_quantity = filtered["TotalQuantity"].sum()
    total_revenue = filtered["TotalRevenue"].sum()
    avg_price = filtered["AveragePrice"].mean()

    # KPI VALUES
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Products", formatters.number(total_products))
    with c2:
        st.metric("Total Quantity", formatters.number(int(total_quantity)))
    with c3:
        st.metric("Revenue", formatters.currency(total_revenue, 2))
    with c4:
        st.metric("Average Price", formatters.currency(avg_price, 2))
    
    st.divider()

    # ABC CLASSIFICATION
    left, right = st.columns(2)
    with left:
        st.subheader("📦 ABC Classification")
        abc = (
            filtered
            .groupby("ABC_Class")["TotalRevenue"]
            .sum()
            .reset_index()
            .sort_values("TotalRevenue", ascending=False)
        )
        fig = px.pie(
            abc,
            names="ABC_Class",
            values="TotalRevenue",
            hole=0.60,
            color="ABC_Class",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        charts.render(fig, height=CHART_MD, showlegend=False)

    # MOVEMENT CATEGORY
    with right:
        st.subheader("🚚 Inventory Movement")
        movement = (
            filtered
            .groupby("MovementCategory")["StockCode"]
            .count()
            .reset_index(name="Products")
            .sort_values("Products", ascending=False)
        )
        fig = px.bar(
            movement,
            x="MovementCategory",
            y="Products",
            text_auto=True,
            color="MovementCategory",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        charts.render(fig, height=CHART_MD, xaxis_title="Movement Category", yaxis_title="Products", showlegend=False)

    st.divider()

    # TOP 10 PRODUCTS BY REVENUE
    st.subheader("💰 Top 10 Products by Revenue")
    revenue = (
        filtered
        .sort_values("TotalRevenue", ascending=False)
        .head(10)
    )
    fig = px.bar(
        revenue,
        x="TotalRevenue",
        y="Description",
        orientation="h",
        text_auto=".2s",
        color="TotalRevenue",
        color_continuous_scale="Blues"
    )
    charts.render(fig, height=CHART_LG, xaxis_title="Revenue", yaxis_title="", coloraxis_showscale=False)

    st.divider()

    # TOP 10 PRODUCTS BY QUANTITY
    left, right = st.columns(2)
    with left:
        st.subheader("📦 Top 10 Products by Quantity")
        quantity = (
            filtered
            .sort_values("TotalQuantity", ascending=False)
            .head(10)
        )
        fig = px.bar(
            quantity,
            x="TotalQuantity",
            y="Description",
            orientation="h",
            text_auto=True,
            color="TotalQuantity",
            color_continuous_scale="Greens"
        )
        charts.render(fig, height=CHART_MD, xaxis_title="Total Quantity", yaxis_title="", coloraxis_showscale=False)

    # AVERAGE PRICE ANALYSIS
    with right:
        st.subheader("💲 Average Price Distribution")
        fig = px.box(
            filtered,
            y="AveragePrice",
            points="outliers",
            color_discrete_sequence=[ACCENT_AMBER]
        )
        charts.render(fig, height=CHART_MD, yaxis_title="Average Price", showlegend=False)

    st.divider()

    # REVENUE VS QUANTITY
    st.subheader("📊 Revenue vs Quantity Analysis")
    fig = px.scatter(
        filtered,
        x="TotalQuantity",
        y="TotalRevenue",
        size="AveragePrice",
        color="ABC_Class",
        hover_name="Description",
        hover_data=["StockCode", "MovementCategory"],
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    charts.render(fig, height=CHART_LG, xaxis_title="Total Quantity", yaxis_title="Total Revenue")

    st.divider()

    # INVENTORY DETAILS TABLE
    st.subheader("📋 Inventory Details")
    inventory_table = filtered.copy()
    inventory_table = inventory_table.sort_values("TotalRevenue", ascending=False)
    st.dataframe(
        inventory_table[
            [
                "StockCode",
                "Description",
                "TotalQuantity",
                "TotalRevenue",
                "TotalOrders",
                "AveragePrice",
                "ABC_Class",
                "MovementCategory"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # BUSINESS INSIGHTS
    highest_revenue = filtered.loc[filtered["TotalRevenue"].idxmax()]
    highest_quantity = filtered.loc[filtered["TotalQuantity"].idxmax()]

    left, right = st.columns(2)
    with left:
        st.success(f"""
### 💰 Highest Revenue Product
**Product**
{highest_revenue['Description']}

**Revenue**
{formatters.currency(highest_revenue['TotalRevenue'], 2)}

**ABC Class**
{highest_revenue['ABC_Class']}
""")

    with right:
        st.info(f"""
### 📦 Highest Quantity Product
**Product**
{highest_quantity['Description']}

**Quantity Sold**
{formatters.number(int(highest_quantity['TotalQuantity']))}

**Movement**
{highest_quantity['MovementCategory']}
""")

    st.divider()

    # DOWNLOAD REPORT
    st.download_button(
        "📥 Download Inventory Report",
        data=filtered.to_csv(index=False),
        file_name="inventory_report.csv",
        mime="text/csv",
        key="download_inventory"
    )

    st.divider()

    # EXECUTIVE SUMMARY
    st.subheader("📌 Executive Summary")
    st.success(f"""
### Inventory Performance Summary
• Total Products : **{formatters.number(total_products)}**
• Total Quantity Sold : **{formatters.number(int(total_quantity))}**
• Total Revenue : **{formatters.currency(total_revenue, 2)}**
• Average Product Price : **{formatters.currency(avg_price, 2)}**
• ABC Classification highlights high-value inventory.
• Movement Categories help identify fast and slow moving products.
• Dashboard supports inventory optimization and stock planning.
""")

    st.divider()
    helpers.render_footer("Inventory Dashboard")