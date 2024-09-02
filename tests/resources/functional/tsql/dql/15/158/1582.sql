--Query type: DQL
DECLARE @months INT = 12, @order_date DATETIME = '1995-01-01 01:01:01.111';
SELECT DATEADD(month, @months, o_orderdate) AS new_order_date
FROM (
    VALUES ('1995-01-01 01:01:01.111')
) AS orders(o_orderdate);