-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/m-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;  
SET @g = geometry::STGeomFromText('POINT(1 2 3 4)', 0);  
SELECT @g.M;