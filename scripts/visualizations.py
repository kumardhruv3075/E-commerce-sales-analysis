import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Enable a clean style
sns.set(style="whitegrid")

# -----------------------------
# Paths
# -----------------------------
BASE_OUTPUT = r"outputs"
PLOTS_DIR = r"outputs/plots"

os.makedirs(PLOTS_DIR, exist_ok=True)

# -----------------------------------
# Step 1: Load Processed CSVs
# -----------------------------------
monthly_df = pd.read_csv(f"{BASE_OUTPUT}/monthly_trends.csv")
category_df = pd.read_csv(f"{BASE_OUTPUT}/category_sales.csv")
state_df = pd.read_csv(f"{BASE_OUTPUT}/state_sales.csv")
top_customers_df = pd.read_csv(f"{BASE_OUTPUT}/top_customers.csv")

# Ensure Month is sorted properly
monthly_df["Month"] = pd.to_datetime(monthly_df["Month"], format="%Y-%m", errors="coerce")
monthly_df = monthly_df.sort_values("Month")

# ---------------------------------------------------
# Plot 1: Monthly Sales Trend (Line Chart)
# ---------------------------------------------------
plt.figure(figsize=(10, 5))
plt.plot(monthly_df["Month_Name"], monthly_df["Total_Sales"], marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{PLOTS_DIR}/monthly_sales_trend.png")
plt.close()

# ---------------------------------------------------
# Plot 2: Category-wise Sales (Bar Chart)
# ---------------------------------------------------
plt.figure(figsize=(10, 5))
sns.barplot(data=category_df, x="Category", y="Amount")
plt.title("Category-wise Sales")
plt.xlabel("Category")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{PLOTS_DIR}/category_sales.png")
plt.close()

# ---------------------------------------------------
# Plot 3: State-wise Sales (Horizontal Bar)
# ---------------------------------------------------
plt.figure(figsize=(10, 6))
state_df_sorted = state_df.sort_values("Amount", ascending=False)

sns.barplot(data=state_df_sorted, x="Amount", y="State")
plt.title("State-wise Sales")
plt.xlabel("Sales")
plt.ylabel("State")
plt.tight_layout()
plt.savefig(f"{PLOTS_DIR}/state_sales.png")
plt.close()

# ---------------------------------------------------
# Plot 4: Top Customers (Bar Chart)
# ---------------------------------------------------
plt.figure(figsize=(10, 6))
sns.barplot(data=top_customers_df, x="Amount", y="CustomerName")
plt.title("Top 10 Customers by Spend")
plt.xlabel("Total Spent")
plt.ylabel("Customer")
plt.tight_layout()
plt.savefig(f"{PLOTS_DIR}/top_customers.png")
plt.close()

print("✅ All visualizations created successfully! Check the outputs/plots folder.")


# ----------------------------
# Profit plots (append at end of visualizations.py)
# ----------------------------

# Category Profit (bar)
cat_profit = pd.read_csv("outputs/category_profitability.csv")
plt.figure(figsize=(10,5))
sns.barplot(data=cat_profit.sort_values("Total_Profit", ascending=False), 
            x="Category", y="Total_Profit")
plt.title("Category-wise Total Profit")
plt.xlabel("Category")
plt.ylabel("Total Profit")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/plots/category_profit.png", dpi=200)
plt.close()

# State Profit (horizontal bar)
st_profit = pd.read_csv("outputs/state_profitability.csv")
st_sorted = st_profit.sort_values("Total_Profit", ascending=False)
plt.figure(figsize=(10,8))
sns.barplot(data=st_sorted, x="Total_Profit", y="State")
plt.title("State-wise Total Profit")
plt.xlabel("Total Profit")
plt.ylabel("State")
plt.tight_layout()
plt.savefig("outputs/plots/state_profit.png", dpi=200)
plt.close()

# Monthly Profit Trend (line)
monthly_profit = pd.read_csv("outputs/monthly_profit_trend.csv")
# create a datetime column for sorted plotting
monthly_profit["Month_DT"] = pd.to_datetime(monthly_profit["Year"].astype(str) + "-" + monthly_profit["Month"].astype(str) + "-01")
monthly_profit = monthly_profit.sort_values("Month_DT")
plt.figure(figsize=(10,5))
sns.lineplot(data=monthly_profit, x="Month_DT", y="Total_Profit", marker="o")
plt.title("Monthly Total Profit Trend")
plt.xlabel("Month")
plt.ylabel("Total Profit")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/plots/monthly_profit_trend.png", dpi=200)
plt.close()

