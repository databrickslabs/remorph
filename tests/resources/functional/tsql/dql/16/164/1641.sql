--Query type: DQL
DECLARE @new_g geography;
SET @new_g = geography::Parse('MULTILINESTRING((-121.358 47.653, -121.348 47.649),(-120.358 47.653, -120.348 47.649))');
SELECT geography::Parse('MULTILINESTRING((-121.358 47.653, -121.348 47.649),(-120.358 47.653, -120.348 47.649))').CurveToLineWithTolerance(0.05,0).ToString() AS new_geography_string
FROM (VALUES (1)) AS temp_result_set(id);