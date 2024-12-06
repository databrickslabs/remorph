-- tsql sql:
WITH customer_orders AS (
  SELECT c_custkey, c_name, SUM(o_totalprice) AS total_revenue
  FROM (
    VALUES
      (1, 'Customer1', 100.0),
      (2, 'Customer2', 200.0),
      (3, 'Customer3', 300.0)
  ) AS customers (c_custkey, c_name, o_totalprice)
  GROUP BY c_custkey, c_name
),
ranked_orders AS (
  SELECT c_custkey, c_name, total_revenue,
    RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank
  FROM customer_orders
)
SELECT TOP 2 c_custkey, c_name, total_revenue, revenue_rank
FROM ranked_orders
ORDER BY revenue_rank;
