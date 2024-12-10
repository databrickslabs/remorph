-- tsql sql:
WITH temp_result AS (
    SELECT l_orderkey, l_extendedprice
    FROM lineitem
)
SELECT l_orderkey, APPROX_PERCENTILE_CONT(0.10) WITHIN GROUP(ORDER BY l_extendedprice) AS 'P10', APPROX_PERCENTILE_CONT(0.90) WITHIN GROUP(ORDER BY l_extendedprice) AS 'P90'
FROM temp_result
GROUP BY l_orderkey;
