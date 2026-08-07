"""Cached data loading functions for all dashboard datasets."""

import pandas as pd
import streamlit as st
from utils.constants import DATA_DIR


@st.cache_data
def load_sales() -> pd.DataFrame:
    """Load daily sales data with parsed dates."""
    df = pd.read_csv(DATA_DIR / "sales_analytics.csv")
    df["ds"] = pd.to_datetime(df["ds"])
    return df


@st.cache_data
def load_customers() -> pd.DataFrame:
    """Load customer analytics data with parsed dates."""
    df = pd.read_csv(DATA_DIR / "customer_analytics.csv")
    df["FirstPurchaseDate"] = pd.to_datetime(df["FirstPurchaseDate"])
    df["LastPurchaseDate"] = pd.to_datetime(df["LastPurchaseDate"])
    return df


@st.cache_data
def load_segmentation() -> pd.DataFrame:
    """Load customer segmentation (RFM) data."""
    return pd.read_csv(DATA_DIR / "customer_segmentation.csv")


@st.cache_data
def load_churn() -> pd.DataFrame:
    """Load customer churn predictions."""
    return pd.read_csv(DATA_DIR / "customer_churn.csv")


@st.cache_data
def load_inventory() -> pd.DataFrame:
    """Load inventory dashboard data."""
    return pd.read_csv(DATA_DIR / "inventory_dashboard.csv")


@st.cache_data
def load_country() -> pd.DataFrame:
    """Load country-level analytics."""
    return pd.read_csv(DATA_DIR / "country_analytics.csv")


@st.cache_data
def load_products() -> pd.DataFrame:
    """Load product analytics data."""
    return pd.read_csv(DATA_DIR / "product_analytics.csv")


@st.cache_data
def load_business_insights() -> pd.DataFrame:
    """Load business insights / KPI summary."""
    return pd.read_csv(DATA_DIR / "business_insights.csv")


@st.cache_data
def load_executive_overview() -> pd.DataFrame:
    """Load executive overview summary row."""
    return pd.read_csv(DATA_DIR / "executive_overview.csv")


@st.cache_data
def load_demand_forecast() -> pd.DataFrame:
    """Load demand forecasting results with parsed dates."""
    df = pd.read_csv(DATA_DIR / "demand_forecasting.csv")
    df["ds"] = pd.to_datetime(df["ds"])
    return df


@st.cache_data
def load_project_summary() -> pd.DataFrame:
    """Load project summary metrics."""
    return pd.read_csv(DATA_DIR / "project_summary.csv")
