--Query type: DQL
WITH OrderDetails AS (
    SELECT o_orderkey, l_partkey, l_quantity
    FROM (
        VALUES (1, 1, 10),
               (1, 2, 20),
               (2, 1, 30),
               (2, 2, 40)
    ) AS OrderDetails(o_orderkey, l_partkey, l_quantity)
)
SELECT o_orderkey, l_partkey, l_quantity, DATEADD(day, SUM(l_quantity) OVER(PARTITION BY o_orderkey), SYSDATETIME()) AS 'Total'
FROM OrderDetails
WHERE o_orderkey IN (1, 2);
