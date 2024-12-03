--Query type: DQL
SELECT current_time_val FROM (VALUES (GETDATE())) AS current_time_dt([current_time_val]);
