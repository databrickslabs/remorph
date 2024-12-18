-- tsql sql:
WITH cte AS (SELECT '2022-10-30T01:01:00' AS date_string)
SELECT CONVERT(DATETIMEOFFSET, date_string, 126) AT TIME ZONE 'Central European Standard Time' AS converted_date
FROM cte
