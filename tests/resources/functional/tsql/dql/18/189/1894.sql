-- tsql sql:
DECLARE @order_time TIME(4) = '12:15:04.1237';
DECLARE @order_datetimeoffset DATETIMEOFFSET(3) = @order_time;

WITH temp_result AS (
    SELECT @order_time AS [Order Time], @order_datetimeoffset AS [Order Datetimeoffset]
)
SELECT *
FROM temp_result;
