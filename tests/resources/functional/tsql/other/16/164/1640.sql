--Query type: DML
WITH g AS (SELECT geography::Parse('MULTILINESTRING((-122.358 47.653, -122.348 47.649))') AS geo)
SELECT geo.CurveToLineWithTolerance(0.1, 0).ToString() AS LineString
FROM g;
