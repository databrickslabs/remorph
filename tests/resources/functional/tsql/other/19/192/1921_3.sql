-- tsql sql:
SET DATEFORMAT ymd;
SELECT CONVERT(date, '20220101') AS DateValue
FROM (
    VALUES (1)
) AS TempTable (Id);
