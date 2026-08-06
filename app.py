# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px
# import plotly.graph_objects as go
# from pathlib import Path

# # -----------------------------
# # Page Config
# # -----------------------------

# st.set_page_config(
#     page_title="Business Analytics Dashboard",
#     page_icon="📊",
#     layout="wide"
# )

# # -----------------------------
# # Custom CSS
# # -----------------------------

# st.markdown("""
# <style>

# .main{
# background-color:#f5f7fa;
# }

# h1,h2,h3{
# color:#003366;
# }

# .metric-card{
# padding:20px;
# border-radius:12px;
# background:white;
# box-shadow:0px 2px 10px rgba(0,0,0,0.1);
# text-align:center;
# }

# .sidebar .sidebar-content{
# background:#003366;
# }

# </style>

# """,unsafe_allow_html=True)

# # -----------------------------
# # Title
# # -----------------------------

# st.title("📊 Business Analytics Dashboard")

# st.markdown("### Executive Insights & Business Performance")

# # -----------------------------
# # Load Data
# # -----------------------------

# BASE=Path("data/dashboard")

# @st.cache_data
# def load_data():

#     data={}

#     files=[
#         "executive_overview.csv",
#         "sales_analytics.csv",
#         "customer_analytics.csv",
#         "customer_segmentation.csv",
#         "customer_churn.csv",
#         "inventory_dashboard.csv",
#         "country_analytics.csv",
#         "product_analytics.csv",
#         "business_insights.csv",
#         "demand_forecasting.csv"
#     ]

#     for file in files:

#         path=BASE/file

#         try:
#             data[file]=pd.read_csv(path)

#         except:

#             data[file]=pd.DataFrame()

#     return data

# data=load_data()

# # -----------------------------
# # Sidebar
# # -----------------------------

# st.sidebar.image(
# "https://img.icons8.com/color/96/combo-chart--v1.png",
# width=90
# )

# st.sidebar.title("Navigation")

# page=st.sidebar.radio(

# "Select Dashboard",

# [
# "Executive Overview",
# "Sales Analytics",
# "Customer Analytics",
# "Customer Segmentation",
# "Customer Churn",
# "Inventory",
# "Country Analysis",
# "Products",
# "Demand Forecast",
# "Business Insights"
# ]

# )


# # -----------------------------
# # Executive Overview
# # -----------------------------

# if page=="Executive Overview":

#     df=data["executive_overview.csv"]

#     st.header("Executive Dashboard")

#     if df.empty:

#         st.warning("executive_overview.csv not found")

#     else:

#         st.dataframe(df.head())

#         numeric=df.select_dtypes(include=np.number)

#         c1,c2,c3,c4=st.columns(4)

#         with c1:

#             st.metric(
#                 "Total Revenue",
#                  f"${df['TotalRevenue'].iloc[0]:,.0f}"
#          )

#         with c2:

#             st.metric(
#                 "Total Orders",
#                  f"{int(df['TotalOrders'].iloc[0]):,}"
#          )

#         with c3:

#             st.metric(
#                 "Total Customers",
#                 f"{int(df['TotalCustomers'].iloc[0]):,}"
#         )

#         with c4:

#             st.metric(
#                 "Average Order Value",
#                 f"${df['AverageOrderValue'].iloc[0]:,.2f}"
#         )

#         st.markdown("---")

#         st.subheader("Numeric Summary")

#         st.dataframe(numeric.describe())

#         st.markdown("---")

#         st.subheader("Missing Values")

#         missing=df.isnull().sum()

#         fig=px.bar(

#             x=missing.index,

#             y=missing.values,

#             labels={"x":"Columns","y":"Missing Values"}

#         )
#         st.plotly_chart(fig,use_container_width=True)

#         st.markdown("---")

#         st.subheader("Correlation Heatmap")

#         if numeric.shape[1]>1:
#             corr=numeric.corr()

#             fig=px.imshow(

#                 corr,

#                 text_auto=True,

#                 color_continuous_scale="Blues"

#             )

#             st.plotly_chart(

#         fig,

#                 use_container_width=True

#             )

#         st.markdown("---")

#         st.subheader("Distribution")

#         column=st.selectbox(

#             "Choose Numeric Column",

#             numeric.columns

#         )
#     fig=px.histogram(

#             df,

#             x=column,

#             nbins=30,

#             color_discrete_sequence=["royalblue"]

#         )

#     st.plotly_chart(

#             fig,

#             use_container_width=True

#         )
        
# # ============================================================
# # SALES ANALYTICS
# # ============================================================

# elif page == "Sales Analytics":

#     st.header("📈 Sales Analytics Dashboard")

#     df = data["sales_analytics.csv"]

#     if df.empty:
#         st.warning("sales_analytics.csv not found.")

#     else:

