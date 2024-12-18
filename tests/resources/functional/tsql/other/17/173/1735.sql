-- tsql sql:
DECLARE @g geometry;
SET @g = geometry::STGeomFromText('LINESTRING(0 0, 0 1, 1 0, 2 1, 3 0, 4 1)', 0);
WITH cte AS (
    SELECT @g AS geom
)
SELECT geom.Reduce(0.75).ToString() AS reduced_geom
FROM cte;
