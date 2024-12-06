-- tsql sql:
CREATE PROCEDURE Sales.uspGetCustomerList
AS
BEGIN
    SELECT *
    FROM Sales.Customers;
END;
