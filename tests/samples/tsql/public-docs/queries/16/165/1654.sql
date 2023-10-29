-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/makevalid-geography-data-type?view=sql-server-ver16

DECLARE @g geography;  
SET @g = geography::STGeomFromText('LINESTRING(0 2, 1 1, 1 0, 1 1, 2 2)', 4326);  
SELECT @g.STIsValid();