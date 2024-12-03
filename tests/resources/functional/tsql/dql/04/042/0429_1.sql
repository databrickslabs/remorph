--Query type: DQL
WITH stats_data AS ( SELECT 1 AS stats_id, 'stats_name_1' AS name, OBJECT_ID('information_schema.tables') AS object_id ) SELECT stats_id, name AS stats_name, STATS_DATE(object_id, stats_id) AS statistics_date FROM stats_data WHERE object_id = OBJECT_ID('information_schema.tables') AND name = 'stats_name_1';
