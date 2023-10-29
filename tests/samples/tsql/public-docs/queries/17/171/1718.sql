-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/stnumcurves-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;  
 SET @g = geometry::Parse('COMPOUNDCURVE(CIRCULARSTRING(10 0, 0 10, -10 0, 0 -10, 10 0))');  
 SELECT @g.STNumCurves();