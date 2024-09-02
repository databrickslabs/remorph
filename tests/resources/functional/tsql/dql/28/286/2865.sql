--Query type: DQL
WITH CustomerCTE AS (
  SELECT 'United States' AS Country, 'New York' AS City, 1 AS CustomerID
  UNION ALL
  SELECT 'Canada', 'Toronto', 2
  UNION ALL
  SELECT 'Mexico', 'Mexico City', 3
),
OrderCTE AS (
  SELECT 1 AS OrderID, 1 AS CustomerID, '2020-01-01' AS OrderDate
  UNION ALL
  SELECT 2, 1, '2020-01-15'
  UNION ALL
  SELECT 3, 2, '2020-02-01'
)
SELECT c.City, COUNT(o.OrderID) AS OrderCount
FROM CustomerCTE c
INNER JOIN OrderCTE o ON c.CustomerID = o.CustomerID
GROUP BY c.City
ORDER BY c.City;