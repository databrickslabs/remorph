--Query type: DQL
DECLARE @g geometry;
SET @g = geometry::Parse('CURVEPOLYGON(CIRCULARSTRING(0 2, 2 0, 4 2, 4 2, 0 2))');
SELECT geom.STArea() AS Area
FROM (VALUES (@g)) AS temp_result(geom);
