--Query type: DCL
WITH cte AS (
    SELECT 'db2' AS database_name, 'FORCE_FAILOVER_ALLOW_DATA_LOSS' AS option_name
),
cte2 AS (
    SELECT 'db3' AS database_name, 'FORCE_FAILOVER_ALLOW_DATA_LOSS' AS option_name
)
SELECT 'ALTER DATABASE ' + database_name + ' ' + option_name AS query
FROM (
    VALUES ('db1', 'FORCE_FAILOVER_ALLOW_DATA_LOSS')
) AS cte3 (database_name, option_name)
UNION ALL
SELECT 'ALTER DATABASE ' + database_name + ' ' + option_name AS query
FROM cte
UNION ALL
SELECT 'ALTER DATABASE ' + database_name + ' ' + option_name AS query
FROM cte2
