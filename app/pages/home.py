"""RetailPulse — Home landing page."""

from __future__ import annotations

import streamlit as st
from utils import load_data, helpers, formatters
from utils.constants import *


# ─── Fallback KPI loaders ────────────────────────────────────
def _load_business_kpis() -> dict:
    """Return top-level KPIs, falling back to executive_overview if needed."""
    try:
        biz = load_data.load_business_insights()

        def _val(metric: str) -> str:
            row = biz.loc[biz["Metric"] == metric, "Value"]
            return str(row.values[0]) if len(row) else "N/A"

        return {
            "revenue": float(_val("Total Revenue")),
            "orders": int(float(_val("Total Orders"))),
            "customers": int(float(_val("Total Customers"))),
            "products": int(float(_val("Products"))),
        }
    except Exception:
        pass

    # ── Fallback: derive from executive_overview ──
    try:
        eo = load_data.load_executive_overview()
        row = eo.iloc[0]
        return {
            "revenue": float(row.get("TotalRevenue", 0)),
            "orders": int(row.get("TotalOrders", 0)),
            "customers": int(row.get("TotalCustomers", 0)),
            "products": int(row.get("TotalProducts", 0)),
        }
    except Exception:
        return {"revenue": 0, "orders": 0, "customers": 0, "products": 0}


def _load_project_kpis() -> dict:
    """Return project-level KPIs, with safe defaults if CSV is missing."""
    defaults = {
        "countries": "N/A",
        "ml_models": "N/A",
        "pages": "N/A",
        "datasets": "N/A",
    }
    try:
        proj = load_data.load_project_summary()

        def _val(metric: str) -> str:
            row = proj.loc[proj["Project Metric"] == metric, "Value"]
            return str(row.values[0]) if len(row) else "N/A"

        return {
            "countries": _val("Countries Covered"),
            "ml_models": _val("Machine Learning Models"),
            "pages": _val("Dashboard Pages"),
            "datasets": _val("Processed Datasets"),
        }
    except Exception:
        pass

    # ── Fallback: try to get countries from executive_overview ──
    try:
        eo = load_data.load_executive_overview()
        defaults["countries"] = str(int(eo.iloc[0].get("CountriesServed", 0)))
    except Exception:
        pass

    return defaults


def _render_about_project() -> None:
    """Render the Home-only project overview section."""
    st.markdown("### 📋 About This Project")
    st.info(
        "**RetailPulse** is a comprehensive, AI-powered retail analytics platform "
        "built on **779,425+ transactions** across **41 countries**. It combines "
        "advanced customer segmentation (RFM), churn prediction, demand forecasting, "
        "and inventory optimization into a single interactive dashboard.\n\n"
        "Navigate to any section using the sidebar to explore deep insights."
    )


def _render_quick_navigation() -> None:
    """Render the Home-only dashboard navigation cards."""
    st.markdown("### 🚀 Quick Navigation")
    nav_cards = [
        ("📊", "Executive Dashboard", "High-level overview of revenue, orders, and customer segments."),
        ("📈", "Sales Analytics", "Daily & monthly revenue trends, growth analysis, and top sales days."),
        ("👥", "Customer Analytics", "Customer behaviour, purchase patterns, and engagement metrics."),
        ("🎯", "Customer Segmentation", "RFM-based customer segmentation and cluster analysis."),
        ("⚠", "Customer Churn", "Predict churn risk, identify at-risk customers, and retention priorities."),
        ("📦", "Inventory", "Monitor stock levels, ABC classification, and product movement."),
        ("🌍", "Country Analysis", "Country-wise revenue, orders, and customer distribution."),
        ("🛍", "Product Analytics", "Product performance, pricing analysis, and top sellers."),
        ("📅", "Demand Forecast", "AI-powered demand forecasting with confidence intervals."),
        ("💡", "Business Insights", "Key business metrics and project summary."),
    ]

    for row_start in range(0, len(nav_cards), 4):
        row_items = nav_cards[row_start : row_start + 4]
        cols = st.columns(len(row_items), gap="medium")
        for col, (icon, title, desc) in zip(cols, row_items):
            with col:
                st.button(
                    f"Open {title}",
                    key=f"quick-nav-{title.lower().replace(' ', '-')}",
                    on_click=helpers.navigate_to_page,
                    args=(f"{icon} {title}",),
                    use_container_width=True,
                )
                st.markdown(
                    f'<div class="home-nav-card">'
                    f'<div class="home-nav-card-icon">{icon}</div>'
                    f'<div class="home-nav-card-title">{title}</div>'
                    f'<div class="home-nav-card-desc">{desc}</div>'
                    f"</div>",
                    unsafe_allow_html=True,
                )


def show() -> None:
    """Render the Home landing page with project overview and quick navigation."""

    # ── Header ──
    helpers.render_page_header(
        "🏠 Welcome to RetailPulse",
        "AI-Powered Customer Analytics & Demand Forecasting Platform",
    )

    # ── KPIs (resilient to missing files) ──
    biz = _load_business_kpis()
    proj = _load_project_kpis()

    # ── Top-level KPIs ──
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("💰 Total Revenue", formatters.currency(biz["revenue"]))
    with c2:
        st.metric("📦 Total Orders", formatters.number(biz["orders"]))
    with c3:
        st.metric("👥 Total Customers", formatters.number(biz["customers"]))
    with c4:
        st.metric("🛍 Products", formatters.number(biz["products"]))

    c5, c6, c7, c8 = st.columns(4)
    with c5:
        st.metric("🌍 Countries Served", proj["countries"])
    with c6:
        st.metric("🤖 ML Models", proj["ml_models"])
    with c7:
        st.metric("📊 Dashboard Pages", proj["pages"])
    with c8:
        st.metric("📁 Processed Datasets", proj["datasets"])

    st.divider()

    # ── Quick Navigation Cards ──
    _render_quick_navigation()

    st.divider()

    # ── Project Description ──
    _render_about_project()

    st.divider()

    # ── Tech Stack ──
    st.markdown("### 🛠 Technology Stack")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.success("**Frontend**\n\nStreamlit • Plotly")
    with c2:
        st.success("**Backend**\n\nPython • Pandas")
    with c3:
        st.success("**ML Models**\n\nScikit-learn • Prophet")
    with c4:
        st.success("**Data**\n\n779K+ Transactions")

    st.divider()
    helpers.render_footer("Home")
