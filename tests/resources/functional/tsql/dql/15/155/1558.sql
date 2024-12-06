-- tsql sql:
DECLARE @order_date DATETIME2 = '2020-04-15 21:22:11';
SELECT DATE_BUCKET(WEEK, 5, CAST(o_orderdate AS DATETIME2)) AS order_week
FROM (
    VALUES ('2020-04-15 21:22:11'), ('2020-04-20 21:22:11'), ('2020-04-25 21:22:11')
) AS orders (o_orderdate);
