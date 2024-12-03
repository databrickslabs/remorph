--Query type: DQL
DECLARE @order_date DATETIME2 = '2020-04-30 00:00:00';
SELECT DATE_BUCKET(DAY, 2147483648, @order_date)
FROM (
    VALUES (@order_date)
) AS dates(order_date);
