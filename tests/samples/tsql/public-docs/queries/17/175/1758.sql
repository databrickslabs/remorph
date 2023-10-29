-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/stgeometrytype-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;  
SET @g = geometry::STGeomFromText('POLYGON((0 0, 3 0, 3 3, 0 3, 0 0))', 0);  
SELECT @g.STGeometryType();