-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/stpointfromtext-geography-data-type?view=sql-server-ver16

DECLARE @g geography;  
SET @g = geography::STPointFromText('POINT(-122.34900 47.65100)', 4326);  
SELECT @g.ToString();