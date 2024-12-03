--Query type: DCL
WITH customer AS (
    SELECT 1 AS c_custkey, 'Customer1' AS c_name, 100.00 AS c_acctbal
), orders AS (
    SELECT 1 AS o_orderkey, 1 AS o_custkey
), lineitem AS (
    SELECT 1 AS l_orderkey, 1 AS l_extendedprice, 0.1 AS l_discount
), nation AS (
    SELECT 1 AS n_nationkey, 'Nation1' AS n_name
), revenue_calc AS (
    SELECT c_custkey, c_name, SUM(l_extendedprice * (1 - l_discount)) AS revenue
    FROM customer
    JOIN orders ON c_custkey = o_custkey
    JOIN lineitem ON o_orderkey = l_orderkey
    GROUP BY c_custkey, c_name
)
SELECT *
FROM revenue_calc
WHERE revenue > 100000.00
ORDER BY revenue DESC;
