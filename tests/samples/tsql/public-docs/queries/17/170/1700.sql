-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/bufferwithcurves-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry = 'CURVEPOLYGON(COMPOUNDCURVE(CIRCULARSTRING(0 4, 4 0, 8 4), (8 4, 0 4)))'; 
 SELECT @g.BufferWithCurves(-1).ToString()