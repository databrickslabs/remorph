-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/stcurven-geography-data-type?view=sql-server-ver16

DECLARE @g geography = 'COMPOUNDCURVE (CIRCULARSTRING (-122.358 47.653, -122.348 47.649, -122.348 47.658), CIRCULARSTRING(-122.348 47.658, -122.358 47.658, -122.358 47.653))';  
 SELECT @g.STCurveN(2).ToString();