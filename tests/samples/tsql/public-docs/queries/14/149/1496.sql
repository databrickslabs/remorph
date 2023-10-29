-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/reorientobject-geography-data-type?view=sql-server-ver16

DECLARE @R GEOGRAPHY = GEOGRAPHY::Parse('Polygon((-10 -10, -10 10, 10 10, 10 -10, -10 -10))');  
SELECT @R.ReorientObject().STAsText();  
--Result: POLYGON ((10 10, -10 10, -10 -10, 10 -10, 10 10))