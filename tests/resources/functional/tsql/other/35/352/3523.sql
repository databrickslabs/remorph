--Query type: DDL
WITH Sales AS (
  SELECT
    s_suppkey,
    s_name,
    s_address,
    SUM(l_extendedprice * (1 - l_discount)) AS total_revenue
  FROM
    (
      VALUES
        (1, 'Supplier1', 'Address1'),
        (2, 'Supplier2', 'Address2'),
        (3, 'Supplier3', 'Address3')
    ) AS supplier (s_suppkey, s_name, s_address)
  INNER JOIN
    (
      VALUES
        (1, 1, 100.0, 0.1),
        (2, 1, 200.0, 0.2),
        (3, 2, 300.0, 0.3)
    ) AS lineitem (l_orderkey, l_suppkey, l_extendedprice, l_discount)
  ON s_suppkey = l_suppkey
  GROUP BY
    s_suppkey, s_name, s_address
),
TopSuppliers AS (
  SELECT
    s_suppkey,
    s_name,
    s_address,
    total_revenue,
    ROW_NUMBER() OVER (ORDER BY total_revenue DESC) AS row_num
  FROM
    Sales
)
SELECT
  s_suppkey,
  s_name,
  s_address,
  total_revenue,
  LAG(total_revenue, 1, 0) OVER (ORDER BY total_revenue DESC) AS prev_total_revenue,
  LEAD(total_revenue, 1, 0) OVER (ORDER BY total_revenue DESC) AS next_total_revenue
FROM
  TopSuppliers
WHERE
  row_num <= 10;
