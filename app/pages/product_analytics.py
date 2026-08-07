import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, charts, helpers, formatters
from utils.constants import *

def show(filter_values: dict | None = None) -> None:
    helpers.render_page_header("🛍 Product Analytics", "Analyze product performance, revenue contribution, and pricing.")
    
    df = load_data.load_products()
    
    if df.empty:
        st.warning("No product data available.")
        return

    # ── Apply filters from sidebar ──
    if filter_values and "revenue_range" in filter_values:
        rmin, rmax = filter_values["revenue_range"]
        df = df[(df["TotalRevenue"] >= rmin) & (df["TotalRevenue"] <= rmax)]
        
    total_products = len(df)
    total_revenue = df['TotalRevenue'].sum()
    total_quantity = df['TotalQuantity'].sum()
    avg_price = df['AveragePrice'].mean()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Products", formatters.number(total_products))
    with col2:
        st.metric("Total Revenue", formatters.currency(total_revenue))
    with col3:
        st.metric("Total Quantity", formatters.number(total_quantity))
    with col4:
        st.metric("Avg Price", formatters.currency(avg_price, decimals=2))
        
    st.markdown("### Top Products")
    col1, col2 = st.columns(2)
    
    with col1:
        top_rev = df.nlargest(10, 'TotalRevenue')
        fig_rev = px.bar(
            top_rev, 
            y='Description', 
            x='TotalRevenue', 
            orientation='h',
            title='Top 10 Products by Revenue',
            color='TotalRevenue',
            color_continuous_scale='Viridis'
        )
        fig_rev.update_layout(yaxis={'categoryorder': 'total ascending'})
        charts.render(fig_rev, height=CHART_MD)
        
    with col2:
        top_qty = df.nlargest(10, 'TotalQuantity')
        fig_qty = px.bar(
            top_qty, 
            y='Description', 
            x='TotalQuantity', 
            orientation='h',
            title='Top 10 Products by Quantity',
            color='TotalQuantity',
            color_continuous_scale='Blues'
        )
        fig_qty.update_layout(yaxis={'categoryorder': 'total ascending'})
        charts.render(fig_qty, height=CHART_MD)

    st.markdown("### Product Distributions")
    col1, col2 = st.columns(2)
    
    with col1:
        fig_dist = px.histogram(
            df, 
            x='TotalRevenue', 
            nbins=50, 
            title='Revenue Distribution',
            color_discrete_sequence=[PRIMARY]
        )
        charts.render(fig_dist, height=CHART_MD)
        
    with col2:
        fig_scatter = px.scatter(
            df,
            x='TotalQuantity',
            y='AveragePrice',
            size='TotalOrders',
            color='TotalRevenue',
            hover_name='Description',
            title='Price vs Quantity (Size: Orders, Color: Revenue)',
            color_continuous_scale='Viridis'
        )
        charts.render(fig_scatter, height=CHART_MD)
        
    st.markdown("### Product Summary")
    st.dataframe(df, use_container_width=True)
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Product Data",
        data=csv,
        file_name='product_analytics.csv',
        mime='text/csv',
        key='dl_products'
    )
    
    st.markdown("### Executive Summary")
    st.info("Product performance highlights the top revenue drivers and volume leaders. Pricing strategies can be optimized based on the Price vs Quantity distribution.")
    
    helpers.render_footer("Product Analytics")
