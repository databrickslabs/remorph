-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/curvetolinewithtolerance-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry; 
 SET @g = geometry::Parse('MULTILINESTRING((1 3, 4 8, 6 9))'); 
 SELECT @g.CurveToLineWithTolerance(0.1,0).ToString();