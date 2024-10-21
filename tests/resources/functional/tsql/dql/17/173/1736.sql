--Query type: DQL
DECLARE @g geometry;
SET @g = geometry::STGeomFromText('LINESTRING(0 0, 2 2, 0 2, 2 0)', 0);
SELECT boundary
FROM (
    SELECT @g.STBoundary().ToString() AS boundary
) AS temp;