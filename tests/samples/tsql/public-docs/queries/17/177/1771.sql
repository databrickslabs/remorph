-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/parse-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;   
SET @g = geometry::Parse('LINESTRING (100 100, 20 180, 180 180)');  
SELECT @g.ToString();