-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/stgeomfromwkb-geometry-data-type?view=sql-server-ver16

DECLARE @g geometry;   
SET @g = geometry::STGeomFromWKB(0x010200000003000000000000000000594000000000000059400000000000003440000000000080664000000000008066400000000000806640, 0);  
SELECT @g.STAsText();