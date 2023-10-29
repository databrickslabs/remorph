-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/stnumpoints-geography-data-type?view=sql-server-ver16

DECLARE @g geography = 'COMPOUNDCURVE(CIRCULARSTRING(-122.358 47.653, -122.348 47.649, -122.348 47.658),( -122.348 47.658, -121.56 48.12, -122.358 47.653))'  
 SELECT @g.STNumPoints();