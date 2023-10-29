-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/stcurven-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry = 'COMPOUNDCURVE(CIRCULARSTRING(0 0, 1 2.1082, 3 6.3246, 0 7, -3 6.3246, -1 2.1082, 0 0))';  
 SELECT @g.STCurveN(2).ToString();