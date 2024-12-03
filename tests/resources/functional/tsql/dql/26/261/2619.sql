--Query type: DQL
WITH TempResult AS (SELECT GETDATE() AS CurrentDateTime)
SELECT CurrentDateTime AS UnconvertedDateTime,
       CAST(CurrentDateTime AS NVARCHAR(30)) AS UsingCast,
       CONVERT(NVARCHAR(30), CurrentDateTime, 126) AS UsingConvertTo_ISO8601
FROM TempResult
