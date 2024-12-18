-- tsql sql:
CREATE VIEW CustomerRevenue AS
WITH customer AS (
    SELECT  1 AS c_custkey, 'Customer1' AS c_name, 100.00 AS c_acctbal, '123 Main St' AS c_address, '123-456-7890' AS c_phone, 'This is a comment' AS c_comment
    UNION ALL
    SELECT  2 AS c_custkey, 'Customer2' AS c_name, 200.00 AS c_acctbal, '456 Elm St' AS c_address, '987-654-3210' AS c_phone, 'This is another comment' AS c_comment
),
orders AS (
    SELECT  1 AS o_orderkey, 1 AS o_custkey
    UNION ALL
    SELECT  2 AS o_orderkey, 2 AS o_custkey
),
lineitem AS (
    SELECT  1 AS l_orderkey, 10.00 AS l_extendedprice, 0.10 AS l_discount
    UNION ALL
    SELECT  2 AS l_orderkey, 20.00 AS l_extendedprice, 0.20 AS l_discount
),
nation AS (
    SELECT  1 AS n_nationkey, 'USA' AS n_name
    UNION ALL
    SELECT  2 AS n_nationkey, 'Canada' AS n_name
),
combined AS (
    SELECT c.c_custkey, c.c_name, l.l_extendedprice, l.l_discount, c.c_acctbal, n.n_name, c.c_address, c.c_phone, c.c_comment
    FROM customer c
    CROSS JOIN orders o
    CROSS JOIN lineitem l
    CROSS JOIN nation n
    WHERE c.c_custkey = o.o_custkey
    AND o.o_orderkey = l.l_orderkey
    AND c.c_acctbal > 0.00
),
revenue AS (
    SELECT c_custkey, c_name, SUM(l_extendedprice * (1 - l_discount)) AS revenue, c_acctbal, n_name, c_address, c_phone, c_comment
    FROM combined
    GROUP BY c_custkey, c_name, c_acctbal, n_name, c_address, c_phone, c_comment
)
SELECT c_custkey, c_name, revenue, c_acctbal, n_name, c_address, c_phone, c_comment
FROM revenue
