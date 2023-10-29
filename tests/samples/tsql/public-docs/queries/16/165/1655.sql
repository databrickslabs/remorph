-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/stnumgeometries-geography-data-type?view=sql-server-ver16

DECLARE @g geography;  
SET @g = geography::STGeomFromText('MULTIPOINT((-122.360 47.656), (-122.343 47.656))', 4326);  
SELECT @g.STNumGeometries();