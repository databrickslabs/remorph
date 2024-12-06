-- tsql sql:
WITH customer AS (
  SELECT *
  FROM (
    VALUES
      (1, 'Customer1', 100.00, '123 Main St', '123-456-7890', 'Comment1', 1),
      (2, 'Customer2', 200.00, '456 Elm St', '987-654-3210', 'Comment2', 2)
    ) AS c (custkey, name, acctbal, address, phone, comment, nationkey)
),
orders AS (
  SELECT *
  FROM (
    VALUES
      (1, 1, '2022-01-01'),
      (2, 2, '2022-01-15')
    ) AS o (orderkey, custkey, orderdate)
),
lineitem AS (
  SELECT *
  FROM (
    VALUES
      (1, 1, 100.00, 0.10),
      (2, 2, 200.00, 0.20)
    ) AS l (linekey, orderkey, extendedprice, discount)
),
nation AS (
  SELECT *
  FROM (
    VALUES
      (1, 'USA'),
      (2, 'Canada')
    ) AS n (nationkey, nation)
)
SELECT
  c.custkey,
  c.name,
  COALESCE(SUM(l.extendedprice * (1 - l.discount)), 0) AS revenue,
  c.acctbal,
  n.nation,
  c.address,
  c.phone,
  c.comment
FROM
  customer c
  INNER JOIN orders o ON c.custkey = o.custkey
  LEFT JOIN lineitem l ON o.orderkey = l.orderkey
  INNER JOIN nation n ON c.nationkey = n.nationkey
WHERE
  c.acctbal > 0.00
GROUP BY
  c.custkey,
  c.name,
  c.acctbal,
  c.address,
  c.phone,
  c.comment,
  n.nation
ORDER BY
  revenue DESC;