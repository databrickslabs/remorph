--Query type: DML
CREATE PROCEDURE dbo.uspGetCustomerOrders
AS
BEGIN
    -- Use SET NOCOUNT ON
    SET NOCOUNT ON;

    -- Use SELECT, FROM, INNER JOIN, WHERE, and ORDER BY
    WITH c AS (
        -- Create a temporary result set using Common Table Expression (CTE)
        SELECT 1 AS CustomerID, 'John' AS FirstName, 'Doe' AS LastName
        UNION ALL
        SELECT 2, 'Jane', 'Doe'
        UNION ALL
        SELECT 3, 'Bob', 'Smith'
    ),
    o AS (
        -- Create another temporary result set using Common Table Expression (CTE)
        SELECT 1 AS OrderID, 1 AS CustomerID, '2022-01-01' AS OrderDate
        UNION ALL
        SELECT 2, 1, '2022-01-15'
        UNION ALL
        SELECT 3, 2, '2022-02-01'
    )
    SELECT 'PROCEDURE', c.CustomerID, o.OrderID, c.FirstName, o.OrderDate
    FROM c
    INNER JOIN o
    ON c.CustomerID = o.CustomerID
    WHERE c.CustomerID LIKE '1%'
    ORDER BY c.CustomerID, o.OrderID;
END;

-- Execute the stored procedure
EXEC dbo.uspGetCustomerOrders;

-- REMORPH CLEANUP: DROP PROCEDURE dbo.uspGetCustomerOrders;
