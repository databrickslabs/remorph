-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/tostring-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;  
SET @g = geometry::STGeomFromText('LINESTRING(0 0, 0 1, 1 0)', 0);  
SELECT @g.ToString();