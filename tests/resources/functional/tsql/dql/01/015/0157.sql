-- tsql sql:
WITH temp_result AS (SELECT '2019-01-01 14:00:00' AS date_str)
SELECT CAST(date_str AS datetime) AT TIME ZONE 'America/New_York' AT TIME ZONE 'America/Los_Angeles' AS conv
FROM temp_result;
