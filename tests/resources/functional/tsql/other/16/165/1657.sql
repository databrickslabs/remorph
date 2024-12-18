-- tsql sql:
DECLARE @g geography;
SET @g = geography::STGeomFromText('MULTIPOINT(-122.360 47.656, -122.343 47.656)', 4326);
SELECT geo.STGeometryN(2).ToString() AS PointString
FROM (VALUES (@g)) AS temp(geo);
