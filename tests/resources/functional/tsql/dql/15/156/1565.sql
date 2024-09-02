--Query type: DQL
DECLARE @order_date DATE = '1995-01-01';
DECLARE @order_datetime2 DATETIME2 = @order_date;
SELECT @order_datetime2 AS 'Order Datetime2', @order_date AS 'Order Date'
FROM (
    VALUES (1)
) AS temp_result (dummy);