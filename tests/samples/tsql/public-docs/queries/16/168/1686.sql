-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/bufferwithcurves-geography-data-type?view=sql-server-ver16

DECLARE @g geography= 'LINESTRING(-122.358 47.653, -122.348 47.649, -122.348 47.658, -122.358 47.658, -122.358 47.653)';  
SELECT @g.BufferWithCurves(2).ToString();