--Query type: DQL
WITH temp_result AS (
    SELECT 1 AS p_partkey, 10.0 AS p_size, 5 AS o_orderkey
    UNION ALL
    SELECT 2, 20.0, 10
    UNION ALL
    SELECT 3, 30.0, 15
)
SELECT p_partkey
FROM temp_result
WHERE p_size < 25.00
GROUP BY p_partkey
HAVING AVG(o_orderkey) > 5
ORDER BY p_partkey;
