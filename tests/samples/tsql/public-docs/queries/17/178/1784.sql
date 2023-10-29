-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/bufferwithcurves-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry= 'LINESTRING(3 4, 8 11)'; 
 SELECT @g.BufferWithCurves(-1).ToString();