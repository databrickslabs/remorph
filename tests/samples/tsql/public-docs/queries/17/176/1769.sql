-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/stmpolyfromtext-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;  
SET @g = geometry::STMPolyFromText('MULTIPOLYGON (((5 5, 10 5, 10 10, 5 5)), ((10 10, 100 10, 200 200, 30 30, 10 10)))', 0);  
SELECT @g.ToString();