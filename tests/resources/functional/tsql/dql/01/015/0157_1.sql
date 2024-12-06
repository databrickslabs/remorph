-- tsql sql:
WITH temp_result AS (SELECT 'Europe/Warsaw' AS from_tz, 'UTC' AS to_tz, '2019-01-01 00:00:00' AS timestamp_ntz) SELECT CAST(timestamp_ntz AS datetime) AT TIME ZONE from_tz AS conv FROM temp_result
