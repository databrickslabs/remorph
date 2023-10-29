-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/bufferwithcurves-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry = 'LINESTRING(3 4, 8 11)'; 
 DECLARE @distance float = 1e-20; 
 SELECT @g.BufferWithCurves(@distance).ToString();