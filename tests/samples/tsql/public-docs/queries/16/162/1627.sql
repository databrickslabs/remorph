-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/stconvexhull-geography-data-type?view=sql-server-ver16

DECLARE @g geography;  
 SELECT @g.STConvexHull();