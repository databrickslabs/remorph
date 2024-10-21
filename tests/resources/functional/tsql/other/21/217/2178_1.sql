--Query type: DDL
CREATE TABLE CustomerLocations
(
    id INT IDENTITY(1, 1),
    GeomCol1 geometry,
    GeomCol2 AS GeomCol1.STAsText()
);

INSERT INTO CustomerLocations (GeomCol1)
SELECT geometry::STGeomFromText('POINT(1 1)', 0) AS GeomCol1
FROM (VALUES (1)) AS temp(id);
-- REMORPH CLEANUP: DROP TABLE CustomerLocations;