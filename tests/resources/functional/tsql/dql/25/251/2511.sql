--Query type: DQL
WITH SalesCTE AS (
    SELECT 'USA' AS Country, 'North' AS Region, 100 AS sales
    UNION ALL
    SELECT 'Canada', 'North', 200
    UNION ALL
    SELECT 'Mexico', 'North', 300
    UNION ALL
    SELECT 'UK', 'Europe', 400
    UNION ALL
    SELECT 'Germany', 'Europe', 500
)
SELECT Country, Region, SUM(sales) AS TotalSales
FROM SalesCTE
GROUP BY Country, Region;