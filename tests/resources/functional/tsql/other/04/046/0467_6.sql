--Query type: DCL
DECLARE @total_sales DECIMAL;
SET @total_sales = 1000.00;
WITH Sales_Report AS (
    SELECT 'Total Sales: ' + CONVERT(VARCHAR, @total_sales) AS Sales_Report
)
SELECT * FROM Sales_Report;