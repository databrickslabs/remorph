-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/geomfromgml-geography-data-type?view=sql-server-ver16

DECLARE @g geography;  
DECLARE @x xml;  
SET @x = '<LineString xmlns="http://www.opengis.net/gml"><posList>47.656 -122.36 47.656 -122.343</posList></LineString>';  
SET @g = geography::GeomFromGml(@x, 4326);  
SELECT @g.ToString();