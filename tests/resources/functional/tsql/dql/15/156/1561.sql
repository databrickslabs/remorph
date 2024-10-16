--Query type: DQL
DECLARE @order_date DATETIME2 = '2020-06-15 21:22:11';
DECLARE @origin_date DATETIME2 = '2019-01-01 00:00:00';

SELECT DATE_BUCKET(HOUR, 2, o_orderdate, @origin_date) AS order_bucket
FROM (
    VALUES (CAST('2020-06-15 21:22:11' AS DATETIME2)),
           (CAST('2020-06-15 22:22:11' AS DATETIME2)),
           (CAST('2020-06-15 23:22:11' AS DATETIME2))
) AS o (o_orderdate);