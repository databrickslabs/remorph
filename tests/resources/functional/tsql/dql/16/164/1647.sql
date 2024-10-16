--Query type: DQL
DECLARE @g geography;
SET @g = geography::STGeomFromText('LINESTRING(-122.360 47.656, -122.343 47.656)', 4326);
SELECT geo.STLength() AS length
FROM (VALUES (@g)) AS temp_table(geo);