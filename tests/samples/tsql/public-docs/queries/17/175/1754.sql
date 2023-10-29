-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/sty-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;  
SET @g = geometry::STGeomFromText('POINT(3 8)', 0);  
SELECT @g.STY;