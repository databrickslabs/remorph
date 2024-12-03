--Query type: DDL
WITH customer AS (
    SELECT c_custkey, c_name, c_acctbal, c_address, c_phone, c_comment, c_nationkey
    FROM (
        VALUES
            (1, 'Customer1', 100.00, '123 Main St', '123-456-7890', 'Comment1', 1),
            (2, 'Customer2', 200.00, '456 Elm St', '987-654-3210', 'Comment2', 2)
    ) AS customer (c_custkey, c_name, c_acctbal, c_address, c_phone, c_comment, c_nationkey)
),
orders AS (
    SELECT o_orderkey, o_custkey, o_totalprice
    FROM (
        VALUES
            (1, 1, 100.00),
            (2, 2, 200.00)
    ) AS orders (o_orderkey, o_custkey, o_totalprice)
),
lineitem AS (
    SELECT l_orderkey, l_extendedprice, l_discount
    FROM (
        VALUES
            (1, 10.00, 0.1),
            (2, 20.00, 0.2)
    ) AS lineitem (l_orderkey, l_extendedprice, l_discount)
),
nation AS (
    SELECT n_nationkey, n_name
    FROM (
        VALUES
            (1, 'USA'),
            (2, 'Canada')
    ) AS nation (n_nationkey, n_name)
)
SELECT
    c.c_custkey,
    c.c_name,
    COALESCE(SUM(l.l_extendedprice * (1 - l.l_discount)), 0) AS revenue,
    c.c_acctbal,
    n.n_name,
    c.c_address,
    c.c_phone,
    c.c_comment
FROM
    customer c
    LEFT JOIN orders o ON c.c_custkey = o.o_custkey
    LEFT JOIN lineitem l ON o.o_orderkey = l.l_orderkey
    LEFT JOIN nation n ON c.c_nationkey = n.n_nationkey
WHERE
    c.c_acctbal > 0.00
GROUP BY
    c.c_custkey,
    c.c_name,
    c.c_acctbal,
    c.c_phone,
    n.n_name,
    c.c_address,
    c.c_comment
ORDER BY
    revenue DESC;
