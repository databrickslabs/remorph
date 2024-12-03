--Query type: DQL
WITH CustomerCTE AS (
    SELECT c_nationkey, SUM(o_totalprice) AS TotalRevenue
    FROM customer c
    INNER JOIN orders o ON c.c_custkey = o.o_custkey
    GROUP BY c_nationkey
)
SELECT c_nationkey, TotalRevenue
FROM CustomerCTE
GROUP BY GROUPING SETS (
    c_nationkey,
    ()
);
