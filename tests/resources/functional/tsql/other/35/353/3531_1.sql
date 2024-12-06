-- tsql sql:
WITH orders AS (
    SELECT o_totalprice, o_orderdate, o_custkey, o_suppkey
    FROM (
        VALUES (100000, '1995-01-01', 1, 1)
    ) AS orders(o_totalprice, o_orderdate, o_custkey, o_suppkey)
),

    customer AS (
    SELECT c_custkey, c_nationkey
    FROM (
        VALUES (1, 1)
    ) AS customer(c_custkey, c_nationkey)
),

    supplier AS (
    SELECT s_suppkey, s_nationkey
    FROM (
        VALUES (1, 1)
    ) AS supplier(s_suppkey, s_nationkey)
)

SELECT SUM(o.o_totalprice) AS total_revenue
FROM orders o
JOIN customer c ON o.o_custkey = c.c_custkey
JOIN supplier s ON o.o_suppkey = s.s_suppkey
WHERE o.o_orderdate >= '1995-01-01' AND o.o_orderdate < '1996-01-01';
