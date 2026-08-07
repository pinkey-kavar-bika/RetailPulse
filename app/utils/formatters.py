"""Number and currency formatting utilities."""

from __future__ import annotations


def currency(value: float, decimals: int = 0) -> str:
    """Format *value* as $X,XXX with *decimals* decimal places."""
    return f"${value:,.{decimals}f}"


def number(value: int | float) -> str:
    """Format *value* with thousands separators."""
    if isinstance(value, float) and value == int(value):
        return f"{int(value):,}"
    return f"{value:,}"


def percent(value: float, decimals: int = 1) -> str:
    """Format *value* as X.X%."""
    return f"{value:.{decimals}f}%"
