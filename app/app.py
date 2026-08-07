"""RetailPulse — AI-Powered Customer Analytics & Demand Forecasting."""

import streamlit as st

# ──────────────────────────────────────────────────────────────
# PAGE CONFIG (must be the first Streamlit call)
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RetailPulse",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────
# IMPORTS — pages
# ──────────────────────────────────────────────────────────────
from pages import (  # noqa: E402
    home,
    executive_overview,
    sales_analytics,
    customer_analytics,
    customer_segmentation,
    customer_churn,
    inventory,
    country_analysis,
    product_analytics,
    demand_forecast,
    business_insights,
)
from utils import filters, helpers  # noqa: E402

# ──────────────────────────────────────────────────────────────
# LOAD GLOBAL CSS
# ──────────────────────────────────────────────────────────────
helpers.load_css()

# ──────────────────────────────────────────────────────────────
# PAGE REGISTRY — single source of truth for navigation
# ──────────────────────────────────────────────────────────────
PAGES: dict[str, object] = {
    "🏠 Home": home,
    "📊 Executive Dashboard": executive_overview,
    "📈 Sales Analytics": sales_analytics,
    "👥 Customer Analytics": customer_analytics,
    "🎯 Customer Segmentation": customer_segmentation,
    "⚠ Customer Churn": customer_churn,
    "📦 Inventory": inventory,
    "🌍 Country Analysis": country_analysis,
    "🛍 Product Analytics": product_analytics,
    "📅 Demand Forecast": demand_forecast,
    "💡 Business Insights": business_insights,
}

# ──────────────────────────────────────────────────────────────
# FILTER REGISTRY — maps page key to its sidebar filter function
# Pages not listed here have no filters (sidebar stays clean).
# ──────────────────────────────────────────────────────────────
PAGE_LAYOUT: dict[str, tuple[str, str, str]] = {
    "🏠 Home": ("🏠 Welcome to RetailPulse", "AI-Powered Customer Analytics & Demand Forecasting Platform", "Home"),
    "📊 Executive Dashboard": ("📊 Executive Dashboard", "A high-level view of retail performance, customer segments, and growth.", "Executive Dashboard"),
    "📈 Sales Analytics": ("📈 Sales Analytics", "Analyze revenue trends and overall sales performance.", "Sales Analytics"),
    "👥 Customer Analytics": ("👥 Customer Analytics", "Understand customer behaviour, value, and purchasing patterns.", "Customer Analytics"),
    "🎯 Customer Segmentation": ("🎯 Customer Segmentation", "Explore RFM segments and customer clusters.", "Customer Segmentation"),
    "⚠ Customer Churn": ("⚠ Customer Churn", "Identify churn risk and prioritize customer-retention actions.", "Customer Churn"),
    "📦 Inventory": ("📦 Inventory Dashboard", "Monitor inventory performance, product movement and stock value.", "Inventory Dashboard"),
    "🌍 Country Analysis": ("🌍 Country Analysis", "Analyze country-wise sales performance, customers and revenue contribution.", "Country Analysis"),
    "🛍 Product Analytics": ("🛍 Product Analytics", "Analyze product performance, revenue contribution, and pricing.", "Product Analytics"),
    "📅 Demand Forecast": ("📅 Demand Forecast", "AI-powered demand forecasting with confidence intervals.", "Demand Forecast"),
    "💡 Business Insights": ("💡 Business Insights", "Key business metrics and project summary.", "Business Insights"),
}

# Maps page keys to filter builders; the shared shell is defined above.
FILTER_REGISTRY: dict[str, callable] = {
    "📈 Sales Analytics": filters.sales_filters,
    "👥 Customer Analytics": filters.customer_analytics_filters,
    "🎯 Customer Segmentation": filters.segmentation_filters,
    "⚠ Customer Churn": filters.churn_filters,
    "📦 Inventory": filters.inventory_filters,
    "🌍 Country Analysis": filters.country_filters,
    "🛍 Product Analytics": filters.product_filters,
}

# ──────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────
with st.sidebar:
    # ── Logo / Brand ──
    st.markdown(
        '<div class="sidebar-brand">'
        '<div class="sidebar-brand-icon">🛒</div>'
        '<div class="sidebar-brand-name">RetailPulse</div>'
        '<div class="sidebar-brand-tagline">Analytics Dashboard</div>'
        "</div>",
        unsafe_allow_html=True,
    )

    st.divider()

    # ── Navigation ──
    st.markdown(
        '<p class="sidebar-section-label">NAVIGATION</p>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        list(PAGES.keys()),
        label_visibility="collapsed",
        key=helpers.NAVIGATION_STATE_KEY,
    )

    # ── Dynamic Filters ──
    # Only rendered when the active page has a registered filter function.
    filter_values: dict = {}
    if page in FILTER_REGISTRY:
        st.divider()
        filter_values = FILTER_REGISTRY[page]()

# ──────────────────────────────────────────────────────────────
# RENDER SELECTED PAGE
# ──────────────────────────────────────────────────────────────
# Pages with filters receive them; others are called with no args.
if filter_values:
    render_body = lambda: PAGES[page].show(filter_values)
else:
    render_body = lambda: PAGES[page].show()

title, subtitle, footer = PAGE_LAYOUT[page]
helpers.render_page_template(title, subtitle, footer, render_body)
