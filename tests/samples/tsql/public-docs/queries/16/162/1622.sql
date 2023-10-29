-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/stconvexhull-geography-data-type?view=sql-server-ver16

DECLARE @g geography = 'POLYGON((20.533 46.566, -18.283 46.1, -22.3 47.45, 20.533 46.566))';  
 SELECT @g.STConvexHull().ToString();