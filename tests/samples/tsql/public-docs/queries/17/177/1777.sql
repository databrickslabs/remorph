-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/stmpointfromwkb-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;   
SET @g = geometry::STMPointFromWKB(0x010400000002000000010100000000000000000059400000000000005940010100000000000000000069400000000000006940, 0);  
SELECT @g.STAsText();