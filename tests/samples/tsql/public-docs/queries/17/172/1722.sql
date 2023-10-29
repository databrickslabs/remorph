-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/stcrosses-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;  
DECLARE @h geometry;  
SET @g = geometry::STGeomFromText('LINESTRING(0 2, 2 0)', 0);  
SET @h = geometry::STGeomFromText('LINESTRING(0 0, 2 2)', 0);  
SELECT @g.STCrosses(@h);