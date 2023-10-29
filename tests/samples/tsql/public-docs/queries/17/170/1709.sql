-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/bufferwithcurves-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry = 'MULTIPOINT((1 1),(1 4))'; 
 SELECT @g.BufferWithCurves(1).ToString(); 
 SELECT @g.BufferWithCurves(1.5).ToString(); 
 SELECT @g.BufferWithCurves(1.6).ToString();