# E-Commerce Analytics (India)

A complete end-to-end data analytics project based on Indian e-commerce sales data.

A complete Data Analytics + BI + SQL + Python project built using:

Python (Pandas, Matplotlib, Seaborn, ReportLab)
Power BI (Dashboards & KPIs)
MySQL (Analytics, Tables, Views, Stored Procedures)
Jupyter Notebook
Automated PDF Reporting

This project analyzes real Indian e-commerce sales data, covering cleaning, merging, feature engineering, SQL analytics, BI dashboards, and automated reporting.


## Objectives

✔ Clean raw e-commerce datasets
✔ Generate new features (Month, Quarter, Weekday, etc.)
✔ Create merged master dataset
✔ Perform exploratory sales analysis
✔ Build dynamic Power BI Dashboard
✔ Build SQL analytics layer for business queries
✔ Automate PDF reports
✔ Package everything for portfolio deployment

## Tools Used

- Python (Pandas, NumPy)
- SQL (MySQL)
- Matplotlib / Seaborn
- PowerBi
- Jupyter Notebook
- VS Code

---

Install Required Libraries

| Library                | Why Needed               |
| ---------------------- | ------------------------ |
| pandas                 | data cleaning + analysis |
| numpy                  | numerical ops            |
| matplotlib             | charts                   |
| seaborn                | better visualizations    |
| mysql-connector-python | Python ↔ MySQL           |
| sqlalchemy             | future proof SQL engine  |
| jupyter                | run notebooks            |

---


## Dataset
**Source:** Kaggle – Indian E-Commerce Sales Dataset

### Original Input Files
- `List of Orders.csv`
- `Order Details.csv`
- `Sales target.csv`

### Processed Dataset
- `merged_orders_cleaned.csv`  
  Created by merging and cleaning the above three files using Python.  
  **All further analysis (Python, SQL, Power BI) is performed on this merged dataset.**

---

## Tech Stack
- **Python 3.13.9**
  - Pandas, NumPy
  - Matplotlib, Seaborn
- **SQL**
  - Advanced queries
  - Views and stored procedures
- **Power BI**
  - Interactive dashboards and KPIs
- **Jupyter Notebook**

---

## Project Workflow
1. **Data Cleaning & Feature Engineering**
   - Merged multiple raw CSV files
   - Date standardization and time-based features (Year, Month, Quarter, Weekday)
2. **Exploratory Data Analysis**
   - Sales, profit, quantity trends
   - Category, sub-category, and state-level analysis
3. **Advanced SQL Analytics**
   - Analytical queries, views, and stored procedures
4. **Automated Visualizations**
   - Python-based charts saved programmatically
5. **Power BI Dashboard**
   - Interactive KPIs and business-focused visuals

---

## Key Business Questions Answered
- How do sales and profit trend across months and quarters?
- Which product categories and sub-categories are most profitable?
- Which states and regions contribute the most to revenue?
- Who are the top customers by revenue?
- How do actual sales compare against predefined targets?

---

## Key Insights
- A small number of states contribute a significant share of total revenue
- Certain categories generate high sales but relatively lower profit margins
- Clear seasonality is visible in monthly sales and profit trends
- Sales and profit do not always move together, highlighting pricing and cost factors

---

## Dashboards & Visuals
- **Power BI Dashboard**: Sales KPIs, trends, category and state-wise performance
- **Python Visualizations**:
  - Monthly sales & profit trends
  - Category-wise and state-wise performance
  - Customer contribution analysis

(Refer to the `outputs/plots/` and `PowerBi/` directories)

---

## Repository Structure

indian-ecommerce-sales-analysis/
│
├── data/ # Raw and cleaned datasets
├── notebooks/ # Jupyter analysis notebook
├── scripts/ # Python analysis & visualization scripts
├── sql/ # SQL queries, views, procedures
├── outputs/ # CSV insights, plots, PDF report
├── PowerBi/ # Power BI dashboard (.pbix)
├── README.md
└── requirements.txt

---

## How to Run
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run data analysis:
   scripts/analysis.py
4. Generate visualizations:
   scripts/visualizations.py
5. Open the Power BI dashboard from - PowerBi/
