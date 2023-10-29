-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/stmlinefromtext-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;  
SET @g = geometry::STMLineFromText('MULTILINESTRING ((100 100, 200 200), (3 4, 7 8, 10 10))', 0);  
  
SELECT @g.ToString();