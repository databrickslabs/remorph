-- tsql sql:
WITH temp_customer AS (
  SELECT *
  FROM (
    VALUES
      (1, 'Customer1', 100.00, 'Address1', 'Phone1', 'Comment1'),
      (2, 'Customer2', 200.00, 'Address2', 'Phone2', 'Comment2')
    ) AS t (c_custkey, c_name, c_acctbal, c_address, c_phone, c_comment)
),
     temp_orders AS (
  SELECT *
  FROM (
    VALUES
      (1, 1, 1000.00),
      (2, 1, 2000.00)
    ) AS t (o_orderkey, o_custkey, o_totalprice)
),
     temp_lineitem AS (
  SELECT *
  FROM (
    VALUES
      (1, 1, 10.00, 0.1, 1),
      (2, 1, 20.00, 0.2, 2)
    ) AS t (l_orderkey, l_extendedprice, l_discount, l_suppkey, l_quantity)
)
SELECT
  c_custkey,
  c_name,
  SUM(l_extendedprice * (1 - l_discount)) AS revenue,
  c_acctbal,
  c_address,
  c_phone,
  c_comment
FROM
  temp_customer
  INNER JOIN temp_orders
    ON c_custkey = o_custkey
  INNER JOIN temp_lineitem
    ON o_orderkey = l_orderkey
WHERE
  c_acctbal > 0.00
  AND l_orderkey IN (
    SELECT
      l_orderkey
    FROM
      temp_lineitem
    GROUP BY
      l_orderkey
    HAVING
      SUM(l_extendedprice * (1 - l_discount)) > 100000.00
  )
GROUP BY
  c_custkey,
  c_name,
  c_acctbal,
  c_address,
  c_phone,
  c_comment
ORDER BY
  revenue DESC;
