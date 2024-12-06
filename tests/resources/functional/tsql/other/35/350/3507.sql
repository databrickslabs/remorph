-- tsql sql:
WITH customer AS (
  SELECT 1 AS c_custkey, 'Customer1' AS c_name, 100.0 AS c_acctbal, '123 Main St' AS c_address, '123-456-7890' AS c_phone, 'Comment1' AS c_comment, 1 AS c_nationkey
  UNION ALL
  SELECT 2, 'Customer2', 200.0, '456 Elm St', '987-654-3210', 'Comment2', 2
),
orders AS (
  SELECT 1 AS o_orderkey, 1 AS o_custkey, 100.0 AS o_totalprice
  UNION ALL
  SELECT 2, 2, 200.0
),
lineitem AS (
  SELECT 1 AS l_orderkey, 1 AS l_linenumber, 10.0 AS l_extendedprice, 'R' AS l_returnflag
  UNION ALL
  SELECT 2, 2, 20.0, 'R'
),
nation AS (
  SELECT 1 AS n_nationkey, 'USA' AS n_name
  UNION ALL
  SELECT 2, 'Canada'
)
SELECT
  c.c_custkey,
  c.c_name,
  SUM(l.l_extendedprice * (1 - 0.0)) AS revenue,
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
WHERE
  l.l_returnflag = 'R'
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
