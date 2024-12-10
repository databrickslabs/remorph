-- tsql sql:
WITH SupplierRevenue AS (
    SELECT s_suppkey, SUM(l_extendedprice * (1 - l_discount)) AS revenue
    FROM (
        VALUES ('s1', 100, 0.1), ('s2', 200, 0.2)
    ) AS lineitem(s_suppkey, l_extendedprice, l_discount)
    GROUP BY s_suppkey
) -- Calculates total revenue for each supplier
SELECT * FROM SupplierRevenue;
