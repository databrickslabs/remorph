-- tsql sql:
WITH orders AS (
  SELECT '1-URGENT' AS orderpriority, '1993-01-01' AS orderdate, 1 AS orderkey, 1 AS shippriority
  UNION ALL
  SELECT '2-HIGH', '1993-02-01', 2, 2
  UNION ALL
  SELECT '3-MEDIUM', '1993-03-01', 3, 3
),
lineitem AS (
  SELECT 1 AS orderkey, 10.0 AS extendedprice, 0.1 AS discount
  UNION ALL
  SELECT 2, 20.0, 0.2
  UNION ALL
  SELECT 3, 30.0, 0.3
)
SELECT
  CASE
    WHEN T1.orderpriority = '1-URGENT' OR T1.orderpriority = '2-HIGH'
    THEN 'High'
    ELSE 'Low'
  END AS order_priority,
  SUM(T2.extendedprice * (1 - T2.discount)) AS revenue,
  T1.orderdate,
  T1.shippriority
FROM orders AS T1
JOIN lineitem AS T2 ON T1.orderkey = T2.orderkey
WHERE T1.orderdate >= '1993-01-01' AND T1.orderdate < '1994-01-01'
GROUP BY
  CASE
    WHEN T1.orderpriority = '1-URGENT' OR T1.orderpriority = '2-HIGH'
    THEN 'High'
    ELSE 'Low'
  END,
  T1.orderdate,
  T1.shippriority
ORDER BY revenue DESC, T1.orderdate;
