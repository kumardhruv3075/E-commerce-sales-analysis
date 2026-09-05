USE ecommerce_sales_db;

DELIMITER $$

CREATE PROCEDURE get_yearly_summary(IN input_year INT)
BEGIN
    SELECT 
        SUM(Amount) AS total_sales,
        SUM(Profit) AS total_profit,
        SUM(Quantity) AS total_quantity
    FROM orders_cleaned
    WHERE Year = input_year;
END $$

DELIMITER ;


CALL get_yearly_summary(2018);
