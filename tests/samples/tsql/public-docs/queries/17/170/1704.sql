-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/reduce-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry = 'LINESTRING(0 0, 4 0, 2 .01, 1 0)';  
DECLARE @h geometry = @g.Reduce(1);  
SELECT @g.STIsValid() AS Valid  
SELECT @g.ToString() AS Original, @h.ToString() AS Reduced;