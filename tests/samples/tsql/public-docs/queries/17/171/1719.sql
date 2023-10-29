-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/starea-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;  
 SET @g = geometry::Parse('CURVEPOLYGON(CIRCULARSTRING(0 2, 2 0, 4 2, 4 2, 0 2))');  
 SELECT @g.STArea() AS Area;