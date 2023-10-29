-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/stgeomcollfromwkb-geography-data-type?view=sql-server-ver16

DECLARE @g geography;  
SET @g = geography::STGeomCollFromWKB(0x01070000000200000001010000007593180456965EC017D9CEF753D34740010200000002000000D7A3703D0A975EC08716D9CEF7D34740CBA145B6F3955EC08716D9CEF7D34740, 4326);  
SELECT @g.ToString();