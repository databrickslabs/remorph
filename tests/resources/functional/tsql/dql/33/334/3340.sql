-- tsql sql:
SELECT DaysToShip, AVG(ExtendedPrice) AS AveragePrice FROM (VALUES (1, 100.0), (2, 200.0), (3, 300.0), (1, 150.0), (2, 250.0), (3, 350.0)) AS Lineitem (DaysToShip, ExtendedPrice) GROUP BY DaysToShip
