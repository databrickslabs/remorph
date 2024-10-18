--Query type: DDL
WITH CustomerData AS (
  SELECT CAST('2022-01-01' AS DATE) AS OrderDate, 'Customer A' AS CustomerName, 100.00 AS OrderTotal
  UNION ALL
  SELECT CAST('2022-01-02' AS DATE), 'Customer B', 200.00
),
ProcessedOrders AS (
  SELECT OrderDate, CustomerName, OrderTotal, SUM(OrderTotal) OVER (ORDER BY OrderDate) AS RunningTotal
  FROM CustomerData
)
SELECT OrderDate, CustomerName, OrderTotal, RunningTotal, CASE WHEN OrderTotal > 150 THEN 'High' ELSE 'Low' END AS OrderCategory, CONVERT(VARCHAR(10), OrderDate, 120) AS OrderDateFormatted
FROM ProcessedOrders
ORDER BY OrderDate