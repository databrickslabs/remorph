--Query type: DQL
DECLARE @g geometry;
SET @g = geometry::STGeomFromText('MULTIPOINT(0 0, 13.5 2, 7 19)', 0);
WITH temp AS (
    SELECT @g.STGeometryN(2).ToString() AS geom
)
SELECT * FROM temp;