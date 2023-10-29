-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/hasz-geometry-datatype?view=sql-server-ver16

DECLARE @p GEOMETRY = 'Point(1 1 1 1)'  
SELECT @p.HasZ   
--Returns: 1 (true)