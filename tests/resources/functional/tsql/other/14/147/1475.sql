--Query type: DCL
DECLARE @MyCounter INT;

WITH MyCTE AS (
    SELECT 10 + 20 AS Result
)

SELECT *
FROM MyCTE;
