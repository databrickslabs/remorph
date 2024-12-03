--Query type: DQL
WITH temp_result AS (SELECT CURRENT_TIMEZONE() AS timezone)
SELECT timezone
FROM temp_result
