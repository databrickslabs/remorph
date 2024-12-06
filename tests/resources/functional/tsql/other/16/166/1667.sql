-- tsql sql:
DECLARE @g geography;
SET @g = (
    SELECT Geo
    FROM (
        VALUES (
            geography::STGeomFromText('POLYGON((-122.358 47.653, -122.348 47.649, -122.348 47.658, -122.358 47.658, -122.358 47.653), (-122.357 47.654, -122.357 47.657, -122.349 47.657, -122.349 47.650, -122.357 47.654))', 4326)
        )
    ) AS GeoData(Geo);
SELECT @g.RingN(2).ToString();
