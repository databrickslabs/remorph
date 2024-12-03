--Query type: DQL
SELECT COUNT(*) FROM (VALUES (1, 'Customer#000000001'), (2, 'Customer#000000002'), (3, 'Customer#000000003')) AS Customer (CustomerID, CustomerName);
