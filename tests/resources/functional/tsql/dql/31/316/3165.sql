-- tsql sql:
WITH OrderDetails AS (
  SELECT 1 AS ProductID, 10 AS OrderQty
  UNION ALL
  SELECT 2 AS ProductID, 20 AS OrderQty
  UNION ALL
  SELECT 3 AS ProductID, 30 AS OrderQty
  UNION ALL
  SELECT 1 AS ProductID, 40 AS OrderQty
  UNION ALL
  SELECT 2 AS ProductID, 50 AS OrderQty
  UNION ALL
  SELECT 3 AS ProductID, 60 AS OrderQty
)
SELECT ProductID
FROM OrderDetails
GROUP BY ProductID
HAVING AVG(OrderQty) > 30
ORDER BY ProductID;
