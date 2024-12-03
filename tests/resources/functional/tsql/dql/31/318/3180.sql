--Query type: DQL
WITH Products AS (
  SELECT 'Product1' AS Name, 10 AS ProductID
  UNION ALL
  SELECT 'Product2', 20
  UNION ALL
  SELECT 'Product3', 30
),
SalesOrderDetails AS (
  SELECT 10 AS ProductID, 5 AS OrderQty, 100 AS UnitPrice, 0.1 AS UnitPriceDiscount
  UNION ALL
  SELECT 20, 10, 200, 0.2
  UNION ALL
  SELECT 30, 15, 300, 0.3
)
SELECT p.Name AS ProductName,
       NonDiscountSales = (sod.OrderQty * sod.UnitPrice),
       Discounts = ((sod.OrderQty * sod.UnitPrice) * sod.UnitPriceDiscount)
FROM Products AS p
INNER JOIN SalesOrderDetails AS sod
ON p.ProductID = sod.ProductID
ORDER BY ProductName DESC;
