--Query type: DQL
WITH Customers AS (SELECT 'ALFKI' AS CustomerID, 'Alfreds Futterkiste' AS CompanyName), Orders AS (SELECT 'ALFKI' AS CustomerID, 'PO-12345' AS OrderID) SELECT c.*, o.* FROM Customers AS c INNER JOIN Orders AS o ON c.CustomerID = o.CustomerID
