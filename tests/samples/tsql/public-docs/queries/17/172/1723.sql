-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/sttouches-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;  
DECLARE @h geometry;  
SET @g = geometry::STGeomFromText('LINESTRING(0 2, 2 0, 4 2)', 0);  
SET @h = geometry::STGeomFromText('POINT(1 1)', 0);  
SELECT @g.STTouches(@h);