-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/mindbcompatibilitylevel-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry = 'CIRCULARSTRING(3 4, 8 9, 5 6)'; 
 IF @g.MinDbCompatibilityLevel() <= 110 
 BEGIN 
 SELECT @g.ToString(); 
 END