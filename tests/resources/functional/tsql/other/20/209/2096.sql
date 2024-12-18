-- tsql sql:
CREATE PROCEDURE Sales.uspGetCustomers
    @CustomerName nvarchar(50)
AS
BEGIN
    -- Select data from a temporary result set using a Table Value Constructor (VALUES) subquery
    SELECT *
    FROM (
        VALUES ('John', 'Doe'),
               ('Jane', 'Doe')
    ) AS Customers (
        FirstName,
        LastName
    )
    WHERE FirstName LIKE @CustomerName + '%';
END

-- Execute the stored procedure
EXECUTE Sales.uspGetCustomers N'John%';

-- REMORPH CLEANUP: DROP PROCEDURE Sales.uspGetCustomers;
