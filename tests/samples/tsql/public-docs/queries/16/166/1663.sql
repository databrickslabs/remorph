-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/stisempty-geography-data-type?view=sql-server-ver16

DECLARE @g geography;  
SET @g = geography::STGeomFromText('POLYGON EMPTY', 4326);  
SELECT @g.STIsEmpty();