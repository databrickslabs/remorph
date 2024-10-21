--Query type: DML
DECLARE @g geography;
WITH GeographyCTE AS (
    SELECT geography::STLineFromText('LINESTRING(-122.358 47.653, -122.348 47.649, -122.348 47.658, -122.358 47.658, -122.358 47.653)', 4326) AS geo
)
SELECT @g = geo
FROM GeographyCTE;
SELECT @g.BufferWithCurves(0).ToString() AS Buffer;