#         st.write("### Dataset Preview")
#         st.dataframe(df.head())

#         # -------------------------
#         # Sidebar Filters
#         # -------------------------

#         st.sidebar.subheader("Sales Filters")

#         object_cols = df.select_dtypes(include="object").columns.tolist()

#         if len(object_cols) > 0:

#             filter_col = st.sidebar.selectbox(
#                 "Select Category",
#                 object_cols
#             )

#             values = df[filter_col].dropna().unique()

#             selected = st.sidebar.multiselect(
#                 "Choose Values",
#                 values,
#                 default=values
#             )

#             df = df[df[filter_col].isin(selected)]

#         # -------------------------
#         # KPI Cards
#         # -------------------------

#         numeric = df.select_dtypes(include=np.number)

#         c1, c2, c3, c4 = st.columns(4)

#         with c1:
#             st.metric(
#                 "Total Sales",
#                 f"${numeric.sum().sum():,.0f}"
#             )

#         with c2:
#             st.metric(
#                 "Average Sales",
#                 f"${numeric.mean().mean():,.2f}"
#             )

#         with c3:
#             st.metric(
#                 "Maximum Sales",
#                 f"${numeric.max().max():,.0f}"
#             )

#         with c4:
#             st.metric(
#                 "Minimum Sales",
#                 f"${numeric.min().min():,.0f}"
#             )

#         st.divider()

#         # -------------------------
#         # Numeric Column Selection
#         # -------------------------

#         num_cols = numeric.columns.tolist()

#         chart_col = st.selectbox(
#             "Choose Numeric Column",
#             num_cols
#         )

#         # -------------------------
#         # Histogram
#         # -------------------------

#         st.subheader("Sales Distribution")

#         fig = px.histogram(
#             df,
#             x=chart_col,
#             nbins=25,
#             color_discrete_sequence=["royalblue"]
#         )

#         st.plotly_chart(
#             fig,
#             use_container_width=True
#         )

#         # -------------------------
#         # Box Plot
#         # -------------------------

#         st.subheader("Box Plot")

#         fig = px.box(
#             df,
#             y=chart_col,
#             color_discrete_sequence=["green"]
#         )

#         st.plotly_chart(
#             fig,
#             use_container_width=True
#         )

#         # -------------------------
#         # Bar Chart
#         # -------------------------

#         if len(object_cols) > 0:

#             category = st.selectbox(
#                 "Category Column",
#                 object_cols
#             )

#             grouped = (
#                 df.groupby(category)[chart_col]
#                 .sum()
#                 .reset_index()
#             )

#             fig = px.bar(
#                 grouped,
#                 x=category,
#                 y=chart_col,
#                 color=chart_col,
#                 text_auto=True
#             )

#             st.plotly_chart(
#                 fig,
#                 use_container_width=True
#             )

#         # -------------------------
#         # Pie Chart
#         # -------------------------

#         if len(object_cols) > 0:

#             grouped = (
#                 df.groupby(category)[chart_col]
#                 .sum()
#                 .reset_index()
#             )

#             fig = px.pie(
#                 grouped,
#                 names=category,
#                 values=chart_col,
#                 hole=0.45
#             )

#             st.plotly_chart(
#                 fig,
#                 use_container_width=True
#             )

#         # -------------------------
#         # Scatter Plot
#         # -------------------------

#         if len(num_cols) >= 2:

#             x_axis = st.selectbox(
#                 "X Axis",
#                 num_cols,
#                 key="sales_x"
#             )

#             y_axis = st.selectbox(
#                 "Y Axis",
#                 num_cols,
#                 index=1,
#                 key="sales_y"
#             )

#             fig = px.scatter(
#                 df,
#                 x=x_axis,
#                 y=y_axis,
#                 color=y_axis,
#                 size=y_axis,
#                 hover_data=df.columns
#             )

#             st.plotly_chart(
#                 fig,
#                 use_container_width=True
#             )

#         # -------------------------
#         # Correlation Heatmap
#         # -------------------------

#         if len(num_cols) > 1:

#             st.subheader("Correlation Matrix")

#             corr = numeric.corr()

#             fig = px.imshow(
#                 corr,
#                 text_auto=True,
#                 color_continuous_scale="RdBu"
#             )

#             st.plotly_chart(
#                 fig,
#                 use_container_width=True
#             )

#         # -------------------------
#         # Line Chart
#         # -------------------------

#         st.subheader("Trend Analysis")

#         fig = px.line(
#             df,
#             y=chart_col,
#             markers=True
#         )

#         st.plotly_chart(
#             fig,
#             use_container_width=True
#         )

#         # -------------------------
#         # Top 10 Records
#         # -------------------------

#         st.subheader("Top 10 Records")

#         top = (
#             df.sort_values(
#                 by=chart_col,
#                 ascending=False
#             )
#             .head(10)
#         )

