--Query type: DQL
DECLARE @g geometry;
SET @g = geometry::STGeomFromText('POINT(10 20)', 4326);
SELECT g.STExteriorRing().ToString()
FROM (VALUES (@g)) AS v(g);