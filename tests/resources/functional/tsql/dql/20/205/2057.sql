-- tsql sql:
CREATE PROCEDURE uspGetCustomerOrders
    @CustomerID int
AS
BEGIN
    WITH c AS (
        SELECT CustomerID, CustomerName
        FROM (
            VALUES (1, 'John Doe'),
                   (2, 'Jane Doe')
        ) AS c (CustomerID, CustomerName)
    ),
    o AS (
        SELECT OrderID, CustomerID, OrderDate
        FROM (
            VALUES (1, 1, '2020-01-01'),
                   (2, 1, '2020-01-15'),
                   (3, 2, '2020-02-01')
        ) AS o (OrderID, CustomerID, OrderDate)
    )
    SELECT c.CustomerName, o.OrderID, o.OrderDate
    FROM c
    INNER JOIN o ON c.CustomerID = o.CustomerID
    WHERE c.CustomerID = @CustomerID;
END;
EXEC uspGetCustomerOrders @CustomerID = 1;
