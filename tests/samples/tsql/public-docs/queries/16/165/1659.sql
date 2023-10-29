-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/z-geography-data-type?view=sql-server-ver16

DECLARE @g geography;  
SET @g = geography::STGeomFromText('POINT(-122.34900 47.65100 10.3 12)', 4326);  
SELECT @g.Z;