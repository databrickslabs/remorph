--Query type: DQL
WITH QuotaHistory AS (
    SELECT 1 AS CustomerKey, '2005-01-01' AS QuotaDate, 1000.0 AS SalesQuota
    UNION ALL
    SELECT 1 AS CustomerKey, '2006-01-01' AS QuotaDate, 1200.0 AS SalesQuota
    UNION ALL
    SELECT 2 AS CustomerKey, '2005-01-01' AS QuotaDate, 800.0 AS SalesQuota
    UNION ALL
    SELECT 2 AS CustomerKey, '2006-01-01' AS QuotaDate, 1000.0 AS SalesQuota
)
SELECT CustomerKey, YEAR(QuotaDate) AS SalesYear, SalesQuota AS CurrentQuota, LAG(SalesQuota, 1, 0) OVER (ORDER BY YEAR(QuotaDate)) AS PreviousQuota
FROM QuotaHistory
WHERE CustomerKey = 1 AND YEAR(QuotaDate) IN ('2005', '2006');