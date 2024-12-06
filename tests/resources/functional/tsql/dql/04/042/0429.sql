-- tsql sql:
WITH temp_stats AS ( SELECT stats_id, name, object_id FROM ( VALUES (1, 'stats_name_1', 100), (2, 'stats_name_2', 200) ) AS stats (stats_id, name, object_id) ) SELECT stats_id, name AS stats_name, STATS_DATE(object_id, stats_id) AS statistics_date FROM temp_stats WHERE object_id = OBJECT_ID('public.customer') AND name = 'customer_stats';
