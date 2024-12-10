-- tsql sql:
DECLARE @Cities TABLE (Name VARCHAR(100), X DECIMAL(10, 2), Y DECIMAL(10, 2));
INSERT INTO @Cities (Name, X, Y)
VALUES ('Anchorage', 23.5, 45.6), ('New York', 40.7, 74.0), ('Los Angeles', 34.1, 118.2);
UPDATE @Cities
SET X = 24.5
WHERE Name = 'Anchorage';
SELECT * FROM @Cities;
