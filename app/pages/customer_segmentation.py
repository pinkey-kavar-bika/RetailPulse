import streamlit as st
import plotly.express as px
from utils import load_data, charts, helpers, formatters
from utils.constants import *

def show(filter_values: dict | None = None) -> None:
    customers = load_data.load_segmentation()

    # ── Apply filters from sidebar ──
    if filter_values:
        if filter_values.get("segment") and filter_values["segment"] != "All":
            customers = customers[customers["CustomerSegment"] == filter_values["segment"]]

    helpers.render_page_header(
        "🎯 Customer Segmentation",
        "RFM-Based Customer Segmentation Dashboard"
    )

    total_customers = customers["CustomerID"].nunique()
    avg_recency = customers["Recency"].mean()
    avg_frequency = customers["Frequency"].mean()
    avg_monetary = customers["Monetary"].mean()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("👥 Customers", formatters.number(total_customers))
    with c2:
        st.metric("📅 Avg Recency", f"{avg_recency:.1f} Days")
    with c3:
        st.metric("🛒 Avg Frequency", f"{avg_frequency:.2f}")
    with c4:
        st.metric("💰 Avg Monetary", formatters.currency(avg_monetary, decimals=2))

    st.divider()

    left, right = st.columns(2)
    with left:
        st.subheader("👥 Customer Segment Distribution")
        segment = customers["CustomerSegment"].value_counts().reset_index()
        segment.columns = ["Customer Segment", "Customers"]
        fig = px.pie(
            segment,
            names="Customer Segment",
            values="Customers",
            hole=0.60,
            color="Customer Segment",
            color_discrete_sequence=[PRIMARY, ACCENT_GREEN, ACCENT_AMBER, ACCENT_RED, ACCENT_CYAN, ACCENT_PURPLE]
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        charts.render(fig, height=CHART_MD, showlegend=False)

    with right:
        st.subheader("🎯 Cluster Distribution")
        cluster = customers["Cluster"].value_counts().sort_index().reset_index()
        cluster.columns = ["Cluster", "Customers"]
        fig = px.bar(
            cluster,
            x="Cluster",
            y="Customers",
            text_auto=True,
            color="Customers",
            color_continuous_scale="Purples"
        )
        charts.render(
            fig,
            height=CHART_MD,
            xaxis_title="Cluster",
            yaxis_title="Customers",
            coloraxis_showscale=False
        )

    st.divider()

    left, right = st.columns(2)
    with left:
        st.subheader("📅 Recency Distribution")
        fig = px.histogram(
            customers,
            x="Recency",
            nbins=30,
            color_discrete_sequence=[ACCENT_AMBER]
        )
        charts.render(
            fig,
            height=CHART_SM,
            xaxis_title="Recency (Days)",
            yaxis_title="Customers"
        )

    with right:
        st.subheader("🛒 Frequency Distribution")
        fig = px.histogram(
            customers,
            x="Frequency",
            nbins=30,
            color_discrete_sequence=[ACCENT_GREEN]
        )
        charts.render(
            fig,
            height=CHART_SM,
            xaxis_title="Frequency",
            yaxis_title="Customers"
        )

    st.divider()

    left, right = st.columns(2)
    with left:
        st.subheader("💰 Monetary Distribution")
        fig = px.box(
            customers,
            y="Monetary",
            points="outliers",
            color_discrete_sequence=[PRIMARY]
        )
        charts.render(
            fig,
            height=CHART_SM,
            yaxis_title="Monetary Value ($)",
            showlegend=False
        )

    with right:
        st.subheader("📊 Frequency vs Monetary")
        fig = px.scatter(
            customers,
            x="Frequency",
            y="Monetary",
            size="Monetary",
            color="Cluster",
            hover_data=["CustomerID", "CustomerSegment"],
            color_continuous_scale="Viridis"
        )
        charts.render(
            fig,
            height=CHART_SM,
            xaxis_title="Frequency",
            yaxis_title="Monetary"
        )

    st.divider()

    st.subheader("🏆 Top Customer Segments")
    segment_summary = customers.groupby("CustomerSegment").agg(
        Customers=("CustomerID", "count"),
        AvgMonetary=("Monetary", "mean"),
        AvgFrequency=("Frequency", "mean"),
        AvgRecency=("Recency", "mean")
    ).reset_index().sort_values("AvgMonetary", ascending=False)
    
    fig = px.bar(
        segment_summary,
        x="CustomerSegment",
        y="AvgMonetary",
        color="CustomerSegment",
        text_auto=".2s",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    charts.render(
        fig,
        height=CHART_MD,
        xaxis_title="Customer Segment",
        yaxis_title="Average Monetary Value",
        showlegend=False
    )

    st.divider()

    st.subheader("📋 Customer Segment Summary")
    summary = customers.groupby("CustomerSegment").agg(
        Customers=("CustomerID", "count"),
        AvgRecency=("Recency", "mean"),
        AvgFrequency=("Frequency", "mean"),
        AvgMonetary=("Monetary", "mean")
    ).reset_index()
    summary["AvgRecency"] = summary["AvgRecency"].round(1)
    summary["AvgFrequency"] = summary["AvgFrequency"].round(2)
    summary["AvgMonetary"] = summary["AvgMonetary"].round(2)
    st.dataframe(summary, use_container_width=True, hide_index=True)

    st.divider()

    highest_segment = summary.loc[summary["AvgMonetary"].idxmax(), "CustomerSegment"]
    largest_segment = summary.loc[summary["Customers"].idxmax(), "CustomerSegment"]
    lowest_recency = summary.loc[summary["AvgRecency"].idxmin(), "CustomerSegment"]

    c1, c2 = st.columns(2)
    with c1:
        st.success(f"""
### 🏆 Segment Highlights
💰 Highest Average Monetary
**{highest_segment}**

👥 Largest Customer Segment
**{largest_segment}**
""")
    with c2:
        st.info(f"""
### 📈 Customer Engagement
🔥 Most Recent Active Segment
**{lowest_recency}**

🎯 Total Segments
**{customers['CustomerSegment'].nunique()}**
""")

    st.divider()

    st.download_button(
        label="📥 Download Customer Segmentation Report",
        data=customers.to_csv(index=False),
        file_name="customer_segmentation.csv",
        mime="text/csv",
        key="customer_segmentation_download"
    )

    st.divider()

    st.subheader("📌 Executive Summary")
    st.success("""
✅ RFM-based customer segmentation completed.
✅ Customer clusters have been visualized.
✅ Spending (Monetary), purchase frequency, and recency patterns have been analyzed.
✅ High-value customer segments have been identified.
✅ This dashboard supports targeted marketing campaigns and customer retention strategies.
""")

    st.divider()
    helpers.render_footer("Customer Segmentation")