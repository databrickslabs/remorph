--Query type: DDL
CREATE TABLE CustomerOrders
(
    CustomerKey INT IDENTITY(1, 1),
    OrderDate DATE,
    TotalCost DECIMAL(10, 2),
    TotalProfit AS TotalCost * 0.20
);

INSERT INTO CustomerOrders (OrderDate, TotalCost)
SELECT '2022-01-01', 100.00
FROM (
    VALUES (1, '2022-01-01', 100.00, 20.00)
) AS temp_result (CustomerKey, OrderDate, TotalCost, TotalProfit);

SELECT * FROM CustomerOrders;