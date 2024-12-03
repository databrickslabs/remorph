--Query type: DQL
DECLARE @o_orderdate datetime = '1998-03-04';
DECLARE @o_shippriority datetime = '1998-03-04 10:10:05';
WITH cte AS (
    SELECT @o_orderdate AS order_date, @o_shippriority AS ship_priority
)
SELECT
    DATETRUNC(month, order_date) AS order_month,
    DATETRUNC(second, order_date) AS order_second,
    DATETRUNC(second, order_date) AS order_second_var,
    DATETRUNC(minute, ship_priority) AS ship_minute_var
FROM cte
