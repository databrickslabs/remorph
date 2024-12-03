--Query type: DCL
WITH customer_data AS (
    SELECT 1 AS c_custkey, 'Customer1' AS c_name, 100.00 AS c_acctbal, '123 Main St' AS c_address, '123-456-7890' AS c_phone, 'Comment1' AS c_comment, 1 AS c_nationkey
    UNION ALL
    SELECT 2, 'Customer2', 200.00, '456 Elm St', '987-654-3210', 'Comment2', 2
),
order_data AS (
    SELECT 1 AS o_orderkey, 1 AS o_custkey, '1993-10-01' AS o_orderdate, '1993-10-01' AS l_shipdate
    UNION ALL
    SELECT 2, 1, '1993-11-01', '1993-11-01'
    UNION ALL
    SELECT 3, 2, '1993-12-01', '1993-12-01'
),
lineitem_data AS (
    SELECT 1 AS l_orderkey, 1 AS l_linenumber, 100.00 AS l_extendedprice, 0.10 AS l_discount
    UNION ALL
    SELECT 2, 1, 200.00, 0.20
    UNION ALL
    SELECT 3, 2, 300.00, 0.30
),
nation_data AS (
    SELECT 1 AS n_nationkey, 'USA' AS n_name
    UNION ALL
    SELECT 2, 'Canada'
)
SELECT c.c_custkey, c.c_name, SUM(l.l_extendedprice * (1 - l.l_discount)) AS revenue, c.c_acctbal, n.n_name, c.c_address, c.c_phone, c.c_comment
FROM customer_data c
JOIN order_data o ON c.c_custkey = o.o_custkey
JOIN lineitem_data l ON o.o_orderkey = l.l_orderkey
JOIN nation_data n ON c.c_nationkey = n.n_nationkey
WHERE c.c_acctbal > 0.00 AND o.l_shipdate >= '1993-10-01' AND o.l_shipdate < '1994-01-01'
GROUP BY c.c_custkey, c.c_name, c.c_acctbal, c.c_phone, n.n_name, c.c_address, c.c_comment
ORDER BY revenue DESC;
