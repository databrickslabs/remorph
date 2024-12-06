-- tsql sql:
SELECT CustomerName, CustomerId, OrderTotal, ROW_NUMBER() OVER (ORDER BY CustomerName) AS RowId FROM (VALUES ('John Doe', 1, 100.00), ('Jane Doe', 2, 200.00), ('Bob Smith', 3, 50.00)) AS CustomerInfo(CustomerName, CustomerId, OrderTotal) ORDER BY OrderTotal;
