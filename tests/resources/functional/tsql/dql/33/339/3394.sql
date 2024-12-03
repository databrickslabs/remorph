--Query type: DQL
WITH temp_indexes AS (
    SELECT 'index_name' AS name, OBJECT_ID('Person.Address') AS object_id, 1 AS index_id
)
SELECT name AS index_name, STATS_DATE(object_id, index_id) AS statistics_update_date
FROM temp_indexes
WHERE object_id = OBJECT_ID('Person.Address');
