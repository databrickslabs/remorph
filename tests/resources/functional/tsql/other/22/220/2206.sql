--Query type: DML
CREATE TABLE Locations
(
    LocationName nvarchar(255),
    LocationPoint geometry
);

INSERT INTO Locations (LocationName, LocationPoint)
SELECT LocationName, LocationPoint
FROM (
    VALUES
    (
        'New York',
        geometry::Point(-74.0060, 40.7128, 4326)
    ),
    (
        'Los Angeles',
        geometry::Point(-118.2437, 34.0522, 4326)
    ),
    (
        'Chicago',
        geometry::Point(-87.6298, 41.8781, 4326)
    )
) AS LocationValues (LocationName, LocationPoint);

SELECT *
FROM Locations;
-- REMORPH CLEANUP: DROP TABLE Locations;
