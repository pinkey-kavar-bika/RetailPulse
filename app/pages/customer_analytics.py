import streamlit as st
import plotly.express as px
from utils import load_data, charts, helpers, formatters
from utils.constants import *

def show(filter_values: dict | None = None) -> None:
    customers = load_data.load_customers()

    # ── Apply filters from sidebar ──
    if filter_values:
        if filter_values.get("country") and filter_values["country"] != "All":
            customers = customers[customers["Country"] == filter_values["country"]]
        if filter_values.get("segment") and filter_values["segment"] != "All":
            customers = customers[customers["CustomerSegment"] == filter_values["segment"]]

    helpers.render_page_header(
        "👥 Customer Analytics",
        "Analyze customer purchasing behaviour, revenue and engagement."
    )

    total_customers = customers["CustomerID"].nunique()
    total_revenue = customers["TotalRevenue"].sum()
    total_invoices = customers["TotalInvoices"].sum()
    avg_order_value = customers["AvgOrderValue"].mean()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("👥 Customers", formatters.number(total_customers))
    with c2:
        st.metric("💰 Revenue", formatters.currency(total_revenue))
    with c3:
        st.metric("🧾 Total Invoices", formatters.number(int(total_invoices)))
    with c4:
        st.metric("🛒 Avg Order Value", formatters.currency(avg_order_value, decimals=2))

    st.divider()

    left, right = st.columns(2)
    with left:
        st.subheader("Top 10 Customers by Revenue")
        top_customers = customers.sort_values("TotalRevenue", ascending=False).head(10)
        fig = px.bar(
            top_customers,
            x="TotalRevenue",
            y=top_customers["CustomerID"].astype(str),
            orientation="h",
            text_auto=".2s",
            color="TotalRevenue",
            color_continuous_scale="Blues"
        )
        charts.render(
            fig,
            height=CHART_MD,
            yaxis=dict(categoryorder="total ascending"),
            xaxis_title="Revenue ($)",
            yaxis_title="Customer ID",
            coloraxis_showscale=False
        )

    with right:
        st.subheader("Invoice Distribution")
        fig = px.histogram(
            customers,
            x="TotalInvoices",
            nbins=25,
            color_discrete_sequence=[PRIMARY]
        )
        charts.render(
            fig,
            height=CHART_MD,
            xaxis_title="Invoices",
            yaxis_title="Customers"
        )

    st.divider()

    left, right = st.columns(2)
    with left:
        st.subheader("Average Order Value")
        fig = px.box(
            customers,
            y="AvgOrderValue",
            points="outliers",
            color_discrete_sequence=[ACCENT_GREEN]
        )
        charts.render(
            fig,
            height=CHART_SM,
            yaxis_title="Average Order Value ($)",
            showlegend=False
        )

    with right:
        st.subheader("Basket Size")
        fig = px.box(
            customers,
            y="AvgBasketSize",
            color_discrete_sequence=[ACCENT_AMBER]
        )
        charts.render(
            fig,
            height=CHART_SM,
            yaxis_title="Average Basket Size",
            showlegend=False
        )

    st.divider()

    left, right = st.columns(2)
    with left:
        st.subheader("Customer Segments")
        segment = customers["CustomerSegment"].value_counts().reset_index()
        segment.columns = ["CustomerSegment", "Count"]
        fig = px.pie(
            segment,
            names="CustomerSegment",
            values="Count",
            hole=0.60,
            color="CustomerSegment",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        charts.render(fig, height=CHART_MD, showlegend=False)

    with right:
        st.subheader("Cluster Distribution")
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
        st.subheader("Top Countries")
        country = customers.groupby("Country")["TotalRevenue"].sum().reset_index().sort_values("TotalRevenue", ascending=False).head(10)
        fig = px.bar(
            country,
            x="TotalRevenue",
            y="Country",
            orientation="h",
            text_auto=".2s",
            color="Country",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        charts.render(
            fig,
            height=CHART_MD,
            yaxis=dict(categoryorder="total ascending"),
            xaxis_title="Revenue ($)",
            yaxis_title="",
            showlegend=False
        )

    with right:
        st.subheader("Preferred Purchase Hour")
        hour = customers["PreferredPurchaseHour"].value_counts().sort_index().reset_index()
        hour.columns = ["Hour", "Customers"]
        fig = px.line(
            hour,
            x="Hour",
            y="Customers",
            markers=True,
            color_discrete_sequence=[PRIMARY]
        )
        fig.update_traces(line=dict(width=4))
        charts.render(
            fig,
            height=CHART_MD,
            xaxis_title="Hour of Day",
            yaxis_title="Customers"
        )

    st.divider()

    left, right = st.columns(2)
    with left:
        st.subheader("Preferred Shopping Season")
        season = customers["PreferredSeason"].value_counts().reset_index()
        season.columns = ["Season", "Customers"]
        fig = px.pie(
            season,
            names="Season",
            values="Customers",
            hole=0.55,
            color="Season",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_traces(textinfo="percent+label")
        charts.render(fig, height=CHART_SM, showlegend=False)

    with right:
        st.subheader("Customer Behaviour")
        fig = px.scatter(
            customers,
            x="Recency",
            y="Monetary",
            size="Frequency",
            color="Cluster",
            hover_data=["CustomerID", "CustomerSegment"],
            color_continuous_scale="Viridis"
        )
        charts.render(
            fig,
            height=CHART_SM,
            xaxis_title="Recency",
            yaxis_title="Monetary"
        )

    st.divider()

    highest_revenue = customers.loc[customers["TotalRevenue"].idxmax()]
    highest_invoice = customers.loc[customers["TotalInvoices"].idxmax()]

    c1, c2 = st.columns(2)
    with c1:
        st.success(f"""
### 🏆 Highest Revenue Customer
👤 Customer ID
**{highest_revenue['CustomerID']}**

💰 Revenue
**${highest_revenue['TotalRevenue']:,.2f}**

🧾 Invoices
**{highest_revenue['TotalInvoices']}**
""")
    with c2:
        st.info(f"""
### 📦 Most Active Customer
👤 Customer ID
**{highest_invoice['CustomerID']}**

🧾 Total Invoices
**{highest_invoice['TotalInvoices']}**

💵 Avg Order Value
**${highest_invoice['AvgOrderValue']:,.2f}**
""")

    st.divider()

    st.subheader("📋 Customer Summary")
    summary = customers[
        ["CustomerID", "Country", "TotalRevenue", "TotalInvoices", "AvgOrderValue", "CustomerSegment"]
    ].sort_values("TotalRevenue", ascending=False)
    st.dataframe(summary, use_container_width=True, hide_index=True)

    st.divider()

    st.download_button(
        "📥 Download Customer Analytics Report",
        data=customers.to_csv(index=False),
        file_name="customer_analytics.csv",
        mime="text/csv",
        key="customer_analytics_download"
    )

    st.divider()

    st.success("""
### 📌 Executive Summary
✅ Customer revenue distribution analyzed.
✅ High-value customers identified.
✅ Purchase behaviour visualized using RFM metrics.
✅ Country and seasonal preferences analyzed.
✅ Dashboard supports customer retention and marketing strategies.
""")

    st.divider()
    helpers.render_footer("Customer Analytics")
