import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, charts, helpers, formatters
from utils.constants import *

def show(filter_values: dict | None = None) -> None:
    # =====================================================
    # LOAD DATA
    # =====================================================
    sales = load_data.load_sales()

    # ── Apply filters from sidebar ──
    if filter_values and "date_range" in filter_values:
        dr = filter_values["date_range"]
        if isinstance(dr, tuple) and len(dr) == 2:
            import pandas as pd
            sales = sales[
                (sales["ds"].dt.date >= dr[0])
                & (sales["ds"].dt.date <= dr[1])
            ]

    # =====================================================
    # HEADER
    # =====================================================
    helpers.render_page_header(
        "📈 Sales Analytics",
        "Analyze revenue trends and overall sales performance."
    )

    # =====================================================
    # KPI VALUES
    # =====================================================
    total_revenue = sales["y"].sum()
    avg_daily = sales["y"].mean()
    max_sales = sales["y"].max()
    total_days = sales["ds"].nunique()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("💰 Total Revenue", formatters.currency(total_revenue))
    with c2:
        st.metric("📊 Average Daily Sales", formatters.currency(avg_daily))
    with c3:
        st.metric("🔥 Highest Sales", formatters.currency(max_sales))
    with c4:
        st.metric("📅 Sales Days", formatters.number(total_days))

    st.divider()

    # =====================================================
    # DAILY SALES TREND
    # =====================================================
    st.subheader("📈 Daily Sales Trend")
    fig = px.line(
        sales,
        x="ds",
        y="y",
        markers=True,
        color_discrete_sequence=[PRIMARY]
    )
    fig.update_traces(line=dict(width=3))
    charts.render(
        fig,
        height=CHART_MD,
        xaxis_title="Date",
        yaxis_title="Revenue ($)",
        hovermode="x unified"
    )

    st.divider()

    # =====================================================
    # MONTHLY REVENUE
    # =====================================================
    monthly = (
        sales
        .set_index("ds")
        .resample("ME")
        .sum()
        .reset_index()
    )
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
    # 7-DAY MOVING AVERAGE
    # =====================================================
    st.subheader("📉 7-Day Moving Average")
    moving = sales.copy()
    moving["Moving Average"] = moving["y"].rolling(window=7).mean()

    fig = px.line(
        moving,
        x="ds",
        y=["y", "Moving Average"],
        template="plotly_white"
    )
    fig.data[0].name = "Daily Revenue"
    fig.data[1].name = "7-Day Average"
    fig.data[0].line.color = PRIMARY_DARK
    fig.data[1].line.color = ACCENT_AMBER

    charts.render(
        fig,
        height=CHART_MD,
        hovermode="x unified",
        xaxis_title="Date",
        yaxis_title="Revenue ($)"
    )

    st.divider()

    # =====================================================
    # TOP 10 SALES DAYS
    # =====================================================
    st.subheader("🏆 Top 10 Highest Revenue Days")
    top_days = (
        sales
        .sort_values("y", ascending=False)
        .head(10)
        .copy()
    )
    top_days["Date"] = top_days["ds"].dt.strftime("%d %b %Y")

    fig = px.bar(
        top_days,
        x="y",
        y="Date",
        orientation="h",
        text_auto=".2s",
        color="y",
        color_continuous_scale="Purples"
    )
    charts.render(
        fig,
        height=CHART_MD,
        yaxis=dict(categoryorder="total ascending"),
        xaxis_title="Revenue ($)",
        yaxis_title="",
        coloraxis_showscale=False
    )

    st.divider()

    # =====================================================
    # REVENUE GROWTH ANALYSIS
    # =====================================================
    st.subheader("📊 Revenue Growth Analysis")
    monthly_growth = monthly.copy()
    monthly_growth["Growth %"] = monthly_growth["y"].pct_change() * 100

    fig = px.bar(
        monthly_growth,
        x="Month",
        y="Growth %",
        text_auto=".1f",
        color="Growth %",
        color_continuous_scale="RdYlGn"
    )
    charts.render(
        fig,
        height=CHART_SM,
        xaxis_title="",
        yaxis_title="Growth (%)"
    )

    st.divider()

    # =====================================================
    # SALES INSIGHTS
    # =====================================================
    st.subheader("💡 Sales Insights")
    best_day = sales.loc[sales["y"].idxmax()]
    worst_day = sales.loc[sales["y"].idxmin()]

    best_month = monthly.loc[monthly["y"].idxmax()]
    worst_month = monthly.loc[monthly["y"].idxmin()]

    total_months = monthly.shape[0]

    c1, c2 = st.columns(2)

    with c1:
        st.success(f"""
### 📈 Performance Highlights

💰 **Total Revenue**
${total_revenue:,.2f}

📅 **Best Revenue Month**
{best_month['Month']}
Revenue: ${best_month['y']:,.2f}

🔥 **Highest Revenue Day**
{best_day['ds'].strftime('%d %b %Y')}
Revenue: ${best_day['y']:,.2f}
""")

    with c2:
        st.info(f"""
### 📊 Business Statistics

📉 **Lowest Revenue Month**
{worst_month['Month']}
Revenue: ${worst_month['y']:,.2f}

📅 **Lowest Revenue Day**
{worst_day['ds'].strftime('%d %b %Y')}
Revenue: ${worst_day['y']:,.2f}

🗓 **Months Available**
{total_months}
""")

    st.divider()

    # =====================================================
    # MONTHLY SUMMARY TABLE
    # =====================================================
    st.subheader("📋 Monthly Revenue Summary")
    summary = monthly.copy()
    summary.columns = ["Date", "Revenue", "Month"]
    summary = summary[["Month", "Revenue"]]
    summary["Revenue"] = summary["Revenue"].round(2)

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # =====================================================
    # DOWNLOAD REPORT
    # =====================================================
    st.download_button(
        "📥 Download Sales Analytics CSV",
        data=sales.to_csv(index=False),
        file_name="sales_analytics.csv",
        mime="text/csv",
        key="download_sales_analytics"
    )

    st.divider()

    st.success("""
### 📌 Executive Summary

✅ Daily revenue trend has been analyzed.

✅ Monthly revenue highlights seasonality.

✅ Moving average smooths sales fluctuations.

✅ Highest revenue days help identify peak demand.

✅ Revenue growth analysis supports business planning.
""")

    st.divider()
    helpers.render_footer("Sales Analytics Dashboard • AI-Powered Business Intelligence")