--Query type: DCL
SET DATEFIRST 5;
SELECT DATEPART(dw, SYSDATETIME()) AS 'Current Day', @@DATEFIRST AS 'First Day of Week'
FROM (
    VALUES ('2023-01-01')
) AS date_table(date_column);
