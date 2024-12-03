--Query type: DQL
WITH dates AS (SELECT '2007-05-08 12:35:29.1234567 +12:15' AS date_string)
SELECT CAST(date_string AS time(7)) AS 'time_value',
       CAST(date_string AS date) AS 'date_value',
       CAST(date_string AS smalldatetime) AS 'smalldatetime_value',
       CAST(date_string AS datetime) AS 'datetime_value',
       CAST(date_string AS datetime2(7)) AS 'datetime2_value',
       CAST(date_string AS datetimeoffset(7)) AS 'datetimeoffset_value'
FROM dates