#         st.dataframe(top)

#         # -------------------------
#         # Download CSV
#         # -------------------------

#         csv = df.to_csv(index=False)

#         st.download_button(
#             "📥 Download Filtered Data",
#             csv,
#             "sales_dashboard.csv",
#             "text/csv"
#         )
        
# # ============================================================
# # CUSTOMER ANALYTICS
# # ============================================================

# elif page == "Customer Analytics":

#     st.header("👥 Customer Analytics")

#     df = data["customer_analytics.csv"]

#     if df.empty:
#         st.warning("customer_analytics.csv not found")

#     else:

#         st.dataframe(df.head())

#         numeric = df.select_dtypes(include=np.number)
#         object_cols = df.select_dtypes(include="object").columns.tolist()

#         c1, c2, c3, c4 = st.columns(4)

#         c1.metric("Customers", len(df))
#         c2.metric("Numeric Columns", len(numeric.columns))
#         c3.metric("Average", round(numeric.mean().mean(),2))
#         c4.metric("Maximum", round(numeric.max().max(),2))

#         st.divider()

#         column = st.selectbox(
#             "Select Numeric Column",
#             numeric.columns
#         )

#         fig = px.histogram(
#             df,
#             x=column,
#             nbins=30,
#             color_discrete_sequence=["royalblue"]
#         )

#         st.plotly_chart(fig,use_container_width=True)

#         fig = px.box(
#             df,
#             y=column,
#             color_discrete_sequence=["green"]
#         )

#         st.plotly_chart(fig,use_container_width=True)

#         if len(object_cols)>0:

#             category = st.selectbox(
#                 "Category",
#                 object_cols
#             )

#             temp = (
#                 df.groupby(category)[column]
#                 .mean()
#                 .reset_index()
#             )

#             fig = px.bar(
#                 temp,
#                 x=category,
#                 y=column,
#                 color=column,
#                 text_auto=True
#             )

#             st.plotly_chart(
#                 fig,
#                 use_container_width=True
#             )

#         if len(numeric.columns)>=2:

#             x = st.selectbox(
#                 "X",
#                 numeric.columns,
#                 key="custx"
#             )

#             y = st.selectbox(
#                 "Y",
#                 numeric.columns,
#                 index=1,
#                 key="custy"
#             )

#             fig = px.scatter(
#                 df,
#                 x=x,
#                 y=y,
#                 color=y,
#                 size=y,
#                 hover_data=df.columns
#             )

#             st.plotly_chart(
#                 fig,
#                 use_container_width=True
#             )

# # ============================================================
# # CUSTOMER SEGMENTATION
# # ============================================================

# elif page=="Customer Segmentation":

#     st.header("🎯 Customer Segmentation")

#     df=data["customer_segmentation.csv"]

#     if df.empty:

#         st.warning("customer_segmentation.csv not found")

#     else:

#         st.dataframe(df.head())

#         numeric=df.select_dtypes(include=np.number)
#         object_cols=df.select_dtypes(include="object").columns.tolist()

#         st.subheader("Dataset Summary")

#         st.write(df.describe(include="all"))

#         if len(object_cols)>0:

#             category=st.selectbox(
#                 "Segment Column",
#                 object_cols
#             )

#             fig=px.pie(
#                 df,
#                 names=category,
#                 hole=0.45
#             )

#             st.plotly_chart(
#                 fig,
#                 use_container_width=True
#             )

#             counts=(
#                 df[category]
#                 .value_counts()
#                 .reset_index()
#             )

#             counts.columns=[category,"Count"]

#             fig=px.bar(
#                 counts,
#                 x=category,
#                 y="Count",
#                 color="Count",
#                 text_auto=True
#             )

#             st.plotly_chart(
#                 fig,
#                 use_container_width=True
#             )

#         if len(numeric.columns)>=2:

#             x=numeric.columns[0]
#             y=numeric.columns[1]

#             fig=px.scatter(
#                 df,
#                 x=x,
#                 y=y,
#                 color=y,
#                 size=y,
#                 hover_data=df.columns
#             )

#             st.plotly_chart(
#                 fig,
#                 use_container_width=True
#             )

#         if len(numeric.columns)>1:

#             corr=numeric.corr()

#             fig=px.imshow(
#                 corr,
#                 text_auto=True,
#                 color_continuous_scale="Viridis"
#             )

#             st.plotly_chart(
#                 fig,
#                 use_container_width=True
#             )

# # ============================================================
# # CUSTOMER CHURN
# # ============================================================

# elif page=="Customer Churn":

#     st.header("⚠ Customer Churn Dashboard")

#     df=data["customer_churn.csv"]

#     if df.empty:

#         st.warning("customer_churn.csv not found")

#     else:

#         st.dataframe(df.head())

