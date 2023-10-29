-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/strelate-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;  
DECLARE @h geometry;  
SET @g = geometry::STGeomFromText('LINESTRING(0 2, 2 0, 4 2)', 0);  
SET @h = geometry::STGeomFromText('POINT(5 5)', 0);  
SELECT @g.STRelate(@h, 'FF*FF****');