--Query type: DQL
DECLARE @g geometry = geometry::STGeomFromText('LINESTRING(0 0, 2 2, 1 0, 0 0)', 0);
SELECT geom.STIsRing() AS IsRing
FROM (VALUES (@g)) AS temp_result(geom);