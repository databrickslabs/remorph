-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/hasm-geography-data-type?view=sql-server-ver16

DECLARE @p GEOGRAPHY = 'Point(1 1 1 1)'  
SELECT @p.HasM   
--Returns: 1 (true)