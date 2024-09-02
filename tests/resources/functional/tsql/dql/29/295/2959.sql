--Query type: DQL
WITH customer_stats AS (
    SELECT 'customer_stats' AS name, 1 AS object_id, 1 AS stats_id
),
 customer_stats_columns AS (
    SELECT 1 AS stats_column_id, 1 AS object_id, 1 AS stats_id, 1 AS column_id
),
 customer_columns AS (
    SELECT 'c_name' AS name, 1 AS object_id, 1 AS column_id
)
SELECT cs.name AS customer_stats_name, cc.name AS customer_column_name, csc.stats_column_id
FROM customer_stats AS cs
INNER JOIN customer_stats_columns AS csc ON cs.object_id = csc.object_id AND cs.stats_id = csc.stats_id
INNER JOIN customer_columns AS cc ON csc.object_id = cc.object_id AND cc.column_id = csc.column_id
WHERE cs.object_id = OBJECT_ID('customer');