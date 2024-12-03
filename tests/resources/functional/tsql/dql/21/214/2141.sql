--Query type: DQL
WITH temp_result AS ( SELECT c_custkey, c_nationkey, c_acctbal FROM customer ) SELECT c_custkey, c_nationkey, SUM(c_acctbal) AS total_balance FROM temp_result GROUP BY CUBE (c_custkey, c_nationkey)
