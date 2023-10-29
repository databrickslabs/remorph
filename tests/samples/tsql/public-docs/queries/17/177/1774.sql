-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/stlinefromwkb-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;   
SET @g = geometry::STLineFromWKB(0x0102000000020000000000000000005940000000000000594000000000000069400000000000006940, 0);  
SELECT @g.STAsText();