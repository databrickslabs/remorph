-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/stgeometryn-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;  
SET @g = geometry::STGeomFromText('MULTIPOINT(0 0, 13.5 2, 7 19)', 0);  
SELECT @g.STGeometryN(2).ToString();