-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/geomfromgml-geography-data-type?view=sql-server-ver16

DECLARE @g geography;  
DECLARE @x xml;  
SET @x = '<FullGlobe xmlns="http://schemas.microsoft.com/sqlserver/2011/geography" />';  
SET @g = geography::GeomFromGml(@x, 4326);  
SELECT @g.ToString();