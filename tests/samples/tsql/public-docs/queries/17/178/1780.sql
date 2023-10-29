-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/stpolyfromtext-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;   
SET @g = geometry::STPolyFromText('POLYGON ((5 5, 10 5, 10 10, 5 5))', 0);  
SELECT @g.ToString();