-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/hasm-geometry-datatype?view=sql-server-ver16

DECLARE @p GEOMETRY = 'Point(1 1 1 1)'  
SELECT @p.HasM   
--Returns: 1 (true)