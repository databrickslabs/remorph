-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/curvetolinewithtolerance-geography-data-type?view=sql-server-ver16

DECLARE @g geography;  
SET @g = geography::Parse('MULTILINESTRING((-122.358 47.653, -122.348 47.649))');  
SELECT @g.CurveToLineWithTolerance(0.1,0).ToString();