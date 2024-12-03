--Query type: DQL
DECLARE @g geometry;
SET @g = geometry::STGeomFromText('POLYGON((0 0, 3 0, 3 3, 0 3, 0 0),(2 2, 2 1, 1 1, 1 2, 2 2))', 0);
WITH temp AS (
    SELECT @g.STPointOnSurface().ToString() AS point_on_surface
)
SELECT * FROM temp
