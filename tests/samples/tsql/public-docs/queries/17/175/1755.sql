-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/stisempty-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;  
SET @g = geometry::STGeomFromText('POLYGON EMPTY', 0);  
SELECT @g.STIsEmpty();