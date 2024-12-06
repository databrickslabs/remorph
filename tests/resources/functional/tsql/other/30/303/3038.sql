-- tsql sql:
CREATE TABLE Locations (Name nvarchar(50), Location geography);
INSERT INTO Locations (Name, Location)
VALUES
    ('New York', geography::Point(40.7128, 74.0060, 4326)),
    ('Los Angeles', geography::Point(34.0522, 118.2437, 4326)),
    ('Chicago', geography::Point(41.8781, 87.6298, 4326));
WITH L AS (
    SELECT Name, Location
    FROM Locations
    WHERE Name = 'New York'
)
UPDATE L
SET Location = Location.SetXY(23.5, 23.5);
SELECT * FROM Locations;
-- REMORPH CLEANUP: DROP TABLE Locations;
