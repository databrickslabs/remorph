--Query type: DQL
WITH QuotaHistory AS (
    SELECT 1 AS CustomerKey, '2022-01-01' AS QuotaDate, 1000.0 AS SalesQuota
    UNION ALL
    SELECT 1 AS CustomerKey, '2022-04-01' AS QuotaDate, 1200.0 AS SalesQuota
    UNION ALL
    SELECT 1 AS CustomerKey, '2022-07-01' AS QuotaDate, 1500.0 AS SalesQuota
    UNION ALL
    SELECT 2 AS CustomerKey, '2022-01-01' AS QuotaDate, 2000.0 AS SalesQuota
    UNION ALL
    SELECT 2 AS CustomerKey, '2022-04-01' AS QuotaDate, 2500.0 AS SalesQuota
    UNION ALL
    SELECT 2 AS CustomerKey, '2022-07-01' AS QuotaDate, 3000.0 AS SalesQuota
)
SELECT
    CustomerKey,
    DATEPART(QUARTER, QuotaDate) AS Quarter,
    YEAR(QuotaDate) AS SalesYear,
    SalesQuota AS QuotaThisQuarter,
    SalesQuota - FIRST_VALUE(SalesQuota) OVER (PARTITION BY CustomerKey, YEAR(QuotaDate) ORDER BY DATEPART(QUARTER, QuotaDate)) AS DifferenceFromFirstQuarter,
    SalesQuota - LAST_VALUE(SalesQuota) OVER (PARTITION BY CustomerKey, YEAR(QuotaDate) ORDER BY DATEPART(QUARTER, QuotaDate) RANGE BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING) AS DifferenceFromLastQuarter
FROM
    QuotaHistory
WHERE
    YEAR(QuotaDate) > 2020
    AND CustomerKey BETWEEN 1 AND 2
ORDER BY
    CustomerKey,
    SalesYear,
    Quarter;