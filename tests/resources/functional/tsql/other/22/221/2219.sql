--Query type: DCL
WITH SalesCTE AS (
    SELECT o_orderkey, SUM(l_extendedprice * (1 - l_discount)) AS total_revenue
    FROM (
        VALUES ('o_orderkey', 'l_extendedprice', 'l_discount')
    ) AS lineitem(o_orderkey, l_extendedprice, l_discount)
    GROUP BY o_orderkey
),
CustomerCTE AS (
    SELECT c_custkey, c_name, c_nationkey
    FROM (
        VALUES ('c_custkey', 'c_name', 'c_nationkey')
    ) AS customer(c_custkey, c_name, c_nationkey)
)
SELECT TOP 10 c_name, c_nationkey, total_revenue, ROW_NUMBER() OVER (PARTITION BY c_nationkey ORDER BY total_revenue DESC) AS row_num
FROM SalesCTE
JOIN CustomerCTE ON SalesCTE.o_orderkey = CustomerCTE.c_custkey
GROUP BY c_name, c_nationkey, total_revenue
HAVING SUM(total_revenue) > 1000000
ORDER BY c_nationkey, total_revenue DESC
