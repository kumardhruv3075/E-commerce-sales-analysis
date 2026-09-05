Use ecommerce_sales_db;

CREATE TABLE monthly_summary (
    Year INT,
    Month INT,
    Month_Name VARCHAR(20),
    Total_Sales DECIMAL(12,2),
    Total_Profit DECIMAL(12,2),
    Total_Quantity INT
);

INSERT INTO monthly_summary (Year, Month, Month_Name, Total_Sales, Total_Profit, Total_Quantity)
SELECT 
    Year,
    Month,
    Month_Name,
    SUM(Amount) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    SUM(Quantity) AS Total_Quantity
FROM orders_cleaned
GROUP BY Year, Month, Month_Name
ORDER BY Year, Month;


SELECT * FROM monthly_summary ORDER BY Year, Month;

