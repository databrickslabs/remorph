-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/bufferwithtolerance-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;  
SET @g = geometry::STGeomFromText('POINT(3 3)', 0);  
SELECT @g.BufferWithTolerance(1, .5, 0).ToString();