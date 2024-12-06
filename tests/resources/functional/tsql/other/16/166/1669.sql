-- tsql sql:
DECLARE @g geography;
SET @g = geography::STLineFromText('LINESTRING(-122.360 47.656, -122.343 47.656 )', 4326);
SELECT @g.ToString() AS geography_string
FROM (
    VALUES ('LINESTRING(-122.360 47.656, -122.343 47.656 )')
) AS geography_table(geography_string);
