--Query type: DQL
SELECT CustomerKey, CustomerName FROM (VALUES (1, 'Customer1'), (2, 'Customer2'), (3, 'Customer3')) AS TempResult (CustomerKey, CustomerName) WHERE CustomerKey <= 500;
