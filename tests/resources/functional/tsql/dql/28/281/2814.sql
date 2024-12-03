--Query type: DQL
WITH TempResult AS (SELECT SYSDATETIME() AS DateTimeValue)
SELECT TOP (1) DateTimeValue AS UnconvertedDateTime, CAST(DateTimeValue AS NVARCHAR(30)) AS UsingCast, CONVERT(NVARCHAR(30), DateTimeValue, 126) AS UsingConvertTo_ISO8601
FROM TempResult
