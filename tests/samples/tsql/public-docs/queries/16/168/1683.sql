-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/null-geography-data-type?view=sql-server-ver16

DECLARE @g geography;   
SET @g = geography::[Null];  
SELECT @g