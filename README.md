# 🛍️ RetailPulse: AI-Powered Customer Analytics & Demand Forecasting

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-orange)
![Prophet](https://img.shields.io/badge/Prophet-Forecasting-success)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

</p>

---

# 📌 Overview

RetailPulse is an end-to-end AI-powered Retail Analytics platform developed using the **Online Retail II** dataset. The project transforms retail transaction data into interactive business intelligence dashboards, enabling data-driven decision-making through customer analytics, demand forecasting, churn prediction, inventory insights, and product performance analysis.

The application is built using **Python**, **Machine Learning**, **Streamlit**, and modern data visualization libraries to provide an intuitive analytics experience.

---

# 🎯 Problem Statement

Retail organizations generate massive volumes of transactional data every day. Extracting meaningful insights from this data is challenging due to:

- Large-scale customer transactions
- Changing customer purchasing behaviour
- Demand uncertainty
- Inventory optimization challenges
- Difficulty identifying high-value customers
- Lack of centralized business analytics

RetailPulse addresses these challenges by providing an intelligent analytics platform that converts raw retail data into actionable insights.

---

# 🚀 Key Features

- Interactive Streamlit Dashboard
- Executive Business Dashboard
- Sales Performance Analytics
- Customer Behaviour Analysis
- RFM Customer Segmentation
- Customer Churn Prediction
- Demand Forecasting
- Inventory Analytics
- Product Performance Analytics
- Country-wise Sales Analysis
- Business Insights Dashboard
- Interactive Charts & KPIs

---

# 📂 Dataset

**Dataset:** Online Retail II

**Source:** UCI Machine Learning Repository

The project uses the Online Retail II transactional dataset containing online retail sales data from a UK-based retailer. The dataset is used for customer analytics, segmentation, demand forecasting, inventory optimization, and business intelligence.

### Dataset Statistics

| Metric | Value |
|---------|------:|
| Records | **1,066,371** |
| Features | **8** |
| Customers | **5,942** |
| Products (Stock Codes) | **5,305** |
| Product Descriptions | **5,698** |
| Countries | **43** |

### Dataset Features

- Invoice
- StockCode
- Description
- Quantity
- InvoiceDate
- Price
- Customer ID
- Country

---

# 🛠 Tech Stack

## Programming Language

- Python

## Data Analysis

- Pandas
- NumPy

## Data Visualization

- Plotly
- Matplotlib
- Seaborn

## Machine Learning

- Scikit-learn
- Prophet

## Dashboard

- Streamlit

## Development Tools

- Git
- GitHub
- VS Code

---

# 🤖 Machine Learning Models

The project includes trained machine learning models for:

- Customer Churn Prediction (`churn_model.pkl`)
- Demand Forecasting using Prophet (`prophet_model.pkl`)

---
# 📊 Dashboard Overview

RetailPulse includes **11 interactive dashboards**, each designed to provide actionable insights into different aspects of retail business performance.

---

## 🏠 Home

Provides a centralized overview of the platform with key business KPIs and quick navigation to all analytics modules.

![Home Dashboard](images/home.png)

---

## 📈 Executive Dashboard

Presents high-level business performance metrics, including revenue, orders, customers, and executive KPIs for quick decision-making.

![Executive Dashboard](images/executive_dashboard.png)

---

## 📊 Sales Analytics

Analyzes sales performance through revenue trends, monthly sales, growth patterns, and key sales metrics.

![Sales Analytics](images/sales_analytics.png)

---

## 👥 Customer Analytics

Visualizes customer behavior, purchasing patterns, engagement metrics, and overall customer performance.

![Customer Analytics](images/customer_analytics.png)

---

## 🎯 Customer Segmentation

Segments customers using **RFM (Recency, Frequency, Monetary)** analysis to identify valuable customer groups and marketing opportunities.

![Customer Segmentation](images/customer_segmentation.png)

---

## ⚠ Customer Churn

Predicts customers at risk of leaving the business and provides insights that support customer retention strategies.

![Customer Churn](images/customer_churn.png)

---

## 📦 Inventory

Monitors inventory status, stock levels, inventory KPIs, and product availability to support inventory optimization.

![Inventory Dashboard](images/inventory.png)

---

## 🌍 Country Analysis

Provides geographical insights by analyzing country-wise sales, revenue distribution, and international business performance.

![Country Analysis](images/country_analysis.png)

---

## 🛒 Product Analytics

Evaluates product performance through sales, pricing, revenue contribution, and top-performing products.

![Product Analytics](images/product_analytics.png)

---

## 📅 Demand Forecast

Uses the **Prophet forecasting model** to predict future sales trends and support inventory and business planning.

![Demand Forecast](images/demand_forecast.png)

---

## 💡 Business Insights

Summarizes key findings, business recommendations, and strategic insights generated from the overall retail analytics pipeline.

![Business Insights](images/business_insights.png)

---

# 📁 Project Structure

```text
RetailPulse/
│
├── 📂 app/
│   ├── 📂 .streamlit/
│   │   └── config.toml              # Streamlit configuration
│   │
│   ├── 📂 assets/
│   │   └── style.css                # Custom dashboard styling
│   │
│   ├── 📂 pages/                    # Dashboard pages
│   │
│   ├── 📂 utils/                    # Utility functions
│   │
│   └── app.py                       # Main Streamlit application
│
├── 📂 data/
│   ├── 📂 raw/                      # Original Online Retail II dataset
│   │   └── online_retail_II.xlsx
│   │
│   ├── 📂 processed/                # Processed datasets
│   │   ├── customer_churn_predictions.csv
│   │   ├── customer_features.csv
│   │   ├── customer_rfm.csv
│   │   ├── customer_segments.csv
│   │   ├── daily_sales.csv
│   │   ├── feature_importance.csv
│   │   ├── forecast.csv
│   │   ├── inventory_analysis.csv
│   │   ├── online_retail_II_cleaned.csv
│   │   └── online_retail_II_merged.csv
│   │
│   └── 📂 dashboard/                # Dashboard-ready datasets
│       ├── executive_overview.csv
│       ├── sales_analytics.csv
│       ├── customer_analytics.csv
│       ├── customer_segmentation.csv
│       ├── customer_churn.csv
│       ├── inventory_dashboard.csv
│       ├── country_analytics.csv
│       ├── product_analytics.csv
│       ├── demand_forecasting.csv
│       ├── business_insights.csv
│       └── project_summary.csv
│
├── 📂 models/
│   ├── churn_model.pkl              # Customer Churn Prediction Model
│   └── prophet_model.pkl            # Demand Forecasting Model
│
├── 📂 notebooks/
│   ├── 01_Data_Understanding.ipynb
│   ├── 02_Data_Cleaning.ipynb
│   ├── 03_Exploratory_Data_Analysis.ipynb
│   ├── 04_Feature_Engineering.ipynb
│   ├── 05_Customer_Segmentation.ipynb
│   ├── 06_Demand_Forecasting.ipynb
│   ├── 07_Customer_Feature_Engineering.ipynb
│   ├── 08_Customer_Churn_Prediction.ipynb
│   ├── 09_Inventory_Optimization.ipynb
│   └── 10_Dashboard_Dataset_Preparation.ipynb
│
├── 📂 images/
│   └── dashboards/                  # Dashboard images
│
├── requirements.txt                 # Python dependencies
├── README.md                        # Project documentation
├── LICENSE                          # MIT License
└── .gitignore
```

---

# 📈 Project Workflow

The following workflow illustrates the complete end-to-end data science pipeline implemented in RetailPulse, from raw data understanding to the final interactive Streamlit dashboard.

<p align="center">
  <img src="images/project_workflow.png" alt="RetailPulse Project Workflow" width="700"/>
</p>

# ⚙️ Installation                      

Clone the repository:

```bash
git clone https://github.com/pinkey-kavar-bika/RetailPulse.git
```

Navigate to the project directory:

```bash
cd RetailPulse
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app/app.py
```

---

# 📌 Future Improvements

- Real-time data pipeline
- Automated model retraining
- Enhanced forecasting models
- Role-based authentication
- Dashboard export functionality
- Advanced business recommendations

---

# 👥 Contributors

- Nasrin Khatoon - https://github.com/nasrin567
- Pinkey Kavar Bika - https://github.com/pinkey-kavar-bika 
- Sheikh Moin - https://github.com/sheikhmoin-09

---

# 📄 License

This project is licensed under the MIT License.

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
