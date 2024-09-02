--Query type: DCL
WITH customer_data AS (
    SELECT *
    FROM (
        VALUES
            (1, 'Customer1', 100.00, '123 Main St', '123-456-7890', 'Comment1'),
            (2, 'Customer2', 200.00, '456 Elm St', '987-654-3210', 'Comment2')
    ) AS cust (c_custkey, c_name, c_acctbal, c_address, c_phone, c_comment)
),
order_data AS (
    SELECT *
    FROM (
        VALUES
            (1, 1, '1993-10-01'),
            (2, 1, '1993-11-01'),
            (3, 2, '1993-12-01')
    ) AS ord (o_orderkey, o_custkey, o_orderdate)
),
lineitem_data AS (
    SELECT *
    FROM (
        VALUES
            (1, 1, 100.00, 0.10),
            (2, 1, 200.00, 0.20),
            (3, 2, 300.00, 0.30)
    ) AS line (l_orderkey, l_linenumber, l_extendedprice, l_discount)
),
nation_data AS (
    SELECT *
    FROM (
        VALUES
            (1, 'USA'),
            (2, 'Canada')
    ) AS nation (n_nationkey, n_name)
)
SELECT
    c.c_custkey,
    c.c_name,
    SUM(l.l_extendedprice * (1 - l.l_discount)) AS revenue,
    c.c_acctbal,
    n.n_name,
    c.c_address,
    c.c_phone,
    c.c_comment
FROM
    customer_data c
    INNER JOIN order_data o ON c.c_custkey = o.o_custkey
    INNER JOIN lineitem_data l ON o.o_orderkey = l.l_orderkey
    INNER JOIN nation_data n ON c.c_custkey = n.n_nationkey
WHERE
    c.c_acctbal > 0.00
    AND o.o_orderdate >= '1993-10-01'
    AND o.o_orderdate < '1994-01-01'
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