#         numeric=df.select_dtypes(include=np.number)
#         object_cols=df.select_dtypes(include="object").columns.tolist()

#         c1,c2,c3,c4=st.columns(4)

#         c1.metric("Records",len(df))
#         c2.metric("Numeric",len(numeric.columns))
#         c3.metric("Object",len(object_cols))
#         c4.metric("Average",round(numeric.mean().mean(),2))

#         st.divider()

#         if len(object_cols)>0:

#             churn=st.selectbox(
#                 "Select Category",
#                 object_cols
#             )

#             fig=px.pie(
#                 df,
#                 names=churn,
#                 hole=.5
#             )

#             st.plotly_chart(
#                 fig,
#                 use_container_width=True
#             )

#             temp=(
#                 df[churn]
#                 .value_counts()
#                 .reset_index()
#             )

#             temp.columns=[churn,"Count"]

#             fig=px.bar(
#                 temp,
#                 x=churn,
#                 y="Count",
#                 color="Count",
#                 text_auto=True
#             )

#             st.plotly_chart(
#                 fig,
#                 use_container_width=True
#             )

#         if len(numeric.columns)>=2:

#             x=st.selectbox(
#                 "X Axis",
#                 numeric.columns,
#                 key="cx"
#             )

#             y=st.selectbox(
#                 "Y Axis",
#                 numeric.columns,
#                 index=1,
#                 key="cy"
#             )

#             fig=px.scatter(
#                 df,
#                 x=x,
#                 y=y,
#                 color=y,
#                 size=y
#             )

#             st.plotly_chart(
#                 fig,
#                 use_container_width=True
#             )

#         if len(numeric.columns)>1:

#             fig=px.imshow(
#                 numeric.corr(),
#                 text_auto=True,
#                 color_continuous_scale="RdBu"
#             )

#             st.plotly_chart(
#                 fig,
#                 use_container_width=True
#             )

#         csv=df.to_csv(index=False)

#         st.download_button(
#             "📥 Download Customer Churn Data",
#             csv,
#             "customer_churn.csv",
#             "text/csv"
#         )
        
# # ============================================================
# # INVENTORY DASHBOARD
# # ============================================================

# elif page == "Inventory":

#     st.header("📦 Inventory Dashboard")

#     df = data["inventory_dashboard.csv"]

#     if df.empty:
#         st.warning("inventory_dashboard.csv not found")

#     else:

#         st.dataframe(df.head())

#         numeric = df.select_dtypes(include=np.number)
#         object_cols = df.select_dtypes(include="object").columns.tolist()

#         col1, col2, col3 = st.columns(3)

#         col1.metric("Total Records", len(df))
#         col2.metric("Average", round(numeric.mean().mean(),2))
#         col3.metric("Maximum", round(numeric.max().max(),2))

#         st.divider()

#         if len(object_cols)>0:

#             category = st.selectbox(
#                 "Category",
#                 object_cols,
#                 key="inventory"
#             )

#             value = st.selectbox(
#                 "Value",
#                 numeric.columns,
#                 key="inventory_value"
#             )

#             temp = (
#                 df.groupby(category)[value]
#                 .sum()
#                 .reset_index()
#             )

#             fig = px.bar(
#                 temp,
#                 x=category,
#                 y=value,
#                 color=value,
#                 text_auto=True
#             )

#             st.plotly_chart(fig,use_container_width=True)

#         value = st.selectbox(
#             "Distribution",
#             numeric.columns,
#             key="inventory_hist"
#         )

#         fig = px.histogram(df,x=value)

#         st.plotly_chart(fig,use_container_width=True)

# # ============================================================
# # COUNTRY ANALYSIS
# # ============================================================

# elif page=="Country Analysis":

#     st.header("🌍 Country Analysis")

#     df = data["country_analytics.csv"]

#     if df.empty:

#         st.warning("country_analytics.csv not found")

#     else:

#         st.dataframe(df.head())

#         numeric=df.select_dtypes(include=np.number)
#         object_cols=df.select_dtypes(include="object").columns.tolist()

#         if len(object_cols)>0:

#             category=object_cols[0]

#             value=numeric.columns[0]

#             temp=(
#                 df.groupby(category)[value]
#                 .sum()
#                 .reset_index()
#             )

#             fig=px.bar(
#                 temp,
#                 x=category,
#                 y=value,
#                 color=value,
#                 text_auto=True
#             )

#             st.plotly_chart(
#                 fig,
#                 use_container_width=True
#             )

#             fig=px.pie(
#                 temp,
#                 names=category,
#                 values=value,
#                 hole=.45
#             )

#             st.plotly_chart(
#                 fig,
#                 use_container_width=True
#             )

# # ============================================================
# # PRODUCT ANALYTICS
# # ============================================================

# elif page=="Products":

#     st.header("📦 Product Analytics")

