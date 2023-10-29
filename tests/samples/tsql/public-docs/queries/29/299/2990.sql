-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/makevalid-geography-data-type?view=sql-server-ver16

SET @g = @g.MakeValid();  
SELECT @g.STIsValid();