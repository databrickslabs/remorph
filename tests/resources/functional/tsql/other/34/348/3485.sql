-- tsql sql:
WITH customer_data AS (
    SELECT 1 AS c_custkey, 'Customer1' AS c_name, 100.00 AS c_acctbal, 'Address1' AS c_address, 'Phone1' AS c_phone, 'Comment1' AS c_comment, 1 AS c_nationkey
    UNION ALL
    SELECT 2, 'Customer2', 200.00, 'Address2', 'Phone2', 'Comment2', 2
),
order_data AS (
    SELECT 1 AS o_orderkey, 1 AS o_custkey, 1000.00 AS o_totalprice
    UNION ALL
    SELECT 2, 1, 2000.00
),
lineitem_data AS (
    SELECT 1 AS l_orderkey, 1 AS l_linenumber, 10.00 AS l_extendedprice, 0.1 AS l_discount
    UNION ALL
    SELECT 2, 1, 20.00, 0.2
),
nation_data AS (
    SELECT 1 AS n_nationkey, 'Nation1' AS n_name
    UNION ALL
    SELECT 2, 'Nation2'
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
JOIN
    order_data o ON c.c_custkey = o.o_custkey
JOIN
    lineitem_data l ON o.o_orderkey = l.l_orderkey
JOIN
    nation_data n ON c.c_nationkey = n.n_nationkey
WHERE
    c.c_acctbal > 0.00
    AND l.l_orderkey IN (
        SELECT l_orderkey
        FROM lineitem_data
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
    revenue DESC;
