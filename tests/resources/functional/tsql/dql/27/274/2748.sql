--Query type: DQL
WITH CustomerCTE AS (
    SELECT 'Customer1' AS CustomerName, 1 AS CustomerID
    UNION ALL
    SELECT 'Customer2', 2
)
SELECT c.CustomerName, o.OrderTotal, @@SPID AS SessionID
FROM CustomerCTE c
INNER JOIN (
    VALUES ('Order1', 100.00, 1), ('Order2', 200.00, 2)
) AS o(OrderName, OrderTotal, CustomerID)
ON c.CustomerID = o.CustomerID
