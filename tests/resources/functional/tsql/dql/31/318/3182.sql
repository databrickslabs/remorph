-- tsql sql:
WITH CustomerCTE AS (
    SELECT CustomerID, CustomerName
    FROM (
        VALUES (1, 'Customer1'),
               (2, 'Customer2')
    ) AS Customer(CustomerID, CustomerName)
),
OrderCTE AS (
    SELECT OrderID, CustomerID, OrderDate
    FROM (
        VALUES (1, 1, '2022-01-01'),
               (2, 2, '2022-01-02')
    ) AS Orders(OrderID, CustomerID, OrderDate)
)
SELECT c.CustomerName, o.OrderID, o.OrderDate
FROM CustomerCTE c WITH (INDEX(AK_Customer_CustomerID))
JOIN OrderCTE o ON c.CustomerID = o.CustomerID
WHERE c.CustomerName = 'Customer1';
