--Query type: DQL
SELECT CustomerID, CompanyName FROM (VALUES (1, 'Customer 1'), (2, 'Customer 2')) AS Customers (CustomerID, CompanyName);