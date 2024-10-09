--Query type: DQL
WITH SalesRegion AS (
    SELECT DISTINCT r_name, r_regionkey
    FROM (
        VALUES ('North', 1), ('South', 2), ('East', 3), ('West', 4)
    ) AS region(r_name, r_regionkey)
),
SalesNation AS (
    SELECT DISTINCT n_name, n_nationkey, n_regionkey
    FROM (
        VALUES ('USA', 1, 1), ('Canada', 2, 1), ('Mexico', 3, 2)
    ) AS nation(n_name, n_nationkey, n_regionkey)
),
SalesCustomer AS (
    SELECT DISTINCT c_name, c_nationkey, c_custkey
    FROM (
        VALUES ('Customer1', 1, 1), ('Customer2', 2, 2), ('Customer3', 3, 3)
    ) AS customer(c_name, c_nationkey, c_custkey)
),
Orders AS (
    SELECT DISTINCT o_orderkey, o_custkey, o_orderdate, o_totalprice
    FROM (
        VALUES (1, 1, '2020-01-01', 100.00), (2, 2, '2020-01-02', 200.00), (3, 3, '2020-01-03', 300.00)
    ) AS orders(o_orderkey, o_custkey, o_orderdate, o_totalprice)
),
Lineitem AS (
    SELECT DISTINCT l_orderkey, l_custkey, l_extendedprice
    FROM (
        VALUES (1, 1, 100.00), (2, 2, 200.00), (3, 3, 300.00)
    ) AS lineitem(l_orderkey, l_custkey, l_extendedprice)
)
SELECT DISTINCT T4.n_name,
    MIN(T1.o_totalprice) OVER (PARTITION BY T4.n_nationkey) AS MinOrderTotal,
    MAX(T1.o_totalprice) OVER (PARTITION BY T4.n_nationkey) AS MaxOrderTotal,
    AVG(T1.o_totalprice) OVER (PARTITION BY T4.n_nationkey) AS AvgOrderTotal,
    COUNT(T1.o_orderkey) OVER (PARTITION BY T4.n_nationkey) AS OrdersPerNation
FROM Orders AS T1
JOIN Lineitem AS T2 ON T1.o_orderkey = T2.l_orderkey
JOIN SalesCustomer AS T3 ON T2.l_custkey = T3.c_custkey
JOIN SalesNation AS T4 ON T3.c_nationkey = T4.n_nationkey
JOIN SalesRegion AS T5 ON T4.n_regionkey = T5.r_regionkey
WHERE T1.o_orderdate IS NOT NULL
ORDER BY T4.n_name