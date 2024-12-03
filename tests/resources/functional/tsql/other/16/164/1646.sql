--Query type: DML
DECLARE @g geography;
SET @g = geography::STGeomFromText('LINESTRING(-122.360 47.656, -122.343 47.656)', 4326);
SELECT STEndPoint.ToString()
FROM (VALUES (@g)) AS g(geom);
