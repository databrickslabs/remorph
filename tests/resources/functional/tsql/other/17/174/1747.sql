-- tsql sql:
WITH Geometries AS ( SELECT geometry::STGeomFromText('LINESTRING(0 2, 1 1, 1 0, 1 1, 2 2)', 0) AS geom ) SELECT geom.STIsValid() AS IsValid FROM Geometries;
