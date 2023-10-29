-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/stisvalid-geography-data-type?view=sql-server-ver16

DECLARE @g geography = geography::STGeomFromText('LINESTRING(0 0, 2 2, 1 0)', 4326);  
SELECT @g.STIsValid();  
DECLARE @g geography