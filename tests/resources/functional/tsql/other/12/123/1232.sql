--Query type: DDL
DROP TABLE IF EXISTS #TempTable;
WITH TempTable AS (
    SELECT *
    FROM (
        VALUES (1, 'John Doe'),
               (2, 'Jane Doe')
    ) AS T (CustomerID, CustomerName)
)
SELECT *
FROM TempTable;