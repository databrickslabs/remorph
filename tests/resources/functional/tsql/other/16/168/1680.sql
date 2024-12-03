--Query type: DML
DECLARE @g geography;
SET @g = (
    SELECT Geo
    FROM (
        VALUES (
            geography::STMPointFromText('MULTIPOINT(-122.360 47.656, -122.343 47.656)', 4326)
        )
    ) AS GeoData(Geo);
SELECT @g.ToString();
