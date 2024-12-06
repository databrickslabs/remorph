-- tsql sql:
CREATE TABLE dbo.CustomerOrders
WITH (DISTRIBUTION = ROUND_ROBIN)
AS
SELECT OrderKey, CustomerName, OrderStatus, TotalRevenue
FROM (
    VALUES (1, 'John Doe', 'Shipped', 100.00),
    (2, 'Jane Doe', 'Pending', 200.00)
) AS CustomerOrders (OrderKey, CustomerName, OrderStatus, TotalRevenue);