#     df=data["product_analytics.csv"]

#     if df.empty:

#         st.warning("product_analytics.csv not found")

#     else:

#         st.dataframe(df.head())

#         numeric=df.select_dtypes(include=np.number)
#         object_cols=df.select_dtypes(include="object").columns.tolist()

#         if len(object_cols)>0:

#             product=object_cols[0]

#             value=numeric.columns[0]

#             temp=(
#                 df.groupby(product)[value]
#                 .sum()
#                 .reset_index()
#             )

#             fig=px.bar(
#                 temp,
#                 x=product,
#                 y=value,
#                 color=value,
#                 text_auto=True
#             )

#             st.plotly_chart(
#                 fig,
#                 use_container_width=True
#             )

#         fig=px.box(
#             df,
#             y=numeric.columns[0]
#         )

#         st.plotly_chart(
#             fig,
#             use_container_width=True
#         )

# # ============================================================
# # DEMAND FORECAST
# # ============================================================

# elif page=="Demand Forecast":

#     st.header("📈 Demand Forecast")

#     df=data["demand_forecasting.csv"]

#     if df.empty:

#         st.warning("demand_forecasting.csv not found")

#     else:

#         st.dataframe(df.head())

#         numeric=df.select_dtypes(include=np.number)

#         column=st.selectbox(
#             "Forecast Column",
#             numeric.columns
#         )

#         fig=px.line(
#             df,
#             y=column,
#             markers=True
#         )

#         st.plotly_chart(
#             fig,
#             use_container_width=True
#         )

#         fig=px.area(
#             df,
#             y=column
#         )

#         st.plotly_chart(
#             fig,
#             use_container_width=True
#         )

# # ============================================================
# # BUSINESS INSIGHTS
# # ============================================================

# elif page == "Business Insights":

#     st.header("💡 Business Insights")

#     df = data["business_insights.csv"]

#     if df.empty:

#         st.warning("business_insights.csv not found")

#     else:

#         st.dataframe(df)

#         st.subheader("Quick Summary")

#         st.write(df.describe(include="all"))

#         numeric = df.select_dtypes(include=np.number)

#         if len(numeric.columns) > 0:

#             column = st.selectbox(
#                 "Select Column",
#                 numeric.columns
#             )

#             fig = px.bar(
#                 df,
#                 y=column
#             )

#             st.plotly_chart(
#                 fig,
#                 use_container_width=True
#             )

#         st.success("✔ Dashboard Completed Successfully")

