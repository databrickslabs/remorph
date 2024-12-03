--Query type: DML
CREATE PROCEDURE Sales.uspGetCustomers
    @LastName nvarchar(50),
    @FirstName nvarchar(50)
AS
BEGIN
    WITH Customers AS (
        SELECT 1 AS CustomerID, 'Company A' AS CompanyName, 'John Smith' AS ContactName, 'Sales Manager' AS ContactTitle, '123 Main St' AS Address, 'New York' AS City, 'NY' AS Region, '10001' AS PostalCode, 'USA' AS Country, '123-456-7890' AS Phone, '123-456-7891' AS Fax
        UNION ALL
        SELECT 2, 'Company B', 'Jane Doe', 'Marketing Manager', '456 Elm St', 'Los Angeles', 'CA', '90001', 'USA', '987-654-3210', '987-654-3211'
        UNION ALL
        SELECT 3, 'Company C', 'Bob Johnson', 'IT Manager', '789 Oak St', 'Chicago', 'IL', '60001', 'USA', '555-123-4567', '555-123-4568'
    )
    SELECT c.CustomerID, c.CompanyName, c.ContactName, c.ContactTitle, c.Address, c.City, c.Region, c.PostalCode, c.Country, c.Phone, c.Fax
    FROM Customers c
    WHERE c.ContactName LIKE @LastName + '%' AND c.ContactTitle LIKE @FirstName + '%';
END;
EXEC Sales.uspGetCustomers @LastName = N'Smith', @FirstName = N'Sales%';
-- REMORPH CLEANUP: DROP PROCEDURE Sales.uspGetCustomers;
