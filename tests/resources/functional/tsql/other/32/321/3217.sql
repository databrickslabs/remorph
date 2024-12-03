--Query type: DCL
WITH SalesData AS (
    SELECT 1 AS OrderID, 100 AS Total, '2022-01-01' AS OrderDate
    UNION ALL
    SELECT 2, 200, '2022-01-15'
    UNION ALL
    SELECT 3, 300, '2022-02-01'
),
SalesSummary AS (
    SELECT SUM(Total) AS TotalSales, AVG(Total) AS AverageSales, MAX(Total) AS MaxSales, MIN(Total) AS MinSales
    FROM SalesData
),
Metrics AS (
    SELECT 'Total Sales' AS Metric, TotalSales AS Value
    FROM SalesSummary
    UNION ALL
    SELECT 'Average Sales', AverageSales
    FROM SalesSummary
    UNION ALL
    SELECT 'Max Sales', MaxSales
    FROM SalesSummary
    UNION ALL
    SELECT 'Min Sales', MinSales
    FROM SalesSummary
)
SELECT *
FROM Metrics;
