--Query type: DDL
WITH orders AS (
  SELECT * FROM (
    VALUES 
      (1, 1, 2, 100000.0, '1995-01-01'), 
      (2, 2, 3, 50000.0, '1995-02-01'), 
      (3, 3, 1, 200000.0, '1995-03-01')
    ) AS orders (o_orderkey, o_custkey, o_suppkey, o_totalprice, o_orderdate)
),
  customer AS (
    SELECT * FROM (
      VALUES 
        (1, 1), 
        (2, 2), 
        (3, 3)
    ) AS customer (c_custkey, c_nationkey)
),
  supplier AS (
    SELECT * FROM (
      VALUES 
        (1, 1), 
        (2, 2), 
        (3, 3)
    ) AS supplier (s_suppkey, s_nationkey)
)
SELECT 
  CASE 
    WHEN o.o_totalprice > 100000 THEN 'High' 
    WHEN o.o_totalprice > 50000 THEN 'Medium' 
    ELSE 'Low' 
  END AS price_category,
  SUM(o.o_totalprice) AS total_revenue,
  AVG(o.o_totalprice) AS avg_order_value,
  COUNT(DISTINCT o.o_orderkey) AS num_orders,
  COUNT(DISTINCT c.c_nationkey) AS num_customers,
  COUNT(DISTINCT s.s_nationkey) AS num_suppliers
FROM orders o
JOIN customer c ON o.o_custkey = c.c_custkey
JOIN supplier s ON o.o_suppkey = s.s_suppkey
WHERE o.o_orderdate >= '1995-01-01' AND o.o_orderdate < '1996-01-01'
GROUP BY 
  CASE 
    WHEN o.o_totalprice > 100000 THEN 'High' 
    WHEN o.o_totalprice > 50000 THEN 'Medium' 
    ELSE 'Low' 
  END
ORDER BY total_revenue DESC;