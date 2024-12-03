--Query type: DQL
WITH TempResult AS ( SELECT 1 AS CustomerID, 'Customer1' AS CustomerName UNION ALL SELECT 2, 'Customer2' ) SELECT CustomerID, CustomerName FROM TempResult;
