--Query type: DQL
WITH SalesQuota AS (
    SELECT 1 AS EmployeeKey, 600000 AS SalesAmountQuota, 2001 AS CalendarYear
    UNION ALL
    SELECT 2, 700000, 2001
    UNION ALL
    SELECT 3, 400000, 2002
    UNION ALL
    SELECT 4, 800000, 2001
    UNION ALL
    SELECT 5, 900000, 2001
)
SELECT COUNT(EmployeeKey) AS TotalCount, AVG(SalesAmountQuota) AS [Average Sales Quota]
FROM SalesQuota
WHERE SalesAmountQuota > 500000 AND CalendarYear = 2001;
