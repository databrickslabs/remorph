--Query type: DQL
WITH geom AS ( SELECT geometry::STGeomFromText('LINESTRING(0 0, 2 2, 1 0)', 0) AS g ) SELECT g.STStartPoint().ToString() FROM geom
