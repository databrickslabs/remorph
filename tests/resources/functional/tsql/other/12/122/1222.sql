--Query type: DDL
CREATE TABLE SpatialTable4 (id int PRIMARY KEY, object GEOGRAPHY);
CREATE SPATIAL INDEX SIndx_SpatialTable4_geography_col1 ON SpatialTable4(object);
WITH temp AS (
    SELECT 1 AS id, GEOGRAPHY::Point(10, 10, 4326) AS object
)
INSERT INTO SpatialTable4
SELECT * FROM temp;
SELECT * FROM SpatialTable4;
-- REMORPH CLEANUP: DROP TABLE SpatialTable4;
-- REMORPH CLEANUP: DROP INDEX SIndx_SpatialTable4_geography_col1 ON SpatialTable4;