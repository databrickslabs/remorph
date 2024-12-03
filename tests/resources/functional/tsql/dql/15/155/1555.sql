--Query type: DQL
DECLARE @order_date DATETIME = GETDATE();

WITH orders AS (
    SELECT 1 AS o_orderkey, '2022-01-01' AS o_orderdate
    UNION ALL
    SELECT 2 AS o_orderkey, '2022-02-01' AS o_orderdate
),
lineitem AS (
    SELECT 1 AS l_orderkey, 1 AS l_linenumber
    UNION ALL
    SELECT 2 AS l_orderkey, 2 AS l_linenumber
)

SELECT EOMONTH(@order_date) AS 'This Month',
       EOMONTH(@order_date, 1) AS 'Next Month',
       EOMONTH(@order_date, -1) AS 'Last Month'
FROM orders
INNER JOIN lineitem ON orders.o_orderkey = lineitem.l_orderkey
