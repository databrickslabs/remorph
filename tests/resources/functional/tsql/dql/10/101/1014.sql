-- tsql sql:
SELECT CONVERT(DATETIME, '12/26/2004', 101) AS [DateValue], dbo.ISOweek(CONVERT(DATETIME, '12/26/2004', 101)) AS [WeekNumber] FROM (VALUES ('12/26/2004')) AS DateTable([DateValue])
