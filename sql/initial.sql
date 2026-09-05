SELECT * FROM ecommerce_sales_db.orders_cleaned;

SELECT SUM(Amount) AS TotalRevenue
FROM orders_cleaned;

SELECT SUM(Profit) AS TotalProfit
FROM orders_cleaned;

SELECT SUM(Quantity) AS TotalQuantity
FROM orders_cleaned;


SELECT Year, Month, Month_Name,
    SUM(Amount) AS MonthlyRevenue
FROM orders_cleaned
GROUP BY Year, Month, Month_Name
ORDER BY Year, Month ASC;


SELECT 
    State,
    SUM(Amount) AS TotalRevenue,
    SUM(Profit) AS TotalProfit
FROM orders_cleaned
GROUP BY State
ORDER BY TotalRevenue DESC;


SELECT CustomerName,
SUM(Amount) AS Revenue
FROM orders_cleaned
GROUP BY CustomerName
ORDER BY Revenue DESC
LIMIT 10;

SELECT 
    Category,
    SubCategory,
    SUM(Amount) AS TotalRevenue,
    SUM(Profit) AS TotalProfit
FROM orders_cleaned
GROUP BY Category, SubCategory
ORDER BY TotalProfit DESC;

SELECT 
    OrderDate,
    SUM(Amount) AS DailyRevenue
FROM orders_cleaned
GROUP BY OrderDate
ORDER BY OrderDate;
