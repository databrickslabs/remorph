--Query type: DDL
WITH customer AS (
    SELECT 1 AS c_custkey, 'Customer1' AS c_name, 100.00 AS c_acctbal, 1 AS c_nationkey, '123 Main St' AS c_address, '123-456-7890' AS c_phone, 'Comment1' AS c_comment
), orders AS (
    SELECT 1 AS o_orderkey, 1 AS o_custkey
), lineitem AS (
    SELECT 1 AS l_orderkey, 100.00 AS l_extendedprice, 0.10 AS l_discount
), nation AS (
    SELECT 1 AS n_nationkey, 'Nation1' AS n_name
)
SELECT c_custkey, c_name, SUM(l_extendedprice * (1 - l_discount)) AS revenue, c_acctbal, n_name, c_address, c_phone, c_comment
FROM customer
JOIN orders ON c_custkey = o_custkey
JOIN lineitem ON o_orderkey = l_orderkey
JOIN nation ON c_nationkey = n_nationkey
WHERE c_acctbal > 0.00 AND l_orderkey IN (
    SELECT l_orderkey FROM lineitem GROUP BY l_orderkey HAVING SUM(l_extendedprice * (1 - l_discount)) > 100000.00
)
GROUP BY c_custkey, c_name, c_acctbal, n_name, c_address, c_phone, c_comment
ORDER BY revenue DESC;
