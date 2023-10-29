-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/stsymdifference-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry = 'CURVEPOLYGON (CIRCULARSTRING (0 -4, 4 0, 0 4, -4 0, 0 -4))';  
 DECLARE @h geometry = 'POLYGON ((1 -1, 2 -1, 2 1, 1 1, 1 -1))';  
 SELECT @h.STSymDifference(@g).ToString();