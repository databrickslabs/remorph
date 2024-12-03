--Query type: DDL
CREATE TABLE SpatialTable
(
    locationId INT IDENTITY(1, 1),
    location GEOGRAPHY,
    deliveryArea AS location.STBuffer(10) PERSISTED
);

WITH tempResult AS
(
    SELECT 1 AS locationId, GEOGRAPHY::Point(0, 0, 4326) AS location
)
INSERT INTO SpatialTable (location)
SELECT location
FROM tempResult;

SELECT *
FROM SpatialTable;
-- REMORPH CLEANUP: DROP TABLE SpatialTable;
