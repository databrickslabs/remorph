-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/stlinefromtext-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;  
SET @g = geometry::STLineFromText('LINESTRING (100 100, 200 200)', 0);  
SELECT @g.ToString();