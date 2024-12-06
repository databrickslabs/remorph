-- tsql sql:
DECLARE @ASOF DATETIMEOFFSET;
SET @ASOF = DATEADD(month, -1, GETDATE()) AT TIME ZONE 'UTC';

WITH TempResult AS (
    SELECT CustomerID, CAST(OrderDate AS datetime) AT TIME ZONE 'Pacific Standard Time' AS OrderDate_PST, TotalDue
    FROM (
        VALUES (1, '2022-01-01 12:00:00', 100.00),
               (2, '2022-02-01 13:00:00', 200.00),
               (3, '2022-03-01 14:00:00', 300.00)
    ) AS Orders(CustomerID, OrderDate, TotalDue)
)

SELECT CustomerID, OrderDate_PST, TotalDue
FROM TempResult
WHERE OrderDate_PST <= @ASOF;
