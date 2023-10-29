-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/isvaliddetailed-geometry-datatype?view=sql-server-ver16

DECLARE @p GEOMETRY = 'Polygon((2 2, 4 4, 4 2, 2 4, 2 2))'  
SELECT @p.IsValidDetailed()  
--Returns: 24404: Not valid because polygon ring (1) intersects itself or some other ring.