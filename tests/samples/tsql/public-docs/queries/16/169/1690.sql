-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/makevalid-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry = 'CIRCULARSTRING(1 1, 1 1, 1 1)';  
SELECT @g.MakeValid().ToString();