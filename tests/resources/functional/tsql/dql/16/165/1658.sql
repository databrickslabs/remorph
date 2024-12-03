--Query type: DQL
DECLARE @g geography;
SET @g = geography::STGeomFromText('POINT(-122.34900 47.65100 10.3 12)', 4326);
SELECT geo_text, geo_text_zm
FROM (
    VALUES (@g.STAsText(), @g.AsTextZM())
) AS temp_result(geo_text, geo_text_zm);
