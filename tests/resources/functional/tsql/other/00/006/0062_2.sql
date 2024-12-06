-- tsql sql:
WITH customers AS (
    SELECT c_custkey, c_name
    FROM (
        VALUES (1, 'Customer1'),
               (2, 'Customer2')
    ) AS customers (c_custkey, c_name)
),
orders AS (
    SELECT o_orderkey, c_custkey, o_orderdate
    FROM (
        VALUES (1, 1, '2020-01-01'),
               (2, 2, '2020-01-15')
    ) AS orders (o_orderkey, c_custkey, o_orderdate)
)
SELECT c.c_custkey, c.c_name, o.o_orderkey, o.o_orderdate
FROM customers c
JOIN orders o ON c.c_custkey = o.c_custkey;
