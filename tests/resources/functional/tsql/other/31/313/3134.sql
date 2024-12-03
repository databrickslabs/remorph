--Query type: DML
DECLARE @OrderIDVariable INT;

WITH Customers AS (
  SELECT 1 AS CustomerID, 'John' AS CustomerName
  UNION ALL
  SELECT 2, 'Alice'
  UNION ALL
  SELECT 3, 'Bob'
),
Orders AS (
  SELECT 1 AS OrderID, 1 AS CustomerID, 100 AS OrderTotal
  UNION ALL
  SELECT 2, 1, 200
  UNION ALL
  SELECT 3, 2, 50
)
SELECT @OrderIDVariable = OrderID
FROM Orders
ORDER BY OrderID DESC;

SELECT @OrderIDVariable;

-- REMORPH CLEANUP: DROP TABLE Customers;
-- REMORPH CLEANUP: DROP TABLE Orders;
