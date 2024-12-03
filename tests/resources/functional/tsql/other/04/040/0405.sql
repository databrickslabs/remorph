--Query type: DDL
WITH customer AS (
    SELECT *
    FROM #customer
),
orders AS (
    SELECT *
    FROM #orders
),
lineitem AS (
    SELECT *
    FROM #lineitem
),
nation AS (
    SELECT *
    FROM #nation
),
region AS (
    SELECT *
    FROM #region
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
    customer c
    INNER JOIN orders o ON c.c_custkey = o.o_custkey
    INNER JOIN lineitem l ON o.o_orderkey = l.l_orderkey
    INNER JOIN nation n ON c.c_nationkey = n.n_nationkey
    INNER JOIN region r ON n.n_regionkey = r.r_regionkey
WHERE
    o.o_orderdate >= '1994-01-01'
    AND l.l_shipdate > '1996-01-01'
    AND r.r_name = 'North America'
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
