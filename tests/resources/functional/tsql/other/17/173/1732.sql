-- tsql sql:
WITH geomCTE AS (SELECT geometry::STGeomFromText('LINESTRING (100 100, 20 180, 180 180)', 0) AS geom)
SELECT geom.STAsText() AS geom_text
FROM geomCTE;
