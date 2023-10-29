-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/parse-geography-data-type?view=sql-server-ver16

DECLARE @g geography;   
SET @g = geography::Parse('LINESTRING(-122.360 47.656, -122.343 47.656)');  
SELECT @g.ToString();