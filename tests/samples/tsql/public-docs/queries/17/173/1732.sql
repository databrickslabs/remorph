-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/stgeomfromtext-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;  
SET @g = geometry::STGeomFromText('LINESTRING (100 100, 20 180, 180 180)', 0);  
SELECT @g.ToString();