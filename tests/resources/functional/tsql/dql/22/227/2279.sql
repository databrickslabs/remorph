-- tsql sql:
WITH dates AS (
  SELECT CAST('2022-05-08 12:35:29.1234567 +12:15' AS TIME(7)) AS time,
         CAST('2022-05-08 12:35:29.1234567 +12:15' AS DATE) AS date,
         CAST('2022-05-08 12:35:29.123' AS SMALLDATETIME) AS smalldatetime,
         CAST('2022-05-08 12:35:29.123' AS DATETIME) AS datetime,
         CAST('2022-05-08 12:35:29.1234567 +12:15' AS DATETIME2(7)) AS datetime2,
         CAST('2022-05-08 12:35:29.1234567 +12:15' AS DATETIMEOFFSET(7)) AS datetimeoffset
)
SELECT
  CAST(dates.time AS TIME(7)) AS time,
  CAST(dates.date AS DATE) AS date,
  CAST(dates.smalldatetime AS SMALLDATETIME) AS smalldatetime,
  CAST(dates.datetime AS DATETIME) AS datetime,
  CAST(dates.datetime2 AS DATETIME2(7)) AS datetime2,
  CAST(dates.datetimeoffset AS DATETIMEOFFSET(7)) AS datetimeoffset
FROM dates;
