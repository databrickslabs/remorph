-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/reduce-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry = 'CIRCULARSTRING(0 0, 8 8, 16 0, 20 -4, 24 0)'; 
 SELECT @g.Reduce(5).ToString(); 
 SELECT @g.Reduce(15).ToString(); 
 SELECT @g.Reduce(16).ToString();