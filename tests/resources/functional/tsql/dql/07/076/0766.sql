--Query type: DQL
WITH temp_result AS ( SELECT n_name, r_name, o_totalprice FROM customer INNER JOIN nation ON c_nationkey = n_nationkey INNER JOIN region ON n_regionkey = r_regionkey INNER JOIN orders ON c_custkey = o_custkey ) SELECT n_name, r_name, cume_dist() OVER ( PARTITION BY r_name ORDER BY o_totalprice ) AS cume_dist FROM temp_result
