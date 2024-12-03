--Query type: DQL
WITH CustomerCTE AS (
    SELECT *
    FROM (
        VALUES (1, 'Customer#1'),
               (2, 'Customer#2')
    ) AS Customer (CustomerID, CustomerName)
),
OrderCTE AS (
    SELECT *
    FROM (
        VALUES (1, 1, 100.00),
               (2, 1, 200.00)
    ) AS Orders (OrderID, CustomerID, TotalDue)
)
SELECT *
FROM CustomerCTE AS c
INNER JOIN OrderCTE AS o WITH (FORCESEEK)
    ON c.CustomerID = o.CustomerID
WHERE o.TotalDue > 100
    AND (o.OrderID > 1 OR o.TotalDue < 1000.00);
