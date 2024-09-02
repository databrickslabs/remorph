--Query type: DML
WITH geom AS ( SELECT geometry::STGeomFromText('LINESTRING(0 0, 2 3)', 0) AS geom ) SELECT geom FROM geom;