import os
import pandas as pd
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# -----------------------------
# Paths & Setup
# -----------------------------
OUTPUT_DIR = "outputs"
PLOTS_DIR = os.path.join(OUTPUT_DIR, "plots")
REPORT_PATH = os.path.join(OUTPUT_DIR, "Ecommerce_Enhanced_Report.pdf")

# helper to format rupee numbers
def rupee(x):
    try:
        return "₹{:,.0f}".format(float(x))
    except Exception:
        return str(x)

# Load base CSVs (safe)
def safe_read_csv(path):
    if not os.path.exists(path):
        print(f"Warning: file not found -> {path}")
        return None
    return pd.read_csv(path)

monthly_df = safe_read_csv(os.path.join(OUTPUT_DIR, "monthly_trends.csv"))
category_df = safe_read_csv(os.path.join(OUTPUT_DIR, "category_sales.csv"))
state_df = safe_read_csv(os.path.join(OUTPUT_DIR, "state_sales.csv"))
customers_df = safe_read_csv(os.path.join(OUTPUT_DIR, "top_customers.csv"))

# If any of those are None, try to exit gracefully later
# Add ranking to customers if available
if customers_df is not None:
    customers_df = customers_df.sort_values("Amount", ascending=False).reset_index(drop=True)
    customers_df.insert(0, "Rank", range(1, len(customers_df) + 1))

# Styles
styles = getSampleStyleSheet()
title_style = styles["Heading1"]
section_style = styles["Heading2"]
body_style = ParagraphStyle(
    name="Body",
    parent=styles["BodyText"],
    fontSize=10,
    leading=13
)

# Helper: Convert DF -> Table with styles
def df_to_table(df, col_formats=None, col_widths=None):
    """
    df: pandas DataFrame
    col_formats: dict colname -> formatting function (e.g. rupee)
    col_widths: list of column widths or None
    """
    if df is None:
        return Paragraph("No data available.", body_style)

    # Prepare table data
    header = list(df.columns)
    rows = df.values.tolist()

    # format values if requested
    if col_formats:
        formatted_rows = []
        for r in rows:
            fr = []
            for i, v in enumerate(r):
                col = header[i]
                if col in col_formats and pd.notna(v):
                    try:
                        fr.append(col_formats[col](v))
                    except Exception:
                        fr.append(v)
                else:
                    fr.append(v)
            formatted_rows.append(fr)
        rows = formatted_rows

    table_data = [header] + rows
    table = Table(table_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.black),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("GRID", (0,0), (-1,-1), 0.25, colors.grey),
        ("BOTTOMPADDING", (0,0), (-1,0), 6),
    ]))
    return table

# Small helper to add image if exists
def add_image_if_exists(path, width=450, height=250):
    if os.path.exists(path):
        return Image(path, width=width, height=height)
    else:
        return Paragraph(f"[Image not found: {os.path.basename(path)}]", body_style)

# Generate short text insights
def monthly_insight_text(monthly_df):
    if monthly_df is None or monthly_df.empty:
        return "Monthly data not available."
    # ensure numeric sort
    try:
        best = monthly_df.loc[monthly_df["Total_Sales"].idxmax()]
        worst = monthly_df.loc[monthly_df["Total_Sales"].idxmin()]
        return (
            f"Highest sales were in <b>{best['Month_Name']} {int(best['Year'])}</b>: "
            f"{rupee(best['Total_Sales'])}. Lowest sales were in "
            f"<b>{worst['Month_Name']} {int(worst['Year'])}</b>: {rupee(worst['Total_Sales'])}."
        )
    except Exception as e:
        return "Could not compute monthly insight."

def category_insight_text(category_df):
    if category_df is None or category_df.empty:
        return "Category data not available."
    try:
        top = category_df.loc[category_df["Amount"].idxmax()]
        return f"Top category: <b>{top['Category']}</b> with sales {rupee(top['Amount'])}."
    except Exception:
        return "Could not compute category insight."

def state_insight_text(state_df):
    if state_df is None or state_df.empty:
        return "State data not available."
    try:
        top = state_df.loc[state_df["Amount"].idxmax()]
        return f"Top state: <b>{top['State']}</b> with sales {rupee(top['Amount'])}."
    except Exception:
        return "Could not compute state insight."

def customers_insight_text(customers_df):
    if customers_df is None or customers_df.empty:
        return "Customer data not available."
    try:
        top = customers_df.iloc[0]
        return f"Highest spending customer: <b>{top['CustomerName']}</b> with {rupee(top['Amount'])}."
    except Exception:
        return "Could not compute customer insight."

# Optional: load subcategory profitability files if they exist, else compute from merged cleaned data
subcat_top_path = os.path.join(OUTPUT_DIR, "subcategory_profit_top10.csv")
subcat_bottom_path = os.path.join(OUTPUT_DIR, "subcategory_profit_bottom10.csv")
subcat_top = safe_read_csv(subcat_top_path)
subcat_bottom = safe_read_csv(subcat_bottom_path)

# If subcat files missing, try computing from cleaned merged data
if subcat_top is None or subcat_bottom is None:
    merged_cleaned_path = os.path.join("data", "merged_orders_cleaned.csv")
    merged_cleaned = safe_read_csv(merged_cleaned_path)
    if merged_cleaned is not None:
        sub = merged_cleaned.groupby("Sub-Category").agg(
            Total_Sales=("Amount", "sum"),
            Total_Profit=("Profit", "sum"),
            Total_Quantity=("Quantity", "sum")
        ).reset_index()
        sub["Profit_Margin_pct"] = (sub["Total_Profit"] / sub["Total_Sales"].replace(0, pd.NA)) * 100
        sub_sorted = sub.sort_values("Total_Profit", ascending=False)
        subcat_top = sub_sorted.head(10)
        subcat_bottom = sub_sorted.tail(10).sort_values("Total_Profit")
    else:
        subcat_top = None
        subcat_bottom = None

