-- tsql sql:
WITH temp_result AS (SELECT n_name, r_name, o_totalprice FROM customer, nation, region, orders WHERE c_nationkey = n_nationkey AND n_regionkey = r_regionkey AND c_custkey = o_custkey) SELECT n_name, r_name, PERCENT_RANK() OVER (PARTITION BY n_name ORDER BY o_totalprice) AS percent_rank FROM temp_result
