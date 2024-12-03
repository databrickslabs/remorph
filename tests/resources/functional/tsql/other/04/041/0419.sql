--Query type: DML
CREATE PROCEDURE Sales.GetOrderDetails
    @SearchTerm NVARCHAR(50)
AS
BEGIN
    WITH OrderDetails AS (
        SELECT
            OrderID,
            ProductName,
            UnitPrice
        FROM
            (
                VALUES
                    (1, 'Product A', 10.99),
                    (2, 'Product B', 5.99),
                    (3, 'Product C', 7.99),
                    (4, 'Product D', 12.99),
                    (5, 'Product E', 8.99)
            ) AS SourceTable(OrderID, ProductName, UnitPrice)
    )
    SELECT
        OrderID,
        ProductName,
        UnitPrice
    FROM
        OrderDetails
    WHERE
        ProductName LIKE @SearchTerm;
END;

-- Execute the stored procedure
EXEC Sales.GetOrderDetails '%Product%';

-- To show the structure of the result set
EXEC Sales.GetOrderDetails '%Product%' WITH RESULT SETS ((OrderID INT, ProductName NVARCHAR(50), UnitPrice DECIMAL(10, 2)));

-- REMORPH CLEANUP: DROP PROCEDURE Sales.GetOrderDetails;
