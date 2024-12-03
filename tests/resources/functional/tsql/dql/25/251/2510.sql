--Query type: DQL
WITH SalesData AS (
  SELECT 'USA' AS Country, 'North' AS Region, 100 AS Sales
  UNION ALL
  SELECT 'USA' AS Country, 'South' AS Region, 200 AS Sales
  UNION ALL
  SELECT 'Canada' AS Country, 'East' AS Region, 300 AS Sales
  UNION ALL
  SELECT 'Canada' AS Country, 'West' AS Region, 400 AS Sales
)
SELECT Country, Region, SUM(Sales) AS TotalSales
FROM SalesData
GROUP BY ROLLUP (Country, Region);