# Build PDF
doc = SimpleDocTemplate(REPORT_PATH, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
elements = []

# Title
elements.append(Paragraph("Indian E-Commerce Sales Analysis — Enhanced Report", title_style))
elements.append(Spacer(1, 12))

# Executive summary block
elements.append(Paragraph("Executive Summary", section_style))
exec_lines = []
if monthly_df is not None:
    total_sales = monthly_df["Total_Sales"].sum()
    total_profit = monthly_df["Total_Profit"].sum()
    exec_lines.append(f"<b>Total Sales:</b> {rupee(total_sales)}")
    exec_lines.append(f"<b>Total Profit:</b> {rupee(total_profit)}")
if category_df is not None:
    try:
        top_cat = category_df.loc[category_df["Amount"].idxmax()]["Category"]
        exec_lines.append(f"<b>Top Category:</b> {top_cat}")
    except Exception:
        pass
if state_df is not None:
    try:
        top_state = state_df.loc[state_df["Amount"].idxmax()]["State"]
        exec_lines.append(f"<b>Top State:</b> {top_state}")
    except Exception:
        pass

exec_text = "<br/>".join(exec_lines) if exec_lines else "Summary data not available."
elements.append(Paragraph(exec_text, body_style))
elements.append(Spacer(1, 12))

# Monthly section (plot + table + text)
elements.append(Paragraph("1) Monthly Sales & Profit", section_style))
elements.append(Spacer(1, 6))
elements.append(Paragraph(monthly_insight_text(monthly_df), body_style))
elements.append(Spacer(1, 6))
monthly_plot = os.path.join(PLOTS_DIR, "monthly_sales_trend.png")
elements.append(add_image_if_exists(monthly_plot))
elements.append(Spacer(1, 8))
elements.append(df_to_table(monthly_df, col_formats={"Total_Sales": rupee, "Total_Profit": rupee}, col_widths=[120, 80, 80]))
elements.append(PageBreak())

# Category section
elements.append(Paragraph("2) Category Performance", section_style))
elements.append(Spacer(1, 6))
elements.append(Paragraph(category_insight_text(category_df), body_style))
elements.append(Spacer(1, 6))
cat_plot = os.path.join(PLOTS_DIR, "category_sales.png")
elements.append(add_image_if_exists(cat_plot))
elements.append(Spacer(1, 8))
elements.append(df_to_table(category_df, col_formats={"Amount": rupee, "Profit": rupee}, col_widths=[160, 80, 80]))
elements.append(PageBreak())

# State section
elements.append(Paragraph("3) State Performance", section_style))
elements.append(Spacer(1, 6))
elements.append(Paragraph(state_insight_text(state_df), body_style))
elements.append(Spacer(1, 6))
state_plot = os.path.join(PLOTS_DIR, "state_sales.png")
elements.append(add_image_if_exists(state_plot))
elements.append(Spacer(1, 8))
elements.append(df_to_table(state_df, col_formats={"Amount": rupee, "Profit": rupee}, col_widths=[160, 80, 80]))
elements.append(PageBreak())

# Sub-category profitability (if available)
elements.append(Paragraph("4) Sub-Category Profitability (Top & Bottom)", section_style))
elements.append(Spacer(1, 6))
if subcat_top is not None:
    elements.append(Paragraph("Top sub-categories by profit:", body_style))
    elements.append(df_to_table(subcat_top, col_formats={"Total_Sales": rupee, "Total_Profit": rupee, "Profit_Margin_pct": lambda x: f"{x:.1f}%"}))
    elements.append(Spacer(1, 6))
if subcat_bottom is not None:
    elements.append(Paragraph("Bottom sub-categories by profit:", body_style))
    elements.append(df_to_table(subcat_bottom, col_formats={"Total_Sales": rupee, "Total_Profit": rupee, "Profit_Margin_pct": lambda x: f"{x:.1f}%"}))
else:
    elements.append(Paragraph("Sub-category profitability data not available.", body_style))
elements.append(PageBreak())

# Top customers (ranked) with plot
elements.append(Paragraph("5) Top 10 Customers (Ranked)", section_style))
elements.append(Spacer(1, 6))
elements.append(Paragraph(customers_insight_text(customers_df), body_style))
elements.append(Spacer(1, 6))
cust_plot = os.path.join(PLOTS_DIR, "top_customers.png")
elements.append(add_image_if_exists(cust_plot))
elements.append(Spacer(1, 8))
elements.append(df_to_table(customers_df, col_formats={"Amount": rupee}, col_widths=[40, 200, 80]))
elements.append(Spacer(1, 12))

# Key insights wrap-up
elements.append(Paragraph("Key Insights & Recommendations", section_style))
insights_list = [
    "Investigate inventory & promotion strategies for the top month to replicate success.",
    "Focus paid marketing and placements on top-performing categories to maximize ROI.",
    "Consider loyalty or retention programs for top 10 customers (high revenue concentration).",
    "Review loss-making sub-categories for pricing or merchandising changes."
]
insight_text = "<br/>".join([f"• {s}" for s in insights_list])
elements.append(Paragraph(insight_text, body_style))

# Build PDF
doc.build(elements)
print("✅ Enhanced PDF generated:", REPORT_PATH)
