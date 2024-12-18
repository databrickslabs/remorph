-- tsql sql:
SET DATEFORMAT dmy;
SELECT TRY_CAST(DateString AS DATETIME2) AS Result
FROM (
    VALUES ('12/31/2022'), ('01/01/2023')
) AS DateValues(DateString);
