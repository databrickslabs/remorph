-- tsql sql:
DECLARE @order_time TIME(4) = '12:15:04.1237';
DECLARE @order_datetime2 DATETIME2(3) = @order_time;
WITH derivedTable AS (
    SELECT @order_datetime2 AS order_datetime2, @order_time AS order_time
)
SELECT order_datetime2, order_time
FROM derivedTable;
