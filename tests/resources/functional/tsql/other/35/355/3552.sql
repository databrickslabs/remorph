-- tsql sql:
WITH temp_customer AS (
  SELECT 1 AS c_custkey, 'Customer1' AS c_name, 100.0 AS c_acctbal, '123 Main St' AS c_address, '123-456-7890' AS c_phone, 'Comment1' AS c_comment, 'Nation1' AS c_nationkey
  UNION ALL
  SELECT 2 AS c_custkey, 'Customer2' AS c_name, 200.0 AS c_acctbal, '456 Elm St' AS c_address, '987-654-3210' AS c_phone, 'Comment2' AS c_comment, 'Nation2' AS c_nationkey
),

  temp_nation AS (
  SELECT 'Nation1' AS n_nationkey, 'NationName1' AS n_name
  UNION ALL
  SELECT 'Nation2' AS n_nationkey, 'NationName2' AS n_name
),

  temp_lineitem AS (
  SELECT 1 AS l_orderkey, 10.0 AS l_extendedprice, 0.1 AS l_discount
  UNION ALL
  SELECT 2 AS l_orderkey, 20.0 AS l_extendedprice, 0.2 AS l_discount
)

SELECT c_custkey, c_name, SUM(l_extendedprice * (1 - l_discount)) AS revenue, c_acctbal, n_name, c_address, c_phone, c_comment
FROM temp_lineitem
INNER JOIN temp_customer ON temp_lineitem.l_orderkey = temp_customer.c_custkey
INNER JOIN temp_nation ON temp_customer.c_nationkey = temp_nation.n_nationkey
WHERE c_acctbal > (SELECT AVG(c_acctbal) FROM temp_customer)
GROUP BY c_custkey, c_name, c_acctbal, c_address, c_phone, n_name, c_comment
ORDER BY revenue DESC;
