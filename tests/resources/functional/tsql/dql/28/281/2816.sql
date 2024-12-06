-- tsql sql:
WITH temp_result AS (
    SELECT c_custkey, c_nationkey, o_totalprice
    FROM customer
    INNER JOIN orders
    ON c_custkey = o_custkey
)
SELECT TOP (1) c_nationkey, c_custkey, o_totalprice
FROM temp_result
WHERE c_nationkey = 1
UNION ALL
SELECT TOP (1) c_nationkey, c_custkey, o_totalprice
FROM temp_result
WHERE c_nationkey = 2
ORDER BY o_totalprice ASC;
