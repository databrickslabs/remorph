-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/stcurvetoline-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry; 
 SET @g = geometry::Parse('LINESTRING(1 3, 5 5, 4 3, 1 3)'); 
 SET @g = @g.STCurveToLine(); 
 SELECT @g.STGeometryType();