# # ============================================================
# # FOOTER
# # ============================================================
 
 
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(
    page_title="Business Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------

st.markdown("""
<style>

.main{
background-color:#f5f7fa;
}

h1,h2,h3{
color:#003366;
}

.metric-card{
padding:20px;
border-radius:12px;
background:white;
box-shadow:0px 2px 10px rgba(0,0,0,0.1);
text-align:center;
}

.sidebar .sidebar-content{
background:#003366;
}

</style>

""",unsafe_allow_html=True)

# -----------------------------
# Title
# -----------------------------

st.title("📊 Business Analytics Dashboard")

st.markdown("### Executive Insights & Business Performance")

# -----------------------------
# Load Data
# -----------------------------

BASE=Path("data/dashboard")

@st.cache_data
def load_data():

    data={}

    files=[
        "executive_overview.csv",
        "sales_analytics.csv",
        "customer_analytics.csv",
        "customer_segmentation.csv",
        "customer_churn.csv",
        "inventory_dashboard.csv",
        "country_analytics.csv",
        "product_analytics.csv",
        "business_insights.csv",
        "demand_forecasting.csv"
    ]

    for file in files:

        path=BASE/file

        try:
            data[file]=pd.read_csv(path)

        except:

            data[file]=pd.DataFrame()

    return data

data=load_data()

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.image(
"https://img.icons8.com/color/96/combo-chart--v1.png",
width=90
)

st.sidebar.title("Navigation")

page=st.sidebar.radio(

"Select Dashboard",

[
"Executive Overview",
"Sales Analytics",
"Customer Analytics",
"Customer Segmentation",
"Customer Churn",
"Inventory",
"Country Analysis",
"Products",
"Demand Forecast",
"Business Insights"
]

)


# -----------------------------
# Executive Overview
# -----------------------------

if page=="Executive Overview":

    df=data["executive_overview.csv"]

    st.header("Executive Dashboard")

    if df.empty:

        st.warning("executive_overview.csv not found")

    else:

        st.dataframe(df.head())

        numeric=df.select_dtypes(include=np.number)

        c1,c2,c3,c4=st.columns(4)

        with c1:

            st.metric(
                "Total Revenue",
                 f"${df['TotalRevenue'].iloc[0]:,.0f}"
            )

        with c2:

            st.metric(
                "Total Orders",
                f"{int(df['TotalOrders'].iloc[0]):,}"
            )

        with c3:

            st.metric(
                "Total Customers",
                f"{int(df['TotalCustomers'].iloc[0]):,}"
            )

        with c4:

            st.metric(
                "Average Order Value",
                f"${df['AverageOrderValue'].iloc[0]:,.2f}"
            )

        st.markdown("---")

        st.subheader("Numeric Summary")

        st.dataframe(numeric.describe())

        st.markdown("---")

        st.subheader("Missing Values")

        missing=df.isnull().sum()

        fig=px.bar(

            x=missing.index,

            y=missing.values,

            labels={"x":"Columns","y":"Missing Values"}

        )
        st.plotly_chart(fig,use_container_width=True)

        st.markdown("---")

        st.subheader("Correlation Heatmap")

        if numeric.shape[1]>1:
            corr=numeric.corr()

            fig=px.imshow(

                corr,

                text_auto=True,

                color_continuous_scale="Blues"

            )

            st.plotly_chart(

                fig,

                use_container_width=True

            )

        st.markdown("---")

        st.subheader("Distribution")

        column=st.selectbox(

            "Choose Numeric Column",

            numeric.columns

        )
        fig=px.histogram(

            df,

            x=column,

            nbins=30,

            color_discrete_sequence=["royalblue"]

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )
        
# ============================================================
# SALES ANALYTICS
# ============================================================

elif page == "Sales Analytics":

    st.header("📈 Sales Analytics Dashboard")

    df = data["sales_analytics.csv"]

    if df.empty:
        st.warning("sales_analytics.csv not found.")

    else:

        st.write("### Dataset Preview")
        st.dataframe(df.head())

        # -------------------------
        # Sidebar Filters
        # -------------------------

        st.sidebar.subheader("Sales Filters")

        object_cols = df.select_dtypes(include="object").columns.tolist()

        if len(object_cols) > 0:

            filter_col = st.sidebar.selectbox(
                "Select Category",
                object_cols
            )

            values = df[filter_col].dropna().unique()

            selected = st.sidebar.multiselect(
                "Choose Values",
                values,
                default=values
            )

            df = df[df[filter_col].isin(selected)]

        # -------------------------
        # KPI Cards
        # -------------------------

        numeric = df.select_dtypes(include=np.number)

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Total Sales",
                f"${numeric.sum().sum():,.0f}"
            )

        with c2:
            st.metric(
                "Average Sales",
                f"${numeric.mean().mean():,.2f}"
            )

        with c3:
            st.metric(
                "Maximum Sales",
                f"${numeric.max().max():,.0f}"
            )

        with c4:
            st.metric(
                "Minimum Sales",
                f"${numeric.min().min():,.0f}"
            )

        st.divider()

        # -------------------------
        # Numeric Column Selection
        # -------------------------

        num_cols = numeric.columns.tolist()

        chart_col = st.selectbox(
            "Choose Numeric Column",
            num_cols
        )

        # -------------------------
        # Histogram
        # -------------------------

        st.subheader("Sales Distribution")

        fig = px.histogram(
            df,
            x=chart_col,
            nbins=25,
            color_discrete_sequence=["royalblue"]
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # -------------------------
        # Box Plot
        # -------------------------

        st.subheader("Box Plot")

        fig = px.box(
            df,
            y=chart_col,
            color_discrete_sequence=["green"]
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # -------------------------
        # Bar Chart
        # -------------------------

        if len(object_cols) > 0:

            category = st.selectbox(
                "Category Column",
                object_cols
            )

            grouped = (
                df.groupby(category)[chart_col]
                .sum()
                .reset_index()
            )

            fig = px.bar(
                grouped,
                x=category,
                y=chart_col,
                color=chart_col,
                text_auto=True
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # -------------------------
        # Pie Chart
        # -------------------------

        if len(object_cols) > 0:

            grouped = (
                df.groupby(category)[chart_col]
                .sum()
                .reset_index()
            )

            fig = px.pie(
                grouped,
                names=category,
                values=chart_col,
                hole=0.45
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # -------------------------
        # Scatter Plot
        # -------------------------

        if len(num_cols) >= 2:

            x_axis = st.selectbox(
                "X Axis",
                num_cols,
                key="sales_x"
            )

            y_axis = st.selectbox(
                "Y Axis",
                num_cols,
                index=1,
                key="sales_y"
            )

            fig = px.scatter(
                df,
                x=x_axis,
                y=y_axis,
                color=y_axis,
                size=y_axis,
                hover_data=df.columns
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # -------------------------
        # Correlation Heatmap
        # -------------------------

        if len(num_cols) > 1:

            st.subheader("Correlation Matrix")

            corr = numeric.corr()

            fig = px.imshow(
                corr,
                text_auto=True,
                color_continuous_scale="RdBu"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # -------------------------
        # Line Chart
        # -------------------------

        st.subheader("Trend Analysis")

        fig = px.line(
            df,
            y=chart_col,
            markers=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # -------------------------
        # Top 10 Records
        # -------------------------

        st.subheader("Top 10 Records")

        top = (
            df.sort_values(
                by=chart_col,
                ascending=False
            )
            .head(10)
        )

        st.dataframe(top)

        # -------------------------
        # Download CSV
        # -------------------------

        csv = df.to_csv(index=False)

        st.download_button(
            "📥 Download Filtered Data",
            csv,
            "sales_dashboard.csv",
            "text/csv"
        )
        
# ============================================================
# CUSTOMER ANALYTICS
# ============================================================

elif page == "Customer Analytics":

    st.header("👥 Customer Analytics")

    df = data["customer_analytics.csv"]

    if df.empty:
        st.warning("customer_analytics.csv not found")

    else:

        st.dataframe(df.head())

        numeric = df.select_dtypes(include=np.number)
        object_cols = df.select_dtypes(include="object").columns.tolist()

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Customers", len(df))
        c2.metric("Numeric Columns", len(numeric.columns))
        c3.metric("Average", round(numeric.mean().mean(),2))
        c4.metric("Maximum", round(numeric.max().max(),2))

        st.divider()

        column = st.selectbox(
            "Select Numeric Column",
            numeric.columns
        )

        fig = px.histogram(
            df,
            x=column,
            nbins=30,
            color_discrete_sequence=["royalblue"]
        )

        st.plotly_chart(fig,use_container_width=True)

        fig = px.box(
            df,
            y=column,
            color_discrete_sequence=["green"]
        )

        st.plotly_chart(fig,use_container_width=True)

        if len(object_cols)>0:

            category = st.selectbox(
                "Category",
                object_cols
            )

            temp = (
                df.groupby(category)[column]
                .mean()
                .reset_index()
            )

            fig = px.bar(
                temp,
                x=category,
                y=column,
                color=column,
                text_auto=True
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        if len(numeric.columns)>=2:

            x = st.selectbox(
                "X",
                numeric.columns,
                key="custx"
            )

            y = st.selectbox(
                "Y",
                numeric.columns,
                index=1,
                key="custy"
            )

            fig = px.scatter(
                df,
                x=x,
                y=y,
                color=y,
                size=y,
                hover_data=df.columns
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

# ============================================================
# CUSTOMER SEGMENTATION
# ============================================================

elif page=="Customer Segmentation":

    st.header("🎯 Customer Segmentation")

    df=data["customer_segmentation.csv"]

    if df.empty:

        st.warning("customer_segmentation.csv not found")

    else:

        st.dataframe(df.head())

        numeric=df.select_dtypes(include=np.number)
        object_cols=df.select_dtypes(include="object").columns.tolist()

        st.subheader("Dataset Summary")

        st.write(df.describe(include="all"))

        if len(object_cols)>0:

            category=st.selectbox(
                "Segment Column",
                object_cols
            )

            fig=px.pie(
                df,
                names=category,
                hole=0.45
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            counts=(
                df[category]
                .value_counts()
                .reset_index()
            )

            counts.columns=[category,"Count"]

            fig=px.bar(
                counts,
                x=category,
                y="Count",
                color="Count",
                text_auto=True
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        if len(numeric.columns)>=2:

            x=numeric.columns[0]
            y=numeric.columns[1]

            fig=px.scatter(
                df,
                x=x,
                y=y,
                color=y,
                size=y,
                hover_data=df.columns
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        if len(numeric.columns)>1:

            corr=numeric.corr()

            fig=px.imshow(
                corr,
                text_auto=True,
                color_continuous_scale="Viridis"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

# ============================================================
# CUSTOMER CHURN
# ============================================================

elif page=="Customer Churn":

    st.header("⚠ Customer Churn Dashboard")

    df=data["customer_churn.csv"]

    if df.empty:

        st.warning("customer_churn.csv not found")

    else:

        st.dataframe(df.head())

        numeric=df.select_dtypes(include=np.number)
        object_cols=df.select_dtypes(include="object").columns.tolist()

        c1,c2,c3,c4=st.columns(4)

        c1.metric("Records",len(df))
        c2.metric("Numeric",len(numeric.columns))
        c3.metric("Object",len(object_cols))
        c4.metric("Average",round(numeric.mean().mean(),2))

        st.divider()

        if len(object_cols)>0:

            churn=st.selectbox(
                "Select Category",
                object_cols
            )

            fig=px.pie(
                df,
                names=churn,
                hole=.5
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            temp=(
                df[churn]
                .value_counts()
                .reset_index()
            )

            temp.columns=[churn,"Count"]

            fig=px.bar(
                temp,
                x=churn,
                y="Count",
                color="Count",
                text_auto=True
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        if len(numeric.columns)>=2:

            x=st.selectbox(
                "X Axis",
                numeric.columns,
                key="cx"
            )

            y=st.selectbox(
                "Y Axis",
                numeric.columns,
                index=1,
                key="cy"
            )

            fig=px.scatter(
                df,
                x=x,
                y=y,
                color=y,
                size=y
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        if len(numeric.columns)>1:

            fig=px.imshow(
                numeric.corr(),
                text_auto=True,
                color_continuous_scale="RdBu"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        csv=df.to_csv(index=False)

        st.download_button(
            "📥 Download Customer Churn Data",
            csv,
            "customer_churn.csv",
            "text/csv"
        )
        
# ============================================================
# INVENTORY DASHBOARD
# ============================================================

elif page == "Inventory":

    st.header("📦 Inventory Dashboard")

    df = data["inventory_dashboard.csv"]

    if df.empty:
        st.warning("inventory_dashboard.csv not found")

    else:

        st.dataframe(df.head())

        numeric = df.select_dtypes(include=np.number)
        object_cols = df.select_dtypes(include="object").columns.tolist()

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Records", len(df))
        col2.metric("Average", round(numeric.mean().mean(),2))
        col3.metric("Maximum", round(numeric.max().max(),2))

        st.divider()

        if len(object_cols)>0:

            category = st.selectbox(
                "Category",
                object_cols,
                key="inventory"
            )

            value = st.selectbox(
                "Value",
                numeric.columns,
                key="inventory_value"
            )

            temp = (
                df.groupby(category)[value]
                .sum()
                .reset_index()
            )

            fig = px.bar(
                temp,
                x=category,
                y=value,
                color=value,
                text_auto=True
            )

            st.plotly_chart(fig,use_container_width=True)

        value = st.selectbox(
            "Distribution",
            numeric.columns,
            key="inventory_hist"
        )

        fig = px.histogram(df,x=value)

        st.plotly_chart(fig,use_container_width=True)

# ============================================================
# COUNTRY ANALYSIS
# ============================================================

elif page=="Country Analysis":

    st.header("🌍 Country Analysis")

    df = data["country_analytics.csv"]

    if df.empty:

        st.warning("country_analytics.csv not found")

    else:

        st.dataframe(df.head())

        numeric=df.select_dtypes(include=np.number)
        object_cols=df.select_dtypes(include="object").columns.tolist()

        if len(object_cols)>0:

            category=object_cols[0]

            value=numeric.columns[0]

            temp=(
                df.groupby(category)[value]
                .sum()
                .reset_index()
            )

            fig=px.bar(
                temp,
                x=category,
                y=value,
                color=value,
                text_auto=True
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            fig=px.pie(
                temp,
                names=category,
                values=value,
                hole=.45
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

# ============================================================
# PRODUCT ANALYTICS
# ============================================================

elif page=="Products":

    st.header("📦 Product Analytics")

    df=data["product_analytics.csv"]

    if df.empty:

        st.warning("product_analytics.csv not found")

    else:

        st.dataframe(df.head())

        numeric=df.select_dtypes(include=np.number)
        object_cols=df.select_dtypes(include="object").columns.tolist()

        if len(object_cols)>0:

            product=object_cols[0]

            value=numeric.columns[0]

            temp=(
                df.groupby(product)[value]
                .sum()
                .reset_index()
            )

            fig=px.bar(
                temp,
                x=product,
                y=value,
                color=value,
                text_auto=True
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        fig=px.box(
            df,
            y=numeric.columns[0]
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ============================================================
# DEMAND FORECAST
# ============================================================

elif page=="Demand Forecast":

    st.header("📈 Demand Forecast")

    df=data["demand_forecasting.csv"]

    if df.empty:

        st.warning("demand_forecasting.csv not found")

    else:

        st.dataframe(df.head())

        numeric=df.select_dtypes(include=np.number)

        column=st.selectbox(
            "Forecast Column",
            numeric.columns
        )

        fig=px.line(
            df,
            y=column,
            markers=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        fig=px.area(
            df,
            y=column
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ============================================================
# BUSINESS INSIGHTS
# ============================================================

elif page == "Business Insights":

    st.header("💡 Business Insights")

    df = data["business_insights.csv"]

    if df.empty:

        st.warning("business_insights.csv not found")

    else:

        st.dataframe(df)

        st.subheader("Quick Summary")

        st.write(df.describe(include="all"))

        numeric = df.select_dtypes(include=np.number)

        if len(numeric.columns) > 0:

            column = st.selectbox(
                "Select Column",
                numeric.columns
            )

            fig = px.bar(
                df,
                y=column
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.success("✔ Dashboard Completed Successfully")

# ============================================================
# FOOTER
# ============================================================