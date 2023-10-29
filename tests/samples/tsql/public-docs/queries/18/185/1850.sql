-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/isvaliddetailed-geography-data-type?view=sql-server-ver16

DECLARE @p GEOGRAPHY = 'Polygon((2 2, 4 4, 4 2, 2 4, 2 2))'  
SELECT @p.IsValidDetailed()  
--Returns: 24409: Not valid because some portion of polygon ring (1) lies in the interior of a polygon.