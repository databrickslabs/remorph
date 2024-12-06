-- tsql sql:
CREATE PROCEDURE uspGetCustomerOrders
    @CustomerID INT
AS
BEGIN
    SELECT OrderID, CustomerID, OrderDate
    FROM (
        VALUES (1, 1, '2020-01-01'),
               (2, 1, '2020-01-15'),
               (3, 2, '2020-02-01')
    ) AS Orders(OrderID, CustomerID, OrderDate)
    WHERE CustomerID = @CustomerID;
END

DECLARE @retstat INT;
EXECUTE @retstat = uspGetCustomerOrders @CustomerID = 1;

SELECT OrderID, CustomerID, OrderDate
FROM (
    VALUES (1, 1, '2020-01-01'),
           (2, 1, '2020-01-15'),
           (3, 2, '2020-02-01')
) AS Orders(OrderID, CustomerID, OrderDate)
WHERE CustomerID = 1;

-- REMORPH CLEANUP: DROP PROCEDURE uspGetCustomerOrders;
