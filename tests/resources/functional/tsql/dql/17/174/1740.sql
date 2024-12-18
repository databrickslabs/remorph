-- tsql sql:
DECLARE @geom geometry;
SET @geom = geometry::STGeomFromText('LINESTRING(1 1, 3 3, 2 1)', 0);
WITH geom_cte AS (
    SELECT @geom AS geom
)
SELECT geom.STLength()
FROM geom_cte;
