--Query type: DQL
WITH temp_result AS (
    SELECT p_partkey, ps_supplycost, AVG(ps_availqty) AS avg_availqty, SUM(ps_supplycost * ps_availqty) AS total_cost
    FROM partsupp
    GROUP BY p_partkey, ps_supplycost
)
SELECT p_partkey, ps_supplycost, avg_availqty, total_cost
FROM temp_result
ORDER BY p_partkey;
