-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/null-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;   
SET @g = geometry::[Null];  
SELECT @g