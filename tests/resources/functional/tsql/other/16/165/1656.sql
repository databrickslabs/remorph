-- tsql sql:
DECLARE @g geography;
WITH GeographyData AS (
    SELECT geography::STGeomFromText('MULTIPOINT(-122.360 47.656, -122.343 47.656)', 4326) AS Geo
)
SELECT @g = Geo
FROM GeographyData;
SELECT @g.InstanceOf('GEOMETRYCOLLECTION');
