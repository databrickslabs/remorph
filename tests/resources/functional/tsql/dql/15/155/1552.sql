--Query type: DQL
WITH dates AS (
    SELECT CAST('1912-10-25' AS DATE) AS date_value,
           CAST('1912-10-25 00:00:00.000 +00:00' AS DATETIMEOFFSET(3)) AS datetimeoffset_value
)
SELECT date_value AS [date],
       datetimeoffset_value AS [datetimeoffset]
FROM dates;