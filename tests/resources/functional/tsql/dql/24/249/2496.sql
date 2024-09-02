--Query type: DQL
WITH temp_result AS ( SELECT 1 AS dummy ) SELECT CURRENT_TIMEZONE_ID() AS timezone_id FROM temp_result;