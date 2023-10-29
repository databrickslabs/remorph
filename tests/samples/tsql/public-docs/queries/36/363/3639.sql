-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/case-transact-sql?view=sql-server-ver16

WITH Data (value)
AS (
    SELECT 0
    UNION ALL
    SELECT 1
    )
SELECT CASE
        WHEN MIN(value) <= 0 THEN 0
        WHEN MAX(1 / value) >= 100 THEN 1
        END
FROM Data;
GO