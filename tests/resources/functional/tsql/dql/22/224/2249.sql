--Query type: DQL
SELECT TOP (1) * FROM (VALUES ('order1', 100.0), ('order2', 200.0), ('order3', 300.0)) AS OrderQueue (OrderID, OrderTotal);