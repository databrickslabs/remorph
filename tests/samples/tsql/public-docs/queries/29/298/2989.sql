-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/makevalid-geometry-data-type?view=sql-server-ver16

SET @g = @g.MakeValid();  
SELECT @g.STIsValid();