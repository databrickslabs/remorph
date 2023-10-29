-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/stcurvetoline-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry; 
 SET @g = @g.STCurveToLine(); 
 SELECT @g.STGeometryType(); 
 SET @g = geometry::Parse('LINESTRING EMPTY'); 
 SELECT @g.STGeometryType();