--Query type: DQL
DECLARE @region geography;
DECLARE @nation geography;
DECLARE @result geography;

SELECT @region = geog
FROM (
    VALUES (
        geography::STGeomFromText('POLYGON ((-122.358 47.653, -122.348 47.649, -122.348 47.658, -122.358 47.658, -122.358 47.653))', 4326)
    )
) AS region(geog);

SELECT @nation = geog
FROM (
    VALUES (
        geography::STGeomFromText('POLYGON ((-122.358 47.653, -122.348 47.649, -122.348 47.658, -122.358 47.658, -122.358 47.653))', 4326)
    )
) AS nation(geog);

SELECT @result = @region.STIntersection(@nation);

SELECT @result.STAsText();
