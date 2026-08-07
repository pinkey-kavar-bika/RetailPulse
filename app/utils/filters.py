"""Reusable sidebar filter builders for each dashboard page.

Each function renders its filters in the sidebar and returns
a dict of filter values that the corresponding page can consume.
All filter widgets use unique keys to avoid conflicts when
switching between pages.
"""

from __future__ import annotations

import streamlit as st
import pandas as pd
from utils import load_data


def _filter_header() -> None:
    """Render the standard filter section header."""
    st.sidebar.markdown(
        '<p class="sidebar-section-label">🔍 FILTERS</p>',
        unsafe_allow_html=True,
    )


# ─── Sales Analytics ────────────────────────────────────────
def sales_filters() -> dict:
    """Render filters for Sales Analytics and return filter values."""
    _filter_header()
    sales = load_data.load_sales()

    date_min = sales["ds"].min().date()
    date_max = sales["ds"].max().date()
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(date_min, date_max),
        min_value=date_min,
        max_value=date_max,
        key="filter_sales_date",
    )

    return {"date_range": date_range}


# ─── Customer Analytics ─────────────────────────────────────
def customer_analytics_filters() -> dict:
    """Render filters for Customer Analytics."""
    _filter_header()
    customers = load_data.load_customers()

    country = st.sidebar.selectbox(
        "Country",
        ["All"] + sorted(customers["Country"].dropna().unique().tolist()),
        key="filter_ca_country",
    )
    segment = st.sidebar.selectbox(
        "Customer Segment",
        ["All"] + sorted(customers["CustomerSegment"].dropna().unique().tolist()),
        key="filter_ca_segment",
    )

    return {"country": country, "segment": segment}


# ─── Customer Segmentation ──────────────────────────────────
def segmentation_filters() -> dict:
    """Render filters for Customer Segmentation."""
    _filter_header()
    customers = load_data.load_segmentation()

    segment = st.sidebar.selectbox(
        "Customer Segment",
        ["All"] + sorted(customers["CustomerSegment"].dropna().unique().tolist()),
        key="filter_seg_segment",
    )

    return {"segment": segment}


# ─── Customer Churn ──────────────────────────────────────────
def churn_filters() -> dict:
    """Render filters for Customer Churn and return filter values."""
    _filter_header()
    churn = load_data.load_churn()

    country = st.sidebar.selectbox(
        "Country",
        ["All"] + sorted(churn["Country"].dropna().unique().tolist()),
        key="filter_churn_country",
    )
    segment = st.sidebar.selectbox(
        "Customer Segment",
        ["All"] + sorted(churn["CustomerSegment"].dropna().unique().tolist()),
        key="filter_churn_segment",
    )
    predicted = st.sidebar.selectbox(
        "Predicted Churn",
        ["All", "Churn", "No Churn"],
        key="filter_churn_predicted",
    )
    min_prob, max_prob = st.sidebar.slider(
        "Churn Probability Range (%)",
        min_value=0,
        max_value=100,
        value=(0, 100),
        step=5,
        key="filter_churn_prob",
    )

    return {
        "country": country,
        "segment": segment,
        "predicted": predicted,
        "prob_range": (min_prob, max_prob),
    }


# ─── Inventory ───────────────────────────────────────────────
def inventory_filters() -> dict:
    """Render filters for Inventory and return filter values."""
    _filter_header()
    inv = load_data.load_inventory()

    abc = st.sidebar.selectbox(
        "ABC Class",
        ["All"] + sorted(inv["ABC_Class"].dropna().unique().tolist()),
        key="filter_inv_abc",
    )
    movement = st.sidebar.selectbox(
        "Movement Category",
        ["All"] + sorted(inv["MovementCategory"].dropna().unique().tolist()),
        key="filter_inv_movement",
    )

    return {"abc_class": abc, "movement": movement}


# ─── Country Analysis ────────────────────────────────────────
def country_filters() -> dict:
    """Render filters for Country Analysis and return filter values."""
    _filter_header()
    country_df = load_data.load_country()

    country = st.sidebar.selectbox(
        "Country",
        ["All"] + sorted(country_df["Country"].dropna().unique().tolist()),
        key="filter_country_country",
    )

    return {"country": country}


# ─── Product Analytics ───────────────────────────────────────
def product_filters() -> dict:
    """Render filters for Product Analytics."""
    _filter_header()
    products = load_data.load_products()

    min_rev = float(products["TotalRevenue"].min())
    max_rev = float(products["TotalRevenue"].max())
    rev_range = st.sidebar.slider(
        "Revenue Range ($)",
        min_value=min_rev,
        max_value=max_rev,
        value=(min_rev, max_rev),
        key="filter_prod_rev",
    )

    return {"revenue_range": rev_range}
