--Query type: DML
SET DATEFIRST 3;
SELECT 'Week-3', DATETRUNC(week, date_value)
FROM (
    VALUES (
        CAST('2022-01-01' AS DATE),
        CAST('2022-01-08' AS DATE),
        CAST('2022-01-15' AS DATE)
    )
) AS dates (date_value);