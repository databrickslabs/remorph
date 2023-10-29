-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/stgeomfromwkb-geography-data-type?view=sql-server-ver16

DECLARE @g geography;  
SET @g = geography::STGeomFromWKB(0x010200000002000000D7A3703D0A975EC08716D9CEF7D34740CBA145B6F3955EC08716D9CEF7D34740, 4326);  
SELECT @g.ToString();