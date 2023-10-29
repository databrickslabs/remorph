-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/stpointfromtext-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;  
SET @g = geometry::STPointFromText('POINT (100 100)', 0);  
SELECT @g.ToString();