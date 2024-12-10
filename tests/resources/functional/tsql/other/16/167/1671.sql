-- tsql sql:
DECLARE @g GEOGRAPHY;
SET @g = (
    SELECT GeoData
    FROM (
        VALUES (
            geography::STMLineFromText('MULTILINESTRING ((-122.358 47.653, -122.348 47.649, -122.348 47.658, -122.358 47.658, -122.358 47.653), (-122.357 47.654, -122.357 47.657, -122.349 47.657, -122.349 47.650, -122.357 47.654))', 4326)
        )
    ) AS GeoData(GeoData)
);
SELECT @g.ToString() AS GeoDataString;
