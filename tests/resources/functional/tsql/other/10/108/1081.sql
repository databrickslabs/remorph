-- tsql sql:
CREATE PROCEDURE Sales.uspCustomersInRegion
    @RegionValue int
WITH EXECUTE AS OWNER
AS
BEGIN
    SET NOCOUNT ON;

    WITH CustomerCTE AS (
        SELECT CustomerID, LastName, FirstName, Region
        FROM (
            VALUES (1, 'Smith', 'John', 1),
                   (2, 'Johnson', 'Mary', 2),
                   (3, 'Williams', 'David', 1),
                   (4, 'Jones', 'Emily', 3),
                   (5, 'Brown', 'Michael', 2)
        ) AS Customer(CustomerID, LastName, FirstName, Region)
    ),
    SalesOrderHeaderCTE AS (
        SELECT SalesOrderID, CustomerID, OrderDate
        FROM (
            VALUES (1, 1, '2020-01-01'),
                   (2, 2, '2020-01-15'),
                   (3, 3, '2020-02-01'),
                   (4, 4, '2020-03-01'),
                   (5, 5, '2020-04-01')
        ) AS SalesOrderHeader(SalesOrderID, CustomerID, OrderDate)
    )

    SELECT c.CustomerID, c.LastName, c.FirstName, soh.OrderDate
    FROM CustomerCTE c
    INNER JOIN SalesOrderHeaderCTE soh ON c.CustomerID = soh.CustomerID
    WHERE c.Region = @RegionValue
    ORDER BY c.LastName, c.FirstName;
END;
