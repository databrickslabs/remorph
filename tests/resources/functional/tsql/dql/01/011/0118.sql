--Query type: DQL
WITH geom AS ( SELECT geometry::STGeomFromText('LINESTRING(5 5, 6 6, 7 7, 8 8)', 0) AS geom ) SELECT geom.STPointN(geom.STNumPoints()).ToString() AS endpoint FROM geom;