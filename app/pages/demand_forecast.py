import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data, charts, helpers, formatters
from utils.constants import *
import numpy as np

def show() -> None:
    helpers.render_page_header("📅 Demand Forecast", "AI-powered demand forecasting with confidence intervals.")
    
    forecast_df = load_data.load_demand_forecast()
    sales_df = load_data.load_sales()
    
    if forecast_df.empty or sales_df.empty:
        st.warning("Data not available.")
        return
        
    forecast_df = forecast_df.copy()
    forecast_df['ds'] = pd.to_datetime(forecast_df['ds'])
    forecast_period = forecast_df[forecast_df['ds'] > sales_df['ds'].max()]

    forecast_days = len(forecast_period)
    avg_predicted_revenue = forecast_period['yhat'].mean() if forecast_days else 0
    forecast_range = (
        (forecast_period['yhat_upper'] - forecast_period['yhat_lower']).mean()
        if forecast_days else 0
    )
    actual_data_points = len(sales_df)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Forecast Days", formatters.number(forecast_days))
    with col2:
        st.metric("Avg Predicted Revenue", formatters.currency(avg_predicted_revenue))
    with col3:
        st.metric("Forecast Range", formatters.currency(forecast_range))
    with col4:
        st.metric("Actual Data Points", formatters.number(actual_data_points))
        
    st.markdown("### Sales vs Forecast")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sales_df['ds'], y=sales_df['y'],
        mode='lines',
        name='Actual Sales',
        line=dict(color=PRIMARY)
    ))
    
    fig.add_trace(go.Scatter(
        x=forecast_df['ds'], y=forecast_df['yhat_upper'],
        mode='lines',
        line=dict(width=0),
        showlegend=False,
        name='Upper Bound'
    ))
    
    fig.add_trace(go.Scatter(
        x=forecast_df['ds'], y=forecast_df['yhat_lower'],
        mode='lines',
        line=dict(width=0),
        fill='tonexty',
        fillcolor='rgba(16, 185, 129, 0.2)', # ACCENT_GREEN with opacity
        name='Confidence Interval'
    ))
    
    fig.add_trace(go.Scatter(
        x=forecast_df['ds'], y=forecast_df['yhat'],
        mode='lines',
        name='Forecast',
        line=dict(color=ACCENT_GREEN, dash='dash')
    ))
    
    fig.update_layout(title='Revenue Forecast')
    charts.render(fig, height=CHART_LG)
    
    st.markdown("### Monthly Forecast Summary")
    # Resample
    monthly_forecast = (
        forecast_period
        .set_index('ds')
        .resample('ME')['yhat']
        .sum()
        .reset_index()
    )
    fig_monthly = px.bar(
        monthly_forecast, 
        x='ds', 
        y='yhat', 
        title='Monthly Forecasted Revenue',
        color_discrete_sequence=[ACCENT_PURPLE]
    )
    charts.render(fig_monthly, height=CHART_MD)
    
    st.markdown("### Historical Fit Accuracy")
    
    sales_df['ds'] = pd.to_datetime(sales_df['ds'])
    merged = pd.merge(sales_df, forecast_df, on='ds', how='inner')
    merged_nonzero = merged[merged['y'] != 0]
    if not merged_nonzero.empty:
        mae = np.mean(np.abs(merged['y'] - merged['yhat']))
        mape = np.mean(
            np.abs(
                (merged_nonzero['y'] - merged_nonzero['yhat'])
                / merged_nonzero['y']
            )
        ) * 100
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Mean Absolute Error (MAE)", formatters.currency(mae))
        with col2:
            st.metric("Mean Absolute Percentage Error (MAPE)", formatters.percent(mape))
    else:
        st.info("No non-zero historical sales dates are available to compute accuracy.")
        
    st.markdown("### Forecast Data")
    st.dataframe(forecast_period, use_container_width=True)
    
    csv = forecast_period.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Forecast Data",
        data=csv,
        file_name='demand_forecast.csv',
        mime='text/csv',
        key='dl_forecast'
    )
    
    st.markdown("### Executive Summary")
    st.info("The AI-powered forecast predicts future trends with confidence intervals, allowing for better inventory and resource planning.")
    
    helpers.render_footer("Demand Forecast")
