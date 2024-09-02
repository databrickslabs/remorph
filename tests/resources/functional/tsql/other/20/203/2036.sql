--Query type: DDL
DROP TABLE IF EXISTS #TempTable;

WITH TempTable AS (
    SELECT *
    FROM (
        VALUES (
            (1, '1995-01-01'),
            (2, '1995-01-02'),
            (3, '1995-01-03')
        ) AS TempTable (CustomerKey, OrderDate)
    )
)

SELECT *
FROM TempTable;