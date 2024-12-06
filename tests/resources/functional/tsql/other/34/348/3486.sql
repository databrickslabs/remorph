-- tsql sql:
WITH temp_customer AS ( SELECT 1 AS c_custkey, 'Customer1' AS c_name, 100.00 AS c_acctbal, 'Address1' AS c_address, 'Phone1' AS c_phone, 'Comment1' AS c_comment, 1 AS c_nationkey UNION ALL SELECT 2, 'Customer2', 200.00, 'Address2', 'Phone2', 'Comment2', 2 ), temp_orders AS ( SELECT 1 AS o_orderkey, 1 AS o_custkey, 1000.00 AS o_totalprice UNION ALL SELECT 2, 1, 2000.00 ), temp_lineitem AS ( SELECT 1 AS l_orderkey, 1 AS l_linenumber, 10.00 AS l_extendedprice, 0.1 AS l_discount UNION ALL SELECT 2, 1, 20.00, 0.2 ), temp_nation AS ( SELECT 1 AS n_nationkey, 'Nation1' AS n_name UNION ALL SELECT 2, 'Nation2' ) SELECT c_custkey, c_name, SUM(l_extendedprice * (1 - l_discount)) AS revenue, c_acctbal, n_name, c_address, c_phone, c_comment FROM temp_customer INNER JOIN temp_orders ON c_custkey = o_custkey INNER JOIN temp_lineitem ON o_orderkey = l_orderkey INNER JOIN temp_nation ON c_nationkey = n_nationkey WHERE c_acctbal > 0.00 AND l_orderkey IN ( SELECT l_orderkey FROM temp_lineitem GROUP BY l_orderkey HAVING SUM(l_extendedprice * (1 - l_discount)) > 100000.00 ) GROUP BY c_custkey, c_name, c_acctbal, n_name, c_address, c_phone, c_comment ORDER BY revenue DESC
