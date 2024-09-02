--Query type: DDL
WITH CustomerOrders AS (
    SELECT c_custkey, c_nationkey, o_orderkey
    FROM (
        VALUES (1, 2, 3), (4, 5, 6)
    ) AS CustomerOrders (c_custkey, c_nationkey, o_orderkey)
)
SELECT *
FROM CustomerOrders
WHERE c_nationkey = 2;