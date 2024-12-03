--Query type: DDL
CREATE TABLE SpatialTable (
    locationId INT IDENTITY(1,1) PRIMARY KEY,
    location geometry,
    deliveryArea AS location.STBuffer(10) PERSISTED
);

WITH TempTable AS (
    SELECT geometry::Point(10, 10, 0) AS location
    UNION ALL
    SELECT geometry::Point(20, 20, 0) AS location
)
INSERT INTO SpatialTable (location)
SELECT location
FROM TempTable;
