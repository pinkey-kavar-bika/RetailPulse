"""Application-wide constants for RetailPulse dashboard."""

from pathlib import Path

# ─── Data Paths ───────────────────────────────────────────────
DATA_DIR = Path("data/dashboard")

# ─── Color Palette ────────────────────────────────────────────
PRIMARY = "#4F46E5"
PRIMARY_DARK = "#312E81"
SECONDARY = "#6366F1"
ACCENT_GREEN = "#10B981"
ACCENT_AMBER = "#F59E0B"
ACCENT_RED = "#EF4444"
ACCENT_PURPLE = "#8B5CF6"
ACCENT_CYAN = "#06B6D4"

TEXT_PRIMARY = "#1E293B"
TEXT_SECONDARY = "#64748B"
BG_PAGE = "#F8FAFC"
BG_CARD = "#FFFFFF"

# ─── Color Sequences ─────────────────────────────────────────
COLORS_CATEGORICAL = [
    "#4F46E5", "#10B981", "#F59E0B", "#EF4444",
    "#8B5CF6", "#06B6D4", "#EC4899", "#14B8A6",
]

COLORS_SEGMENT = {
    "VIP Customers": "#4F46E5",
    "Loyal Customers": "#10B981",
    "Regular Customers": "#F59E0B",
    "At-Risk Customers": "#EF4444",
}

COLORS_RISK = {
    "Low Risk": "#10B981",
    "Medium Risk": "#F59E0B",
    "High Risk": "#EF4444",
}

COLORS_CHURN = {
    "Retained": "#10B981",
    "Churn": "#EF4444",
    "Churned": "#EF4444",
}

# ─── Chart Dimensions ────────────────────────────────────────
CHART_SM = 420
CHART_MD = 480
CHART_LG = 550

# ─── App Info ─────────────────────────────────────────────────
APP_NAME = "RetailPulse"
APP_ICON = "📊"
APP_TAGLINE = "AI-Powered Customer Analytics & Demand Forecasting"
