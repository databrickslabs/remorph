-- tsql sql:
DECLARE @order_time TIME(4) = '14:30:00.0000';
DECLARE @order_datetime DATETIME = @order_time;
SELECT @order_time AS [Order Time], @order_datetime AS [Order Datetime]
FROM (VALUES (1)) AS temp_table(order_id);
