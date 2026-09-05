USE ecommerce_sales_db;


WITH monthly AS (
    SELECT 
        Year,
        Month,
        Month_Name,
        SUM(Amount) AS Revenue
    FROM orders_cleaned
    GROUP BY Year, Month, Month_Name
)
SELECT 
    *,
    LAG(Revenue) OVER (ORDER BY Year, Month) AS PrevMonthRevenue,
    ROUND(
        (Revenue - LAG(Revenue) OVER (ORDER BY Year, Month))
        / LAG(Revenue) OVER (ORDER BY Year, Month) * 100,
        2
    ) AS MoM_Growth_Percent
FROM monthly
ORDER BY Year, Month;

WITH monthly AS (
    SELECT 
        Year,
        Month,
        SUM(Amount) AS Revenue
    FROM orders_cleaned
    GROUP BY Year, Month
)
SELECT 
    *,
    LAG(Revenue) OVER (PARTITION BY Month ORDER BY Year) AS PrevYearRevenue,
    ROUND(
        (Revenue - LAG(Revenue) OVER (PARTITION BY Month ORDER BY Year))
        / LAG(Revenue) OVER (PARTITION BY Month ORDER BY Year) * 100,
        2
    ) AS YoY_Growth_Percent
FROM monthly
ORDER BY Year, Month;






SELECT 
    OrderDate,
    SUM(Amount) AS DailyRevenue,
    SUM(SUM(Amount)) OVER (ORDER BY OrderDate) AS CumulativeRevenue
FROM orders_cleaned
GROUP BY OrderDate
ORDER BY OrderDate;



WITH state_sales AS (
    SELECT 
        State,
        SUM(Amount) AS Revenue
    FROM orders_cleaned
    GROUP BY State
)
SELECT 
    State,
    Revenue,
    ROUND(Revenue / SUM(Revenue) OVER () * 100, 2) AS ContributionPercent
FROM state_sales
ORDER BY Revenue DESC;



SELECT
    Category,
    SUM(Amount) AS Revenue,
    SUM(Profit) AS Profit,
    RANK() OVER (ORDER BY SUM(Profit) DESC) AS ProfitRank
FROM orders_cleaned
GROUP BY Category
ORDER BY ProfitRank;




SELECT
    CustomerName,
    SUM(Amount) AS LifetimeRevenue,
    COUNT(OrderID) AS TotalOrders,
    ROUND(SUM(Amount) / COUNT(OrderID), 2) AS AvgOrderValue
FROM orders_cleaned
GROUP BY CustomerName
ORDER BY LifetimeRevenue DESC;


SELECT
    CustomerName,
    SUM(Amount) AS Revenue
FROM orders_cleaned
GROUP BY CustomerName
ORDER BY Revenue DESC
LIMIT 20;




