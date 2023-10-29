-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/stconvexhull-geography-data-type?view=sql-server-ver16

DECLARE @g geography;  
 SET @g = geography::Parse('POLYGON((-120.533 46.566, -118.283 46.1, -122.3 47.45, -120.533 46.566))');  
 SELECT @g.STConvexHull().ToString();