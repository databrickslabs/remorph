-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/point-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;   
SET @g = geometry::Point(1, 10, 0);  
SELECT @g.ToString();