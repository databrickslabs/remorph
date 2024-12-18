-- tsql sql:
DECLARE @g geography;
SET @g = (
    SELECT GeoPoint
    FROM (
        VALUES (
            geography::STPointFromText('POINT(-122.34900 47.65100)', 4326)
        )
    ) AS GeoData(GeoPoint);
SELECT @g.ToString() AS GeoPointString;
