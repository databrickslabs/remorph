-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/stpointfromwkb-geography-data-type?view=sql-server-ver16

DECLARE @g geography;  
SET @g = geography::STPointFromWKB(0x010100000017D9CEF753D347407593180456965EC0, 4326);  
SELECT @g.ToString();