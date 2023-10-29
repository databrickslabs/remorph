-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/geomfromgml-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;  
DECLARE @x xml;  
SET @x = '<LineString xmlns="http://www.opengis.net/gml"> <posList>100 100 20 180 180 180</posList> </LineString>';  
SET @g = geometry::GeomFromGml(@x, 0);  
SELECT @g.ToString();