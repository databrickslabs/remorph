-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/stpointfromwkb-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;   
SET @g = geometry::STPointFromWKB(0x010100000000000000000059400000000000005940, 0);  
SELECT @g.STAsText();