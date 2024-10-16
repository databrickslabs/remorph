--Query type: DQL
DECLARE @g geometry;
SET @g = geometry::STGeomFromText('POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))', 0);
SELECT g.STBoundary().ToString() AS boundary
FROM (VALUES (@g)) AS temp(g);