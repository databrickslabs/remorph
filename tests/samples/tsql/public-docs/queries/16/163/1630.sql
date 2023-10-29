-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/stgeomcollfromtext-geography-data-type?view=sql-server-ver16

DECLARE @g geography;  
DECLARE @g geography;  
SET @g = geography::STGeomCollFromText('GEOMETRYCOLLECTION ( POINT(-122.34900 47.65100), LINESTRING(-122.360 47.656, -122.343 47.656) )', 4326);  
SELECT @g.ToString();