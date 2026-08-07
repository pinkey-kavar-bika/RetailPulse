import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data, charts, helpers, formatters
from utils.constants import *

def show(filter_values: dict | None = None) -> None:
    # =====================================================
    # LOAD DATA
    # =====================================================
    churn = load_data.load_churn()

    churn["ChurnStatus"] = churn["PredictedChurn"].map({
        1: "Churn",
        0: "Retained"
    })
    churn["ChurnProbabilityPct"] = churn["ChurnProbability"] * 100
    churn["RiskBand"] = pd.cut(
        churn["ChurnProbabilityPct"],
        bins=[-0.01, 40, 70, 100],
        labels=["Low Risk", "Medium Risk", "High Risk"]
    )

    # =====================================================
    # APPLY FILTERS (from centralized sidebar)
    # =====================================================
    filtered = churn.copy()

    if filter_values:
        selected_country = filter_values.get("country", "All")
        selected_segment = filter_values.get("segment", "All")
        selected_churn = filter_values.get("predicted", "All")
        prob_range = filter_values.get("prob_range", (0, 100))

        if selected_country != "All":
            filtered = filtered[filtered["Country"] == selected_country]
        if selected_segment != "All":
            filtered = filtered[filtered["CustomerSegment"] == selected_segment]
        if selected_churn == "Churn":
            filtered = filtered[filtered["PredictedChurn"] == 1]
        elif selected_churn == "No Churn":
            filtered = filtered[filtered["PredictedChurn"] == 0]
        filtered = filtered[
            (filtered["ChurnProbabilityPct"] >= prob_range[0])
            & (filtered["ChurnProbabilityPct"] <= prob_range[1])
        ]

    # =====================================================
    # HEADER
    # =====================================================
    helpers.render_page_header(
        "⚠ Customer Churn Analysis",
        "Monitor customer churn risk and identify customers requiring attention."
    )

    # =====================================================
    # KPI VALUES
    # =====================================================
    total_customers = filtered["CustomerID"].nunique()
    churn_customers = (filtered["PredictedChurn"] == 1).sum()
    retained_customers = (filtered["PredictedChurn"] == 0).sum()
    
    avg_probability = (
        filtered["ChurnProbability"].mean() * 100
        if not filtered.empty else 0
    )
    churn_rate = (
        churn_customers / total_customers * 100
        if total_customers > 0 else 0
    )
    high_risk_count = (
        filtered["RiskBand"] == "High Risk"
    ).sum() if not filtered.empty else 0

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric("Total Customers", formatters.number(total_customers))
    with c2:
        st.metric("Churn Rate", formatters.percent(churn_rate))
    with c3:
        st.metric("Likely to Churn", formatters.number(churn_customers))
    with c4:
        st.metric("Avg Churn Probability", formatters.percent(avg_probability))
    with c5:
        st.metric("High Risk Customers", formatters.number(high_risk_count))

    st.divider()

    if filtered.empty:
        st.warning("No customers match the selected filters. Adjust the filters to view churn analytics.")
        st.download_button(
            "📥 Download Customer Churn Report",
            data=filtered.to_csv(index=False),
            file_name="customer_churn_report.csv",
            mime="text/csv",
            key="btn_dl_empty"
        )
        st.divider()
        helpers.render_footer("Customer Churn Dashboard")
        return

    # =====================================================
    # ROW 1: CHURN SPLIT + RISK DISTRIBUTION
    # =====================================================
    left, right = st.columns(2)

    with left:
        st.subheader("📊 Churn vs Retained Breakdown")
        churn_order = ["Retained", "Churn"]
        churn_summary = (
            filtered["ChurnStatus"]
            .value_counts()
            .reindex(churn_order, fill_value=0)
            .rename_axis("Status")
            .reset_index(name="Customers")
        )
        churn_summary["Percent"] = (
            (churn_summary["Customers"] / total_customers * 100).round(2)
            if total_customers > 0 else 0
        )
        num_statuses = (churn_summary["Customers"] > 0).sum()

        if num_statuses >= 2:
            fig = go.Figure(data=[go.Pie(
                labels=churn_summary["Status"],
                values=churn_summary["Customers"],
                hole=0.55,
                marker=dict(colors=[ACCENT_GREEN, ACCENT_RED]),
                textinfo="label+percent",
                textposition="outside",
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Customers: %{value:,}<br>"
                    "Share: %{percent}<extra></extra>"
                )
            )])
            fig.update_layout(**charts.styled_layout(
                height=CHART_SM,
                title="Predicted Churn Split",
                annotations=[dict(
                    text=f"{churn_rate:.1f}%<br>Churn",
                    x=0.5, y=0.5,
                    font=dict(size=18, color=PRIMARY_DARK),
                    showarrow=False
                )],
                showlegend=True,
                legend=dict(orientation="h", y=-0.05),
                margin=dict(l=20, r=20, t=60, b=60)
            ))
        else:
            status_label = churn_summary.loc[
                churn_summary["Customers"] > 0, "Status"
            ].iloc[0]
            fig = go.Figure(data=[go.Indicator(
                mode="number+delta",
                value=churn_summary.loc[
                    churn_summary["Customers"] > 0, "Customers"
                ].iloc[0],
                title=dict(
                    text=f"All filtered customers are: <b>{status_label}</b>"
                ),
                number=dict(font=dict(size=52, color=PRIMARY_DARK)),
            )])
            fig.update_layout(**charts.styled_layout(
                height=CHART_SM,
                margin=dict(l=20, r=20, t=60, b=40)
            ))

        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("📈 Risk Band Distribution")
        risk_order = ["Low Risk", "Medium Risk", "High Risk"]
        risk_summary = (
            filtered["RiskBand"]
            .value_counts()
            .reindex(risk_order, fill_value=0)
            .rename_axis("RiskBand")
            .reset_index(name="Customers")
        )
        risk_summary["Percent"] = (
            (risk_summary["Customers"] / total_customers * 100).round(2)
            if total_customers > 0 else 0
        )
        non_empty_bands = (risk_summary["Customers"] > 0).sum()

        if non_empty_bands >= 2:
            fig = px.bar(
                risk_summary[risk_summary["Customers"] > 0],
                x="RiskBand",
                y="Customers",
                text="Customers",
                color="RiskBand",
                category_orders={"RiskBand": risk_order},
                color_discrete_map={
                    "Low Risk": ACCENT_GREEN,
                    "Medium Risk": ACCENT_AMBER,
                    "High Risk": ACCENT_RED
                },
                hover_data={
                    "RiskBand": True,
                    "Customers": ":,",
                    "Percent": ":.1f"
                }
            )
            fig.update_traces(
                texttemplate="%{y:,} (%{customdata[1]:.1f}%)",
                textposition="outside",
                cliponaxis=False,
                customdata=risk_summary[risk_summary["Customers"] > 0][["RiskBand", "Percent"]].values
            )
        else:
            band_label = risk_summary.loc[
                risk_summary["Customers"] > 0, "RiskBand"
            ].iloc[0] if non_empty_bands > 0 else "N/A"
            band_count = risk_summary.loc[
                risk_summary["Customers"] > 0, "Customers"
            ].iloc[0] if non_empty_bands > 0 else 0

            fig = go.Figure(data=[go.Indicator(
                mode="number",
                value=band_count,
                title=dict(
                    text=f"All filtered customers fall in: <b>{band_label}</b>"
                ),
                number=dict(font=dict(size=52, color=PRIMARY_DARK)),
            )])

        fig.update_layout(**charts.styled_layout(
            height=CHART_SM,
            title="Customers by Churn Probability Band",
            xaxis_title="Risk Band",
            yaxis_title="Customers",
            showlegend=False,
            margin=dict(l=20, r=40, t=60, b=40)
        ))

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # =====================================================
    # ROW 2: PROBABILITY HISTOGRAM + VIOLIN BY SEGMENT
    # =====================================================
    left, right = st.columns(2)

    with left:
        st.subheader("📉 Churn Probability Distribution")
        fig = px.histogram(
            filtered,
            x="ChurnProbabilityPct",
            nbins=25,
            color="ChurnStatus",
            category_orders={"ChurnStatus": churn_order},
            color_discrete_map={
                "Churn": ACCENT_RED,
                "Retained": ACCENT_GREEN
            },
            marginal="rug",
            labels={"ChurnProbabilityPct": "Churn Probability (%)"}
        )
        fig.add_vline(
            x=70,
            line_dash="dash",
            line_color=ACCENT_RED,
            annotation_text="High-risk threshold (70%)",
            annotation_position="top right"
        )
        fig.update_layout(**charts.styled_layout(
            height=CHART_MD,
            title="Distribution of Predicted Churn Probability",
            xaxis_title="Churn Probability (%)",
            yaxis_title="Number of Customers",
            legend_title_text="Predicted Status",
            bargap=0.05,
            margin=dict(l=20, r=30, t=70, b=40)
        ))
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("🎻 Probability Spread by Segment")
        segments_in_data = filtered["CustomerSegment"].nunique()
        if segments_in_data >= 2:
            fig = px.violin(
                filtered,
                x="CustomerSegment",
                y="ChurnProbabilityPct",
                color="CustomerSegment",
                box=True,
                points="outliers",
                color_discrete_sequence=[PRIMARY, ACCENT_RED, ACCENT_GREEN, ACCENT_AMBER],
                labels={
                    "ChurnProbabilityPct": "Churn Probability (%)",
                    "CustomerSegment": "Segment"
                }
            )
        else:
            fig = px.box(
                filtered,
                x="CustomerSegment",
                y="ChurnProbabilityPct",
                color="CustomerSegment",
                points="all",
                color_discrete_sequence=[PRIMARY],
                labels={
                    "ChurnProbabilityPct": "Churn Probability (%)",
                    "CustomerSegment": "Segment"
                }
            )
        fig.update_layout(**charts.styled_layout(
            height=CHART_MD,
            title="Churn Probability Distribution by Segment",
            xaxis_title="Customer Segment",
            yaxis_title="Churn Probability (%)",
            showlegend=False,
            margin=dict(l=20, r=30, t=70, b=80)
        ))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # =====================================================
    # ROW 3: COUNTRY CHURN RATE + SEGMENT CHURN ANALYSIS
    # =====================================================
    left, right = st.columns(2)

    with left:
        st.subheader("🌍 Country-wise Churn Rate")
        country_churn = (
            filtered
            .groupby("Country")
            .agg(
                Customers=("CustomerID", "nunique"),
                Churned=("PredictedChurn", "sum"),
                AvgProbability=("ChurnProbabilityPct", "mean")
            )
            .reset_index()
        )
        country_churn["ChurnRate"] = (
            country_churn["Churned"] / country_churn["Customers"] * 100
        )
        country_churn["Retained"] = (
            country_churn["Customers"] - country_churn["Churned"]
        )
        MIN_CUSTOMERS = 5
        country_significant = country_churn[
            country_churn["Customers"] >= MIN_CUSTOMERS
        ].copy()

        if len(country_significant) >= 2:
            country_significant = country_significant.sort_values(
                "ChurnRate", ascending=True
            ).tail(15)
            fig = px.bar(
                country_significant,
                x="ChurnRate",
                y="Country",
                orientation="h",
                text="ChurnRate",
                color="ChurnRate",
                color_continuous_scale="RdYlGn_r",
                hover_data={
                    "Country": True,
                    "ChurnRate": ":.1f",
                    "Customers": ":,",
                    "Churned": ":,",
                    "Retained": ":,",
                    "AvgProbability": ":.1f"
                }
            )
            fig.update_traces(
                texttemplate="%{x:.1f}% (n=%{customdata[1]:,})",
                textposition="outside",
                cliponaxis=False,
                customdata=country_significant[["Country", "Customers"]].values
            )
            fig.update_layout(**charts.styled_layout(
                height=CHART_LG,
                title=f"Top Countries by Churn Rate (min {MIN_CUSTOMERS} customers)",
                yaxis=dict(categoryorder="total ascending"),
                xaxis_title="Churn Rate (%)",
                yaxis_title="",
                coloraxis_showscale=False,
                margin=dict(l=20, r=80, t=70, b=40)
            ))
        elif len(country_significant) == 1:
            row = country_significant.iloc[0]
            fig = go.Figure(data=[go.Indicator(
                mode="number+delta",
                value=row["ChurnRate"],
                number=dict(suffix="%", font=dict(size=52, color=PRIMARY_DARK)),
                title=dict(text=f"Churn Rate — {row['Country']}"),
                delta=dict(
                    reference=50,
                    suffix="%",
                    relative=False,
                    increasing=dict(color=ACCENT_RED),
                    decreasing=dict(color=ACCENT_GREEN)
                )
            )])
            fig.update_layout(**charts.styled_layout(
                height=CHART_LG,
                margin=dict(l=20, r=20, t=70, b=40)
            ))
        else:
            small_countries = country_churn.sort_values(
                "ChurnRate", ascending=True
            ).tail(10)
            fig = px.bar(
                small_countries,
                x="ChurnRate",
                y="Country",
                orientation="h",
                text="ChurnRate",
                color="Customers",
                color_continuous_scale="Blues",
                hover_data={
                    "Country": True,
                    "ChurnRate": ":.1f",
                    "Customers": ":,",
                    "Churned": ":,"
                }
            )
            fig.update_traces(
                texttemplate="%{x:.1f}%",
                textposition="outside",
                cliponaxis=False
            )
            fig.update_layout(**charts.styled_layout(
                height=CHART_LG,
                title="Churn Rate by Country (⚠ small sample sizes)",
                yaxis=dict(categoryorder="total ascending"),
                xaxis_title="Churn Rate (%)",
                yaxis_title="",
                coloraxis_colorbar=dict(title="Customers"),
                margin=dict(l=20, r=60, t=70, b=40)
            ))

        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("👥 Segment Churn Analysis")
        segment_churn = (
            filtered
            .groupby("CustomerSegment")
            .agg(
                Customers=("CustomerID", "nunique"),
                Churned=("PredictedChurn", "sum"),
                AvgProbability=("ChurnProbabilityPct", "mean")
            )
            .reset_index()
        )
        segment_churn["ChurnRate"] = (
            segment_churn["Churned"] / segment_churn["Customers"] * 100
        )
        segment_churn["RetainedCount"] = (
            segment_churn["Customers"] - segment_churn["Churned"]
        )
        segment_order = ["VIP Customers", "Loyal Customers",
                         "Regular Customers", "At-Risk Customers"]
        segment_churn["CustomerSegment"] = pd.Categorical(
            segment_churn["CustomerSegment"],
            categories=segment_order,
            ordered=True
        )
        segment_churn = segment_churn.sort_values("CustomerSegment")
        num_segments = len(segment_churn)

        if num_segments >= 2:
            seg_melted = segment_churn.melt(
                id_vars=["CustomerSegment", "Customers"],
                value_vars=["Churned", "RetainedCount"],
                var_name="Status",
                value_name="Count"
            )
            seg_melted["Status"] = seg_melted["Status"].map({
                "Churned": "Churned",
                "RetainedCount": "Retained"
            })
            fig = px.bar(
                seg_melted,
                x="CustomerSegment",
                y="Count",
                color="Status",
                barmode="stack",
                text="Count",
                color_discrete_map={
                    "Churned": ACCENT_RED,
                    "Retained": ACCENT_GREEN
                },
                labels={
                    "CustomerSegment": "Segment",
                    "Count": "Customers"
                },
                hover_data={
                    "CustomerSegment": True,
                    "Count": ":,",
                    "Status": True
                }
            )
            fig.update_traces(
                texttemplate="%{y:,}",
                textposition="inside",
                cliponaxis=False
            )
            for _, row in segment_churn.iterrows():
                fig.add_annotation(
                    x=row["CustomerSegment"],
                    y=row["Customers"],
                    text=f"{row['ChurnRate']:.1f}%",
                    showarrow=False,
                    yshift=12,
                    font=dict(size=12, color=PRIMARY_DARK, weight="bold")
                )
        else:
            row = segment_churn.iloc[0]
            fig = go.Figure(data=[go.Indicator(
                mode="number",
                value=row["ChurnRate"],
                number=dict(suffix="%", font=dict(size=52, color=PRIMARY_DARK)),
                title=dict(
                    text=f"Churn Rate — {row['CustomerSegment']}<br>"
                         f"<span style='font-size:14px;color:#64748B'>"
                         f"{int(row['Churned'])} churned / "
                         f"{int(row['Customers'])} total</span>"
                )
            )])

        fig.update_layout(**charts.styled_layout(
            height=CHART_LG,
            title="Churn Composition by Segment (% labels = churn rate)",
            xaxis_title="Customer Segment",
            yaxis_title="Number of Customers",
            legend=dict(orientation="h", y=-0.15),
            margin=dict(l=20, r=30, t=70, b=80)
        ))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # =====================================================
    # ROW 4: HEATMAP + RETENTION PRIORITY SCATTER
    # =====================================================
    left, right = st.columns(2)

    with left:
        st.subheader("🔥 Avg Churn Probability Heatmap")
        heatmap_data = (
            filtered
            .groupby(["Country", "CustomerSegment"])
            ["ChurnProbabilityPct"]
            .mean()
            .reset_index()
        )
        country_totals = filtered.groupby("Country")["CustomerID"].nunique()
        top_countries = country_totals.nlargest(12).index.tolist()
        heatmap_data = heatmap_data[
            heatmap_data["Country"].isin(top_countries)
        ]

        if len(heatmap_data) > 0:
            heatmap_pivot = heatmap_data.pivot_table(
                index="Country",
                columns="CustomerSegment",
                values="ChurnProbabilityPct",
                aggfunc="mean"
            )
            country_avg = heatmap_pivot.mean(axis=1).sort_values(ascending=True)
            heatmap_pivot = heatmap_pivot.reindex(country_avg.index)

            fig = px.imshow(
                heatmap_pivot.round(1),
                text_auto=".1f",
                color_continuous_scale="RdYlGn_r",
                aspect="auto",
                labels=dict(
                    x="Segment",
                    y="Country",
                    color="Avg Prob (%)"
                )
            )
            fig.update_layout(**charts.styled_layout(
                height=CHART_LG,
                title="Avg Churn Probability (%) — Country × Segment",
                margin=dict(l=20, r=30, t=70, b=60)
            ))
        else:
            fig = go.Figure()
            fig.add_annotation(
                text="Insufficient data for heatmap",
                x=0.5, y=0.5, xref="paper", yref="paper",
                showarrow=False, font=dict(size=16, color=TEXT_SECONDARY)
            )
            fig.update_layout(**charts.styled_layout(height=CHART_LG))

        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("🎯 Retention Priority Matrix")
        country_priority = (
            filtered
            .groupby("Country")
            .agg(
                Customers=("CustomerID", "nunique"),
                ChurnRate=("PredictedChurn", "mean"),
                AvgProbability=("ChurnProbabilityPct", "mean")
            )
            .reset_index()
        )
        country_priority["ChurnRate"] = country_priority["ChurnRate"] * 100
        country_priority = country_priority[
            country_priority["Customers"] >= 3
        ]

        if len(country_priority) >= 3:
            fig = px.scatter(
                country_priority,
                x="AvgProbability",
                y="ChurnRate",
                size="Customers",
                color="AvgProbability",
                color_continuous_scale="RdYlGn_r",
                text="Country",
                size_max=50,
                hover_data={
                    "Country": True,
                    "Customers": ":,",
                    "ChurnRate": ":.1f",
                    "AvgProbability": ":.1f"
                },
                labels={
                    "AvgProbability": "Avg Churn Probability (%)",
                    "ChurnRate": "Churn Rate (%)"
                }
            )
            fig.update_traces(
                textposition="top center",
                textfont=dict(size=9)
            )
            median_prob = country_priority["AvgProbability"].median()
            median_rate = country_priority["ChurnRate"].median()
            fig.add_hline(
                y=median_rate, line_dash="dot",
                line_color="#94A3B8",
                annotation_text="Median churn rate",
                annotation_position="top left"
            )
            fig.add_vline(
                x=median_prob, line_dash="dot",
                line_color="#94A3B8",
                annotation_text="Median probability",
                annotation_position="top right"
            )
            fig.update_layout(**charts.styled_layout(
                height=CHART_LG,
                title="Countries by Churn Rate vs Avg Probability (bubble = customer count)",
                coloraxis_showscale=False,
                margin=dict(l=20, r=30, t=70, b=40)
            ))
        else:
            fig = go.Figure()
            fig.add_annotation(
                text="Need at least 3 countries with 3+ customers for scatter view",
                x=0.5, y=0.5, xref="paper", yref="paper",
                showarrow=False, font=dict(size=14, color=TEXT_SECONDARY)
            )
            fig.update_layout(**charts.styled_layout(
                height=CHART_LG,
                title="Retention Priority Matrix"
            ))

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # =====================================================
    # ROW 5: TOP HIGH-RISK CUSTOMERS + SEGMENT DONUT
    # =====================================================
    left, right = st.columns([3, 2])

    with left:
        st.subheader("🔥 Top 15 Highest-Risk Customers")
        high_risk = (
            filtered
            .sort_values("ChurnProbability", ascending=False)
            .head(15)
        )
        high_risk_display = high_risk[
            ["CustomerID", "Country", "CustomerSegment",
             "ChurnProbabilityPct", "ChurnStatus"]
        ].copy()
        high_risk_display["CustomerID"] = (
            high_risk_display["CustomerID"].astype("Int64").astype(str)
        )
        fig = px.bar(
            high_risk_display,
            x="ChurnProbabilityPct",
            y="CustomerID",
            orientation="h",
            text="ChurnProbabilityPct",
            color="CustomerSegment",
            color_discrete_map={
                "At-Risk Customers": ACCENT_RED,
                "Regular Customers": ACCENT_AMBER,
                "Loyal Customers": ACCENT_GREEN,
                "VIP Customers": PRIMARY
            },
            hover_data={
                "Country": True,
                "CustomerSegment": True,
                "ChurnProbabilityPct": ":.1f",
                "ChurnStatus": True
            },
            labels={
                "ChurnProbabilityPct": "Churn Probability (%)",
                "CustomerID": "Customer ID"
            }
        )
        fig.update_traces(
            texttemplate="%{x:.1f}%",
            textposition="outside",
            cliponaxis=False
        )
        fig.update_layout(**charts.styled_layout(
            height=CHART_LG,
            title="Highest Churn Probability Customers Requiring Retention Action",
            xaxis_title="Churn Probability (%)",
            yaxis_title="Customer ID",
            yaxis=dict(categoryorder="total ascending"),
            legend=dict(
                title="Segment",
                orientation="h",
                y=-0.12
            ),
            margin=dict(l=20, r=60, t=70, b=80)
        ))
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("🧩 Customer Segment Mix")
        segment_counts = (
            filtered["CustomerSegment"]
            .value_counts()
            .reset_index()
        )
        segment_counts.columns = ["Segment", "Count"]
        segment_counts["Percent"] = (
            segment_counts["Count"] / segment_counts["Count"].sum() * 100
        ).round(1)
        fig = go.Figure(data=[go.Pie(
            labels=segment_counts["Segment"],
            values=segment_counts["Count"],
            hole=0.5,
            marker=dict(colors=[PRIMARY, ACCENT_RED, ACCENT_GREEN, ACCENT_AMBER]),
            textinfo="label+percent",
            textposition="outside",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Customers: %{value:,}<br>"
                "Share: %{percent}<extra></extra>"
            )
        )])
        fig.update_layout(**charts.styled_layout(
            height=CHART_LG,
            title="Segment Composition (Filtered)",
            showlegend=False,
            margin=dict(l=10, r=10, t=60, b=40)
        ))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # =====================================================
    # HIGH RISK CUSTOMER TABLE
    # =====================================================
    st.subheader("📋 Customer Detail Table")
    table_data = filtered[
        ["CustomerID", "Country", "CustomerSegment",
         "PredictedChurn", "ChurnProbability", "RiskBand"]
    ].copy()
    table_data["ChurnProbability"] = (
        table_data["ChurnProbability"] * 100
    ).round(2)
    table_data["PredictedChurn"] = (
        table_data["PredictedChurn"].map({
            1: "Churn",
            0: "Retained"
        })
    )
    table_data = table_data.sort_values(
        "ChurnProbability",
        ascending=False
    )
    table_data.columns = [
        "Customer ID", "Country", "Segment",
        "Prediction", "Churn Prob (%)", "Risk Band"
    ]
    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True,
        height=400
    )

    st.divider()

    # =====================================================
    # BUSINESS INSIGHTS
    # =====================================================
    highest_risk = filtered.loc[
        filtered["ChurnProbability"].idxmax()
    ]
    lowest_risk = filtered.loc[
        filtered["ChurnProbability"].idxmin()
    ]
    c1, c2 = st.columns(2)

    with c1:
        st.success(f"""
### 🎯 Highest Churn Risk
Customer ID
**{highest_risk['CustomerID']:.0f}**
Country
**{highest_risk['Country']}**
Segment
**{highest_risk['CustomerSegment']}**
Probability
**{highest_risk['ChurnProbability']*100:.2f}%**
""")
    with c2:
        st.info(f"""
### ✅ Lowest Churn Risk
Customer ID
**{lowest_risk['CustomerID']:.0f}**
Country
**{lowest_risk['Country']}**
Segment
**{lowest_risk['CustomerSegment']}**
Probability
**{lowest_risk['ChurnProbability']*100:.2f}%**
""")

    st.divider()

    # =====================================================
    # DOWNLOAD REPORT
    # =====================================================
    st.download_button(
        "📥 Download Customer Churn Report",
        data=filtered.to_csv(index=False),
        file_name="customer_churn_report.csv",
        mime="text/csv",
        key="btn_dl_main"
    )

    st.divider()

    # =====================================================
    # EXECUTIVE SUMMARY
    # =====================================================
    st.subheader("📌 Executive Summary")

    top_churn_country = ""
    if len(country_churn[country_churn["Customers"] >= MIN_CUSTOMERS]) > 0:
        top_row = (
            country_churn[country_churn["Customers"] >= MIN_CUSTOMERS]
            .sort_values("ChurnRate", ascending=False)
            .iloc[0]
        )
        top_churn_country = (
            f"• Highest churn-rate country (≥{MIN_CUSTOMERS} customers) : "
            f"**{top_row['Country']}** at **{top_row['ChurnRate']:.1f}%** "
            f"({int(top_row['Churned'])} of {int(top_row['Customers'])})"
        )

    at_risk_segment = segment_churn[
        segment_churn["CustomerSegment"] == "At-Risk Customers"
    ]
    at_risk_note = ""
    if len(at_risk_segment) > 0:
        ar = at_risk_segment.iloc[0]
        at_risk_note = (
            f"• At-Risk segment : **{int(ar['Customers'])}** customers "
            f"with **{ar['ChurnRate']:.1f}%** churn rate and "
            f"**{ar['AvgProbability']:.1f}%** avg probability"
        )

    st.success(f"""
### Churn Analysis Summary
• Total Customers Analysed : **{total_customers:,}**
• Predicted Churn Rate : **{churn_rate:.1f}%**
• Average Churn Probability : **{avg_probability:.1f}%**
• High Risk Customers (>70% probability) : **{high_risk_count:,}**
{top_churn_country}
{at_risk_note}
• Dashboard enables proactive customer retention strategies.
""")

    st.divider()
    helpers.render_footer("Customer Churn Dashboard")
