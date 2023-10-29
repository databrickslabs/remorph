-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/stmpointfromwkb-geography-data-type?view=sql-server-ver16

DECLARE @g geography;   
SET @g = geography::STMPointFromWKB(0x0104000000020000000101000000D7A3703D0A975EC08716D9CEF7D347400101000000CBA145B6F3955EC08716D9CEF7D34740, 4326);  
SELECT @g.ToString();