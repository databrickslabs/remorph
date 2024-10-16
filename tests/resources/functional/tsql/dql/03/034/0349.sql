--Query type: DQL
WITH CustomerCTE AS (
    SELECT CustomerKey, CustomerName
    FROM (
        VALUES (1, 'Customer1'),
               (2, 'Customer2'),
               (3, 'Customer3')
    ) AS Customer(CustomerKey, CustomerName)
)
SELECT CustomerKey, CustomerName
FROM CustomerCTE
WHERE CustomerKey BETWEEN 1 AND 3;