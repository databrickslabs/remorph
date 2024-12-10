-- tsql sql:
WITH CustomerCTE AS (
    SELECT CustomerID, CustomerName
    FROM (
        VALUES (1, 'Customer1'),
               (2, 'Customer2')
    ) AS Customer (CustomerID, CustomerName)
),
OrderCTE AS (
    SELECT OrderID, CustomerID
    FROM (
        VALUES (1, 1),
               (2, 2)
    ) AS [Order] (OrderID, CustomerID)
)
SELECT c.CustomerID, o.OrderID
FROM CustomerCTE AS c
INNER JOIN OrderCTE AS o
    ON c.CustomerID = o.CustomerID;
