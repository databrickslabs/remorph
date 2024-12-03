--Query type: DQL
DECLARE @order_date DATE = '1995-01-01';
DECLARE @order_datetime2 DATETIME2(3) = @order_date;
SELECT *
FROM (
    VALUES (@order_date, @order_datetime2)
) AS temp_result (OrderDate, OrderDatetime2);
