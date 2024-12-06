-- tsql sql:
DECLARE @total_sales DECIMAL(10, 2) = 100.00;
SET @total_sales *= 1.08;
SELECT @total_sales AS Total_Sales_With_Tax;
