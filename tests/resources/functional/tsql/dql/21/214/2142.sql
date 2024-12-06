-- tsql sql:
WITH temp_result AS (
    SELECT nationkey, regionkey, SUM(acctbal) AS total_balance
    FROM customer
    GROUP BY nationkey, regionkey
)
SELECT nationkey, regionkey, total_balance
FROM temp_result
GROUP BY GROUPING SETS (
    CUBE(nationkey, regionkey),
    ()
)
