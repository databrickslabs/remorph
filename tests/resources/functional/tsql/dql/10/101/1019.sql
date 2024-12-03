--Query type: DQL
SELECT CustomerID, FirstName, LastName, Address, RecursionLevel FROM dbo.ufn_GetCustomerReports((SELECT CustomerID, FirstName, LastName, Address, RecursionLevel FROM (VALUES (1, 'John', 'Doe', '123 Main St', 0), (2, 'Jane', 'Doe', '456 Elm St', 1)) AS Customer(CustomerID, FirstName, LastName, Address, RecursionLevel)))
