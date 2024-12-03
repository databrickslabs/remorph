--Query type: DQL
WITH Orders AS ( SELECT 1 AS OrderKey, '2022-01-01' AS OrderDate ) SELECT OrderKey, OrderDate, DATEADD(day, 2, OrderDate) AS PromisedShipDate FROM Orders
