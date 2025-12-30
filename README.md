# Vendor Performance Analysis 📊

## 📌 Project Overview
This project analyzes vendor and brand performance using sales, purchase, inventory, and profitability data.  
The goal is to identify **top-performing vendors and brands**, **low-performing vendors**, and understand the **relationship between sales and gross profit** to support data-driven business decisions.

This project combines **data engineering, exploratory data analysis, and business intelligence dashboards**.

## 🎯 Objectives
- Analyze total sales, purchases, gross profit, and profit margin
- Identify top vendors and brands by sales
- Detect low-performing vendors using sales-to-purchase ratio
- Analyze profit vs loss patterns across brands
- Build an interactive dashboard for business insights

## 🛠️ Tech Stack
- **Python** (Pandas, NumPy)
- **Jupyter Notebook** (EDA & analysis)
- **Power BI** (Dashboard & visualizations)
- **CSV datasets**
- **SQLite** (inventory.db)
- **Git & GitHub**

## 📊 Dashboard Highlights
The Power BI dashboard includes:
- KPI cards for Total Sales, Total Purchase, Gross Profit, Profit Margin
- Purchase contribution by vendor (Donut Chart)
- Top Vendors by Sales
- Top Brands by Sales
- Low Performing Vendors (Sales-to-Purchase Ratio)
- Profit vs Loss analysis using scatter plots

## 📈 Key Insights
- A small number of vendors contribute the majority of total sales
- Certain vendors show high purchase volume but low profitability
- Some brands consistently generate profit across different sales ranges
- Low-performing vendors are identified using poor sales-to-purchase ratios
- Strong positive correlation between sales volume and gross profit

## 🚫 Dataset Note
Due to GitHub file size limitations, large raw inventory CSV files are not included.  
They can be regenerated using the provided ingestion scripts.

## 📌 Future Improvements
- Vendor profitability prediction using ML
- Automated anomaly detection for losses
- Time-series forecasting for sales
- Integration with real-time databases
