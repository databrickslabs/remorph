-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/point-geography-data-type?view=sql-server-ver16

DECLARE @g geography;   
SET @g = geography::Point(47.65100, -122.34900, 4326)  
SELECT @g.ToString();