--Query type: DQL
WITH geography_data AS (
    SELECT geography::Parse('CURVEPOLYGON(CIRCULARSTRING(-122.358 47.653, -122.348 47.649, -122.348 47.658, -122.358 47.658, -122.358 47.653))') AS geo
)
SELECT geo.BufferWithCurves(-2).ToString() AS buffer
FROM geography_data AS gd;
