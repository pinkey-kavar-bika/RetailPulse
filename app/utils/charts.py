"""Shared Plotly chart configuration and styling utilities."""

from __future__ import annotations

import streamlit as st
from utils.constants import CHART_MD, TEXT_PRIMARY


def styled_layout(height: int = CHART_MD, **overrides) -> dict:
    """Return a standard Plotly layout dict.

    All keyword arguments are merged on top of the defaults,
    so callers can override any property.
    """
    base: dict = {
        "height": height,
        "paper_bgcolor": "white",
        "plot_bgcolor": "white",
        "font": dict(family="Inter, sans-serif", color=TEXT_PRIMARY, size=13),
        "hoverlabel": dict(
            bgcolor="white",
            font_size=13,
            font_family="Inter, sans-serif",
            bordercolor="#E2E8F0",
        ),
        "margin": dict(l=24, r=24, t=48, b=40),
    }
    base.update(overrides)
    return base


def render(fig, height: int = CHART_MD, **layout_kwargs) -> None:
    """Apply styled layout to *fig* and render via st.plotly_chart."""
    fig.update_layout(**styled_layout(height, **layout_kwargs))
    st.plotly_chart(fig, use_container_width=True)
