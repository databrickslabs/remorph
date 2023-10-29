-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/stissimple-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;  
SET @g = geometry::STGeomFromText('LINESTRING(0 0, 2 2, 0 2, 2 0)', 0);  
SELECT @g.STIsSimple();