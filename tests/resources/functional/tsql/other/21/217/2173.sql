--Query type: DDL
CREATE PROCEDURE Sales.uspGetCustomerList
AS
BEGIN
    SELECT *
    FROM Sales.Customers;
END;
