-- tsql sql:
SET DATEFIRST 3;

WITH temp_customer AS (
    SELECT *
    FROM (
        VALUES
            (1, 'Customer1', 100.00, 'Address1', 'Phone1', 'Comment1'),
            (2, 'Customer2', 200.00, 'Address2', 'Phone2', 'Comment2')
    ) AS customer (c_custkey, c_name, c_acctbal, c_address, c_phone, c_comment)
),

    temp_orders AS (
    SELECT *
    FROM (
        VALUES
            (1, 1, 1000.00),
            (2, 1, 2000.00)
    ) AS orders (o_orderkey, o_custkey, o_totalprice)
),

    temp_lineitem AS (
    SELECT *
    FROM (
        VALUES
            (1, 1, 10.00, 0.1, 1),
            (2, 1, 20.00, 0.2, 2)
    ) AS lineitem (l_orderkey, l_extendedprice, l_discount, l_suppkey, l_linenumber)
),

    temp_nation AS (
    SELECT *
    FROM (
        VALUES
            (1, 'Nation1'),
            (2, 'Nation2')
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
    temp_customer c
    INNER JOIN temp_orders o ON c.c_custkey = o.o_custkey
    INNER JOIN temp_lineitem l ON o.o_orderkey = l.l_orderkey
    INNER JOIN temp_nation n ON c.c_custkey = n.n_nationkey
WHERE
    c.c_acctbal > 0.00
    AND l.l_orderkey IN (
        SELECT l_orderkey
        FROM temp_lineitem
        GROUP BY l_orderkey
        HAVING SUM(l_extendedprice * (1 - l_discount)) > 100000.00
    )
GROUP BY
    c.c_custkey,
    c.c_name,
    c.c_acctbal,
    n.n_name,
    c.c_address,
    c.c_phone,
    c.c_comment
ORDER BY
    revenue DESC
