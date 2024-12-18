-- tsql sql:
WITH customer AS (
    SELECT * FROM (VALUES
        (1, 'Customer1', 100.0, '123 Main St', '123-456-7890', 'Comment1', 1),
        (2, 'Customer2', 200.0, '456 Elm St', '987-654-3210', 'Comment2', 2)
    ) AS customer(c_custkey, c_name, c_acctbal, c_address, c_phone, c_comment, c_nationkey)
),
orders AS (
    SELECT * FROM (VALUES
        (1, 1, '2020-01-01'),
        (2, 2, '2020-01-15')
    ) AS orders(o_orderkey, o_custkey, o_orderdate)
),
lineitem AS (
    SELECT * FROM (VALUES
        (1, 1, 10.0, 0.1, 'R'),
        (2, 2, 20.0, 0.2, 'R')
    ) AS lineitem(l_orderkey, l_partkey, l_extendedprice, l_discount, l_returnflag)
),
nation AS (
    SELECT * FROM (VALUES
        (1, 'USA'),
        (2, 'Canada')
    ) AS nation(n_nationkey, n_name)
),
temp_result AS (
    SELECT
        c.c_custkey AS custkey,
        c.c_name AS name,
        l.l_extendedprice AS extendedprice,
        l.l_discount AS discount,
        c.c_acctbal AS acctbal,
        n.n_name AS nation,
        c.c_address AS address,
        c.c_phone AS phone,
        c.c_comment AS comment
    FROM customer c
    INNER JOIN orders o ON c.c_custkey = o.o_custkey
    INNER JOIN lineitem l ON o.o_orderkey = l.l_orderkey
    INNER JOIN nation n ON c.c_nationkey = n.n_nationkey
    WHERE l.l_returnflag = 'R'
)
SELECT
    custkey,
    name,
    SUM(extendedprice * (1 - discount)) AS revenue,
    acctbal,
    nation,
    address,
    phone,
    comment
FROM temp_result
GROUP BY
    custkey,
    name,
    acctbal,
    phone,
    nation,
    address,
    comment
ORDER BY revenue DESC;
